import pickle
import cv2
import numpy as np


vagas = []
with open('vagas.pkl', 'rb') as arquivo:
    vagas = pickle.load(arquivo)

video = cv2.VideoCapture('video.mp4')

while True:
    check, img = video.read()
    imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25,16)
    imgMedian = cv2.medianBlur(imgTh, 5)
    kernel = np.ones((3,3),np.int8)
    imgDil = cv2.dilate(imgMedian,kernel)

    vagasAbertas = 0
    for x,y,w,h in vagas:

        vaga = imgDil[y:y+h, x:x+w]
        count = cv2.countNonZero(vaga)
        cv2.putText(img, str(count),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        if count < 900:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            vagasAbertas += 1
        else:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cv2.rectangle(img, (90, 0), (415, 60), (0, 255, 0), -1)
        cv2.putText(img, f'Livre:{vagasAbertas}/69', (95, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 5)




    cv2.imshow('video', img)
    #cv2.imshow('video TH', imgDil)

    cv2.waitKey(10)