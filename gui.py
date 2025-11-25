"""
Módulo de interface gráfica
Implementa todas as telas do jogo usando pygame, com responsividade total
"""

import pygame
import json
import os
import time 
# Importe a classe Game (assumindo que ela está em 'game.py')
from game import Game, GAME_TIME_LIMIT


# --- PALETA DE CORES ---
COLORS = {
    'background': (10, 15, 30),
    'panel_bg': (20, 30, 50),
    'panel_border': (40, 60, 90),
    
    'text_primary': (230, 240, 255),
    'text_secondary': (140, 160, 190),
    'text_dark': (80, 100, 130),

    'accent_cyan': (0, 220, 255),
    'accent_purple': (180, 100, 255),
    'accent_yellow': (255, 220, 0),
    
    'success': (0, 255, 150),
    'error': (255, 60, 60),
    'warning': (255, 200, 0),

    'priority_emergency': (255, 60, 60),
    'priority_standard': (255, 200, 0),
    'priority_low': (0, 255, 150),

    'button': (180, 100, 255),
    'button_hover': (210, 130, 255),
    'button_active': (150, 80, 230),
    
    'input_bg': (30, 45, 70),
    'input_border': (80, 100, 130),
    'input_focus': (0, 220, 255),
}

RANKING_FILE = "ranking.json"
MAX_RANKING_ENTRIES = 10


