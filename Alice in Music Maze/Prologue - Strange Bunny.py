import pygame
import sys
import os
import time
import random

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
MUSIC_FOLDER = "music & soundscape"
MUSIC_FILE = "A-very-happy-christmas.mp3"

# 背景颜色定义
BACKGROUND_COLOR = "white"
# 文本框颜色定义
TEXTBOX_COLOR = (255, 255, 224)  # 浅黄色

# 加载音效
def load_sounds(folder_path):
    sounds = []
    for i in range(1, 8):  # 从1.wav到7.wav
        sound_file = os.path.join(folder_path, f"{i}.wav")
        if os.path.exists(sound_file):
            sounds.append(pygame.mixer.Sound(sound_file))
    return sounds
# 加载音效
sound_effects = load_sounds(MUSIC_FOLDER)

# 迷宫布局（1表示墙壁，0表示路径）
MAZE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# 为每个地块绑定音效
tile_sounds = {}
for y in range(len(MAZE)):
    for x in range(len(MAZE[y])):
        if MAZE[y][x] == 0:  # 仅对路径地块进行绑定
            tile_sounds[(x, y)] = random.choice(sound_effects)

# 对象位置
player_pos = [1 * TILE_SIZE + TILE_SIZE // 2, 1 * TILE_SIZE + TILE_SIZE // 2]
rabbit_pos = [3 * TILE_SIZE + TILE_SIZE // 2, 3 * TILE_SIZE + TILE_SIZE // 2]  # 兔子的初始位置
exit_pos = (18, 13)
item_pos = [9 * TILE_SIZE + TILE_SIZE // 2, 3 * TILE_SIZE + TILE_SIZE // 2]
narrow_path_pos = [(11, 9), (13, 9)]

# 加载图片
def load_images(folder_path):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            name = os.path.splitext(filename)[0]
            img = pygame.image.load(os.path.join(folder_path, filename))
            if name == 'start_background':
                images[name] = img
            else:
                images[name] = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    return images

# 加载图片
images = load_images(IMAGE_FOLDER)
# 加载完成图片
finish_image = pygame.image.load(os.path.join(IMAGE_FOLDER, "finish.png"))

# 加载背景音乐
def load_music(music_file):
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_file))
    pygame.mixer.music.play(-1)
def load_finish_music():
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, "finish_music.mp3"))
    pygame.mixer.music.play(-1)  # 播放一次
# 加载背景音乐
load_music(MUSIC_FILE)

# 加载缩小药水音效
def load_sound(sound_file):
    return pygame.mixer.Sound(os.path.join(MUSIC_FOLDER, sound_file))

# 加载缩小药水音效
shrinking_potion_sound = load_sound("shrinking_potion.wav")

# 防止中文输入法打字使游戏无法运行！！
pygame.key.stop_text_input()

# ————————————————————————————————————————资源加载完毕————————————————————————————————————————————

# 初始化游戏
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alice in Music Maze")
clock = pygame.time.Clock()

# 检查游戏状态
player_shrunk = False
last_move_time = 0
move_cooldown = 100
textbox_visible = True
textbox_start_time = pygame.time.get_ticks()  # 检查文本框显示时机
potion_collected = False  # 用于跟踪药水是否已被碰到
textbox_message = "Yawn~ The air is so fresh in the forest!"  # 初始文本框消息
rabbit_staying = False  # 用于标志兔子停留状态
# 设置结束文本框相关参数
end_text_visible = False
end_text_start_time = 0
end_text_message = "Alice chases a rabbit down a hole ......Stay tuned for a follow up story!"

# 设置兔子的初始状态
rabbit_visible = False
rabbit_path = []  # 存储兔子的移动路径
rabbit_index = 0  # 路径索引
rabbit_task_done = False  # 标志是否完成兔子移动任务

# 计算兔子从起点到终点的路径（使用 BFS 或 A* 算法）
def find_shortest_path(start, end):
    from collections import deque

    queue = deque([(start, [])])
    visited = set()
    while queue:
        (current, path) = queue.popleft()
        if current == end:
            return path
        if current in visited:
            continue
        visited.add(current)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(MAZE[0]) and 0 <= neighbor[1] < len(MAZE):
                if MAZE[neighbor[1]][neighbor[0]] == 0 and neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

    return []

# 设置兔子路径
rabbit_path = find_shortest_path((3, 3), (18, 13))

