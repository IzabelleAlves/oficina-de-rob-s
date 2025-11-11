"""
Oficina de Reparo de Robôs
Jogo completo em Python 3.10+ com pygame
Autor: Sistema de IA
Ano: 2024
"""

from gui import GUI


def main():
    """Função principal que inicia o jogo"""
    try:
        gui = GUI()
        gui.run()
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

