import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de l'écran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Tir Spatial")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Vaisseau spatial
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40
spaceship = pygame.image.load(r"c:\Users\pc\Downloads\vaisseau-spatial-vaisseau-spatial-colore-arriere-plan_808092-4636.jpg")  # Remplacez par une image de vaisseau (50x40 px)
spaceship = pygame.transform.scale(spaceship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Astéroïdes
ASTEROID_WIDTH, ASTEROID_HEIGHT = 50, 50
asteroid_image = pygame.image.load(r"c:\Users\pc\Downloads\qu-est-ce-qu-un-asteroide.jpg")  # Remplacez par une image d'astéroïde (50x50 px)
asteroid_image = pygame.transform.scale(asteroid_image, (ASTEROID_WIDTH, ASTEROID_HEIGHT))

# Projectile
BULLET_WIDTH, BULLET_HEIGHT = 10, 20

# Sons
shoot_sound = pygame.mixer.Sound(r"c:\\Users\pc\\Downloads\\laser-shot-ingame-230500.mp3")  # Remplacez par un fichier son laser
explosion_sound = pygame.mixer.Sound(r"c:\\Users\\pc\\Downloads\\large-underwater-explosion-190270.mp3")  # Remplacez par un fichier son explosion

# FPS
FPS = 60
clock = pygame.time.Clock()

# Classes du jeu
class Spaceship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = 5
        self.lives = 3
        self.score = 0

    def draw(self):
        screen.blit(spaceship, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + SPACESHIP_WIDTH + self.speed < WIDTH:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y - self.speed > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y + SPACESHIP_HEIGHT + self.speed < HEIGHT:
            self.y += self.speed


class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH - ASTEROID_WIDTH)
        self.y = random.randint(-100, -ASTEROID_HEIGHT)
        self.speed = random.randint(3, 6)

    def move(self):
        self.y += self.speed

    def draw(self):
        screen.blit(asteroid_image, (self.x, self.y))


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT))


# Fonction principale
def main():
    run = True
    spaceship_obj = Spaceship()
    asteroids = [Asteroid() for _ in range(5)]
    bullets = []

    while run:
        clock.tick(FPS)
        screen.fill(BLACK)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Mouvement du vaisseau
        keys = pygame.key.get_pressed()
        spaceship_obj.move(keys)

        # Tirs
        if keys[pygame.K_SPACE]:
            if len(bullets) < 10:  # Limite de tirs à l'écran
                bullets.append(Bullet(spaceship_obj.x + SPACESHIP_WIDTH // 2 - BULLET_WIDTH // 2, spaceship_obj.y))
                shoot_sound.play()

        # Dessiner le vaisseau
        spaceship_obj.draw()

        # Gestion des astéroïdes
        for asteroid in asteroids:
            asteroid.move()
            asteroid.draw()
            # Collision entre le vaisseau et un astéroïde
            if (
                spaceship_obj.x < asteroid.x + ASTEROID_WIDTH
                and spaceship_obj.x + SPACESHIP_WIDTH > asteroid.x
                and spaceship_obj.y < asteroid.y + ASTEROID_HEIGHT
                and spaceship_obj.y + SPACESHIP_HEIGHT > asteroid.y
            ):
                explosion_sound.play()
                spaceship_obj.lives -= 1
                asteroids.remove(asteroid)
                asteroids.append(Asteroid())

            # Réinitialiser l'astéroïde s'il sort de l'écran
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
                asteroids.append(Asteroid())

        # Gestion des tirs
        for bullet in bullets:
            bullet.move()
            bullet.draw()

            # Collision entre un tir et un astéroïde
            for asteroid in asteroids:
                if (
                    bullet.x < asteroid.x + ASTEROID_WIDTH
                    and bullet.x + BULLET_WIDTH > asteroid.x
                    and bullet.y < asteroid.y + ASTEROID_HEIGHT
                    and bullet.y + BULLET_HEIGHT > asteroid.y
                ):
                    explosion_sound.play()
                    spaceship_obj.score += 10
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    asteroids.append(Asteroid())
                    break

            # Supprimer les tirs hors écran
            if bullet.y < 0:
                bullets.remove(bullet)

        # Afficher le score et les vies
        font = pygame.font.SysFont("comicsans", 30)
        lives_text = font.render(f"Lives: {spaceship_obj.lives}", True, WHITE)
        score_text = font.render(f"Score: {spaceship_obj.score}", True, WHITE)
        screen.blit(lives_text, (10, 10))
        screen.blit(score_text, (WIDTH - 150, 10))

        # Vérifier si le joueur a perdu
        if spaceship_obj.lives <= 0:
            game_over_font = pygame.font.SysFont("comicsans", 50)
            game_over_text = game_over_font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            pygame.display.update()
            pygame.time.wait(3000)
            run = False

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
