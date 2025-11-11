"""
Módulo de lógica do jogo
Gerencia robôs, componentes, validação de códigos e estado do jogo
"""

import random
import time
from structures import RobotLinkedList, ComponentStack


class Component:
    """Representa um componente defeituoso de um robô"""
    def __init__(self, name, replacement_code, repair_time):
        self.name = name
        self.replacement_code = replacement_code
        self.repair_time = repair_time  # em segundos
    
    def __str__(self):
        return f"{self.name} (Código: {self.replacement_code})"


class Robot:
    """Representa um robô que precisa de reparo"""
    def __init__(self, robot_id, model_name, priority):
        self.id = robot_id
        self.model_name = model_name
        self.priority = priority  # "emergência", "padrão", "baixo risco"
        self.state = "pendente"  # "pendente" ou "consertado"
        self.components = ComponentStack()
    
    def add_component(self, component):
        """Adiciona um componente à pilha do robô"""
        self.components.push(component)
    
    def is_fixed(self):
        """Verifica se o robô foi completamente consertado"""
        return self.components.is_empty()
    
    def get_top_component(self):
        """Retorna o componente no topo da pilha"""
        return self.components.peek()
    
    def remove_top_component(self):
        """Remove e retorna o componente do topo da pilha"""
        return self.components.pop()
    
    def __str__(self):
        return f"Robô #{self.id} - {self.model_name} ({self.priority})"


