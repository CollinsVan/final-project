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

# 初始化Pygame
pygame.init()

# 常量
WIDTH, HEIGHT = 800, 600 # 设置窗口宽度和高度
TILE_SIZE = 40 # 每个格子的大小
PLAYER_RADIUS = 15 # 玩家角色的半径
PLAYER_COLOR = "red" # 玩家角色的颜色
BACKGROUND_COLOR = "white" # 背景颜色
MAZE_COLOR = "black" # 迷宫墙壁颜色
ITEM_COLOR = "blue" # 道具颜色
FPS = 30 # 帧率
PLAYER_SPEED = 5 # 玩家移动速度
# 新加的
PLAYER_SPEED = TILE_SIZE  # 每次移动一个格子

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

# 玩家起始位置
player_pos = [1 * TILE_SIZE + TILE_SIZE // 2, 1 * TILE_SIZE + TILE_SIZE // 2]
# 道具位置（用来缩小玩家）
item_pos = [9 * TILE_SIZE + TILE_SIZE // 2, 3 * TILE_SIZE + TILE_SIZE // 2]
# 出口位置
exit_pos = (18, 13)

# 设置显示窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # 创建窗口
pygame.display.set_caption("Maze Game") # 设置窗口标题
clock = pygame.time.Clock() # 创建时钟对象，用于控制帧率

def draw_maze():
    for y, row in enumerate(MAZE):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, MAZE_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def is_colliding(pos1, pos2, radius):
    return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 < radius ** 2 # 检查两个圆形是否碰撞

def can_move(new_pos, radius, player_shrunk):
    # 检查新位置是否在迷宫边界内，并且不与墙壁碰撞
    grid_x = new_pos[0] // TILE_SIZE
    grid_y = new_pos[1] // TILE_SIZE
    if 0 <= grid_x < len(MAZE[0]) and 0 <= grid_y < len(MAZE):
        if MAZE[grid_y][grid_x] == 0:
            # 检查特殊狭窄的格子
            if (grid_x, grid_y) in [(11, 9), (13, 9)]: # 特殊狭窄位置
                return player_shrunk  # 只有在玩家变小的情况下才能通过
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
        
        if can_move(new_pos, PLAYER_RADIUS, player_shrunk):
            player_pos = new_pos  # 只有在合法的情况下才更新位置
            last_move_time = current_time  # 更新移动时间        

    # 新加的
    # 绘制屏幕
    screen.fill(BACKGROUND_COLOR) # 填充背景颜色
    draw_maze() # 绘制迷宫
    pygame.draw.circle(screen, PLAYER_COLOR, player_pos, PLAYER_RADIUS if not player_shrunk else PLAYER_RADIUS // 2) # 绘制玩家角色
    pygame.draw.circle(screen, ITEM_COLOR, item_pos, PLAYER_RADIUS // 2) # 绘制道具
    pygame.draw.rect(screen, "green", (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)) # 绘制出口

    # 检查与道具的碰撞
    if is_colliding(player_pos, item_pos, PLAYER_RADIUS):
        player_shrunk = True

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()