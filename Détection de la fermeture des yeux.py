import cv2
import pygame

# Initialiser pygame pour jouer du son
pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\pc\OneDrive\Bureau\sos\divers\Balti - Ya Hasra (Official Music Video).mp3")  # Assurez-vous que le chemin est correct

# Charger les classifieurs en cascade pour le visage et les yeux
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

# Initialiser la caméra
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir en niveaux de gris pour la détection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détecter les visages
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    for (x, y, w, h) in faces:
        # Dessiner un rectangle autour du visage
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Détecter les yeux dans la région du visage
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) == 0:  # Si aucun œil n'est détecté
            print("Yeux fermés !")
            if not pygame.mixer.music.get_busy():  # Jouer la sonnerie si elle n'est pas déjà en cours
                pygame.mixer.music.play()
        else:
            print("Yeux ouverts")
            pygame.mixer.music.stop()  # Arrêter la sonnerie si les yeux sont ouverts

    # Afficher la vidéo
    cv2.imshow("Camera", frame)

    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
