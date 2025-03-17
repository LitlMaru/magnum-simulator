import pygame
import numpy as np
import math
from Boton import Boton
from Utilidades import dibujar_imagen
import config

# Configuración de la pantalla
ancho, alto = config.ANCHO, config.ALTO
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()
mostrarBrujula= True
mostratMedidorEstatico = False
pantalla = pygame.display.set_mode((ancho, alto))
fuente = pygame.font.Font(None, 28)
pygame.display.set_caption("Simulación de Campo Magnético")

textboxFuerza_imagen = pygame.image.load("Imagenes/textboxFuerza.png")
textboxFuerza__rect = textboxFuerza_imagen.get_rect(topleft=(800, 400))

fuerza = "" 
textboxActivo = False


# Clase para representar un imán con dos polos
class Iman:
    def __init__(self, x, y, fuerza):
        self.x = x
        self.y = y
        self.fuerza = fuerza
        self.ancho = 180    
        self.alto = 39

    def polos(self):
        return (self.x - self.ancho // 4, self.y), (self.x + self.ancho // 4, self.y)

# Clase para representar una brújula
class Brujula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0  # Ángulo actual de la brújula
        self.angulo_objetivo = 0  # Ángulo al que la brújula debe apuntar
        self.velocidad_ajuste = 0.05  # Velocidad de ajuste 

    def actualizar(self, Bx, By):
        self.angulo_objetivo = np.arctan2(By, Bx)
        diferencia_angular = self.angulo_objetivo - self.angulo
        if diferencia_angular > np.pi:
            diferencia_angular -= 2 * np.pi
        elif diferencia_angular < -np.pi:
            diferencia_angular += 2 * np.pi
        self.angulo += diferencia_angular * self.velocidad_ajuste

# Función para calcular el campo magnético en un punto
def campo_magnetico(x, y, imanes):
    Bx, By = 0, 0
    k = 1e3  # Constante simplificada
    for iman in imanes:
        (xN, yN), (xS, yS) = iman.polos()
        for polo_x, polo_y, polaridad in [(xN, yN, 1), (xS, yS, -1)]:
            dx = polo_x - x
            dy = polo_y - y
            r = np.hypot(dx, dy)
            if r > 1:
                B = k * polaridad * iman.fuerza / r**2
                theta = np.arctan2(dy, dx)
                Bx += B * np.cos(theta)
                By += B * np.sin(theta)
    return Bx, By

# Función para dibujar líneas de campo
def dibujar_campo(imanes):
    for x in range(0, ancho, 30):
        for y in range(0, alto, 30):
            Bx, By = campo_magnetico(x, y, imanes)
            if Bx or By:
                magnitud = np.hypot(Bx, By)
                Bx, By = (Bx / magnitud) * 10, (By / magnitud) * 10
                pygame.draw.line(pantalla, WHITE, (x, y), (x + Bx, y + By), 1)
                pygame.draw.circle(pantalla, WHITE, (int(x + Bx), int(y + By)), 2)

# Lista de imanes y brújula
imanes = [Iman(ancho// 2, alto // 2, 1)]
brujula = Brujula(ancho * 1 // 3, alto * 1 // 3)
iman_seleccionado = None
brujula_seleccionada = None

boton_brujula = Boton(800, 100, "Imagenes/checkboxBrujula.png", "Imagenes/checkboxBrujula.png", "Imagenes/checkboxBrujulaVerde.png", "Imagenes/checkboxBrujulaVerde.png", 0.7)
boton_medidor_estatico = Boton(800, 180, "Imagenes/checkboxMedidorEstatico.png", "Imagenes/checkboxMedidorEstatico.png", "Imagenes/checkboxMedidorEstaticoVerde.png", "Imagenes/checkboxMedidorEstaticoVerde.png", 0.7)
# Bucle principal
ejecutando = True
reloj = pygame.time.Clock()  # Para controlar la velocidad de actualización
while ejecutando:
    dt = reloj.tick(60) / 1000  # Delta time en segundos
    pantalla.fill(BLACK)
    dibujar_campo(imanes)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for iman in imanes:
                if abs(mx - iman.x) < iman.ancho // 2 and abs(my - iman.y) < iman.alto // 2:
                    iman_seleccionado = iman
            if np.hypot(mx - brujula.x, my - brujula.y) < 15:
                brujula_seleccionada = brujula

            if textboxFuerza__rect.collidepoint(event.pos):
                textboxActivo = True
            else: textboxActivo = False

        elif event.type == pygame.MOUSEBUTTONUP:
            iman_seleccionado = None
            brujula_seleccionada = None

        elif event.type == pygame.KEYDOWN:
            if textboxActivo:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    fuerza = fuerza[:-1]
                elif event.key in {pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9}:
                    fuerza += event.unicode
                else: pass
        
        if boton_brujula.controlar_eventos(event):
            mostrarBrujula = not mostrarBrujula

        if boton_medidor_estatico.controlar_eventos(event):
            mostratMedidorEstatico = not mostratMedidorEstatico
    
    if iman_seleccionado:
        iman_seleccionado.x, iman_seleccionado.y = pygame.mouse.get_pos()
    if brujula_seleccionada:
        brujula.x, brujula.y = pygame.mouse.get_pos()
    
    pantalla.blit(textboxFuerza_imagen, textboxFuerza__rect.topleft)

    superficieTexto = fuente.render(fuerza, True, WHITE)

    if textboxActivo:
        cursor_rect = pygame.Rect(textboxFuerza__rect.topright, (2, textboxFuerza__rect.height))
        pygame.draw.rect(pantalla, BLACK, cursor_rect)
    # Calcular el campo magnético en la posición de la brújula
    Bx, By = campo_magnetico(brujula.x, brujula.y, imanes)
    # Actualizar la brújula para que se ajuste gradualmente
    brujula.actualizar(Bx, By)
    
    # Dibujar los imanes
    for iman in imanes:
        dibujar_imagen(pantalla, "Imagenes/iman.png", (iman.x, iman.y), 0.45, 0.45)
    
    # Dibujar la brújula
    if mostrarBrujula:
        dibujar_imagen(pantalla, "Imagenes/aroBrujula.png", (brujula.x, brujula.y), 0.4, 0.4)
        dibujar_imagen(pantalla, "Imagenes/agujaBrujula.png", (brujula.x, brujula.y), 0.45, 0.45, -math.degrees(brujula.angulo)) 

    boton_brujula.dibujar(pantalla)
    boton_medidor_estatico.dibujar(pantalla)
    
    pygame.display.flip()

pygame.quit()