# Oficina de Reparo de Robôs

Jogo completo em Python 3.10+ com pygame onde você é Alex Nova, técnico-chefe da Oficina Central de Reparo de Robôs no ano 2175.

## História

Após uma falha massiva de energia na cidade futurista Neon Forge, centenas de robôs ficaram danificados. Sua missão é consertar os robôs que chegam antes que o caos tecnológico se espalhe pela cidade.

## Requisitos

- Python 3.10 ou superior
- pygame 2.5.0 ou superior

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Jogar

1. Execute o jogo:
```bash
python main.py
```

2. Na tela inicial, leia a história e instruções, depois clique em "Iniciar Jogo"

3. **Objetivo**: Conserte os robôs substituindo seus componentes defeituosos antes que a oficina lotar

4. **Como jogar**:
   - Selecione um robô clicando na lista à esquerda
   - Veja a pilha de componentes no painel central (o componente no topo precisa ser consertado primeiro)
   - Digite o código de substituição de 4 dígitos no campo à direita
   - Clique em "Substituir Componente" ou pressione Enter
   - Quando todos os componentes de um robô forem substituídos, ele será removido da lista

5. **Game Over**: O jogo termina quando a oficina atinge o limite de 10 robôs

6. **Vitória**: Conserte todos os robôs e mantenha a oficina vazia por 3 segundos

## Estrutura do Projeto

- `main.py`: Ponto de entrada do jogo
- `game.py`: Lógica do jogo (robôs, componentes, validação)
- `gui.py`: Interface gráfica com pygame
- `structures.py`: Estruturas de dados manuais (lista encadeada e pilha)
- `ranking.json`: Arquivo JSON com o ranking de jogadores (criado automaticamente)

## Características Técnicas

- **Lista Encadeada Manual**: Implementação própria para armazenar robôs
- **Pilha Encadeada Manual**: Implementação própria para armazenar componentes de cada robô
- **Ordenação por Prioridade**: Robôs são ordenados automaticamente (emergência > padrão > baixo risco)
- **Sistema de Ranking**: Salva os melhores scores em arquivo JSON
- **Interface Futurista**: Design moderno com paleta de cores metálicas e azuis

## Classes Principais

- `Robot`: Representa um robô com ID, modelo, prioridade e pilha de componentes
- `Component`: Representa um componente defeituoso com nome, código e tempo de reparo
- `RobotLinkedList`: Lista encadeada manual para robôs
- `ComponentStack`: Pilha encadeada manual para componentes
- `Game`: Gerencia a lógica do jogo
- `GUI`: Gerencia a interface gráfica

## Score

O score é calculado como:
```
Score = (Robôs Consertados × 100) + (Componentes Substituídos × 10) - Tempo Total (segundos)
```

## Desenvolvido com

- Python 3.10+
- pygame 2.5.0+

