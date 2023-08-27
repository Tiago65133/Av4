import pygame
import sys
import sqlite3

# Conectando ao banco de dados 
conn = sqlite3.connect("jogo_da_velha.db")
cursor = conn.cursor()

# Criando a tabela 
cursor.execute("""
CREATE TABLE IF NOT EXISTS partidas (
    id INTEGER PRIMARY KEY,
    jogador_o TEXT,
    jogador_x TEXT,
    vencedor TEXT,
    data_partida TEXT
)
""")

# Função para inserir um novo registro de partida
def inserir_partida(jogador_o, jogador_x, vencedor, data_partida):
    cursor.execute("""
    INSERT INTO partidas (jogador_o, jogador_x, vencedor, data_partida)
    VALUES (?, ?, ?, ?)
    """, (jogador_o, jogador_x, vencedor, data_partida))
    conn.commit()

# Inserção de partida 
inserir_partida("JogadorO", "JogadorX", "JogadorO", "2023-08-27")

# Consulta para obter todos os registros de partidas
def obter_partidas():
    cursor.execute("SELECT * FROM partidas")
    return cursor.fetchall()

# Consulta para obter os registros
partidas = obter_partidas()
for partida in partidas:
    print(partida)

# Fechando a conexão com o banco de dados
conn.close()


# Inicialização do Pygame
pygame.init()

# Configurações do jogo
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 2 - SQUARE_SIZE // 10
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Cores
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Velha")
screen.fill(BG_COLOR)

# Tabuleiro
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

# Funções auxiliares
def draw_lines():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in board:
        if None in row:
            return False
    return True

def check_win(player):
    # Verificação das linhas
    for row in board:
        if all(square == player for square in row):
            return True
    # Verificação das colunas
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True
    # Verificação das diagonais
    if all(board[i][i] == player for i in range(BOARD_ROWS)) or all(board[i][BOARD_COLS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True
    return False

def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

draw_lines()

# Variáveis do jogo
player = "O"
game_over = False

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]  
            mouseY = event.pos[1]  
            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                player = "X" if player == "O" else "O"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_game()
            game_over = False

    draw_figures()

    if game_over:
        pygame.time.wait(1000)
        restart_game()

    pygame.display.update()
