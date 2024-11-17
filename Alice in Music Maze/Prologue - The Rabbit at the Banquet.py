import pygame
import sys
import os

# 初始化Pygame
pygame.init()

# 常量
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
PLAYER_RADIUS = 15
FPS = 30
PLAYER_SPEED = TILE_SIZE

# 文件夹路径
IMAGE_FOLDER = "images"

# 颜色定义
BACKGROUND_COLOR = "white"

# 迷宫布局（1表示墙壁，0表示路径）
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

# 对象位置
player_pos = [1 * TILE_SIZE + TILE_SIZE // 2, 1 * TILE_SIZE + TILE_SIZE // 2]  # 玩家起始位置
exit_pos = (18, 13)  # 出口位置

# 加载图片
def load_images(folder_path):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            name = os.path.splitext(filename)[0]
            img = pygame.image.load(os.path.join(folder_path, filename))
            images[name] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return images

# 加载文件夹内的图片
images = load_images(IMAGE_FOLDER)

# 游戏状态
last_move_time = 0  # 上一次移动的时间

# 设置显示窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# 绘制迷宫
def draw_maze():
    for y, row in enumerate(MAZE):
        for x, tile in enumerate(row):
            if tile == 1:  # 墙壁
                if 'wall' in images:
                    screen.blit(images['wall'], (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    pygame.draw.rect(screen, 'black', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 0:  # 路径
                if 'road' in images:
                    screen.blit(images['road'], (x * TILE_SIZE, y * TILE_SIZE))

def can_move(new_pos):
    # 检查新位置是否在迷宫边界内，并且不与墙壁碰撞
    grid_x = new_pos[0] // TILE_SIZE
    grid_y = new_pos[1] // TILE_SIZE
    if 0 <= grid_x < len(MAZE[0]) and 0 <= grid_y < len(MAZE):
        if MAZE[grid_y][grid_x] == 0:
            return True
    return False

player_shrunk = False
last_move_time = 0
move_cooldown = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 检查按键并更新位置
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    new_pos = player_pos[:]
        
    if current_time - last_move_time >= move_cooldown:
        if keys[pygame.K_w]:  # 向上移动
            new_pos[1] -= PLAYER_SPEED
        elif keys[pygame.K_s]:  # 向下移动
            new_pos[1] += PLAYER_SPEED
        elif keys[pygame.K_a]:  # 向左移动
            new_pos[0] -= PLAYER_SPEED
        elif keys[pygame.K_d]:  # 向右移动
            new_pos[0] += PLAYER_SPEED

        if can_move(new_pos):
            player_pos = new_pos  # 更新玩家位置
            last_move_time = current_time  # 更新最后移动时间

    # 绘制游戏元素
    screen.fill(BACKGROUND_COLOR)
    draw_maze()
    if 'player' in images:
        screen.blit(images['player'], (player_pos[0] - TILE_SIZE // 2, player_pos[1] - TILE_SIZE // 2))
    else:
        pygame.draw.circle(screen, 'red', player_pos, TILE_SIZE // 2)

    if 'exit' in images:
        screen.blit(images['exit'], (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE))
    else:
        pygame.draw.rect(screen, 'green', (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