# 设置迷宫路线
def draw_maze():
    for y, row in enumerate(MAZE):
        for x, tile in enumerate(row):
            if tile == 1:  # 墙壁
                if 'wall' in images:
                    screen.blit(images['wall'], (x * TILE_SIZE, y * TILE_SIZE))
                else:
                    pygame.draw.rect(screen, 'black', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 0:  # 路径
                if 'path' in images:
                    screen.blit(images['path'], (x * TILE_SIZE, y * TILE_SIZE))

def can_move(new_pos):
    grid_x = new_pos[0] // TILE_SIZE
    grid_y = new_pos[1] // TILE_SIZE
    if 0 <= grid_x < len(MAZE[0]) and 0 <= grid_y < len(MAZE):
        if MAZE[grid_y][grid_x] == 0:
            if (grid_x, grid_y) in narrow_path_pos and not player_shrunk:
                return False
            return True
    return False

# 设置文本框样式
def draw_textbox(message):
    if textbox_visible:
        # 创建文本框的矩形
        textbox_rect = pygame.Rect((WIDTH - 700) // 2, HEIGHT - 100, 700, 100)
        # 创建一个带有圆角的文本框
        rounded_rect = pygame.Surface(textbox_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(rounded_rect, TEXTBOX_COLOR, (0, 0, textbox_rect.width, textbox_rect.height), border_radius=10)
        # 描边
        pygame.draw.rect(rounded_rect, (229, 202, 96), (0, 0, textbox_rect.width, textbox_rect.height), width=5,
                         border_radius=10)
        # 绘制带描边的圆角矩形
        screen.blit(rounded_rect, textbox_rect.topleft)
        font = pygame.font.Font(None, 24)
        speaker_text = font.render("Alice", True, (191, 155, 11))
        message_text = font.render(message, True, (0, 0, 0))
        # 绘制文本
        if textbox_visible:
            message_text = font.render(message, True, (0, 0, 0))
            screen.blit(speaker_text, (textbox_rect.x + 20, textbox_rect.y + 18))
            screen.blit(message_text, (textbox_rect.x + 20, textbox_rect.y + 46))

# 绘制起始页面
def draw_start_page():
    screen.fill((169, 169, 169))  # 填充灰色背景

    # 如果背景图存在，加载并显示
    if 'start_background' in images:
        background = pygame.transform.scale(images['start_background'], (WIDTH, HEIGHT))
        screen.blit(background, (0, 0))

    # 绘制文本
    font = pygame.font.Font(None, 36)
    text = font.render("  Press any key to start the game!", True, (255, 255, 224))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
    screen.blit(text, text_rect)

    pygame.display.flip()

# ————————————————————————————————地图、人物、音乐等参数设置完毕————————————————————————————————————

running = True
game_started = False
audio_played_tiles = set()  # 用于跟踪已播放音频的地块

while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_started and event.type == pygame.KEYDOWN:  # 玩家按下任意键开始游戏
            game_started = True
    if not game_started:
        draw_start_page()
    else:
        # 检查文本框显示时间
        if textbox_visible and pygame.time.get_ticks() - textbox_start_time >= 2000:
            textbox_visible = False

            # 如果任务未完成，启动兔子移动
            if not rabbit_task_done:
                rabbit_visible = True  # 兔子开始可见

        # 检查兔子移动逻辑
        if rabbit_visible and rabbit_index < len(rabbit_path):
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time >= move_cooldown:
                # 获取当前目标格子
                current_target = rabbit_path[rabbit_index]
                target_x, target_y = current_target[0] * TILE_SIZE + TILE_SIZE // 2, current_target[
                    1] * TILE_SIZE + TILE_SIZE // 2

                # 计算兔子下一步移动方向
                new_pos = rabbit_pos[:]
                if rabbit_pos[0] < target_x:
                    new_pos[0] += TILE_SIZE
                elif rabbit_pos[0] > target_x:
                    new_pos[0] -= TILE_SIZE

                if rabbit_pos[1] < target_y:
                    new_pos[1] += TILE_SIZE
                elif rabbit_pos[1] > target_y:
                    new_pos[1] -= TILE_SIZE

                # 更新兔子的位置
                rabbit_pos = new_pos
                last_move_time = current_time

                # 如果兔子到达目标格子，更新路径索引
                if rabbit_pos[0] == target_x and rabbit_pos[1] == target_y:
                    rabbit_index += 1

                # 如果到达终点
                if rabbit_index >= len(rabbit_path):
                    rabbit_staying = True  # 兔子停留状态
                    rabbit_visible = False  # 隐藏兔子
                    rabbit_task_done = True  # 标记任务完成

        # 检查按键并更新位置
        if not textbox_visible:  # 只有在文本框不显示时，才允许移动
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            new_pos = player_pos[:]

            if current_time - last_move_time >= move_cooldown:
                if keys[pygame.K_w]:
                    new_pos[1] -= PLAYER_SPEED
                elif keys[pygame.K_s]:
                    new_pos[1] += PLAYER_SPEED
                elif keys[pygame.K_a]:
                    new_pos[0] -= PLAYER_SPEED
                elif keys[pygame.K_d]:
                    new_pos[0] += PLAYER_SPEED

                if can_move(new_pos):
                    player_pos = new_pos
                    last_move_time = current_time

                    # 播放地块绑定的音效
                    grid_x = player_pos[0] // TILE_SIZE
                    grid_y = player_pos[1] // TILE_SIZE
                    if (grid_x, grid_y) in tile_sounds and (grid_x, grid_y) not in audio_played_tiles:
                        tile_sound = tile_sounds[(grid_x, grid_y)]
                        tile_sound.play()
                        audio_played_tiles.add((grid_x, grid_y))  # 将地块添加到已播放集合中

                # 检查药水碰撞
                if not potion_collected and abs(player_pos[0] - item_pos[0]) < TILE_SIZE // 2 and abs(
                        player_pos[1] - item_pos[1]) < TILE_SIZE // 2:
                    player_shrunk = True
                    shrinking_potion_sound.play()  # 播放缩小药水音效

                # 检查玩家是否碰到窄路
                if (new_pos[0] // TILE_SIZE, new_pos[1] // TILE_SIZE) in narrow_path_pos and not player_shrunk:
                    textbox_message = "Emmm, I'm too big, is there any way to get smaller?"
                    textbox_visible = True
                    textbox_start_time = pygame.time.get_ticks()  # 重置显示时间

            # 检查玩家是否走到特定地块 (3, 1)
            if (new_pos[0] // TILE_SIZE, new_pos[1] // TILE_SIZE) == (3, 1):
                textbox_message = "Do these grounds sing?"
                textbox_visible = True
                textbox_start_time = pygame.time.get_ticks()  # 重置显示时间

            # 检查玩家是否走到特定地块 (12, 9)
            if (new_pos[0] // TILE_SIZE, new_pos[1] // TILE_SIZE) == (12, 9):
                textbox_message = "Oh! I can get through them!"
                textbox_visible = True
                textbox_start_time = pygame.time.get_ticks()  # 重置显示时间

            # 检查玩家是否到达出口
            if (player_pos[0] // TILE_SIZE, player_pos[1] // TILE_SIZE) == exit_pos:
                load_finish_music()  # 播放完成音乐
                screen.blit(finish_image, (0, 0))  # 显示完成图片
                # 绘制文本
                font = pygame.font.Font(None, 24)
                text = font.render("Alice chases a rabbit down a hole ...... Stay tuned for the rest of the story!", True, (191, 155, 11))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
                screen.blit(text, text_rect)

                pygame.display.flip()  # 更新屏幕
                pygame.time.delay(1000)  # 显示完成图片1秒

        # 绘制游戏元素
        screen.fill(BACKGROUND_COLOR)
        draw_maze()

        # 绘制玩家
        if player_shrunk:
            if 'player_small' in images:
                screen.blit(images['player_small'], (player_pos[0] - TILE_SIZE // 2, player_pos[1] - TILE_SIZE // 2))
            else:
                pygame.draw.circle(screen, 'red', player_pos, PLAYER_RADIUS // 2)
        else:
            if 'player' in images:
                screen.blit(images['player'], (player_pos[0] - TILE_SIZE // 2, player_pos[1] - TILE_SIZE // 2))
            else:
                pygame.draw.circle(screen, 'red', player_pos, TILE_SIZE // 2)

        # 绘制缩小药水
        if 'shrinking_potion' in images:
            screen.blit(images['shrinking_potion'], (item_pos[0] - TILE_SIZE // 2, item_pos[1] - TILE_SIZE // 2))
        else:
            pygame.draw.circle(screen, "blue", item_pos, TILE_SIZE // 4)

        # 绘制出口
        if 'exit' in images:
            screen.blit(images['exit'], (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE))
        else:
            pygame.draw.rect(screen, 'green', (exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # 绘制狭窄路径
        if 'narrow_path' in images:
            for pos in narrow_path_pos:
                screen.blit(images['narrow_path'], (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE))
        else:
            for pos in narrow_path_pos:
                pygame.draw.rect(screen, 'grey', (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        # 绘制引导精灵
        if rabbit_visible:
            if 'rabbit' in images:
                screen.blit(images['rabbit'], (rabbit_pos[0] - TILE_SIZE // 2, rabbit_pos[1] - TILE_SIZE // 2))
            else:
                pygame.draw.circle(screen, 'orange', rabbit_pos, TILE_SIZE // 2)

        # 绘制文本框
        draw_textbox(textbox_message)

        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
sys.exit()
