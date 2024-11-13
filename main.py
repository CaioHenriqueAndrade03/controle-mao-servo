import cv2
import mediapipe as mp
import numpy as np
import serial
import time

#Reconhece o arduino
arduino = serial.Serial('COM5', 9600)  
time.sleep(2)

#reconhece a mao
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

def enviar_comando(posicoes):
    comando = f"d1:{posicoes[0]};d2:{posicoes[1]};d3:{posicoes[2]};d4:{posicoes[3]};d5:{posicoes[4]};\n"
    arduino.write(comando.encode())

def calcular_distancia(ponto1, ponto2):
    return int(np.linalg.norm(np.array(ponto1) - np.array(ponto2)))


webcam = cv2.VideoCapture(0)

while webcam.isOpened():
    success, frame = webcam.read()
    if not success:
        print("Erro ao capturar imagem.")
        break

    #Inverte a imagem
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Processa a imagem
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            #Desenha os pontos de referência na mão
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtem as coordenadas dos pontos da palma e dos dedos
            palma = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            dedao = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            indicador = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            medio = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            anelar = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            mindinho = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # Converte para pixels e calcula distâncias
            frame_height, frame_width, _ = frame.shape
            palma_px = (int(palma.x * frame_width), int(palma.y * frame_height))
            dedos_px = [
                (int(dedao.x * frame_width), int(dedao.y * frame_height)),
                (int(indicador.x * frame_width), int(indicador.y * frame_height)),
                (int(medio.x * frame_width), int(medio.y * frame_height)),
                (int(anelar.x * frame_width), int(anelar.y * frame_height)),
                (int(mindinho.x * frame_width), int(mindinho.y * frame_height))
            ]
            posicoes_dedos = [calcular_distancia(palma_px, dedo_px) for dedo_px in dedos_px]

            #Trava os valores de 0 a 180 pro arduino
            posicoes_dedos = [min(180, max(0, int(d * 180 / 200))) for d in posicoes_dedos]

            enviar_comando(posicoes_dedos)

    #Aparece a imagem
    cv2.imshow("Controle de Servo com Visão Computacional", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
arduino.close()
