"""
Módulo de interface gráfica
Implementa todas as telas do jogo usando pygame

Revisão de Design v2.0
- Nova paleta de cores (Hi-Contrast Sci-Fi)
- Cantos arredondados (Design moderno)
- Seção "Componente Alvo" dedicada para fácil visualização do código
- Ícones de robô vetoriais
- Carregamento de fonte personalizada
---
Revisão v2.1
- REMOVIDO todo o sistema de Ranking
"""

import pygame
import json
import os
from game import Game


# --- NOVA PALETA DE CORES (High-Contrast Sci-Fi) ---
COLORS = {
    'background': (10, 15, 30),      # Azul-noite muito escuro
    'panel_bg': (20, 30, 50),        # Azul-noite escuro
    'panel_border': (40, 60, 90),    # Borda sutil
    
    'text_primary': (230, 240, 255), # Quase branco
    'text_secondary': (140, 160, 190),# Cinza-azulado claro
    'text_dark': (80, 100, 130),      # Cinza-azulado escuro

    'accent_cyan': (0, 220, 255),    # Ciano Neon (Foco principal)
    'accent_purple': (180, 100, 255),# Roxo Neon (Botões)
    'accent_yellow': (255, 220, 0),  # Amarelo (Destaque código)
    
    'success': (0, 255, 150),        # Verde Neon
    'error': (255, 60, 60),          # Vermelho Neon
    'warning': (255, 200, 0),        # Laranja/Amarelo

    'priority_emergency': (255, 60, 60),  # Vermelho
    'priority_standard': (255, 200, 0), # Laranja
    'priority_low': (0, 255, 150),      # Verde

    'button': (180, 100, 255),       # Roxo
    'button_hover': (210, 130, 255), # Roxo claro
    'button_active': (150, 80, 230), # Roxo escuro
    
    'input_bg': (30, 45, 70),        # Fundo do input
    'input_border': (80, 100, 130),
    'input_focus': (0, 220, 255),    # Ciano Neon
}


