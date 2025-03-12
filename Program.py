import pygame
from pygame.locals import *

# Inicialización de Pygame y la pantalla
pygame.init()
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("MAGNUM")

# Cargar la imagen de fondo y ajustarla al tamaño de la ventana
fondo_menu_img = pygame.image.load("imagenes/fondoMenu.png")
fondo_menu_img = pygame.transform.scale(fondo_menu_img, (screen_width, screen_height))

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

# Funciones para los botones
def campo_electrico():
    print("Información sobre el campo eléctrico")

def campo_magnetico():
    print("Información sobre el campo magnético")

def informaciones():
    print("Más información sobre el programa")

# Crear un botón sencillo
def dibujar_boton(texto, pos_x, pos_y):
    font = pygame.font.SysFont(None, 36)
    button_surface = font.render(texto, True, BLANCO)
    button_rect = button_surface.get_rect(center=(pos_x, pos_y))
    pygame.draw.rect(screen, AZUL, button_rect.inflate(20, 10))  # Rectángulo con margen
    screen.blit(button_surface, button_rect)
    return button_rect

# Ciclo principal de eventos
running = True
while running:
    # Dibujar el fondo escalado
    screen.blit(fondo_menu_img, (0, 0))

    # Mostrar los botones
    rect_campo_electrico = dibujar_boton("Campo eléctrico", 450, 150)
    rect_campo_magnetico = dibujar_boton("Campo magnético", 450, 200)
    rect_informaciones = dibujar_boton("Informaciones", 450, 250)

    # Actualizar la pantalla
    pygame.display.update()

    # Comprobar eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if rect_campo_electrico.collidepoint(event.pos):
                campo_electrico()
            elif rect_campo_magnetico.collidepoint(event.pos):
                campo_magnetico()
            elif rect_informaciones.collidepoint(event.pos):
                informaciones()

# Salir de Pygame
pygame.quit()
