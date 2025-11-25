"""
Módulo de lógica do jogo.
Controla a criação de robôs, a pontuação, o tempo e a validação de códigos.
"""
import time
import random

# Importa as estruturas de dados (Component e RobotLinkedList) do structures.py
from structures import Component, ComponentStack, RobotLinkedList

# --- CONFIGURAÇÕES DO JOGO ---
GAME_TIME_LIMIT = 90  # Tempo total em segundos (1:30 minuto)
MAX_ROBOTS = 5       # Número máximo de robôs na fila de reparo
ROBOT_SPAWN_INTERVAL = 8 # Intervalo de tempo (segundos) para spawn de novos robôs
# ----------------------------

class Robot:
    """
    Representa um robô que precisa de reparo.
    Está aqui para garantir que o Game consiga instanciar Robôs antes de
    selecioná-los e para evitar circular dependency.
    """
    def __init__(self, robot_id, model_name, priority, components_stack):
        self.id = robot_id
        self.model_name = model_name
        self.priority = priority
        self.components = components_stack

    def get_top_component(self):
        return self.components.peek()
    
    def is_repaired(self):
        return self.components.is_empty()


class Game:
    def __init__(self):
        self.robots = RobotLinkedList()
        self.robot_id_counter = 1
        self.selected_robot_id = None
        
        self.start_time = None
        self.last_spawn_time = 0
        self.game_over = False
        self.game_won = False # Indica se o tempo acabou (False) ou se a missão foi completa (True - não implementado)
        
        self.robots_fixed = 0
        self.components_replaced = 0
        self.final_score = 0
        self.max_robots = MAX_ROBOTS # Exposto para a GUI
        
        self.message = "Bem-vindo! Clique em INICIAR JOGO."
        
        # Inicializa a fila com 3 robôs
        for _ in range(3):
            self._generate_new_robot(self.robot_id_counter)
            self.robot_id_counter += 1
            
        self.robots.sort_by_priority() # Ordena a fila inicial
        self.select_robot(self.robots.head.data.id if self.robots.head else None)


    def start_game(self):
        """Reinicia o estado do jogo para começar uma nova partida."""
        self.robots = RobotLinkedList()
        self.robot_id_counter = 1
        self.selected_robot_id = None
        
        self.start_time = time.time()
        self.last_spawn_time = self.start_time
        self.game_over = False
        self.game_won = False
        self.robots_fixed = 0
        self.components_replaced = 0
        self.final_score = 0
        self.message = "Jogo iniciado! Priorize a EMERGÊNCIA."
        
        # Gera os robôs iniciais
        for _ in range(3):
            self._generate_new_robot(self.robot_id_counter)
            self.robot_id_counter += 1
            
        self.robots.sort_by_priority()
        self.select_robot(self.robots.head.data.id if self.robots.head else None)


    def _generate_new_robot(self, robot_id):
        """
        Gera um novo robô com componentes e prioridade aleatórios.
        """
        model_name = random.choice([
            "Modelo Sentinel", "Unidade Worker-7", "Drone de Carga", "Cyborg Patrulha"
        ])
        
        # Distribuição de prioridade (Mais "padrão", menos "emergência")
        priority = random.choices(
            ["emergência", "padrão", "baixo risco"],
            weights=[20, 50, 30],
            k=1
        )[0]

        num_components = random.randint(2, 5)
        components_stack = ComponentStack()

        # --- CORREÇÃO APLICADA AQUI ---
        # A classe Component (em structures.py) já gera o código alfanumérico
        # automaticamente em seu __init__. Apenas instanciamos o componente.
        for _ in range(num_components):
            component_name = random.choice([
                "Sensor de Fluxo", "Placa Lógica", "Atuador de Junta", 
                "Capacitor de Plasma", "Conector de Energia", "Painel de Controle"
            ])
            # Apenas instancie a classe Component, sem passar o código.
            new_component = Component(component_name) 
            components_stack.push(new_component)
        # -----------------------------

        new_robot = Robot(robot_id, model_name, priority, components_stack)
        self.robots.append(new_robot)
        self.robots.sort_by_priority() # Reordena após adicionar
        
        # Se nenhum robô estiver selecionado, selecione o novo (o mais prioritário)
        if self.selected_robot_id is None:
            self.select_robot(new_robot.id)

    
    def select_robot(self, robot_id):
        """Seleciona um robô para exibição na GUI."""
        if robot_id is not None:
            robot = self.robots.find(robot_id)
            if robot:
                self.selected_robot_id = robot_id
    
    def get_selected_robot(self):
        """Retorna o objeto Robot atualmente selecionado."""
        return self.robots.find(self.selected_robot_id)

    
    def validate_code(self, input_code: str):
        """
        Valida o código de substituição do componente no topo da pilha.
        """
        robot = self.get_selected_robot()
        
        if not robot:
            self.message = "Erro: Selecione um robô para reparo."
            return

        top_component = robot.get_top_component()
        
        if not top_component:
            self.message = "Erro: Este robô já está consertado. Selecione outro."
            return
        
        # Garante que a comparação seja feita em CAIXA ALTA (já corrigido na GUI, mas por segurança)
        if input_code.upper() == top_component.replacement_code.upper():
            
            # 1. Componente Reparado
            repaired_component = robot.components.pop()
            self.components_replaced += 1
            self.message = f"SUCESSO! Componente '{repaired_component.name}' substituído."
            
            # 2. Atualiza a pontuação
            self._update_score(robot.priority)
            
            # 3. Verifica se o robô está totalmente consertado
            if robot.is_repaired():
                self._finish_robot_repair(robot)
                
            # 4. Re-seleciona o robô mais prioritário
            self._select_next_robot_in_queue()

        else:
            self.message = "CÓDIGO INCORRETO! Tente novamente."

    
    def _update_score(self, priority: str):
        """Adiciona pontos com base na prioridade do robô."""
        points = {
            "emergência": 150,
            "padrão": 100,
            "baixo risco": 50
        }
        self.final_score += points.get(priority, 0)
    
    
    def _finish_robot_repair(self, robot):
        """Remove o robô consertado da fila e atualiza as estatísticas."""
        self.robots_fixed += 1
        self.final_score += 50 # Bônus por robô
        self.message += f" - Robô #{robot.id} REPARO FINALIZADO com sucesso!"
        self.robots.remove(robot.id)
        
    
    def _select_next_robot_in_queue(self):
        """Selecona o próximo robô mais prioritário ou deseleciona se a fila estiver vazia."""
        if self.robots.is_empty():
            self.selected_robot_id = None
            self.message = "Fila de reparo vazia. Aguardando novos robôs..."
        else:
            # Seleciona o robô que está no topo da fila após a ordenação
            self.select_robot(self.robots.head.data.id)


    # --- CONTROLE DE TEMPO E FLUXO ---

    def get_time_left(self):
        """Retorna o tempo restante de jogo em segundos."""
        if self.start_time is None:
            return GAME_TIME_LIMIT
        
        time_passed = time.time() - self.start_time
        time_left = GAME_TIME_LIMIT - time_passed
        return max(0, time_left)

    def get_total_time_played(self):
        """Retorna o tempo total de jogo jogado (usado no game over)."""
        if self.start_time is None or not self.game_over:
            return 0
        return self.start_time + GAME_TIME_LIMIT - self.start_time
    
    def update(self, current_time):
        """Lógica de atualização do jogo (chamada a cada frame)."""
        if self.game_over or self.start_time is None:
            return

        time_left = self.get_time_left()

        # 1. Fim de Jogo
        if time_left <= 0:
            self.game_over = True
            self.message = "TEMPO ESGOTADO! Fim de Jogo."
            return

        # 2. Spawn de Novos Robôs
        if current_time - self.last_spawn_time >= ROBOT_SPAWN_INTERVAL:
            if len(self.robots) < MAX_ROBOTS:
                self._generate_new_robot(self.robot_id_counter)
                self.robot_id_counter += 1
                self.last_spawn_time = current_time
                self.message = f"Novo robô #{self.robot_id_counter - 1} chegou para reparo."
            else:
                self.message = "Oficina lotada! Máximo de robôs atingido."
                self.last_spawn_time = current_time # Resetar para tentar novamente

        # 3. Manter a seleção no robô mais prioritário
        if not self.robots.is_empty() and (self.selected_robot_id is None or self.selected_robot_id != self.robots.head.data.id):
             self.select_robot(self.robots.head.data.id)