import cv2
import numpy as np
from time import sleep

# Paramètres de détection
largura_min = 80
altura_min = 80
offset = 6
pos_linha = 550  # Ligne de comptage
delay = 60  # FPS de la vidéo

detec = []  # Liste pour stocker les centres des véhicules détectés
carros = 0  # Compteur de véhicules

def pega_centro(x, y, w, h):
    """
    Calculer le centre d'un rectangle
    """
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# Ouvrir la vidéo
cap = cv2.VideoCapture(r'c:\\Users\\pc\\Downloads\\video.mp4')

# Utiliser un soustracteur de fond pour détecter les objets en mouvement
subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame1 = cap.read()
    
    if not ret:
        break  # Si la vidéo est terminée, sortir de la boucle

    tempo = float(1/delay)  
    sleep(tempo)  # Ajuster la vitesse de lecture de la vidéo en fonction du FPS

    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # Convertir en niveaux de gris
    blur = cv2.GaussianBlur(grey, (3, 3), 5)  # Appliquer un flou pour réduire le bruit
    img_sub = subtracao.apply(blur)  # Appliquer la soustraction de fond
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))  # Dilater les zones détectées
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # Structure pour la morphologie

    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)  # Fermer les petites ouvertures dans les objets

    # Trouver les contours dans l'image traitée
    contorno, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Tracer une ligne pour compter les véhicules
    cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (176, 130, 39), 2)

    for(i, c) in enumerate(contorno):
        (x, y, w, h) = cv2.boundingRect(c)  # Obtenir le rectangle autour du contour

        # Valider la taille des objets (pour éviter les objets trop petits)
        if not (w >= largura_min and h >= altura_min):
            continue

        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Dessiner le rectangle autour du véhicule
        centro = pega_centro(x, y, w, h)  # Calculer le centre du rectangle
        detec.append(centro)  # Ajouter le centre à la liste des détections
        cv2.circle(frame1, centro, 4, (0, 0, 255), -1)  # Marquer le centre avec un cercle rouge

        # Compter les véhicules qui passent la ligne
        for (x, y) in detec:
            if (y < (pos_linha + offset)) and (y > (pos_linha - offset)):
                carros += 1
                cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)  # Changer la couleur de la ligne
                detec.remove((x, y))  # Retirer le véhicule de la liste des détections
                print("No. of cars detected : " + str(carros))

    # Afficher le nombre de véhicules détectés
    cv2.putText(frame1, "VEHICLE COUNT : " + str(carros), (320, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 4)

    # Afficher l'image avec la détection de véhicules
    cv2.imshow("Video Original", frame1)
    cv2.imshow("Detecting", dilatada)

    # Quitter si la touche 'Esc' est pressée
    if cv2.waitKey(1) == 27:
        break

# Libérer la vidéo et fermer toutes les fenêtres
cv2.destroyAllWindows()
cap.release()