class GUI:
    def __init__(self):
        pygame.init()
        # --- DEFINIÇÃO INICIAL DA JANELA (Configurada para ser RESIZABLE) ---
        self.width = 1200
        self.height = 800
        # Adiciona a flag pygame.RESIZABLE
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Oficina de Reparo de Robôs - Neon Forge")
        self.clock = pygame.time.Clock()
        
        self.load_fonts()
        
        self.game = Game()
        self.state = "menu"
        
        self.input_code = ""
        self.input_active = False
        
        self.input_name = "Novo Técnico"
        self.input_name_active = False
        self.ranking_saved = False

        self.ranking = self.load_ranking()
        
        # O self.ui_rects será recalculado no _calculate_ui_rects
        self.ui_rects = {}
        self._calculate_ui_rects()
        
    def _calculate_ui_rects(self):
        """Recalcula todos os retângulos da UI com base nas dimensões atuais"""
        
        # Define as dimensões com base na tela atual
        self.width, self.height = self.screen.get_size()
        
        # --- Dimensões Padrão para os Painéis (para manter a proporção) ---
        panel_h_margin = self.width * 0.015 # 1.5% de margem horizontal
        panel_v_margin = self.height * 0.025 # 2.5% de margem vertical
        
        # Painéis do Jogo (Playing Screen)
        P_LEFT_WIDTH = int(self.width * 0.3)
        P_CENTER_WIDTH = int(self.width * 0.35)
        P_RIGHT_WIDTH = int(self.width * 0.3)
        P_HEIGHT = int(self.height * 0.65)
        
        # Coordenadas X
        P_LEFT_X = int(panel_h_margin)
        P_CENTER_X = int(P_LEFT_X + P_LEFT_WIDTH + panel_h_margin)
        P_RIGHT_X = int(P_CENTER_X + P_CENTER_WIDTH + panel_h_margin)

        # Coordenada Y (topo)
        P_Y = int(panel_v_margin)
        
        # --- POSICIONAMENTO RESPONSIVO DOS BOTÕES DO MENU ---
        MENU_BTN_HEIGHT = 60
        MENU_BTN_WIDTH = 300
        # O botão Ranking fica 100 pixels acima da borda inferior
        MENU_RANKING_Y = self.height - 100
        # O botão Iniciar fica 20 pixels acima do Ranking
        MENU_START_Y = MENU_RANKING_Y - MENU_BTN_HEIGHT - 20 

        # --- POSICIONAMENTO RESPONSIVO DO GAME OVER ---
        GO_INPUT_START_Y = self.height * 0.55
        GO_INPUT_Y = GO_INPUT_START_Y + 30
        GO_SAVE_Y = GO_INPUT_START_Y + 90
        
        self.ui_rects.update({
            # Menu Screen (Centralizado e Responsivo)
            'menu_start': pygame.Rect(self.width // 2 - MENU_BTN_WIDTH // 2, MENU_START_Y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT),
            'menu_ranking': pygame.Rect(self.width // 2 - MENU_BTN_WIDTH // 2, MENU_RANKING_Y, MENU_BTN_WIDTH, MENU_BTN_HEIGHT),

            # Playing Screen Panels (Distribuídos)
            'play_panel_left': pygame.Rect(P_LEFT_X, P_Y, P_LEFT_WIDTH, P_HEIGHT),
            'play_panel_center': pygame.Rect(P_CENTER_X, P_Y, P_CENTER_WIDTH, P_HEIGHT),
            'play_panel_right': pygame.Rect(P_RIGHT_X, P_Y, P_RIGHT_WIDTH, P_HEIGHT),
            
            # Playing Screen Controls (Dentro do Painel Direito)
            'play_input_code': pygame.Rect(P_RIGHT_X + 10, P_Y + P_HEIGHT - 120, P_RIGHT_WIDTH - 20, 40),
            'play_submit_code': pygame.Rect(P_RIGHT_X + 10, P_Y + P_HEIGHT - 70, P_RIGHT_WIDTH - 20, 50),
            
            # Game Over Screen
            'over_input_name': pygame.Rect(self.width // 2 - 150, GO_INPUT_Y, 300, 40),
            'over_save_rank': pygame.Rect(self.width // 2 - 150, GO_SAVE_Y, 300, 60),
        })


    def load_fonts(self):
        # AQUI VOCÊ DEVE TER SEUS ARQUIVOS DE FONTE EM UMA PASTA 'font'
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
            # Fallback para fontes padrão do Pygame
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 32)
            self.font_medium_regular = pygame.font.Font(None, 30)
            self.font_small = pygame.font.Font(None, 24)
            self.font_small_bold = pygame.font.Font(None, 24)
            self.font_tiny = pygame.font.Font(None, 20)

    def load_ranking(self):
        """Carrega o ranking do arquivo JSON"""
        if os.path.exists(RANKING_FILE):
            with open(RANKING_FILE, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_ranking(self):
        """Salva o ranking no arquivo JSON"""
        self.ranking.sort(key=lambda x: x['score'], reverse=True)
        self.ranking = self.ranking[:MAX_RANKING_ENTRIES]
        with open(RANKING_FILE, 'w') as f:
            json.dump(self.ranking, f, indent=4)

    def add_to_ranking(self, name, score, time_total, fixed_robots):
        """Adiciona um novo score ao ranking e salva"""
        entry = {
            'name': name,
            'score': score,
            'fixed_robots': fixed_robots,
            'time': round(time_total, 2)
        }
        self.ranking.append(entry)
        self.save_ranking()

    def draw_text(self, text, font, color, x, y, center=False, center_x=False, center_y=False):
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
        return rect 

    def draw_button(self, text, x, y, width, height, hover=False, active=False):
        if active:
            color = COLORS['button_active']
        elif hover:
            color = COLORS['button_hover']
        else:
            color = COLORS['button']
        
        pygame.draw.rect(self.screen, (0,0,0,50), (x+2, y+2, width, height), border_radius=8)
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=8)
        
        self.draw_text(text, self.font_medium, COLORS['text_primary'], 
                         x + width // 2, y + height // 2, center=True)
        
        return pygame.Rect(x, y, width, height)
    
    def draw_input_box(self, text, x, y, width, height, active=False, placeholder=""):
        bg_color = COLORS['input_bg']
        border_color = COLORS['input_focus'] if active else COLORS['input_border']
        text_color = COLORS['text_primary']
        
        pygame.draw.rect(self.screen, bg_color, (x, y, width, height), border_radius=5)
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2, border_radius=5)
        
        if text or active:
            display_text = text
        else:
            display_text = placeholder
            text_color = COLORS['text_dark']
            
        text_surf = self.font_medium_regular.render(display_text, True, text_color)
        self.screen.blit(text_surf, (x + 10, y + height // 2 - text_surf.get_height() // 2))
        
        if active:
            current_time = pygame.time.get_ticks()
            if (current_time // 500) % 2:
                if not text:
                    cursor_x = x + 10
                else:
                    cursor_x = x + 10 + text_surf.get_width()
                    
                pygame.draw.line(self.screen, COLORS['text_primary'], 
                                 (cursor_x, y + 10), 
                                 (cursor_x, y + height - 10), 2)
        
        return pygame.Rect(x, y, width, height)

    def draw_panel(self, rect):
        pygame.draw.rect(self.screen, COLORS['panel_bg'], rect, border_radius=8)
        pygame.draw.rect(self.screen, COLORS['panel_border'], rect, 2, border_radius=8)

    def draw_robot_icon(self, x, y, robot):
        if robot is None:
            head_color = COLORS['text_dark']
            eye_color = COLORS['panel_border']
            head_rect = pygame.Rect(x - 30, y, 60, 50)
            pygame.draw.rect(self.screen, head_color, head_rect, border_radius=10)
            pygame.draw.rect(self.screen, eye_color, (x - 15, y + 15, 30, 20), border_radius=5)
            self.draw_text("?", self.font_large, COLORS['panel_bg'], x, y + 25, center=True)
            return

        seed = hash(robot.model_name) % 3
        head_color = COLORS['text_secondary']
        eye_color = COLORS['accent_cyan']

        pygame.draw.line(self.screen, head_color, (x, y - 20), (x, y - 10), 2)
        pygame.draw.circle(self.screen, eye_color, (x, y - 25), 5)
        
        if seed == 0:
            head_rect = pygame.Rect(x - 30, y, 60, 50)
            pygame.draw.rect(self.screen, head_color, head_rect, border_radius=10)
        else:
            head_rect = pygame.Rect(x - 35, y, 70, 50)
            pygame.draw.ellipse(self.screen, head_color, head_rect)
            
        if seed == 1:
            pygame.draw.rect(self.screen, eye_color, (x - 20, y + 15, 40, 20), border_radius=5)
        else:
            pygame.draw.circle(self.screen, eye_color, (x - 12, y + 20), 8)
            pygame.draw.circle(self.screen, eye_color, (x + 12, y + 20), 8)
        
        pygame.draw.rect(self.screen, COLORS['text_dark'], (x - 10, y + 50, 20, 10), border_radius=3)
        

    def draw_menu_screen(self):
        """Desenha a tela inicial com a história e opções (Totalmente Responsivo)"""
        self._calculate_ui_rects()
        
        self.screen.fill(COLORS['background'])
        mouse_pos = pygame.mouse.get_pos()
        
        self.draw_text("OFICINA DE REPARO DE ROBÔS", 
                         self.font_large, COLORS['accent_cyan'], 
                         self.width // 2, self.height * 0.1, center=True)
        
        self.draw_text("Neon Forge - Ano 2175", 
                       self.font_medium, COLORS['text_secondary'], 
                       self.width // 2, self.height * 0.18, center=True)
        
        # --- DEFINIÇÃO DO TEXTO E CÁLCULO DA ALTURA NECESSÁRIA ---
        story_text = [
            "No ano 2175, após uma falha massiva de energia na cidade",
            "futurista Neon Forge, centenas de robôs ficaram danificados.",
            "",
            "MISSAO: Conserte o máximo de robôs possível em **1:30 minuto**.",
            "Priorize os casos de emergência para maximizar seu score.",
            "",
            "INSTRUÇÕES:",
            "• Selecione um robô para ver seus componentes.",
            # CORREÇÃO AQUI: Código de 4 dígitos -> Código de 4 caracteres alfanuméricos
            "• Digite o CÓDIGO de 4 caracteres alfanuméricos do componente no TOPO para repará-lo.",
        ]
        
        LINE_HEIGHT = 30
        PADDING_TOP_BOTTOM = 60 # 30px em cima e 30px embaixo
        
        # Calcula a altura exata necessária para todo o texto + padding
        required_height = len(story_text) * LINE_HEIGHT + PADDING_TOP_BOTTOM
        
        # Garante que o painel tenha pelo menos uma altura mínima ou 40% da tela
        story_panel_height = max(required_height, self.height * 0.4) 
        story_panel_width = self.width * 0.7
        
        # Calcula a posição Y para centralizar o painel entre o título e os botões
        story_panel_y = self.height * 0.25 
        
        story_panel = pygame.Rect(self.width // 2 - story_panel_width // 2, story_panel_y, 
                                  story_panel_width, story_panel_height)
                                  
        self.draw_panel(story_panel)
        
        # --- POSICIONAMENTO DO TEXTO ---
        MARGIN_LEFT = story_panel.x + 30 
        MARGIN_LEFT_BULLET = story_panel.x + 50 
        
        y_offset = story_panel.y + 30 # Começa com 30px de padding interno
        for line in story_text:
            color = COLORS['text_primary']
            font = self.font_small
            x_offset = MARGIN_LEFT
            
            if line.startswith("INSTRUÇÕES:"):
                color = COLORS['accent_yellow']
                font = self.font_small_bold
            elif line.startswith("•"):
                color = COLORS['accent_cyan']
                x_offset = MARGIN_LEFT_BULLET
            elif line.startswith("MISSAO:"):
                color = COLORS['error']
                font = self.font_small_bold


            self.draw_text(line, font, color, x_offset, y_offset)
            y_offset += LINE_HEIGHT
        
        # --- BOTÕES (Usando os retângulos responsivos calculados) ---
        start_rect = self.ui_rects['menu_start']
        hover_start = start_rect.collidepoint(mouse_pos)
        self.draw_button("INICIAR JOGO", start_rect.x, start_rect.y, 
                         start_rect.width, start_rect.height, hover=hover_start)

        ranking_rect = self.ui_rects['menu_ranking']
        hover_ranking = ranking_rect.collidepoint(mouse_pos)
        self.draw_button("RANKING", ranking_rect.x, ranking_rect.y, 
                         ranking_rect.width, ranking_rect.height, hover=hover_ranking)
    
    def draw_ranking_screen(self):
        """Desenha a tela de Ranking (Totalmente Responsivo)"""
        self._calculate_ui_rects()
        self.screen.fill(COLORS['background'])
        mouse_pos = pygame.mouse.get_pos()
        
        self.draw_text("MELHORES TÉCNICOS - RANKING", 
                         self.font_large, COLORS['accent_cyan'], 
                         self.width // 2, self.height * 0.1, center=True)
        
        ranking_panel_width = self.width * 0.75
        ranking_panel_height = self.height * 0.65
        ranking_panel = pygame.Rect(self.width // 2 - ranking_panel_width // 2, self.height * 0.18, 
                                    ranking_panel_width, ranking_panel_height)
        self.draw_panel(ranking_panel)
        
        # Cabeçalhos
        header_y = ranking_panel.y + 30
        x_name = ranking_panel.x + ranking_panel_width * 0.1
        x_robots = ranking_panel.x + ranking_panel_width * 0.5
        x_time = ranking_panel.x + ranking_panel_width * 0.65
        x_score = ranking_panel.x + ranking_panel_width * 0.8
        
        self.draw_text("#", self.font_small_bold, COLORS['accent_yellow'], ranking_panel.x + 30, header_y)
        self.draw_text("NOME", self.font_small_bold, COLORS['accent_yellow'], x_name, header_y)
        self.draw_text("ROBÔS", self.font_small_bold, COLORS['accent_yellow'], x_robots, header_y)
        self.draw_text("TEMPO", self.font_small_bold, COLORS['accent_yellow'], x_time, header_y)
        self.draw_text("SCORE", self.font_small_bold, COLORS['accent_yellow'], x_score, header_y)
        
        pygame.draw.line(self.screen, COLORS['panel_border'], (ranking_panel.x + 20, header_y + 30), 
                         (ranking_panel.right - 20, header_y + 30), 1)

        y_offset = header_y + 50
        
        if not self.ranking:
            self.draw_text("Ranking vazio. Seja o primeiro!", self.font_medium_regular, COLORS['text_dark'],
                             ranking_panel.centerx, ranking_panel.centery, center=True)
        
        for i, entry in enumerate(self.ranking):
            
            total_time = entry['time']
            minutes = int(total_time // 60)
            seconds = int(total_time % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"

            color = COLORS['text_primary']
            
            self.draw_text(str(i + 1), self.font_small, color, ranking_panel.x + 30, y_offset)
            self.draw_text(entry['name'], self.font_small, color, x_name, y_offset)
            self.draw_text(str(entry['fixed_robots']), self.font_small, COLORS['success'], x_robots, y_offset)
            self.draw_text(time_str, self.font_small, COLORS['accent_cyan'], x_time, y_offset)
            self.draw_text(str(entry['score']), self.font_small, COLORS['accent_yellow'], x_score, y_offset)
            
            y_offset += 40

        # Botão VOLTAR AO MENU (Responsivo: 100px da borda inferior)
        menu_button_rect = pygame.Rect(self.width // 2 - 150, self.height - 100, 300, 60)
        hover_menu = menu_button_rect.collidepoint(mouse_pos)
        self.draw_button("VOLTAR AO MENU", menu_button_rect.x, menu_button_rect.y,
                         menu_button_rect.width, menu_button_rect.height, hover=hover_menu)
        
    def draw_playing_screen(self):
        """Desenha a tela principal do jogo (Totalmente Responsivo)"""
        self._calculate_ui_rects()
        self.screen.fill(COLORS['background'])
        mouse_pos = pygame.mouse.get_pos()
        
        panel_left = self.ui_rects['play_panel_left']
        panel_center = self.ui_rects['play_panel_center']
        panel_right = self.ui_rects['play_panel_right']
        
        # === Painel Esquerdo - Fila de Reparo ===
        self.draw_panel(panel_left)
        
        self.draw_text("FILA DE REPARO", self.font_medium, COLORS['accent_cyan'],
                      panel_left.x + 10, panel_left.y + 15)
        
        robots = self.game.robots.get_all()
        y_offset = 60
        
        for robot in robots:
            robot_rect = pygame.Rect(panel_left.x + 10, panel_left.y + y_offset, 
                                     panel_left.width - 20, 60)
            
            if robot_rect.bottom > panel_left.bottom - 10:
                self.draw_text("...", self.font_medium, COLORS['text_dark'],
                              panel_left.centerx, panel_left.bottom - 25, center=True)
                break 
            
            # --- Lógica de Destaque ---
            bg_color = None
            if robot.id == self.game.selected_robot_id:
                bg_color = COLORS['accent_cyan']
            elif robot_rect.collidepoint(mouse_pos):
                bg_color = COLORS['panel_border']
            
            if bg_color:
                pygame.draw.rect(self.screen, bg_color, robot_rect, border_radius=5)
            
            priority_color = COLORS.get(f"priority_{robot.priority.replace(' ', '_')}", COLORS['text_secondary'])
            
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
            
            y_offset += 65

        # === Painel Central - Diagnóstico ===
        self.draw_panel(panel_center)
        
        self.draw_text("DIAGNÓSTICO", self.font_medium, COLORS['accent_cyan'],
                      panel_center.x + 10, panel_center.y + 15)
        
        selected_robot = self.game.get_selected_robot()
        
        # Ícone do Robô Centralizado
        self.draw_robot_icon(panel_center.centerx, panel_center.y + 80, selected_robot)
        
        if selected_robot:
            components = selected_robot.components.get_all()
            if components:
                y_offset = panel_center.y + 160
                
                for i, component in enumerate(components):
                    comp_rect = pygame.Rect(panel_center.x + 10, y_offset,
                                             panel_center.width - 20, 50)
                    
                    if comp_rect.bottom > panel_center.bottom - 10:
                        self.draw_text("...", self.font_medium, COLORS['text_dark'],
                                      panel_center.centerx, panel_center.bottom - 25, center=True)
                        break
                    
                    if i == 0:
                        pygame.draw.rect(self.screen, COLORS['accent_cyan'], comp_rect, 2, border_radius=5)
                        self.draw_text("→ TOPO", self.font_tiny, COLORS['accent_cyan'],
                                      comp_rect.x + 5, comp_rect.y + 5)
                        text_color = COLORS['text_primary']
                        # Código alfanumérico visível
                        code_text = f"Código: {component.replacement_code}"
                        code_color = COLORS['accent_yellow']
                    else:
                        pygame.draw.rect(self.screen, COLORS['panel_border'], comp_rect, 1, border_radius=5)
                        text_color = COLORS['text_dark']
                        code_text = "Código: XXXX"
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
        self.draw_panel(panel_right)
        
        # --- SEÇÃO: CRONÔMETRO ---
        time_left = self.game.get_time_left()
        
        # Lógica de formatação de tempo (assumimos que o cálculo em game.py está correto)
        if time_left >= 0:
            minutes = int(time_left // 60)
            seconds = int(time_left % 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
        else:
            time_str = "00:00"

        time_color = COLORS['error'] if time_left < 10 else COLORS['warning'] if time_left < 30 else COLORS['accent_cyan']

        self.draw_text("TEMPO RESTANTE", self.font_medium_regular, COLORS['text_secondary'],
                      panel_right.centerx, panel_right.y + 20, center_x=True)
        self.draw_text(time_str, self.font_large, time_color,
                      panel_right.centerx, panel_right.y + 60, center=True)

        # --- SEÇÃO: COMPONENTE ALVO ---
        target_y = panel_right.y + 100
        self.draw_text("COMPONENTE ALVO", self.font_medium_regular, COLORS['accent_cyan'],
                      panel_right.x + 10, target_y)
        
        target_box = pygame.Rect(panel_right.x + 10, target_y + 30, panel_right.width - 20, 70)
        pygame.draw.rect(self.screen, COLORS['background'], target_box, border_radius=5)
        
        top_component = selected_robot.get_top_component() if selected_robot else None
        if top_component:
            self.draw_text(top_component.replacement_code, self.font_large, COLORS['accent_yellow'],
                          target_box.centerx, target_box.centery, center=True)
        else:
            self.draw_text("Nenhum Alvo", self.font_medium_regular, COLORS['text_dark'],
                          target_box.centerx, target_box.centery, center=True)

        # --- Estatísticas ---
        stats_y = target_y + 110
        self.draw_text("ESTATÍSTICAS", self.font_small_bold, COLORS['text_secondary'],
                      panel_right.x + 10, stats_y)
        stats_y += 30
        
        self.draw_text(f"Robôs Consertados: {self.game.robots_fixed}", 
                      self.font_small, COLORS['success'],
                      panel_right.x + 10, stats_y)
        stats_y += 25
        self.draw_text(f"Componentes: {self.game.components_replaced}", 
                      self.font_small, COLORS['accent_cyan'],
                      panel_right.x + 10, stats_y)
        stats_y += 25
        capacity_color = COLORS['error'] if len(self.game.robots) >= self.game.max_robots - 1 else COLORS['warning']
        self.draw_text(f"Oficina: {len(self.game.robots)}/{self.game.max_robots}", 
                      self.font_small, capacity_color,
                      panel_right.x + 10, stats_y)
        
        # --- Input e Botão ---
        input_title_y = stats_y + 40
        self.draw_text("CÓDIGO DE SUBSTITUIÇÃO:", self.font_small_bold, COLORS['text_secondary'],
                      panel_right.x + 10, input_title_y)
        
        input_rect = self.ui_rects['play_input_code']
        # Placeholder atualizado para refletir o código alfanumérico
        self.draw_input_box(self.input_code, input_rect.x, input_rect.y, 
                            input_rect.width, input_rect.height, 
                            active=self.input_active, placeholder="Digite o código (4 alfanuméricos)")
        
        button_rect = self.ui_rects['play_submit_code']
        self.draw_button("SUBSTITUIR", 
                         button_rect.x, button_rect.y,
                         button_rect.width, button_rect.height,
                         hover=button_rect.collidepoint(mouse_pos))
        
        # --- Mensagem do Jogo (Abaixo dos painéis) ---
        message_y_center = panel_left.bottom + (self.height - panel_left.bottom) // 2
        
        # Define o retângulo da mensagem: altura fixa de 60px
        message_rect_height = 60
        message_rect = pygame.Rect(
            self.width * 0.015, # Margem esquerda de 1.5%
            message_y_center - message_rect_height // 2, # Centraliza Y
            self.width * 0.97, # Largura
            message_rect_height # Altura
        )
        
        # Desenha o Painel de fundo da mensagem
        self.draw_panel(message_rect)
        
        if self.game.message:
            msg_color = COLORS['accent_cyan']
            if "incorreto" in self.game.message.lower() or "erro" in self.game.message.lower() or "ESGOTADO" in self.game.message:
                msg_color = COLORS['error']
            elif "sucesso" in self.game.message.lower() or "finalizado" in self.game.message.lower():
                msg_color = COLORS['success']
                
            # Desenha o texto da mensagem no CENTRO do retângulo do painel
            self.draw_text(self.game.message, self.font_medium_regular, msg_color,
                          message_rect.centerx, message_rect.centery, center=True)
    
    def draw_game_over_screen(self):
        """Desenha a tela final com estatísticas e salvamento de ranking (Totalmente Responsivo)"""
        self._calculate_ui_rects()
        self.screen.fill(COLORS['background'])
        mouse_pos = pygame.mouse.get_pos()
        
        if self.game.game_won:
            title = "PARABÉNS! MISSÃO CUMPRIDA!"
            title_color = COLORS['success']
        else:
            title = "TEMPO ESGOTADO - GAME OVER"
            title_color = COLORS['error']
        
        self.draw_text(title, self.font_large, title_color,
                      self.width // 2, self.height * 0.1, center=True)
        
        # Estatísticas
        total_time_played = self.game.get_total_time_played()
        minutes = int(total_time_played // 60)
        seconds = int(total_time_played % 60)
        
        stats_panel_width = self.width * 0.5
        stats_panel_height = self.height * 0.35
        stats_panel = pygame.Rect(self.width // 2 - stats_panel_width // 2, self.height * 0.18, 
                                  stats_panel_width, stats_panel_height)
        self.draw_panel(stats_panel)
        
        score = self.game.final_score
        stats_text = [
            (f"Robôs Consertados:", f"{self.game.robots_fixed}", COLORS['success']),
            (f"Componentes:", f"{self.game.components_replaced}", COLORS['accent_cyan']),
            (f"Tempo Jog.:", f"{minutes:02d}:{seconds:02d}", COLORS['text_primary']),
            (f"Score Final:", f"{score}", COLORS['accent_yellow'])
        ]
        
        y_offset = stats_panel.y + 40
        for label, value, color in stats_text:
            self.draw_text(label, self.font_medium_regular, COLORS['text_secondary'],
                          stats_panel.x + 30, y_offset)
            val_x = stats_panel.right - 30 - self.font_medium_regular.size(value)[0]
            self.draw_text(value, self.font_medium_regular, color, val_x, y_offset)
            y_offset += 50
        
        # --- RANKING INPUT ---
        input_start_y = self.height * 0.55
        self.draw_text("DIGITE SEU NOME PARA O RANKING:", self.font_small_bold, COLORS['text_secondary'],
                      self.width // 2, input_start_y, center_x=True)
        
        name_input_rect = self.ui_rects['over_input_name']
        self.draw_input_box(self.input_name, name_input_rect.x, name_input_rect.y,
                            name_input_rect.width, name_input_rect.height,
                            active=self.input_name_active)
        
        save_button_rect = self.ui_rects['over_save_rank']
        menu_button_rect = pygame.Rect(self.width // 2 - 150, self.height - 100, 300, 60) # Responsivo: 100px da borda inferior

        if not self.ranking_saved:
            hover_save = save_button_rect.collidepoint(mouse_pos)
            self.draw_button("SALVAR RANKING", save_button_rect.x, save_button_rect.y,
                             save_button_rect.width, save_button_rect.height, hover=hover_save)
        else:
            self.draw_text("RANKING SALVO!", self.font_medium, COLORS['success'],
                           save_button_rect.centerx, save_button_rect.centery, center=True)
        
        # Botão VOLTAR AO MENU
        hover_menu = menu_button_rect.collidepoint(mouse_pos)
        self.draw_button("VOLTAR AO MENU", menu_button_rect.x, menu_button_rect.y,
                         menu_button_rect.width, menu_button_rect.height, 
                         hover=hover_menu)
    
    def _submit_code(self):
        """Lógica centralizada de submissão de código"""
        if self.input_code and len(self.input_code) == 4:
            # A validação agora aceita códigos alfanuméricos
            self.game.validate_code(self.input_code)
            self.input_code = ""
            self.input_active = False
            if self.game.game_over:
                self.state = "game_over"
        
    def handle_events(self):
        """Processa eventos do pygame, incluindo redimensionamento"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            # --- Lida com redimensionamento da janela ---
            if event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self._calculate_ui_rects() # Recalcula todos os retângulos
                self.width, self.height = event.w, event.h
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.state == "menu":
                    if self.ui_rects['menu_start'].collidepoint(mouse_pos):
                        self.game.start_game()
                        self.state = "playing"
                        self.input_code = ""
                        self.input_active = False
                    elif self.ui_rects['menu_ranking'].collidepoint(mouse_pos):
                        self.ranking = self.load_ranking()
                        self.state = "ranking"

                elif self.state == "ranking":
                    # Recria o retângulo do botão de menu com base no tamanho atual
                    menu_button_rect = pygame.Rect(self.width // 2 - 150, self.height - 100, 300, 60)
                    if menu_button_rect.collidepoint(mouse_pos):
                         self.state = "menu"
                
                elif self.state == "playing":
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
                    
                    input_rect = self.ui_rects['play_input_code']
                    button_rect = self.ui_rects['play_submit_code']
                    
                    if input_rect.collidepoint(mouse_pos):
                        self.input_active = True
                        self.input_name_active = False
                    elif button_rect.collidepoint(mouse_pos):
                        self._submit_code()
                    else:
                         self.input_active = False
                
                elif self.state == "game_over":
                    # Recalcula os retângulos para clique na tela de game over
                    self._calculate_ui_rects()
                    name_input_rect = self.ui_rects['over_input_name']
                    save_button_rect = self.ui_rects['over_save_rank']
                    menu_button_rect = pygame.Rect(self.width // 2 - 150, self.height - 100, 300, 60)
                    
                    if name_input_rect.collidepoint(mouse_pos):
                        self.input_name_active = True
                        self.input_active = False
                    else:
                        self.input_name_active = False
                        
                    if save_button_rect.collidepoint(mouse_pos) and not self.ranking_saved:
                        if self.input_name.strip():
                            self.add_to_ranking(self.input_name.strip(), self.game.final_score, 
                                                self.game.get_total_time_played(), self.game.robots_fixed)
                            self.ranking_saved = True
                            # Redirecionamento imediato para o ranking
                            self.state = "ranking" 
                        
                    if menu_button_rect.collidepoint(mouse_pos):
                        self.state = "menu"
                        self.game = Game()
                        self.input_code = ""
                        self.input_name = "Novo Técnico"
                        self.input_active = False
                        self.input_name_active = False
                        self.ranking_saved = False
                        self.game.selected_robot_id = None
                        self.ranking = self.load_ranking() 

            if event.type == pygame.KEYDOWN:
                if self.state == "playing" and self.input_active:
                    if event.key == pygame.K_RETURN:
                        self._submit_code()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_code = self.input_code[:-1]
                    else:
                        # --- CORREÇÃO AQUI: Aceita Alfanumérico e converte para MAIÚSCULA ---
                        char = event.unicode.upper()
                        if char.isalnum() and len(self.input_code) < 4:
                            self.input_code += char
                            
                elif self.state == "game_over" and self.input_name_active:
                    if event.key == pygame.K_RETURN:
                        self.input_name_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_name = self.input_name[:-1]
                    else:
                        if event.unicode.isalnum() or event.unicode.isspace():
                            if len(self.input_name) < 20: 
                                self.input_name += event.unicode
        
        return True
    
    def update(self):
        """Atualiza o estado do jogo"""
        if self.state == "playing":
            current_time = time.time()
            self.game.update(current_time)
            
            if self.game.game_over:
                self.state = "game_over"
        
    def draw(self):
        """Desenha a tela atual"""
        if self.state == "menu":
            self.draw_menu_screen()
        elif self.state == "ranking":
            self.draw_ranking_screen()
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