class GUI:
    """Gerencia a interface gráfica do jogo"""
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Oficina de Reparo de Robôs - Neon Forge")
        self.clock = pygame.time.Clock()
        
        # --- CARREGAMENTO DE FONTES ---
        self.load_fonts()
        
        self.game = Game()
        self.state = "menu"  # "menu", "playing", "game_over"
        self.input_code = ""
        self.input_active = False
        
        # --- REMOVIDO --- Variáveis de Ranking
        
        # --- UI RECTS ATUALIZADO ---
        self.ui_rects = {
            'menu_start': pygame.Rect(self.width // 2 - 150, self.height - 120, 300, 60),
            
            'play_panel_left': pygame.Rect(20, 20, 350, 500),
            'play_panel_center': pygame.Rect(390, 20, 400, 500),
            'play_panel_right': pygame.Rect(810, 20, 370, 500),
            
            'play_input_code': pygame.Rect(810 + 10, 20 + 380, 370 - 20, 40),
            'play_submit_code': pygame.Rect(810 + 10, 20 + 430, 370 - 20, 50),
            
            # --- ATUALIZADO --- Posição do botão de menu movida para cima
            'over_back_menu': pygame.Rect(self.width // 2 - 150, 660, 300, 60)
            
            # --- REMOVIDO --- 'over_input_name' e 'over_save_rank'
        }
        
        # --- REMOVIDO --- Carregamento de Ranking
    
    def load_fonts(self):
        """Carrega fontes personalizadas, com fallback para a padrão"""
        self.font_path_regular = os.path.join("font", "RobotoMono-Regular.ttf")
        self.font_path_bold = os.path.join("font", "RobotoMono-Bold.ttf")

        try:
            self.font_large = pygame.font.Font(self.font_path_bold, 42)
            self.font_medium = pygame.font.Font(self.font_path_bold, 30)
            self.font_medium_regular = pygame.font.Font(self.font_path_regular, 28)
            self.font_small = pygame.font.Font(self.font_path_regular, 22)
            self.font_small_bold = pygame.font.Font(self.font_path_bold, 22)
            self.font_tiny = pygame.font.Font(self.font_path_regular, 18)
        except FileNotFoundError:
            print("AVISO: Fonte personalizada não encontrada. Usando fonte padrão.")
            print(f"Procurei por: {self.font_path_regular} e {self.font_path_bold}")
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_medium_regular = pygame.font.Font(None, 30)
            self.font_small = pygame.font.Font(None, 24)
            self.font_small_bold = pygame.font.Font(None, 24)
            self.font_tiny = pygame.font.Font(None, 20)

    # --- REMOVIDO --- Métodos load_ranking, save_ranking, add_to_ranking
    
    def draw_text(self, text, font, color, x, y, center=False, center_x=False, center_y=False):
        """Desenha texto na tela com mais opções de alinhamento"""
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        
        if center:
            rect.center = (x, y)
        elif center_x:
            rect.centerx = x
            rect.y = y
        elif center_y:
            rect.centery = y
            rect.x = x
        else:
            rect.topleft = (x, y)
            
        self.screen.blit(surface, rect)
        return rect # Retorna o rect para colisões

    def draw_button(self, text, x, y, width, height, hover=False, active=False):
        """Desenha um botão moderno na tela"""
        if active:
            color = COLORS['button_active']
        elif hover:
            color = COLORS['button_hover']
        else:
            color = COLORS['button']
        
        # Sombra sutil
        pygame.draw.rect(self.screen, (0,0,0,50), (x+2, y+2, width, height), border_radius=8)
        # Botão principal
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=8)
        
        # Texto
        self.draw_text(text, self.font_medium, COLORS['text_primary'], 
                       x + width // 2, y + height // 2, center=True)
        
        return pygame.Rect(x, y, width, height)
    
    def draw_input_box(self, text, x, y, width, height, active=False):
        """Desenha uma caixa de input moderna"""
        bg_color = COLORS['input_bg']
        border_color = COLORS['input_focus'] if active else COLORS['input_border']
        
        pygame.draw.rect(self.screen, bg_color, (x, y, width, height), border_radius=5)
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2, border_radius=5)
        
        # Desenha o texto
        text_surf = self.font_medium_regular.render(text, True, COLORS['text_primary'])
        self.screen.blit(text_surf, (x + 10, y + height // 2 - text_surf.get_height() // 2))
        
        # Cursor piscante
        if active:
            current_time = pygame.time.get_ticks()
            if (current_time // 500) % 2:
                cursor_x = x + 10 + text_surf.get_width()
                pygame.draw.line(self.screen, COLORS['text_primary'], 
                               (cursor_x, y + 10), 
                               (cursor_x, y + height - 10), 2)
        
        return pygame.Rect(x, y, width, height)

    def draw_panel(self, rect):
        """Helper para desenhar um painel padrão"""
        pygame.draw.rect(self.screen, COLORS['panel_bg'], rect, border_radius=8)
        pygame.draw.rect(self.screen, COLORS['panel_border'], rect, 2, border_radius=8)

    def draw_robot_icon(self, x, y, robot):
        """Desenha um ícone de robô vetorial simples"""
        
        if robot is None:
            # Desenha um robô "vazio" ou placeholder
            head_color = COLORS['text_dark']
            eye_color = COLORS['panel_border']
            head_rect = pygame.Rect(x - 30, y, 60, 50)
            pygame.draw.rect(self.screen, head_color, head_rect, border_radius=10)
            pygame.draw.rect(self.screen, eye_color, (x - 15, y + 15, 30, 20), border_radius=5)
            self.draw_text("?", self.font_large, COLORS['panel_bg'], x, y + 25, center=True)
            return

        # Gera uma "semente" baseada no modelo para variar o visual
        seed = hash(robot.model_name) % 3
        head_color = COLORS['text_secondary']
        eye_color = COLORS['accent_cyan']

        # Antena
        pygame.draw.line(self.screen, head_color, (x, y - 20), (x, y - 10), 2)
        pygame.draw.circle(self.screen, eye_color, (x, y - 25), 5)
        
        # Cabeça
        if seed == 0: # Quadrada
            head_rect = pygame.Rect(x - 30, y, 60, 50)
            pygame.draw.rect(self.screen, head_color, head_rect, border_radius=10)
        else: # Redonda
            head_rect = pygame.Rect(x - 35, y, 70, 50)
            pygame.draw.ellipse(self.screen, head_color, head_rect)
            
        # Olhos
        if seed == 1: # Um visor
            pygame.draw.rect(self.screen, eye_color, (x - 20, y + 15, 40, 20), border_radius=5)
        else: # Dois olhos
            pygame.draw.circle(self.screen, eye_color, (x - 12, y + 20), 8)
            pygame.draw.circle(self.screen, eye_color, (x + 12, y + 20), 8)
        
        # Pescoço
        pygame.draw.rect(self.screen, COLORS['text_dark'], (x - 10, y + 50, 20, 10), border_radius=3)

    def draw_menu_screen(self):
        """Desenha a tela inicial com a história"""
        self.screen.fill(COLORS['background'])
        
        # Título
        self.draw_text("OFICINA DE REPARO DE ROBÔS", 
                       self.font_large, COLORS['accent_cyan'], 
                       self.width // 2, 80, center=True)
        
        self.draw_text("Neon Forge - Ano 2175", 
                      self.font_medium, COLORS['text_secondary'], 
                      self.width // 2, 140, center=True)
        
        # História (agora em um painel)
        story_panel = pygame.Rect(self.width // 2 - 400, 200, 800, 450)
        self.draw_panel(story_panel)
        
        story_text = [
            "No ano 2175, após uma falha massiva de energia na cidade",
            "futurista Neon Forge, centenas de robôs ficaram danificados.",
            "",
            "Você é Alex Nova, técnico-chefe da Oficina Central de",
            "Reparo de Robôs. Sua missão é consertar os robôs que chegam",
            "antes que o caos tecnológico se espalhe pela cidade.",
            "",
            "INSTRUÇÕES:",
            "• Selecione um robô da lista para ver seus componentes.",
            "• O componente no TOPO da pilha é o seu alvo.",
            "• O CÓDIGO do alvo aparecerá no painel da direita.",
            "• Digite o código e pressione 'Substituir' (ou Enter).",
            "• Conserte todos os componentes para finalizar o robô.",
            "• Cuidado! Se a oficina lotar, o jogo termina!",
        ]
        
        y_offset = story_panel.y + 30
        for line in story_text:
            if line.startswith("•"):
                color = COLORS['accent_cyan']
                font = self.font_small
                x_offset = story_panel.x + 50
            elif line.startswith("INSTRUÇÕES:"):
                color = COLORS['accent_yellow']
                font = self.font_small_bold
                x_offset = story_panel.x + 30
            elif line == "":
                y_offset += 10
                continue
            else:
                color = COLORS['text_primary']
                font = self.font_small
                x_offset = story_panel.x + 30
            
            self.draw_text(line, font, color, x_offset, y_offset)
            y_offset += 30
        
        # Botão Iniciar Jogo
        mouse_pos = pygame.mouse.get_pos()
        button_rect = self.ui_rects['menu_start']
        hover = button_rect.collidepoint(mouse_pos)
        self.draw_button("INICIAR JOGO", button_rect.x, button_rect.y, 
                        button_rect.width, button_rect.height, hover=hover)
    
    def draw_playing_screen(self):
        """Desenha a tela principal do jogo"""
        self.screen.fill(COLORS['background'])
        mouse_pos = pygame.mouse.get_pos()
        
        # === Painel Esquerdo - Lista de Robôs ===
        panel_left = self.ui_rects['play_panel_left']
        self.draw_panel(panel_left)
        
        self.draw_text("FILA DE REPARO", self.font_medium, COLORS['accent_cyan'],
                      panel_left.x + 10, panel_left.y + 15)
        
        robots = self.game.robots.get_all()
        y_offset = 60 # Espaço para o título
        
        for robot in robots:
            robot_rect = pygame.Rect(panel_left.x + 10, panel_left.y + y_offset, 
                                    panel_left.width - 20, 60) # Altura 60
            
            # VERIFICAÇÃO DE LIMITE
            if robot_rect.bottom > panel_left.bottom - 10:
                self.draw_text("...", self.font_medium, COLORS['text_dark'],
                             panel_left.centerx, panel_left.bottom - 25, center=True)
                break 
            
            # Destaque
            bg_color = None
            if robot.id == self.game.selected_robot_id:
                bg_color = COLORS['accent_cyan']
            elif robot_rect.collidepoint(mouse_pos):
                bg_color = COLORS['panel_border']
            
            if bg_color:
                pygame.draw.rect(self.screen, bg_color, robot_rect, border_radius=5)
            
            # Cor da prioridade
            priority_color = COLORS.get(f"priority_{robot.priority.replace(' ', '_')}", COLORS['text_secondary'])
            
            # Informações do robô
            text_color = COLORS['panel_bg'] if robot.id == self.game.selected_robot_id else COLORS['text_primary']
            self.draw_text(f"#{robot.id} - {robot.model_name}", 
                          self.font_small_bold, text_color,
                          robot_rect.x + 10, robot_rect.y + 10)
            self.draw_text(f"Prioridade: {robot.priority.upper()}", 
                          self.font_tiny, priority_color,
                          robot_rect.x + 10, robot_rect.y + 35)
            self.draw_text(f"{len(robot.components)} peças", 
                          self.font_tiny, text_color,
                          robot_rect.right - 80, robot_rect.y + 35)
            
            y_offset += 65 # Espaçamento 65

        # === Painel Central - Pilha de Componentes ===
        panel_center = self.ui_rects['play_panel_center']
        self.draw_panel(panel_center)
        
        self.draw_text("DIAGNÓSTICO", self.font_medium, COLORS['accent_cyan'],
                      panel_center.x + 10, panel_center.y + 15)
        
        selected_robot = self.game.get_selected_robot()
        
        # Desenha o ícone do robô
        self.draw_robot_icon(panel_center.centerx, panel_center.y + 80, selected_robot)
        
        if selected_robot:
            components = selected_robot.components.get_all()
            if components:
                y_offset = panel_center.y + 160 # Abaixo do ícone
                
                for i, component in enumerate(components):
                    comp_rect = pygame.Rect(panel_center.x + 10, y_offset,
                                          panel_center.width - 20, 50)
                    
                    if comp_rect.bottom > panel_center.bottom - 10:
                        self.draw_text("...", self.font_medium, COLORS['text_dark'],
                                     panel_center.centerx, panel_center.bottom - 25, center=True)
                        break
                    
                    # Destaca o componente no topo
                    if i == 0:
                        pygame.draw.rect(self.screen, COLORS['accent_cyan'], comp_rect, 2, border_radius=5)
                        self.draw_text("→ TOPO", self.font_tiny, COLORS['accent_cyan'],
                                     comp_rect.x + 5, comp_rect.y + 5)
                        text_color = COLORS['text_primary']
                        code_text = f"Código: {component.replacement_code}" # Mostra código no topo
                        code_color = COLORS['accent_yellow']
                    else:
                        pygame.draw.rect(self.screen, COLORS['panel_border'], comp_rect, 1, border_radius=5)
                        text_color = COLORS['text_dark']
                        code_text = "Código: ????" # Esconde os outros
                        code_color = COLORS['text_dark']
                    
                    self.draw_text(component.name, self.font_small, text_color,
                                 comp_rect.x + 10, comp_rect.y + 25, center_y=True)
                    self.draw_text(code_text, 
                                 self.font_tiny, code_color,
                                 comp_rect.right - 140, comp_rect.y + 25, center_y=True)
                    y_offset += 55
            else:
                self.draw_text("Robô Consertado!", self.font_medium_regular, COLORS['success'],
                             panel_center.centerx, panel_center.centery + 50, center=True)
        else:
            self.draw_text("Selecione um Robô na Fila", self.font_medium_regular, COLORS['text_secondary'],
                         panel_center.centerx, panel_center.centery + 50, center=True)
        
        # === Painel Direito - Estatísticas e Controle ===
        panel_right = self.ui_rects['play_panel_right']
        self.draw_panel(panel_right)
        
        # --- SEÇÃO: COMPONENTE ALVO ---
        target_y = panel_right.y + 20
        self.draw_text("COMPONENTE ALVO", self.font_medium, COLORS['accent_cyan'],
                      panel_right.x + 10, target_y)
        
        target_box = pygame.Rect(panel_right.x + 10, target_y + 40, panel_right.width - 20, 100)
        pygame.draw.rect(self.screen, COLORS['background'], target_box, border_radius=5)
        
        top_component = selected_robot.get_top_component() if selected_robot else None
        if top_component:
            self.draw_text(top_component.name, self.font_small, COLORS['text_primary'],
                         target_box.centerx, target_box.y + 25, center=True)
            # Destaque principal para o código
            self.draw_text(top_component.replacement_code, self.font_large, COLORS['accent_yellow'],
                         target_box.centerx, target_box.y + 65, center=True)
        else:
            self.draw_text("Nenhum Alvo", self.font_medium_regular, COLORS['text_dark'],
                         target_box.centerx, target_box.centery, center=True)

        # --- Estatísticas ---
        stats_y = target_y + 160 # Abaixo da caixa "Alvo"
        self.draw_text("ESTATÍSTICAS", self.font_small_bold, COLORS['text_secondary'],
                      panel_right.x + 10, stats_y)
        stats_y += 30
        
        elapsed_time = self.game.get_elapsed_time()
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        self.draw_text(f"Tempo: {minutes:02d}:{seconds:02d}", 
                      self.font_small, COLORS['text_primary'],
                      panel_right.x + 10, stats_y)
        stats_y += 25
        self.draw_text(f"Robôs Consertados: {self.game.robots_fixed}", 
                      self.font_small, COLORS['success'],
                      panel_right.x + 10, stats_y)
        stats_y += 25
        self.draw_text(f"Componentes: {self.game.components_replaced}", 
                      self.font_small, COLORS['accent_cyan'],
                      panel_right.x + 10, stats_y)
        stats_y += 25
        self.draw_text(f"Oficina: {len(self.game.robots)}/{self.game.max_robots}", 
                      self.font_small, COLORS['warning'],
                      panel_right.x + 10, stats_y)
        
        # --- Input e Botão ---
        input_title_y = stats_y + 40
        self.draw_text("CÓDIGO DE SUBSTITUIÇÃO:", self.font_small_bold, COLORS['text_secondary'],
                      panel_right.x + 10, input_title_y)
        
        input_rect = self.ui_rects['play_input_code']
        self.draw_input_box(self.input_code, input_rect.x, input_rect.y, 
                            input_rect.width, input_rect.height, 
                            active=self.input_active)
        
        button_rect = self.ui_rects['play_submit_code']
        self.draw_button("SUBSTITUIR", 
                        button_rect.x, button_rect.y,
                        button_rect.width, button_rect.height,
                        hover=button_rect.collidepoint(mouse_pos))
        
        # --- Mensagem do Jogo ---
        if self.game.message:
            message_y = 540
            message_rect = pygame.Rect(20, message_y, self.width - 40, 60)
            self.draw_panel(message_rect)
            
            msg_color = COLORS['accent_cyan']
            if "incorreto" in self.game.message.lower():
                msg_color = COLORS['error']
            elif "sucesso" in self.game.message.lower():
                msg_color = COLORS['success']
                
            self.draw_text(self.game.message, self.font_medium_regular, msg_color,
                         message_rect.centerx, message_rect.centery, center=True)
    
    def draw_game_over_screen(self):
        """Desenha a tela final com estatísticas"""
        self.screen.fill(COLORS['background'])
        
        # Título
        if self.game.game_over:
            title = "OFICINA LOTADA - GAME OVER"
            title_color = COLORS['error']
        else:
            title = "PARABÉNS! MISSÃO CUMPRIDA!"
            title_color = COLORS['success']
        
        self.draw_text(title, self.font_large, title_color,
                      self.width // 2, 100, center=True)
        
        # Estatísticas
        total_time = self.game.get_total_time()
        minutes = int(total_time // 60)
        seconds = int(total_time % 60)
        
        stats_panel = pygame.Rect(self.width // 2 - 300, 200, 600, 300)
        self.draw_panel(stats_panel)
        
        score = self.game.robots_fixed * 100 + self.game.components_replaced * 10 - int(total_time)
        stats_text = [
            (f"Robôs Consertados:", f"{self.game.robots_fixed}", COLORS['success']),
            (f"Componentes:", f"{self.game.components_replaced}", COLORS['accent_cyan']),
            (f"Tempo Total:", f"{minutes:02d}:{seconds:02d}", COLORS['text_primary']),
            (f"Score Final:", f"{score}", COLORS['accent_yellow'])
        ]
        
        y_offset = stats_panel.y + 50
        for label, value, color in stats_text:
            self.draw_text(label, self.font_medium_regular, COLORS['text_secondary'],
                         stats_panel.x + 50, y_offset)
            self.draw_text(value, self.font_medium_regular, color,
                         stats_panel.right - 50 - self.font_medium_regular.size(value)[0], y_offset)
            y_offset += 50
        
        # --- REMOVIDO --- Input de nome e Botão Salvar
        
        # Botões
        mouse_pos = pygame.mouse.get_pos()
        menu_button_rect = self.ui_rects['over_back_menu']
        
        self.draw_button("VOLTAR AO MENU", menu_button_rect.x, menu_button_rect.y,
                        menu_button_rect.width, menu_button_rect.height, 
                        hover=menu_button_rect.collidepoint(mouse_pos))
    
    def handle_events(self):
        """Processa eventos do pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.state == "menu":
                    if self.ui_rects['menu_start'].collidepoint(mouse_pos):
                        self.game.start_game()
                        self.state = "playing"
                        self.input_code = ""
                        self.input_active = False
                
                elif self.state == "playing":
                    # Clique na lista de robôs
                    panel_left = self.ui_rects['play_panel_left']
                    if panel_left.collidepoint(mouse_pos):
                        robots = self.game.robots.get_all()
                        y_offset = 60
                        for robot in robots:
                            robot_rect = pygame.Rect(panel_left.x + 10, panel_left.y + y_offset,
                                                    panel_left.width - 20, 60)
                            if robot_rect.bottom > panel_left.bottom - 10:
                                break
                            if robot_rect.collidepoint(mouse_pos):
                                self.game.select_robot(robot.id)
                                break
                            y_offset += 65
                    
                    # Campo de input e botão
                    input_rect = self.ui_rects['play_input_code']
                    button_rect = self.ui_rects['play_submit_code']
                    
                    if input_rect.collidepoint(mouse_pos):
                        self.input_active = True
                    elif not button_rect.collidepoint(mouse_pos):
                        self.input_active = False
                    
                    if button_rect.collidepoint(mouse_pos) and self.input_code:
                        self.game.validate_code(self.input_code)
                        self.input_code = ""
                        self.input_active = False # Desativa após enviar
                
                elif self.state == "game_over":
                    # --- ATUALIZADO ---
                    # Apenas o botão de menu é verificado
                    menu_button_rect = self.ui_rects['over_back_menu']

                    if menu_button_rect.collidepoint(mouse_pos):
                        self.state = "menu"
                        self.game = Game() # Reseta o jogo
                        # --- REMOVIDO --- Limpeza de variáveis de ranking
                        self.input_code = ""
                        self.input_active = False
                        self.game.selected_robot_id = None
            
            if event.type == pygame.KEYDOWN:
                if self.state == "playing" and self.input_active:
                    if event.key == pygame.K_RETURN: # Enter também envia
                        if self.input_code:
                            self.game.validate_code(self.input_code)
                            self.input_code = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_code = self.input_code[:-1]
                    else:
                        if event.unicode.isdigit() and len(self.input_code) < 4:
                            self.input_code += event.unicode
                
                # --- REMOVIDO --- Bloco de input de nome (game_over)
        
        return True
    
    def update(self):
        """Atualiza o estado do jogo"""
        if self.state == "playing":
            current_time = pygame.time.get_ticks() / 1000.0
            self.game.update(current_time)
            
            if self.game.game_over or self.game.game_won:
                self.state = "game_over"
    
    def draw(self):
        """Desenha a tela atual"""
        if self.state == "menu":
            self.draw_menu_screen()
        elif self.state == "playing":
            self.draw_playing_screen()
        elif self.state == "game_over":
            self.draw_game_over_screen()
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

# """
# Módulo de interface gráfica
# Implementa todas as telas do jogo usando pygame
# """

# import pygame
# import json
# import os
# from game import Game


# # Cores da paleta futurista
# COLORS = {
#     'background': (15, 15, 25),
#     'dark': (25, 25, 35),
#     'medium': (40, 40, 55),
#     'light': (60, 60, 80),
#     'accent_blue': (0, 150, 255),
#     'accent_cyan': (0, 255, 255),
#     'accent_purple': (150, 100, 255),
#     'metal': (180, 180, 200),
#     'text': (220, 220, 240),
#     'text_dark': (150, 150, 170),
#     'success': (0, 255, 150),
#     'warning': (255, 200, 0),
#     'error': (255, 100, 100),
#     'priority_emergency': (255, 50, 50),
#     'priority_standard': (255, 200, 0),
#     'priority_low': (100, 255, 100),
#     'button': (50, 100, 200),
#     'button_hover': (70, 120, 230),
#     'button_active': (30, 80, 180),
#     'input_bg': (30, 30, 45),
#     'input_border': (80, 80, 120),
#     'input_focus': (0, 150, 255)
# }


# class GUI:
#     """Gerencia a interface gráfica do jogo"""
#     def __init__(self):
#         pygame.init()
#         self.width = 1200
#         self.height = 800
#         self.screen = pygame.display.set_mode((self.width, self.height))
#         pygame.display.set_caption("Oficina de Reparo de Robôs")
#         self.clock = pygame.time.Clock()
#         self.font_large = pygame.font.Font(None, 48)
#         self.font_medium = pygame.font.Font(None, 32)
#         self.font_small = pygame.font.Font(None, 24)
#         self.font_tiny = pygame.font.Font(None, 20)
        
#         self.game = Game()
#         self.state = "menu"  # "menu", "playing", "game_over"
#         self.input_code = ""
#         self.input_active = False
#         self.input_name = ""
#         self.name_input_active = False
#         self.ranking_saved = False
#         self.ranking_save_time = 0
        
#         # Carrega ou cria o arquivo de ranking
#         self.ranking_file = "ranking.json"
#         self.load_ranking()
    
#     def load_ranking(self):
#         """Carrega o ranking do arquivo JSON"""
#         if os.path.exists(self.ranking_file):
#             try:
#                 with open(self.ranking_file, 'r', encoding='utf-8') as f:
#                     self.ranking = json.load(f)
#             except:
#                 self.ranking = []
#         else:
#             self.ranking = []
    
#     def save_ranking(self):
#         """Salva o ranking no arquivo JSON"""
#         with open(self.ranking_file, 'w', encoding='utf-8') as f:
#             json.dump(self.ranking, f, indent=2, ensure_ascii=False)
    
#     def add_to_ranking(self, name, robots_fixed, components_replaced, time_total):
#         """Adiciona uma entrada ao ranking"""
#         entry = {
#             'name': name if name else "Anônimo",
#             'robots_fixed': robots_fixed,
#             'components_replaced': components_replaced,
#             'time_total': time_total,
#             'score': robots_fixed * 100 + components_replaced * 10 - int(time_total)
#         }
#         self.ranking.append(entry)
#         # Ordena por score (maior primeiro)
#         self.ranking.sort(key=lambda x: x['score'], reverse=True)
#         # Mantém apenas os 10 melhores
#         self.ranking = self.ranking[:10]
#         self.save_ranking()
#         self.ranking_saved = True
#         self.ranking_save_time = pygame.time.get_ticks()
    
#     def draw_text(self, text, font, color, x, y, center=False):
#         """Desenha texto na tela"""
#         surface = font.render(text, True, color)
#         if center:
#             rect = surface.get_rect(center=(x, y))
#             self.screen.blit(surface, rect)
#         else:
#             self.screen.blit(surface, (x, y))
#         return surface.get_rect()
    
#     def draw_button(self, text, x, y, width, height, hover=False, active=False):
#         """Desenha um botão na tela"""
#         if active:
#             color = COLORS['button_active']
#         elif hover:
#             color = COLORS['button_hover']
#         else:
#             color = COLORS['button']
        
#         pygame.draw.rect(self.screen, color, (x, y, width, height))
#         pygame.draw.rect(self.screen, COLORS['accent_blue'], (x, y, width, height), 2)
        
#         text_surf = self.font_medium.render(text, True, COLORS['text'])
#         text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
#         self.screen.blit(text_surf, text_rect)
        
#         return pygame.Rect(x, y, width, height)
    
#     def draw_input_box(self, text, x, y, width, height, active=False):
#         """Desenha uma caixa de input"""
#         bg_color = COLORS['input_focus'] if active else COLORS['input_bg']
#         border_color = COLORS['input_focus'] if active else COLORS['input_border']
        
#         pygame.draw.rect(self.screen, bg_color, (x, y, width, height))
#         pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2)
        
#         # Desenha o texto
#         if text:
#             text_surf = self.font_medium.render(text, True, COLORS['text'])
#             # Trunca o texto se for muito longo
#             if text_surf.get_width() > width - 20:
#                 text_surf = self.font_small.render(text, True, COLORS['text'])
#             self.screen.blit(text_surf, (x + 10, y + height // 2 - text_surf.get_height() // 2))
        
#         # Cursor piscante quando ativo
#         if active:
#             current_time = pygame.time.get_ticks()
#             if (current_time // 500) % 2:
#                 cursor_x = x + 10 + (self.font_medium.size(text)[0] if text else 0)
#                 pygame.draw.line(self.screen, COLORS['text'], 
#                                (cursor_x, y + 10), 
#                                (cursor_x, y + height - 10), 2)
        
#         return pygame.Rect(x, y, width, height)
    
#     def draw_menu_screen(self):
#         """Desenha a tela inicial com a história"""
#         # Fundo com gradiente
#         self.screen.fill(COLORS['background'])
        
#         # Linhas decorativas
#         for i in range(0, self.height, 40):
#             pygame.draw.line(self.screen, COLORS['medium'], (0, i), (self.width, i), 1)
        
#         # Título
#         title_rect = self.draw_text("OFICINA DE REPARO DE ROBÔS", 
#                                    self.font_large, COLORS['accent_cyan'], 
#                                    self.width // 2, 80, center=True)
        
#         # Subtítulo
#         self.draw_text("Neon Forge - Ano 2175", 
#                       self.font_medium, COLORS['metal'], 
#                       self.width // 2, 140, center=True)
        
#         # História
#         story_text = [
#             "No ano 2175, após uma falha massiva de energia na cidade",
#             "futurista Neon Forge, centenas de robôs ficaram danificados.",
#             "",
#             "Você é Alex Nova, técnico-chefe da Oficina Central de",
#             "Reparo de Robôs. Sua missão é consertar os robôs que chegam",
#             "antes que o caos tecnológico se espalhe pela cidade.",
#             "",
#             "Cada robô possui componentes defeituosos que precisam ser",
#             "substituídos. Digite o código correto de substituição para",
#             "cada componente e mantenha a oficina funcionando!",
#             "",
#             "INSTRUÇÕES:",
#             "• Selecione um robô da lista",
#             "• Veja o componente no topo da pilha",
#             "• Digite o código de substituição correto",
#             "• Conserte todos os componentes para finalizar o robô",
#             "• Cuidado! Se a oficina lotar, o jogo termina!"
#         ]
        
#         y_offset = 200
#         for line in story_text:
#             if line.startswith("•"):
#                 color = COLORS['accent_blue']
#                 font = self.font_small
#             elif line.startswith("INSTRUÇÕES:"):
#                 color = COLORS['accent_cyan']
#                 font = self.font_medium
#             elif line == "":
#                 y_offset += 10
#                 continue
#             else:
#                 color = COLORS['text']
#                 font = self.font_small
            
#             self.draw_text(line, font, color, self.width // 2, y_offset, center=True)
#             y_offset += 35
        
#         # Botão Iniciar Jogo
#         mouse_pos = pygame.mouse.get_pos()
#         button_rect = pygame.Rect(self.width // 2 - 150, self.height - 120, 300, 60)
#         hover = button_rect.collidepoint(mouse_pos)
#         self.draw_button("INICIAR JOGO", button_rect.x, button_rect.y, 
#                         button_rect.width, button_rect.height, hover=hover)
    
#     def draw_playing_screen(self):
#         """Desenha a tela principal do jogo"""
#         # Fundo
#         self.screen.fill(COLORS['background'])
        
#         # Linhas decorativas
#         for i in range(0, self.width, 50):
#             pygame.draw.line(self.screen, COLORS['medium'], (i, 0), (i, self.height), 1)
        
#         # Obtém posição do mouse uma vez
#         mouse_pos = pygame.mouse.get_pos()
        
#         # Painel esquerdo - Lista de robôs
#         panel_left = pygame.Rect(20, 20, 350, 500)
#         pygame.draw.rect(self.screen, COLORS['dark'], panel_left)
#         pygame.draw.rect(self.screen, COLORS['accent_blue'], panel_left, 2)
        
#         self.draw_text("ROBÔS EM ATENDIMENTO", self.font_medium, COLORS['accent_cyan'],
#                       panel_left.x + 10, panel_left.y + 10)
        
#         # Lista de robôs
#         robots = self.game.robots.get_all()
#         y_offset = 50
        
#         for robot in robots:
#             robot_rect = pygame.Rect(panel_left.x + 10, panel_left.y + y_offset, 
#                                     panel_left.width - 20, 60)
            
#             # Destaque se selecionado
#             if robot.id == self.game.selected_robot_id:
#                 pygame.draw.rect(self.screen, COLORS['accent_blue'], robot_rect)
#             elif robot_rect.collidepoint(mouse_pos):
#                 pygame.draw.rect(self.screen, COLORS['medium'], robot_rect)
#             else:
#                 pygame.draw.rect(self.screen, COLORS['light'], robot_rect)
            
#             # Cor da prioridade
#             priority_colors = {
#                 'emergência': COLORS['priority_emergency'],
#                 'padrão': COLORS['priority_standard'],
#                 'baixo risco': COLORS['priority_low']
#             }
#             priority_color = priority_colors.get(robot.priority, COLORS['text'])
            
#             # Informações do robô
#             self.draw_text(f"#{robot.id} - {robot.model_name}", 
#                           self.font_small, COLORS['text'],
#                           robot_rect.x + 10, robot_rect.y + 10)
#             self.draw_text(f"Prioridade: {robot.priority.upper()}", 
#                           self.font_tiny, priority_color,
#                           robot_rect.x + 10, robot_rect.y + 35)
#             self.draw_text(f"Componentes: {len(robot.components)}", 
#                           self.font_tiny, COLORS['text_dark'],
#                           robot_rect.x + 10, robot_rect.y + 50)
            
#             y_offset += 70
        
#         # Painel central - Pilha de componentes
#         panel_center = pygame.Rect(390, 20, 400, 500)
#         pygame.draw.rect(self.screen, COLORS['dark'], panel_center)
#         pygame.draw.rect(self.screen, COLORS['accent_blue'], panel_center, 2)
        
#         self.draw_text("PILHA DE COMPONENTES", self.font_medium, COLORS['accent_cyan'],
#                       panel_center.x + 10, panel_center.y + 10)
        
#         selected_robot = self.game.get_selected_robot()
#         if selected_robot:
#             components = selected_robot.components.get_all()
#             if components:
#                 y_offset = 50
#                 for i, component in enumerate(components):
#                     comp_rect = pygame.Rect(panel_center.x + 10, panel_center.y + y_offset,
#                                           panel_center.width - 20, 50)
                    
#                     # Destaca o componente no topo
#                     if i == 0:
#                         pygame.draw.rect(self.screen, COLORS['accent_blue'], comp_rect)
#                         self.draw_text("→ TOPO", self.font_tiny, COLORS['accent_cyan'],
#                                      comp_rect.x + 5, comp_rect.y + 5)
#                     else:
#                         pygame.draw.rect(self.screen, COLORS['medium'], comp_rect)
                    
#                     self.draw_text(component.name, self.font_small, COLORS['text'],
#                                  comp_rect.x + 10, comp_rect.y + 20)
#                     self.draw_text(f"Código: {component.replacement_code}", 
#                                  self.font_tiny, COLORS['text_dark'],
#                                  comp_rect.x + 10, comp_rect.y + 35)
#                     y_offset += 60
#             else:
#                 self.draw_text("Robô consertado!", self.font_medium, COLORS['success'],
#                              panel_center.centerx, panel_center.centery, center=True)
#         else:
#             self.draw_text("Selecione um robô", self.font_medium, COLORS['text_dark'],
#                          panel_center.centerx, panel_center.centery, center=True)
        
#         # Painel direito - Estatísticas e controle
#         panel_right = pygame.Rect(810, 20, 370, 500)
#         pygame.draw.rect(self.screen, COLORS['dark'], panel_right)
#         pygame.draw.rect(self.screen, COLORS['accent_blue'], panel_right, 2)
        
#         self.draw_text("ESTATÍSTICAS", self.font_medium, COLORS['accent_cyan'],
#                       panel_right.x + 10, panel_right.y + 10)
        
#         # Estatísticas
#         elapsed_time = self.game.get_elapsed_time()
#         minutes = int(elapsed_time // 60)
#         seconds = int(elapsed_time % 60)
        
#         stats_y = 50
#         self.draw_text(f"Tempo: {minutes:02d}:{seconds:02d}", 
#                       self.font_small, COLORS['text'],
#                       panel_right.x + 10, panel_right.y + stats_y)
#         stats_y += 40
#         self.draw_text(f"Robôs Consertados: {self.game.robots_fixed}", 
#                       self.font_small, COLORS['success'],
#                       panel_right.x + 10, panel_right.y + stats_y)
#         stats_y += 40
#         self.draw_text(f"Componentes: {self.game.components_replaced}", 
#                       self.font_small, COLORS['accent_blue'],
#                       panel_right.x + 10, panel_right.y + stats_y)
#         stats_y += 40
#         self.draw_text(f"Robôs na Oficina: {len(self.game.robots)}/{self.game.max_robots}", 
#                       self.font_small, COLORS['text'],
#                       panel_right.x + 10, panel_right.y + stats_y)
        
#         # Campo de input para código
#         stats_y += 60
#         self.draw_text("CÓDIGO DE SUBSTITUIÇÃO", self.font_small, COLORS['accent_cyan'],
#                       panel_right.x + 10, panel_right.y + stats_y)
#         stats_y += 30
        
#         input_rect = self.draw_input_box(self.input_code, panel_right.x + 10, 
#                                         panel_right.y + stats_y, 
#                                         panel_right.width - 20, 40, 
#                                         active=self.input_active)
#         stats_y += 60
        
#         # Botão de enviar
#         button_rect = pygame.Rect(panel_right.x + 10, panel_right.y + stats_y,
#                                  panel_right.width - 20, 50)
#         self.draw_button("SUBSTITUIR COMPONENTE", 
#                         button_rect.x, button_rect.y,
#                         button_rect.width, button_rect.height,
#                         hover=button_rect.collidepoint(mouse_pos))
        
#         # Mensagem do jogo
#         if self.game.message:
#             message_y = 540
#             message_rect = pygame.Rect(20, message_y, self.width - 40, 60)
#             pygame.draw.rect(self.screen, COLORS['dark'], message_rect)
#             pygame.draw.rect(self.screen, COLORS['accent_blue'], message_rect, 2)
#             self.draw_text(self.game.message, self.font_medium, COLORS['accent_cyan'],
#                          message_rect.centerx, message_rect.centery, center=True)
    
#     def draw_game_over_screen(self):
#         """Desenha a tela final com estatísticas"""
#         # Fundo
#         self.screen.fill(COLORS['background'])
        
#         # Título
#         if self.game.game_over:
#             title = "OFICINA LOTADA - GAME OVER"
#             title_color = COLORS['error']
#         else:
#             title = "PARABÉNS! MISSÃO CUMPRIDA!"
#             title_color = COLORS['success']
        
#         self.draw_text(title, self.font_large, title_color,
#                       self.width // 2, 100, center=True)
        
#         # Estatísticas
#         total_time = self.game.get_total_time()
#         minutes = int(total_time // 60)
#         seconds = int(total_time % 60)
        
#         stats_panel = pygame.Rect(self.width // 2 - 300, 200, 600, 300)
#         pygame.draw.rect(self.screen, COLORS['dark'], stats_panel)
#         pygame.draw.rect(self.screen, COLORS['accent_blue'], stats_panel, 2)
        
#         stats_text = [
#             f"Robôs Consertados: {self.game.robots_fixed}",
#             f"Componentes Substituídos: {self.game.components_replaced}",
#             f"Tempo Total: {minutes:02d}:{seconds:02d}",
#             f"Score: {self.game.robots_fixed * 100 + self.game.components_replaced * 10 - int(total_time)}"
#         ]
        
#         y_offset = 50
#         for text in stats_text:
#             self.draw_text(text, self.font_medium, COLORS['text'],
#                          stats_panel.centerx, stats_panel.y + y_offset, center=True)
#             y_offset += 50
        
#         # Input para nome
#         name_y = 550
#         self.draw_text("Digite seu nome para o ranking:", 
#                       self.font_medium, COLORS['accent_cyan'],
#                       self.width // 2, name_y, center=True)
#         name_y += 40
        
#         name_input_rect = self.draw_input_box(self.input_name, 
#                                              self.width // 2 - 200, name_y,
#                                              400, 50, 
#                                              active=self.name_input_active)
#         name_y += 70
        
#         # Botão salvar
#         mouse_pos = pygame.mouse.get_pos()
#         save_button_rect = pygame.Rect(self.width // 2 - 150, name_y, 300, 60)
        
#         # Mensagem de confirmação se ranking foi salvo
#         if self.ranking_saved:
#             current_time = pygame.time.get_ticks()
#             if current_time - self.ranking_save_time < 3000:  # 3 segundos
#                 confirm_y = name_y + 75
#                 self.draw_text("✓ Ranking salvo com sucesso!", 
#                               self.font_small, COLORS['success'],
#                               self.width // 2, confirm_y, center=True)
#             else:
#                 self.ranking_saved = False
#         hover = save_button_rect.collidepoint(mouse_pos)
#         self.draw_button("SALVAR NO RANKING", save_button_rect.x, save_button_rect.y,
#                         save_button_rect.width, save_button_rect.height, hover=hover)
        
#         # Botão voltar ao menu
#         menu_button_y = name_y + 80
#         menu_button_rect = pygame.Rect(self.width // 2 - 150, menu_button_y, 300, 60)
#         hover_menu = menu_button_rect.collidepoint(mouse_pos)
#         self.draw_button("VOLTAR AO MENU", menu_button_rect.x, menu_button_rect.y,
#                         menu_button_rect.width, menu_button_rect.height, hover=hover_menu)
        
#         # Ranking (top 5)
#         ranking_y = menu_button_y + 100
#         if len(self.ranking) > 0:
#             self.draw_text("TOP 5 RANKING", self.font_medium, COLORS['accent_cyan'],
#                           self.width // 2, ranking_y, center=True)
#             ranking_y += 40
            
#             for i, entry in enumerate(self.ranking[:5]):
#                 rank_text = f"{i+1}. {entry['name']} - Score: {entry['score']} " \
#                           f"({entry['robots_fixed']} robôs, {entry['components_replaced']} componentes)"
#                 self.draw_text(rank_text, self.font_small, COLORS['text'],
#                              self.width // 2, ranking_y, center=True)
#                 ranking_y += 30
    
#     def handle_events(self):
#         """Processa eventos do pygame"""
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return False
            
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 mouse_pos = pygame.mouse.get_pos()
                
#                 if self.state == "menu":
#                     # Botão Iniciar Jogo
#                     button_rect = pygame.Rect(self.width // 2 - 150, self.height - 120, 300, 60)
#                     if button_rect.collidepoint(mouse_pos):
#                         self.game.start_game()
#                         self.state = "playing"
#                         self.input_code = ""
#                         self.input_active = False
                
#                 elif self.state == "playing":
#                     # Clique na lista de robôs
#                     panel_left = pygame.Rect(20, 20, 350, 500)
#                     if panel_left.collidepoint(mouse_pos):
#                         robots = self.game.robots.get_all()
#                         y_offset = 50
#                         for robot in robots:
#                             robot_rect = pygame.Rect(panel_left.x + 10, panel_left.y + y_offset,
#                                                     panel_left.width - 20, 60)
#                             if robot_rect.collidepoint(mouse_pos):
#                                 self.game.select_robot(robot.id)
#                                 break
#                             y_offset += 70
                    
#                     # Campo de input e botão (mesmas coordenadas do draw)
#                     panel_right = pygame.Rect(810, 20, 370, 500)
#                     # stats_y começa em 50, depois: +40*4 (estatísticas) = 210, +60 = 270, +30 = 300
#                     input_y = panel_right.y + 50 + 40*4 + 60 + 30
#                     input_rect = pygame.Rect(panel_right.x + 10, input_y,
#                                            panel_right.width - 20, 40)
#                     if input_rect.collidepoint(mouse_pos):
#                         self.input_active = True
#                     else:
#                         # Só desativa se não clicou no botão
#                         button_y = input_y + 60
#                         button_rect = pygame.Rect(panel_right.x + 10, button_y,
#                                                 panel_right.width - 20, 50)
#                         if not button_rect.collidepoint(mouse_pos):
#                             self.input_active = False
                    
#                     # Botão substituir
#                     button_y = input_y + 60
#                     button_rect = pygame.Rect(panel_right.x + 10, button_y,
#                                             panel_right.width - 20, 50)
#                     if button_rect.collidepoint(mouse_pos) and self.input_code:
#                         self.game.validate_code(self.input_code)
#                         self.input_code = ""
#                         self.input_active = False
                
#                 elif self.state == "game_over":
#                     # Campo de nome
#                     name_input_rect = pygame.Rect(self.width // 2 - 200, 590, 400, 50)
#                     if name_input_rect.collidepoint(mouse_pos):
#                         self.name_input_active = True
#                     else:
#                         self.name_input_active = False
                    
#                     # Botão salvar
#                     save_button_rect = pygame.Rect(self.width // 2 - 150, 660, 300, 60)
#                     if save_button_rect.collidepoint(mouse_pos):
#                         total_time = self.game.get_total_time()
#                         self.add_to_ranking(self.input_name, 
#                                           self.game.robots_fixed,
#                                           self.game.components_replaced,
#                                           total_time)
#                         self.input_name = ""
                    
#                     # Botão voltar ao menu
#                     menu_button_rect = pygame.Rect(self.width // 2 - 150, 740, 300, 60)
#                     if menu_button_rect.collidepoint(mouse_pos):
#                         self.state = "menu"
#                         self.game = Game()
#                         self.input_name = ""
#                         self.name_input_active = False
#                         self.ranking_saved = False
#                         self.input_code = ""
#                         self.input_active = False
#                         self.game.selected_robot_id = None
            
#             if event.type == pygame.KEYDOWN:
#                 if self.state == "playing" and self.input_active:
#                     if event.key == pygame.K_RETURN:
#                         if self.input_code:
#                             self.game.validate_code(self.input_code)
#                             self.input_code = ""
#                     elif event.key == pygame.K_BACKSPACE:
#                         self.input_code = self.input_code[:-1]
#                     else:
#                         # Apenas números
#                         if event.unicode.isdigit() and len(self.input_code) < 4:
#                             self.input_code += event.unicode
                
#                 elif self.state == "game_over" and self.name_input_active:
#                     if event.key == pygame.K_RETURN:
#                         total_time = self.game.get_total_time()
#                         self.add_to_ranking(self.input_name,
#                                           self.game.robots_fixed,
#                                           self.game.components_replaced,
#                                           total_time)
#                         self.input_name = ""
#                         self.name_input_active = False
#                     elif event.key == pygame.K_BACKSPACE:
#                         self.input_name = self.input_name[:-1]
#                     else:
#                         if len(self.input_name) < 20:
#                             self.input_name += event.unicode
        
#         return True
    
#     def update(self):
#         """Atualiza o estado do jogo"""
#         if self.state == "playing":
#             current_time = pygame.time.get_ticks() / 1000.0
#             self.game.update(current_time)
            
#             if self.game.game_over or self.game.game_won:
#                 self.state = "game_over"
    
#     def draw(self):
#         """Desenha a tela atual"""
#         if self.state == "menu":
#             self.draw_menu_screen()
#         elif self.state == "playing":
#             self.draw_playing_screen()
#         elif self.state == "game_over":
#             self.draw_game_over_screen()
        
#         pygame.display.flip()
    
#     def run(self):
#         """Loop principal do jogo"""
#         running = True
#         while running:
#             running = self.handle_events()
#             self.update()
#             self.draw()
#             self.clock.tick(60)
        
#         pygame.quit()

