import cv2
import numpy as np


def tracking(image, face_mesh):
    mouth = "close"
    face = "center"
    # 画像を反転
    image = cv2.flip(image, 1)

    # メディアパイプに渡す前に画像をBGRからRGBに変換
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # メディアパイプの処理を実行
    results = face_mesh.process(image)

    # RGBからBGRに戻す
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for face_landmarks in results.multi_face_landmarks:
        # 口の開き具合を判定
        upper_lip = np.array([face_landmarks.landmark[13].y, face_landmarks.landmark[13].x]) * [image.shape[0], image.shape[1]]
        lower_lip = np.array([face_landmarks.landmark[14].y, face_landmarks.landmark[14].x]) * [image.shape[0], image.shape[1]]
        mouth_opening = np.linalg.norm(upper_lip - lower_lip)
    
    if mouth_opening > 20:  # 閾値は適宜調整
        mouth = "open"

    # 顔の向きを判定
    nose_tip = np.array([face_landmarks.landmark[1].x, face_landmarks.landmark[1].y]) * [image.shape[1], image.shape[0]]
    left_cheek = np.array([face_landmarks.landmark[234].x, face_landmarks.landmark[234].y]) * [image.shape[1], image.shape[0]]
    right_cheek = np.array([face_landmarks.landmark[454].x, face_landmarks.landmark[454].y]) * [image.shape[1], image.shape[0]]

    if abs(nose_tip[0] - left_cheek[0]) < 50:
        face = "left"
    elif abs(right_cheek[0] - nose_tip[0]) < 50:
        face = "right"

    return mouth,face