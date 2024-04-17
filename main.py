#import random
import pygame
from tracking_functions import tracking
import config as cf

from game_functions import (calc_score, add_enemies, add_potatoes, move_player, check_mode, check_collision, game_over_screen, update_screen,calc_time)


def main():
    # ゲームループ
    add_enemies(1)
    while 1:
        calc_score()
        success, image = cf.cap.read()
        if not success:
            continue
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # ウィンドウを閉じた時に終了する処理
                return 0

        mouth, face = tracking(image, cf.face_mesh)
        move_player(face) # 顔の動きによってプレイヤーを移動させる関数
        check_mode(mouth) # 口の動きによってモードを判定する関数

        if calc_time(cf.enemies_update_time, cf.enemies_update_interval):
            # 敵を追加してから一定時間が経過していれば敵を追加する処理
            add_enemies(1)
            cf.enemies_update_time = cf.current_time
        if calc_time(cf.potatoes_update_time, cf.potatoes_update_interval):
            add_potatoes(1)
            cf.potatoes_update_time = cf.current_time

        if cf.mode == "normal":
            if check_collision():
                game_over_screen()
                return 0
        else:
            check_collision()

        update_screen()
        cf.clock.tick(30)

if __name__ == "__main__":
    main()
    pygame.quit()
