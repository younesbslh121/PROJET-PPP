import cv2
import numpy as np

def region_of_interest(img, vertices):
    """Appliquer un masque pour se concentrer sur la zone d'intérêt."""
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img, lines):
    """Dessiner les lignes détectées sur l'image."""
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 10)

def detect_lane_change():
    cap = cv2.VideoCapture(0)  # Ouvre la caméra (ou utilisez une vidéo de test)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Redimensionner pour un traitement plus rapide
        frame = cv2.resize(frame, (640, 480))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir en niveaux de gris
        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # Appliquer un flou pour réduire le bruit
        edges = cv2.Canny(blur, 50, 150)  # Détecter les bords

        # Définir la région d'intérêt (triangle au bas de l'image)
        height, width = edges.shape
        roi_vertices = [
            (0, height),
            (width / 2, height / 2),
            (width, height)
        ]
        roi = region_of_interest(edges, np.array([roi_vertices], np.int32))

        # Détecter les lignes avec la transformée de Hough
        lines = cv2.HoughLinesP(
            roi, 
            rho=1, 
            theta=np.pi/180, 
            threshold=50, 
            minLineLength=50, 
            maxLineGap=200
        )

        # Dessiner les lignes détectées sur l'image d'origine
        if lines is not None:
            draw_lines(frame, lines)

        # Détecter un changement de trajectoire
        # (par exemple, si les lignes disparaissent ou se déplacent soudainement)
        if lines is None:
            cv2.putText(
                frame, 
                "Attention! Changement de voie involontaire!", 
                (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 0, 255), 
                2
            )

        # Afficher l'image avec les lignes
        cv2.imshow("Detection de Changement de Voie", frame)

        # Quitter si 'q' est pressé
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_lane_change()
