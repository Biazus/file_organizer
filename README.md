

# Organizador Inteligente de Arquivos (CLI) - WORK IN PROGRESS

O Organizador Inteligente de Arquivos é uma ferramenta em Python para automatizar e simplificar a organização de pastas pessoais.  
Ele monitora diretórios definidos pelo usuário (como Downloads ou Desktop), identifica automaticamente o tipo/categoria dos arquivos — por regras simples ou por reconhecimento semântico via IA — e os organiza em subpastas apropriadas, com segurança, transparência e reversibilidade.

## Sumário
- [Utilidade](#utilidade)
- [Benefícios](#benefícios)
- [Regras de Segurança e Ponderações](#regras-de-segurança-e-ponderações)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura Conceitual](#estrutura-conceitual)
- [Exemplo de Uso](#exemplo-de-uso)
- [Futuras Extensões](#futuras-extensões)
- [Licença e Aviso](#licença-e-aviso)
- [Resumo](#resumo)

## Utilidade
Este projeto nasce da necessidade de evitar o acúmulo de arquivos sem nome ou repetidos em pastas como Downloads, que acabam virando uma “caixa de sapatos digital”.  
Com o organizador, o usuário ganha tempo, ordem e clareza, deixando o sistema de arquivos limpo e fácil de navegar.  
A inteligência incorporada permite reconhecer o propósito de arquivos pelo nome e contexto (ex.: entender que “Install 2XKO Early Access” é um instalador de jogo ou que “GOGGalaxy2.0” é um launcher de loja).

## Benefícios
- Organização automática e inteligente: detecta tipos e categorias com base em extensões, nomes, metadados e análise semântica.
- Customização total: o usuário define quais pastas serão organizadas, quais ignorar e como categorizar.
- Segurança e reversão garantidas: cada ação é registrada, permitindo desfazer movimentações.
- Sem dependência gráfica: interface por linha de comando (CLI) com mensagens claras e modo de simulação (dry run).
- Aprendizado contínuo (opcional): o sistema pode ajustar suas classificações com base em correções manuais do usuário.

## Regras de Segurança e Ponderações
Para evitar qualquer interferência indevida ou dano ao sistema, o organizador segue boas práticas rigorosas:
- Atuação restrita a pastas definidas pelo usuário: o programa só opera nas pastas incluídas na configuração, sem acesso a diretórios sensíveis do sistema.
- Blacklist de locais protegidos: impede qualquer ação em pastas como Program Files, Windows, AppData, Steam, node_modules e equivalentes no Linux.
- Movimentações reversíveis: nunca remove arquivos definitivamente; apenas move para diretórios organizados ou para uma área de quarentena.
- Verificações de uso: detecta se arquivos estão sendo usados ativamente (ex.: durante download ou execução) e aguarda antes de agir.
- Confiança mínima nas classificações de IA: arquivos com probabilidade baixa ou categoria ambígua não são movidos automaticamente, apenas listados para revisão.
- Logs completos: cada arquivo processado gera registro com local original, categoria detectada, ação aplicada e data/hora.
- Permissões limitadas: roda sempre sob o usuário padrão, nunca como administrador/root.
- Modo de simulação: permite visualizar todas as ações antes de aplicá-las (sem alterar nada de verdade).

Essas medidas garantem que o programa seja seguro, previsível e fácil de controlar, sem risco de corromper outros softwares ou pastas críticas do sistema.

## Funcionalidades Principais
- Monitoramento em tempo real de pastas com `watchdog`, reagindo a novos arquivos assim que aparecem.
- Classificação automática de arquivos:
  - Heurística (por extensão, nome, tamanho e tipo).
  - Semântica (usando transformers em modo zero-shot classification para interpretar nomes e contextos).
- Movimentação segura de arquivos, com barras de progresso e verificação de integridade.
- Criação automática de estrutura organizada, por exemplo:
  ```
  /Organizados/
  ├── Jogos/
  ├── Instalações/
  ├── Documentos/
  ├── Mídias/
  └── Diversos/
  ```
- Logs legíveis e opção de exportar relatórios em `.json` ou `.csv`.
- Undo e reclassificação manual (via CLI).
- Configurações persistentes em arquivo `.yaml` ou `.json`, permitindo ajustes finos entre execuções.

## Tecnologias Utilizadas
- Python 3.11+
- watchdog – monitoramento em tempo real de pastas
- pathlib, os, shutil – manipulação e movimentação de arquivos
- threading – execução concorrente de tarefas de classificação e monitoramento
- transformers – classificação semântica baseada em linguagem natural
- argparse – interface de linha de comando
- logging – mensagens estruturadas e rastreamento de eventos

## Estrutura Conceitual
Fluxo simplificado de funcionamento:
1. Inicialização: o usuário define via CLI a(s) pasta(s) a monitorar e o modo de execução (dry-run ou ativo).
2. Monitoramento: `watchdog` observa modificações e detecta novos arquivos.
3. Análise: o nome, tipo e metadados são extraídos; a IA classifica semanticamente com base em rótulos pré-definidos.
4. Decisão: com base em confiança, regras e listas de permissão, o arquivo é:
   - Movido para a categoria correta; ou
   - Adicionado à lista de revisão; ou
   - Ignorado com justificativa.
5. Log e relatório: a cada ciclo, o sistema atualiza o arquivo de log persistente, permitindo auditoria e reversão posterior.

## Exemplo de Uso
Execute em modo simulação (dry-run):
```bash
python organizer.py --path "C:/Users/Miller/Downloads" --mode dry --save-plan "plan.json"
```

Saída esperada (modo simulação):
```text
[DRY-RUN] 10 arquivos analisados.

Plano salvo em: plans/plan_2025-10-17.json
```
Exemplo de plano:
```text
[

{"source": "Downloads/Install 2XKO Early Access.exe", "target": "Organizados/Jogos/Instaladores/", "category": "jogo/instalador"},

{"source": "Downloads/nota_fiscal.pdf", "target": "Organizados/Documentos/", "category": "documento"}

]
```

## Futuras Extensões
- Adicionar integração com APIs para reconhecimento de arquivos multimídia.
- Treinar modelo customizado com base nas preferências do usuário.
- Interface visual em Streamlit (modo dashboard) para revisão interativa.
- Implementar cache de classificação para acelerar execuções futuras.

## Licença e Aviso
Este projeto é de uso pessoal e educativo.  
Não possui garantias de desempenho em todos os sistemas e recomenda-se testá-lo em modo simulação antes da primeira execução ativa.  
O autor não se responsabiliza por eventuais danos decorrentes do uso sem revisão das regras de segurança.

## Resumo
Um organizador CLI com inteligência, seguro por design, capaz de manter suas pastas limpas sem que você precise mover um único arquivo manualmente.

## Futuro
Ideia de fazer isso com os favoritos do Chrome também
```