class Game:
    """Gerencia a lógica principal do jogo"""
    def __init__(self, max_robots=10):
        self.robots = RobotLinkedList()
        self.max_robots = max_robots
        self.start_time = None
        self.end_time = None
        self.robots_fixed = 0
        self.components_replaced = 0
        self.game_over = False
        self.game_won = False
        self.selected_robot_id = None
        self.last_robot_arrival = 0
        # --- ATUALIZADO ---
        self.robot_arrival_interval = 4.0  # segundos entre chegadas (COMEÇA MAIS RÁPIDO)
        self.message = ""
        self.message_time = 0
        
        # Contador de ID para evitar IDs duplicados após remoção
        self.robot_id_counter = 0 
        
        # Listas de dados para geração aleatória
        self.model_names = [
            "AX-2000", "Nexus Prime", "Cyborg X7", "Titan MK3",
            "Phoenix Pro", "Quantum Core", "Steel Sentinel", "Aurora Beta",
            "Neon Warrior", "Iron Forge", "Plasma Drive", "Cyber Matrix"
        ]
        
        self.component_names = [
            "Processador Neural", "Sensor Óptico", "Braço Hidráulico",
            "Sistema de Energia", "Unidade de Memória", "Transmissor",
            "Placa Mãe", "Cooler", "Bateria", "Motor de Locomoção",
            "Antena de Comunicação", "Câmera Infravermelha", "Garra Mecânica",
            "Display Holográfico", "Sistema de Navegação"
        ]
    
    def start_game(self):
        """Inicia uma nova partida"""
        self.robots = RobotLinkedList()
        self.start_time = time.time()
        self.end_time = None
        self.robots_fixed = 0
        self.components_replaced = 0
        self.game_over = False
        self.game_won = False
        self.selected_robot_id = None
        self.last_robot_arrival = time.time()
        self.message = "Bem-vindo à Oficina! Robôs estão chegando..."
        self.message_time = time.time()
        
        # --- ATUALIZADO ---
        self.robot_arrival_interval = 4.0 # Reseta a velocidade para um novo jogo
        self.robot_id_counter = 0 # Reseta o contador de ID
        
        # Adiciona o primeiro robô
        self.spawn_robot()
    
    def spawn_robot(self):
        """Gera um ou mais robôs aleatórios com componentes"""
        
        # Decide quantos robôs spawna (1-3, com maior chance de 2)
        num_to_spawn = random.choices([1, 2, 3], weights=[0.4, 0.4, 0.2])[0]
        robots_spawned_names = []

        for _ in range(num_to_spawn):
            if len(self.robots) >= self.max_robots:
                self.game_over = True
                self.end_time = time.time()
                self.message = "Oficina lotada! Game Over!"
                return  # Sai da função inteira
            
            # Usa o contador de ID para garantir IDs únicos
            self.robot_id_counter += 1
            robot_id = self.robot_id_counter

            model_name = random.choice(self.model_names)
            priorities = ["emergência", "padrão", "baixo risco"]
            weights = [0.3, 0.5, 0.2]  # Probabilidades
            priority = random.choices(priorities, weights=weights)[0]
            
            robot = Robot(robot_id, model_name, priority)
            
            # Adiciona 1 a 5 componentes aleatórios
            num_components = random.randint(1, 5)
            for _ in range(num_components):
                component_name = random.choice(self.component_names)
                # Gera código de 4 dígitos
                replacement_code = f"{random.randint(1000, 9999)}"
                repair_time = random.randint(5, 15)
                component = Component(component_name, replacement_code, repair_time)
                robot.add_component(component)
            
            self.robots.append(robot)
            robots_spawned_names.append(f"{model_name} (#{robot_id})")
        
        self.robots.sort_by_priority()  # Ordena por prioridade
        
        # Atualiza a mensagem com base em quantos robôs chegaram
        if robots_spawned_names:
            if len(robots_spawned_names) > 1:
                self.message = f"Novos robôs chegaram! ({len(robots_spawned_names)})"
            else:
                self.message = f"Novo robô chegou! {robots_spawned_names[0]}"
            self.message_time = time.time()
    
    def update(self, current_time):
        """Atualiza o estado do jogo"""
        if self.game_over or self.game_won:
            return
        
        # Verifica se é hora de um novo robô chegar
        if current_time - self.last_robot_arrival >= self.robot_arrival_interval:
            self.spawn_robot()
            self.last_robot_arrival = current_time
            # --- ATUALIZADO ---
            # Aumenta a frequência mais rápido (0.2) e com mínimo menor (1.5)
            self.robot_arrival_interval = max(1.5, self.robot_arrival_interval - 0.2)
        
        # Remove mensagens antigas após 3 segundos
        if self.message and current_time - self.message_time > 3.0:
            if "Novo robô chegou" not in self.message:
                self.message = ""
        
        # Verifica se todos os robôs foram consertados (vitória)
        # Se não houver robôs e já consertou pelo menos um, considera vitória
        if len(self.robots) == 0 and self.robots_fixed > 0:
            if not hasattr(self, 'win_check_time'):
                self.win_check_time = current_time
            # Aguarda 3 segundos sem robôs para confirmar vitória
            elif current_time - self.win_check_time > 3.0:
                self.game_won = True
                self.end_time = time.time()
        else:
            # Reset do timer de vitória se houver robôs novamente
            if hasattr(self, 'win_check_time'):
                delattr(self, 'win_check_time')
    
    def select_robot(self, robot_id):
        """Seleciona um robô para reparo"""
        robot = self.robots.find(robot_id)
        if robot:
            self.selected_robot_id = robot_id
            return True
        return False
    
    def get_selected_robot(self):
        """Retorna o robô selecionado"""
        if self.selected_robot_id is None:
            return None
        return self.robots.find(self.selected_robot_id)
    
    def validate_code(self, code):
        """Valida o código digitado para o componente no topo da pilha"""
        robot = self.get_selected_robot()
        if robot is None:
            self.message = "Selecione um robô primeiro!"
            self.message_time = time.time()
            return False
        
        top_component = robot.get_top_component()
        if top_component is None:
            self.message = "Este robô já está consertado!"
            self.message_time = time.time()
            return False
        
        if code == top_component.replacement_code:
            robot.remove_top_component()
            self.components_replaced += 1
            self.message = "Código correto! Componente substituído!"
            self.message_time = time.time()
            
            # Verifica se o robô foi completamente consertado
            if robot.is_fixed():
                robot.state = "consertado"
                self.robots.remove(robot.id)
                self.robots_fixed += 1
                self.selected_robot_id = None
                self.message = f"Robô #{robot.id} consertado com sucesso!"
                self.message_time = time.time()
            
            return True
        else:
            self.message = "Código incorreto! Tente novamente."
            self.message_time = time.time()
            return False
    
    def get_elapsed_time(self):
        """Retorna o tempo decorrido desde o início do jogo"""
        if self.start_time is None:
            return 0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def get_total_time(self):
        """Retorna o tempo total da partida"""
        if self.start_time is None or self.end_time is None:
            return 0
        return self.end_time - self.start_time

