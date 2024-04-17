import random
import pygame
import os
import config as cf


def calc_score(point=0):
    """スコアの足し引き、カウントアップをする関数"""
    cf.score += point
    if calc_time(cf.score_update_time, cf.score_interval):
        if cf.mode == "normal":
            cf.score += 1
            cf.score_update_time = cf.current_time
        else:
            cf.score -= 3
            cf.score_update_time = cf.current_time
    



def add_enemies(num_enemies):
    for _ in range(num_enemies):
        enemy_x = random.randint(0, cf.width - cf.enemy_size)
        enemy_y = 0
        cf.enemies.append([enemy_x, enemy_y])

def add_potatoes(num_potatoes):
    for _ in range(num_potatoes):
        potato_x = random.randint(0, cf.width - cf.enemy_size)
        potato_y = 0
        cf.potatoes.append([potato_x,potato_y])

def calc_time(last_update_time, interval):
    """一定時間が経過したかを判定する関数"""
    cf.current_time = pygame.time.get_ticks()
    if (cf.current_time - last_update_time) >= interval:
        last_update_time = cf.current_time
        return True
    else:
        return False
    
def move_player(face):
    if face == "left" and cf.player_x > 0:
        cf.player_x -= cf.player_speed
    if face == "right" and cf.player_x < cf.width - cf.player_size:
        cf.player_x += cf.player_speed

def check_mode(mouth):
    if cf.mode == "normal":
        if mouth == "open":
            change_mode()
    else:
        if mouth == "close":
            change_mode()

def draw_screen():
    """プレイヤー、敵、ポテト、スコアを描画する関数"""
    cf.screen.fill(cf.BLACK)

    cf.screen.blit(cf.player_image, (cf.player_x, cf.player_y))

    for enemy in cf.enemies:
        cf.screen.blit(cf.invader_image, (enemy[0], enemy[1]))
    
    for potato in cf.potatoes:
        cf.screen.blit(cf.potato_image, (potato[0], potato[1]))

    score_text = cf.score_font.render(f'SCORE : {cf.score}', True, (255, 255, 255))  # 白色でスコアを描画
    cf.screen.blit(score_text, (10, 10))  # 画面の左上にスコアを表示
    pygame.display.flip()


def update_points():
    """敵とポテトの位置を更新する関数"""
    for enemy in cf.enemies:
        enemy[1] += cf.enemy_speed
        if enemy[1] > cf.height:
            cf.enemies.remove(enemy)
            add_enemies(1)

    for potato in cf.potatoes:
        potato[1] += cf.potato_speed
        if potato[1] > cf.height:
            cf.potatoes.remove(potato)

def check_collision():
    """敵・ポテトとの衝突の判定と点数の計算を行う関数"""
    player_rect = pygame.Rect(cf.player_x, cf.player_y, cf.player_size-10, cf.player_size-30)
    for i,enemy in enumerate(cf.enemies):
        enemy_rect = pygame.Rect(enemy[0], enemy[1], cf.enemy_size-10, cf.enemy_size-30)
        if player_rect.colliderect(enemy_rect):
            if cf.mode == "normal":
                return True
            else:
                cf.eat_enemy.play()
                del cf.enemies[i]
                return True
            
    for i,potato in enumerate(cf.potatoes):
        potato_rect = pygame.Rect(potato[0], potato[1], cf.potato_size-20, cf.potato_size-10)
        if player_rect.colliderect(potato_rect):
            if cf.mode == "normal":
                cf.eat_potato.play()
                calc_score(50)
                del cf.potatoes[i]
            else:
                cf.eat_enemy.play()
                del cf.potatoes[i]
                calc_score(-100)
    return False
    

def flash_screen():
    """ゲームオーバー時に画面を点滅させる関数。"""
    for _ in range(4):  # 2秒間点滅
        cf.screen.fill(cf.BLACK)
        pygame.display.flip()
        pygame.time.delay(250)
        draw_screen()
        pygame.time.delay(250)
    cf.screen.fill(cf.BLACK)

def fade_in_image(duration=2000):
    """画像をフェードインさせる関数。durationはミリ秒単位。"""
    start_time = pygame.time.get_ticks()  # 開始時間
    fade_surface = pygame.Surface((cf.width, cf.height))
    fade_surface = fade_surface.convert_alpha()
    alpha_step = 255 / (duration // cf.clock.get_time())  # アルファ値のステップ計算
    alpha_value = 0  # 初期アルファ値

    while alpha_value < 255:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        current_time = pygame.time.get_ticks()
        if current_time - start_time < duration:
            alpha_value += alpha_step  # アルファ値を増加
            alpha_value = min(255, alpha_value)  # 255を超えないように
            fade_surface.fill((0, 0, 0, 0))  # 透明で塗りつぶし
            fade_surface.blit(cf.game_over_image, (0, 0))  # イメージをコピー
            fade_surface.set_alpha(int(alpha_value))  # アルファ値を設定
            cf.screen.blit(fade_surface, (0, 0))  # スクリーンにブレンドして描画
            pygame.display.flip()
            cf.clock.tick(30)  # フレームレートを保持
        else:
            break

def game_over_bgm():
    pygame.mixer.music.stop()  # 現在のBGMを停止
    pygame.mixer.music.load(os.path.join("music","game_over.mp3"))  # ゲームオーバー時の音楽を読み込む
    pygame.mixer.music.play()  # ゲームオーバー時の音楽を再生

def draw_last_score():
    score_font = pygame.font.Font(None, 72)
    text = score_font.render(f'SCORE : {cf.score}', True, (255, 255, 255))  # 白色でテキストを描画
    score_text = text.get_rect(center=(cf.width // 2, cf.height // 2))  # テキストの矩形情報を取得し、中央揃えに設定
    cf.screen.fill((0,0,0))
    cf.screen.blit(text, score_text)  # 画面の真ん中にスコアを表示
    pygame.display.flip()
    pygame.time.delay(7000)  # 7秒待機

def game_over_screen():
    game_over_bgm()
    flash_screen()
    fade_in_image(2000) # 画像を2秒かけてフェードイン
    draw_last_score()

def update_screen():
    update_points()
    draw_screen()
    

def change_mode():
    if cf.mode == "normal":
        cf.mode = "horror"
        cf.player_size *= 2
        cf.player_image = cf.horror_image
        cf.player_y = cf.height - cf.player_size
        cf.player_x -= cf.player_size/4
        cf.player_speed = 8
    else:
        cf.mode = "normal"
        cf.player_size /= 2
        cf.player_image = cf.normal_image
        cf.player_y = cf.height - cf.player_size - 10
        cf.player_x += cf.player_size/2
        cf.player_speed = 5
