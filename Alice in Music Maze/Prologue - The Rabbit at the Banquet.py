'''
这是注释：
左上是起点，右下是终点，玩家通过ASDW移动，注意提前调整键盘至 “英文模式 ”。
迷宫为 15 行，20 列，注意编程默认从 “0” 开始计数。每个格子均有对应坐标，注释在迷宫数组的右侧。
蓝色小点为缩小药水的位置，玩家碰撞到药水会变小。
(11, 9) 和 (13, 9) 为特殊格子，检测到玩家变小后才允许通过。添加图片素材时这两个格子需要和正常道路的格子区分开，显示出这里是需要喝药水变小才能通过的窄路。
    例如正常格子是草地素材，这里就是藤蔓素材。
'''


import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
PLAYER_RADIUS = 15
PLAYER_COLOR = "red"
BACKGROUND_COLOR = "white"
MAZE_COLOR = "black"
ITEM_COLOR = "blue"
FPS = 30
PLAYER_SPEED = 5

# Maze layout (1 represents wall, 0 represents path)
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # (0,0) (1,0) ... (19,0)
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],  # (0,1) (1,1) ... (19,1)
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],  # (0,2) (1,2) ... (19,2)
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],  # (0,3) (1,3) ... (19,3)
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # (0,4) (1,4) ... (19,4)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # (0,5) (1,5) ... (19,5)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # (0,6) (1,6) ... (19,6)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],  # (0,7) (1,7) ... (19,7)
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # (0,8) (1,8) ... (19,8)
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],  # (0,9) (1,9) ... (19,9)
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],  # (0,10) (1,10) ... (19,10)
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],  # (0,11) (1,11) ... (19,11)
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],  # (0,12) (1,12) ... (19,12)
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # (0,13) (1,13) ... (19,13)
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]   # (0,14) (1,14) ... (19,14)
]

# Player starting position
player_pos = [1 * TILE_SIZE + TILE_SIZE // 2, 1 * TILE_SIZE + TILE_SIZE // 2]

# Item position (to shrink player)
item_pos = [9 * TILE_SIZE + TILE_SIZE // 2, 3 * TILE_SIZE + TILE_SIZE // 2]

# Exit position
exit_pos = (18, 13)  # Grid position of the exit

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

def draw_maze():
    for y, row in enumerate(MAZE):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, MAZE_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def is_colliding(pos1, pos2, radius):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 < radius ** 2

def can_move(new_pos, radius, player_shrunk):
    # Check if the new position is within the maze boundaries and not colliding with walls
    grid_x = new_pos[0] // TILE_SIZE
    grid_y = new_pos[1] // TILE_SIZE
    if 0 <= grid_x < len(MAZE[0]) and 0 <= grid_y < len(MAZE):
        if MAZE[grid_y][grid_x] == 0:
            # Check for special narrow tiles
            if (grid_x, grid_y) in [(11, 9), (13, 9)]:
                return player_shrunk  # Allow passage only if player is shrunk
            return True
    return False

player_shrunk = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_pos = player_pos[:]
    if keys[pygame.K_w]:  # Move up
        new_pos[1] -= PLAYER_SPEED
    if keys[pygame.K_s]:  # Move down
        new_pos[1] += PLAYER_SPEED
    if keys[pygame.K_a]:  # Move left
        new_pos[0] -= PLAYER_SPEED
    if keys[pygame.K_d]:  # Move right
        new_pos[0] += PLAYER_SPEED

    # Check if the new position is valid
    if can_move(new_pos, PLAYER_RADIUS, player_shrunk):
        player_pos = new_pos

    # Check for collision with item
    if is_colliding(player_pos, item_pos, PLAYER_RADIUS):
        player_shrunk = True

    # Determine player size
    current_player_radius = PLAYER_RADIUS // 2 if player_shrunk else PLAYER_RADIUS

    screen.fill(BACKGROUND_COLOR)
    draw_maze()
    pygame.draw.circle(screen, PLAYER_COLOR, player_pos, current_player_radius)
    if not player_shrunk:
        pygame.draw.circle(screen, ITEM_COLOR, item_pos, PLAYER_RADIUS // 2)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()