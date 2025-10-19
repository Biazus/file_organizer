class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # If no instance exists, create a new one
            cls._instance = super().__new__(cls)
        return cls._instance  # Return the existing instance

    def __init__(self, *args, **kwargs):
        if not hasattr(self, "_initialized"):  # Prevent re-initialization
            self._initialized = True
            self.setup()

    def setup(self):
        raise NotImplementedError()
