### JUEGO DE EXPLORADOR PARA ESQUIVAR OBSTACULOS (MONTAÑAS) ##
### USANDO LA LIBRERIA PYGAME ##
import pygame
import random
import sys

##### aca se define el tamaño de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colores de pantalla 
GREEN = (57, 148, 1)
WHITE = (255, 255, 255)

# esta funcion para mostrar el cuadro de dialogo
def show_message_box(screen, message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    dialog_rect = pygame.Rect(0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    dialog_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.draw.rect(screen, GREEN, dialog_rect)
    pygame.draw.rect(screen, WHITE, dialog_rect, 2)
    screen.blit(text, text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# esta funcion es para mostrar el menu de seleccion de jugadores
def show_menu(screen):
    screen.fill(GREEN)
    font = pygame.font.Font(None, 36)

    # opciones de menu cuando inicia el codigo #########
    one_player_text = font.render("1 jugador", True, WHITE)
    one_player_rect = one_player_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    two_players_text = font.render("2 jugadores", True, WHITE)
    two_players_rect = two_players_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(one_player_text, one_player_rect)
    screen.blit(two_players_text, two_players_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if one_player_rect.collidepoint(x, y):
                    return 1
                elif two_players_rect.collidepoint(x, y):
                    return 2

# clase para el jugador #
class Player(pygame.sprite.Sprite):
    def __init__(self, player_num):
        super().__init__()
        self.image = pygame.image.load("explorador.png").convert_alpha()  # cargar imagen del jugador desde donde esta el codigo 
        self.image = pygame.transform.scale(self.image, (50, 50))  # ajustar tamaño de la imagen del jugador
        self.rect = self.image.get_rect()
        if player_num == 1:
            self.rect.x = 100
            self.control_keys = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
        elif player_num == 2:
            self.rect.x = 200
            self.control_keys = {pygame.K_a: False, pygame.K_d: False, pygame.K_w: False, pygame.K_s: False}
        self.rect.y = SCREEN_HEIGHT - 100
        self.speed = 8

    def update(self):
        for key in self.control_keys:
            if self.control_keys[key]:
                if key == pygame.K_LEFT or key == pygame.K_a:
                    self.rect.x -= self.speed
                elif key == pygame.K_RIGHT or key == pygame.K_d:
                    self.rect.x += self.speed
                elif key == pygame.K_UP or key == pygame.K_w:
                    self.rect.y -= self.speed
                elif key == pygame.K_DOWN or key == pygame.K_s:
                    self.rect.y += self.speed

# Clase para los obstáculos (montañas) ###
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("montaña.png").convert_alpha()  # Cargar imagen de montaña
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajustar tamaño de la montaña
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = -self.rect.height

# esta es la funcion main del juego ##
def main_game_loop():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Plataforma PyGame")

    clock = pygame.time.Clock()

    # con esto se puede visualizar el menu #
    num_players = show_menu(screen)

    # se crean jugadores segun la seleccion que esta en la lista ###
    players = []
    for i in range(num_players):
        player = Player(i + 1)
        players.append(player)

    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(players)

    running = True
    player_lost = False  # bandera para controlar si alguno de los jugadores perdio ######

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for player in players:
                    for key in player.control_keys:
                        if event.key == key:
                            player.control_keys[key] = True
            elif event.type == pygame.KEYUP:
                for player in players:
                    for key in player.control_keys:
                        if event.key == key:
                            player.control_keys[key] = False

        screen.fill((57, 148, 1))

        # se crean de forma aleatoria los obtaculos o montañas en el juego ###
        if random.randint(0, 100) < 5:
            obstacle = Obstacle()
            obstacles.add(obstacle)
            all_sprites.add(obstacle)

        # se validan colisiones entre jugadores y montañas ###
        for player in players:
            collisions = pygame.sprite.spritecollide(player, obstacles, False)
            if collisions:
                player_lost = True

        ### actualizan y dibujan los obstaculos que tienen movimiento ###
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        ### aca se valida si debe salir del bucle ###
        if player_lost:
            show_message_box(screen, "¡Perdiste! Da click para salir")
            running = False  

    pygame.quit()

if __name__ == "__main__":
    main_game_loop()