# """
# Módulo de lógica do jogo
# Gerencia robôs, componentes, validação de códigos e estado do jogo
# """

# import random
# import time
# from structures import RobotLinkedList, ComponentStack


# class Component:
#     """Representa um componente defeituoso de um robô"""
#     def __init__(self, name, replacement_code, repair_time):
#         self.name = name
#         self.replacement_code = replacement_code
#         self.repair_time = repair_time  # em segundos
    
#     def __str__(self):
#         return f"{self.name} (Código: {self.replacement_code})"


# class Robot:
#     """Representa um robô que precisa de reparo"""
#     def __init__(self, robot_id, model_name, priority):
#         self.id = robot_id
#         self.model_name = model_name
#         self.priority = priority  # "emergência", "padrão", "baixo risco"
#         self.state = "pendente"  # "pendente" ou "consertado"
#         self.components = ComponentStack()
    
#     def add_component(self, component):
#         """Adiciona um componente à pilha do robô"""
#         self.components.push(component)
    
#     def is_fixed(self):
#         """Verifica se o robô foi completamente consertado"""
#         return self.components.is_empty()
    
#     def get_top_component(self):
#         """Retorna o componente no topo da pilha"""
#         return self.components.peek()
    
#     def remove_top_component(self):
#         """Remove e retorna o componente do topo da pilha"""
#         return self.components.pop()
    
#     def __str__(self):
#         return f"Robô #{self.id} - {self.model_name} ({self.priority})"


# class Game:
#     """Gerencia a lógica principal do jogo"""
#     def __init__(self, max_robots=10):
#         self.robots = RobotLinkedList()
#         self.max_robots = max_robots
#         self.start_time = None
#         self.end_time = None
#         self.robots_fixed = 0
#         self.components_replaced = 0
#         self.game_over = False
#         self.game_won = False
#         self.selected_robot_id = None
#         self.last_robot_arrival = 0
#         self.robot_arrival_interval = 5.0  # segundos entre chegadas
#         self.message = ""
#         self.message_time = 0
        
#         # Listas de dados para geração aleatória
#         self.model_names = [
#             "AX-2000", "Nexus Prime", "Cyborg X7", "Titan MK3",
#             "Phoenix Pro", "Quantum Core", "Steel Sentinel", "Aurora Beta",
#             "Neon Warrior", "Iron Forge", "Plasma Drive", "Cyber Matrix"
#         ]
        
#         self.component_names = [
#             "Processador Neural", "Sensor Óptico", "Braço Hidráulico",
#             "Sistema de Energia", "Unidade de Memória", "Transmissor",
#             "Placa Mãe", "Cooler", "Bateria", "Motor de Locomoção",
#             "Antena de Comunicação", "Câmera Infravermelha", "Garra Mecânica",
#             "Display Holográfico", "Sistema de Navegação"
#         ]
    
#     def start_game(self):
#         """Inicia uma nova partida"""
#         self.robots = RobotLinkedList()
#         self.start_time = time.time()
#         self.end_time = None
#         self.robots_fixed = 0
#         self.components_replaced = 0
#         self.game_over = False
#         self.game_won = False
#         self.selected_robot_id = None
#         self.last_robot_arrival = time.time()
#         self.message = "Bem-vindo à Oficina! Robôs estão chegando..."
#         self.message_time = time.time()
        
#         # Adiciona o primeiro robô
#         self.spawn_robot()
    
#     def spawn_robot(self):
#         """Gera um novo robô aleatório com componentes"""
#         if len(self.robots) >= self.max_robots:
#             self.game_over = True
#             self.end_time = time.time()
#             self.message = "Oficina lotada! Game Over!"
#             return
        
#         robot_id = len(self.robots) + 1
#         model_name = random.choice(self.model_names)
#         priorities = ["emergência", "padrão", "baixo risco"]
#         weights = [0.3, 0.5, 0.2]  # Probabilidades
#         priority = random.choices(priorities, weights=weights)[0]
        
