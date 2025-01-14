import cv2
import time
import numpy as np
from scipy.spatial import distance as dist

def eye_aspect_ratio(eye):
    """Calculer le Eye Aspect Ratio (EAR) pour détecter les yeux fermés."""
    A = dist.euclidean(eye[1], eye[5])  # Distance verticale
    B = dist.euclidean(eye[2], eye[4])  # Distance verticale
    C = dist.euclidean(eye[0], eye[3])  # Distance horizontale
    ear = (A + B) / (2.0 * C)
    return ear

# Constantes pour détecter la somnolence
EAR_THRESHOLD = 0.25  # Seuil pour détecter les yeux fermés
CONSEC_FRAMES = 15    # Nombre de frames consécutifs pour déclencher l'alerte

# Initialisation des compteurs
frame_counter = 0

# Charger le modèle pré-entraîné pour la détection faciale
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def detect_drowsiness():
    global frame_counter
    cap = cv2.VideoCapture(0)  # Capture depuis la webcam

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)  # Détecter les visages

        for (x, y, w, h) in faces:
            # Dessiner un rectangle autour du visage
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Extraire la région du visage
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

            # Détecter les yeux
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            # Vérification de l'état des yeux
            if len(eyes) < 2:  # Si les deux yeux ne sont pas détectés
                frame_counter += 1
            else:
                frame_counter = 0  # Réinitialiser si les yeux sont ouverts

            # Déclencher une alerte si les yeux restent fermés
            if frame_counter >= CONSEC_FRAMES:
                cv2.putText(frame, "SOMNOLENCE DETECTEE!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Afficher la vidéo en temps réel
        cv2.imshow("Detection de Somnolence", frame)

        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_drowsiness()
