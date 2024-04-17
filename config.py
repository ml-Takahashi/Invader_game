import pygame
import cv2
import os
import mediapipe as mp

# 色の定義
BLACK = (0, 0, 0)

# 初期設定
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
score = 0

# Music設定
pygame.mixer.init()
pygame.mixer.music.load(os.path.join("music","maou_bgm_8bit25.mp3"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
eat_enemy = pygame.mixer.Sound(os.path.join("music","eat_enemy.mp3")) # 敵を食べるサウンド
eat_potato = pygame.mixer.Sound(os.path.join("music","eat_potato.mp3")) # ポテトを食べるサウンド

# プレイヤー設定
mode = "normal"
player_size = 80
player_x = width // 4
player_y = height - player_size - 10
player_speed = 7
normal_image = pygame.image.load(os.path.join("images",'clown.jpg'))
normal_image = pygame.transform.scale(normal_image, (player_size, player_size))
horror_image = pygame.image.load(os.path.join("images","horror_clown.jpg"))
horror_image = pygame.transform.scale(horror_image, (player_size*2, player_size*2))
player_image = normal_image


# 敵設定
enemy_size = 80
enemy_speed = 7
enemies = []
invader_image = pygame.image.load(os.path.join("images",'invader.jpg'))
invader_image = pygame.transform.scale(invader_image, (enemy_size, enemy_size))

# アイテム設定
potato_size = 80
potato_speed = 8
potatoes = []
potato_image = pygame.image.load(os.path.join("images","potato.jpg"))
potato_image = pygame.transform.scale(potato_image, (potato_size, potato_size))

# ゲームオーバー画面
game_over_image = pygame.image.load(os.path.join("images","game_over.jpg"))
game_over_image = pygame.transform.scale(game_over_image, (width, height))

# フォントの初期化
pygame.font.init()

# フォントオブジェクトの作成
score_font = pygame.font.Font(None, 30)  # Noneはデフォルトフォントを使用、30はフォントサイズ

# 敵・アイテムを追加するタイミングを計算する変数
current_time = 0 # 現在の時刻
score_update_time = 0  # スコアを更新した最後の時間
score_interval = 500  # スコアを更新する間隔（ms）

enemies_update_time = 0 # 最後に敵を追加した時間
enemies_update_interval = 2000 # 敵を追加する感覚(ms)

potatoes_update_time = 0 # 最後にポテトを追加した時間
potatoes_update_interval = 3000 #ポテトを追加する感覚(ms)


# メディアパイプの顔モデルを初期化
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                max_num_faces=1,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Webカメラからの映像入力を開始
cap = cv2.VideoCapture(0)