"""
Módulo de estruturas de dados manuais
Implementa lista encadeada para robôs e pilha encadeada para componentes
"""


class Node:
    """Nó para estruturas encadeadas"""
    def __init__(self, data):
        self.data = data
        self.next = None


class ComponentStack:
    """
    Pilha encadeada manual para componentes de robôs
    Implementa LIFO (Last In, First Out)
    """
    def __init__(self):
        self.top = None
        self.size = 0
    
    def push(self, component):
        """Adiciona um componente no topo da pilha"""
        new_node = Node(component)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
    
    def pop(self):
        """Remove e retorna o componente do topo da pilha"""
        if self.is_empty():
            return None
        removed = self.top.data
        self.top = self.top.next
        self.size -= 1
        return removed
    
    def peek(self):
        """Retorna o componente do topo sem removê-lo"""
        if self.is_empty():
            return None
        return self.top.data
    
    def is_empty(self):
        """Verifica se a pilha está vazia"""
        return self.top is None
    
    def get_all(self):
        """Retorna todos os componentes da pilha (do topo para a base)"""
        components = []
        current = self.top
        while current is not None:
            components.append(current.data)
            current = current.next
        return components
    
    def __len__(self):
        """Retorna o tamanho da pilha"""
        return self.size


class RobotLinkedList:
    """
    Lista encadeada manual para robôs
    Implementa operações de inserção, remoção, busca e ordenação
    """
    def __init__(self):
        self.head = None
        self.size = 0
    
    def append(self, robot):
        """Adiciona um robô no final da lista"""
        new_node = Node(robot)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def remove(self, robot_id):
        """Remove um robô pelo ID"""
        if self.head is None:
            return False
        
        # Se for o primeiro nó
        if self.head.data.id == robot_id:
            self.head = self.head.next
            self.size -= 1
            return True
        
        # Busca o robô na lista
        current = self.head
        while current.next is not None:
            if current.next.data.id == robot_id:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        
        return False
    
    def find(self, robot_id):
        """Busca um robô pelo ID"""
        current = self.head
        while current is not None:
            if current.data.id == robot_id:
                return current.data
            current = current.next
        return None
    
    def get_all(self):
        """Retorna todos os robôs da lista"""
        robots = []
        current = self.head
        while current is not None:
            robots.append(current.data)
            current = current.next
        return robots
    
    def sort_by_priority(self):
        """
        Ordena a lista por prioridade (emergência > padrão > baixo risco)
        Usa algoritmo de ordenação por inserção
        """
        if self.head is None or self.head.next is None:
            return
        
        # Converte para lista Python temporária para facilitar ordenação
        robots = self.get_all()
        priority_order = {"emergência": 0, "padrão": 1, "baixo risco": 2}
        
        # Ordenação por inserção
        for i in range(1, len(robots)):
            key = robots[i]
            j = i - 1
            while j >= 0 and priority_order[robots[j].priority] > priority_order[key.priority]:
                robots[j + 1] = robots[j]
                j -= 1
            robots[j + 1] = key
        
        # Reconstrói a lista encadeada
        self.head = None
        self.size = 0
        for robot in robots:
            self.append(robot)
    
    def is_empty(self):
        """Verifica se a lista está vazia"""
        return self.head is None
    
    def __len__(self):
        """Retorna o tamanho da lista"""
        return self.size

