import logging
from dataclasses import dataclass
from pathlib import Path

from constants import ALLOWED_MODES, ALLOWED_MOVE_STRATEGIES
from helpers.base_classes import Singleton
from utils.file_readers import YamlReader

logger = logging.getLogger(__name__)


class UserConfig(Singleton):
    """
    Singleton that loads and exposes user configuration.

    On first instantiation, reads a YAML file from the given path, ensures it
    parses to a dict, logs the loaded config, and initializes sub-configs.
    Subsequent constructions return the same instance and do not re-run setup.

    Args:
        path: Filesystem path to the YAML config file.

    Raises:
        ValueError: If the loaded YAML is not a mapping.
    """

    def __init__(self, path: str):
        self.path = path
        super().__init__()

    def setup(self):
        reader = YamlReader(self.path)
        if not isinstance(reader.data, dict):
            raise ValueError(f"Invalid config at {self.path}")

        logger.info(f"Config file found: {reader.data}")
        self.config_dict = reader.data
        self.ai = AIConfig(self.config_dict)
        self.behavior = BehaviorConfig.from_dict(self.config_dict)
        self.folder = FolderConfig.from_dict(self.config_dict)
        # self.labels = LabelsConfig(self.config_dict)
        # self.api = APIConfig(self.config_dict)
        # self.logging = LoggingConfig(self.config_dict)
        # self.security = SecurityConfig(self.config_dict)
        # self.development = DevelopmentConfig(self.config_dict)


@dataclass(slots=True, frozen=True)
class FolderConfig:
    """Immutable configuration for folder paths used by the pipeline.

    Normalizes, expands (~), and resolves all paths; ensures each directory exists.
    Disallows any watch folder from overlapping with output/temp/quarantine. Defaults:
    temp_folder -> <output_folder>/.tmp, quarantine_folder -> <output_folder>/.quarantine.

    Attributes:
        watch_folders (tuple[pathlib.Path, ...]): Folders to watch for incoming files.
        output_folder (pathlib.Path): Destination for processed output.
        temp_folder (pathlib.Path): Working directory for intermediate artifacts.
        quarantine_folder (pathlib.Path): Destination for rejected/problematic files.

    Classmethods:
        from_dict(config_dict): Build a FolderConfig from a dict with a "paths" section.
            Requires "watch_folders" and "output_folder". Creates directories as needed.
            Raises:
                ValueError: If required keys are missing or folders overlap.

    Methods:
        as_dict(): Return a JSON-serializable dict with stringified paths.
    """

    watch_folders: tuple[Path, ...]
    output_folder: Path
    temp_folder: Path
    quarantine_folder: Path

    @classmethod
    def from_dict(cls, config_dict: dict) -> "FolderConfig":
        cfg = config_dict.get("paths", {})
        if "watch_folders" not in cfg or "output_folder" not in cfg:
            raise ValueError(
                "Missing required `paths.watch_folders`/`paths.output_folder`"
            )

        output = Path(cfg["output_folder"]).expanduser().resolve()
        temp = Path(cfg.get("temp_folder", output / ".tmp")).expanduser().resolve()
        quarantine = (
            Path(cfg.get("quarantine_folder", output / ".quarantine"))
            .expanduser()
            .resolve()
        )
        watches = tuple(Path(p).expanduser().resolve() for p in cfg["watch_folders"])

        inst = cls(watches, output, temp, quarantine)

        for p in (
            *inst.watch_folders,
            inst.output_folder,
            inst.temp_folder,
            inst.quarantine_folder,
        ):
            p.mkdir(parents=True, exist_ok=True)

        if any(
            w in {inst.output_folder, inst.temp_folder, inst.quarantine_folder}
            for w in inst.watch_folders
        ):
            raise ValueError("Watch folders must not overlap output/temp/quarantine")

        return inst

    def as_dict(self) -> dict:
        return {
            "watch_folders": [str(p) for p in self.watch_folders],
            "output_folder": str(self.output_folder),
            "temp_folder": str(self.temp_folder),
            "quarantine_folder": str(self.quarantine_folder),
        }


@dataclass(slots=True, frozen=True)
class BehaviorConfig:
    """
    Immutable behavior configuration with validation for mode, move strategy, and runtime flags.

    Attributes:
    - mode_default: Default execution mode; must be one of ALLOWED_MODES.
    - move_strategy: Movement strategy; must be one of ALLOWED_MOVE_STRATEGIES.
    - confidence_threshold: Decision threshold in [0.0, 1.0].
    - stabilization_delay: Non-negative delay before applying changes.
    - logging_enabled: Enable or disable logging.
    - verbose_cli: Enable verbose CLI output.

    Classmethods:
    - from_dict(config_dict): Build from config_dict["behavior"], applying defaults and validating values.
      Returns a BehaviorConfig. Raises ValueError for invalid enums, out-of-range numbers, or non-boolean flags.
    """

    mode_default: str = "auto"
    move_strategy: str = "move"
    confidence_threshold: float = 0.5
    stabilization_delay: int = 0
    logging_enabled: bool = True
    verbose_cli: bool = False

    @classmethod
    def from_dict(cls, config_dict: dict) -> "BehaviorConfig":
        cfg = config_dict.get("behavior", {})

        mode = cfg.get("mode_default", cls.mode_default)
        move = cfg.get("move_strategy", cls.move_strategy)
        if mode not in ALLOWED_MODES:
            raise ValueError("Invalid `behavior.mode_default`")
        if move not in ALLOWED_MOVE_STRATEGIES:
            raise ValueError("Invalid `behavior.move_strategy`")
        thr = float(cfg.get("confidence_threshold", cls.confidence_threshold))
        if not 0.0 <= thr <= 1.0:
            raise ValueError("`behavior.confidence_threshold` must be 0..1")
        delay = int(cfg.get("stabilization_delay", cls.stabilization_delay))
        if delay < 0:
            raise ValueError("`behavior.stabilization_delay` must be >= 0")
        logging_enabled = cfg.get("logging_enabled", cls.logging_enabled)
        verbose_cli = cfg.get("verbose_cli", cls.verbose_cli)
        if not isinstance(logging_enabled, bool) or not isinstance(verbose_cli, bool):
            raise ValueError(
                "`behavior.logging_enabled`/`behavior.verbose_cli` must be boolean"
            )
        return cls(
            mode_default=mode,
            move_strategy=move,
            confidence_threshold=thr,
            stabilization_delay=delay,
            logging_enabled=logging_enabled,
            verbose_cli=verbose_cli,
        )


class LabelsConfig:
    def __init__(self, config_dict: dict):
        pass


class AIConfig:
    def __init__(self, config_dict: dict):
        pass


class APIConfig:
    def __init__(self, config_dict: dict):
        pass


class LoggingConfig:
    def __init__(self, config_dict: dict):
        pass


class SecurityConfig:
    def __init__(self, config_dict: dict):
        pass


class DevelopmentConfig:
    def __init__(self, config_dict: dict):
        pass
