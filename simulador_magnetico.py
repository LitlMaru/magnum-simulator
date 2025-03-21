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
mostrarMedidorEstatico = False
pantalla = pygame.display.set_mode((ancho, alto))
fuente = pygame.font.Font(None, 20)
fuenteTextbox = pygame.font.Font("Fuentes/FutuHv.ttf", 18)
pygame.display.set_caption("Simulación de Campo Magnético")

medidor_img = pygame.image.load("Imagenes/medidorEstatico.png").convert_alpha()
medidor_img = pygame.transform.scale(medidor_img, (138, 195))
medidor_rect = medidor_img.get_rect()


textboxFuerza_imagen = pygame.image.load("Imagenes/textboxFuerza.png")
textboxFuerza_imagen = pygame.transform.scale(textboxFuerza_imagen, (textboxFuerza_imagen.get_width()/1.5, textboxFuerza_imagen.get_height()/1.5))
textboxFuerza__rect = textboxFuerza_imagen.get_rect(topleft=(840, 220))

input_box = pygame.Rect(100, 100, 140, 30)
fuerza = "" 
textboxActivo = False
input_box = pygame.Rect(860, 245, 140, 30)


def dibujar_texto_medidor(texto, salto):
    rect_texto = texto.get_rect(topleft = (mx - 40, my + salto))
    pantalla.blit(texto, rect_texto)

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
                B = k * polaridad * iman.fuerza / r**2 * 20
                theta = np.arctan2(dy, dx)
                Bx += B * np.cos(theta)
                By += B * np.sin(theta)
    return Bx, By

# Función para dibujar líneas de campo
def dibujar_campo(imanes):
    for x in range(0, ancho, 50):
        for y in range(0, alto, 50):
            Bx, By = campo_magnetico(x, y, imanes)
            if Bx or By:
                magnitud = np.hypot(Bx, By)
                Bx, By = (Bx / magnitud) * 10, (By / magnitud) * 10
                #pygame.draw.line(pantalla, WHITE, (x, y), (x + Bx, y + By), 1)
                #pygame.draw.circle(pantalla, WHITE, (int(x + Bx), int(y + By)), 2)
                dibujar_imagen(pantalla, "Imagenes/vectorMagnetico.png", (x, y), 0.4, 0.4,  180 + math.degrees(math.atan2(Bx, By)), min(abs(magnitud * 500), 255))

# Lista de imanes y brújula
imanes = [Iman(ancho// 2, alto // 2, 1)]
brujula = Brujula(ancho * 1 // 3, alto * 1 // 3)
iman_seleccionado = None
brujula_seleccionada = None

boton_iman = Boton(820, 300, "Imagenes/AgregarIman.png", "Imagenes/AgregarImanHover.png", None, None, 0.7)
boton_brujula = Boton(820, 70, "Imagenes/checkboxBrujulaVerde.png", "Imagenes/checkboxBrujulaVerde.png", "Imagenes/checkboxBrujula.png", "Imagenes/checkboxBrujula.png", 0.7)
boton_medidor_estatico = Boton(820, 150, "Imagenes/checkboxMedidorEstatico.png", "Imagenes/checkboxMedidorEstatico.png", "Imagenes/checkboxMedidorEstaticoVerde.png", "Imagenes/checkboxMedidorEstaticoVerde.png", 0.7)
# Bucle principal
ejecutando = True
reloj = pygame.time.Clock()  # Para controlar la velocidad de actualización
while ejecutando:
    dt = reloj.tick(60) / 1000  # Delta time en segundos
    pantalla.fill(BLACK)
    dibujar_campo(imanes)
    pantalla.blit(textboxFuerza_imagen, textboxFuerza__rect)

    mx, my = pygame.mouse.get_pos()
    medidor_rect.topleft = (mx - 69, my - 18)

    mBx, mBy = campo_magnetico(mx, my, imanes)
    mB = math.hypot(mBx, mBy)
    mAngulo = math.atan2(mBx, mBy)

    texto_B = fuente.render(f"B: {mB:.2f} G", True, (255, 255, 255))
    texto_Bx = fuente.render(f"Bx: {mBx:.2f} G", True, (255, 255, 255))
    texto_By = fuente.render(f"By: {mBy:.2f} G", True, (255, 255, 255))
    texto_θ = fuente.render(f"\u03b8: {mAngulo:.2f}°", True, (255, 255, 255))
    
    
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
                elif event.unicode.isdigit() or (event.unicode == '.' and '.' not in fuerza):
                    fuerza += event.unicode
        
        if boton_brujula.controlar_eventos(event):
            mostrarBrujula = not mostrarBrujula

        if boton_medidor_estatico.controlar_eventos(event):
            mostrarMedidorEstatico = not mostrarMedidorEstatico

        if boton_iman.controlar_eventos(event):
            imanes.append(Iman(config.ANCHO//2, config.ALTO //2, float(fuerza)))
            fuerza = ""
    
    if iman_seleccionado:
        iman_seleccionado.x, iman_seleccionado.y = pygame.mouse.get_pos()
    if brujula_seleccionada:
        brujula.x, brujula.y = pygame.mouse.get_pos()
    
    pantalla.blit(textboxFuerza_imagen, textboxFuerza__rect)

    superficieTexto = fuenteTextbox.render(fuerza, True, (0,0,0))
    pantalla.blit(superficieTexto, (input_box.x + 5, input_box.y + 5))

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

    if mostrarMedidorEstatico:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)
    boton_brujula.dibujar(pantalla)
    boton_medidor_estatico.dibujar(pantalla)
    boton_iman.dibujar(pantalla)
    
    if mostrarMedidorEstatico:
        pantalla.blit(medidor_img, medidor_rect)
        dibujar_texto_medidor(texto_B, 80)
        dibujar_texto_medidor(texto_Bx, 100)
        dibujar_texto_medidor(texto_By, 120)
        dibujar_texto_medidor(texto_θ, 140)
        
    
    pygame.display.flip()

pygame.quit()