#         robot = Robot(robot_id, model_name, priority)
        
#         # Adiciona 1 a 5 componentes aleatórios
#         num_components = random.randint(1, 5)
#         for _ in range(num_components):
#             component_name = random.choice(self.component_names)
#             # Gera código de 4 dígitos
#             replacement_code = f"{random.randint(1000, 9999)}"
#             repair_time = random.randint(5, 15)
#             component = Component(component_name, replacement_code, repair_time)
#             robot.add_component(component)
        
#         self.robots.append(robot)
#         self.robots.sort_by_priority()  # Ordena por prioridade
        
#         self.message = f"Novo robô chegou! {robot.model_name} (#{robot_id})"
#         self.message_time = time.time()
    
#     def update(self, current_time):
#         """Atualiza o estado do jogo"""
#         if self.game_over or self.game_won:
#             return
        
#         # Verifica se é hora de um novo robô chegar
#         if current_time - self.last_robot_arrival >= self.robot_arrival_interval:
#             self.spawn_robot()
#             self.last_robot_arrival = current_time
#             # Aumenta gradualmente a frequência
#             self.robot_arrival_interval = max(3.0, self.robot_arrival_interval - 0.1)
        
#         # Remove mensagens antigas após 3 segundos
#         if self.message and current_time - self.message_time > 3.0:
#             if "Novo robô chegou" not in self.message:
#                 self.message = ""
        
#         # Verifica se todos os robôs foram consertados (vitória)
#         # Se não houver robôs e já consertou pelo menos um, considera vitória
#         if len(self.robots) == 0 and self.robots_fixed > 0:
#             if not hasattr(self, 'win_check_time'):
#                 self.win_check_time = current_time
#             # Aguarda 3 segundos sem robôs para confirmar vitória
#             elif current_time - self.win_check_time > 3.0:
#                 self.game_won = True
#                 self.end_time = time.time()
#         else:
#             # Reset do timer de vitória se houver robôs novamente
#             if hasattr(self, 'win_check_time'):
#                 delattr(self, 'win_check_time')
    
#     def select_robot(self, robot_id):
#         """Seleciona um robô para reparo"""
#         robot = self.robots.find(robot_id)
#         if robot:
#             self.selected_robot_id = robot_id
#             return True
#         return False
    
#     def get_selected_robot(self):
#         """Retorna o robô selecionado"""
#         if self.selected_robot_id is None:
#             return None
#         return self.robots.find(self.selected_robot_id)
    
#     def validate_code(self, code):
#         """Valida o código digitado para o componente no topo da pilha"""
#         robot = self.get_selected_robot()
#         if robot is None:
#             self.message = "Selecione um robô primeiro!"
#             self.message_time = time.time()
#             return False
        
#         top_component = robot.get_top_component()
#         if top_component is None:
#             self.message = "Este robô já está consertado!"
#             self.message_time = time.time()
#             return False
        
#         if code == top_component.replacement_code:
#             robot.remove_top_component()
#             self.components_replaced += 1
#             self.message = "Código correto! Componente substituído!"
#             self.message_time = time.time()
            
#             # Verifica se o robô foi completamente consertado
#             if robot.is_fixed():
#                 robot.state = "consertado"
#                 self.robots.remove(robot.id)
#                 self.robots_fixed += 1
#                 self.selected_robot_id = None
#                 self.message = f"Robô #{robot.id} consertado com sucesso!"
#                 self.message_time = time.time()
            
#             return True
#         else:
#             self.message = "Código incorreto! Tente novamente."
#             self.message_time = time.time()
#             return False
    
#     def get_elapsed_time(self):
#         """Retorna o tempo decorrido desde o início do jogo"""
#         if self.start_time is None:
#             return 0
#         end = self.end_time if self.end_time else time.time()
#         return end - self.start_time
    
#     def get_total_time(self):
#         """Retorna o tempo total da partida"""
#         if self.start_time is None or self.end_time is None:
#             return 0
#         return self.end_time - self.start_time

