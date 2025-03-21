import pygame
from pygame.locals import *
import config
import ctypes
import Simulador_Electrico
import Simulador_Magnetico
import pygetwindow as gw    
from Boton import Boton

# Inicialización de Pygame y la pantalla
pygame.init()
ancho, alto = config.ANCHO, config.ALTO
pantalla = pygame.display.set_mode((ancho, alto), pygame.NOFRAME)
pygame.display.set_caption("MAGNUM")

hwnd = ctypes.windll.user32.GetForegroundWindow()

# Cargar la imagen de fondo y ajustarla al tamaño de la ventana
fondo_menu_img = pygame.image.load("imagenes/fondoMenu.png")
barra_img = pygame.image.load("Imagenes/barraTitulo.png")
barra_img = pygame.transform.scale(barra_img, (ancho, 59))
fondo_menu_img = pygame.transform.scale(fondo_menu_img, (ancho, alto - 59))

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)

dragging = False
offset_x, offset_y = 0,0

# Funciones para los botones
def campo_electrico():
    print("Información sobre el campo eléctrico")

def campo_magnetico():
    print("Información sobre el campo magnético")

def informaciones():
    print("Más información sobre el programa")
    
boton_menu = pygame.Rect(40,0, 160, 89)
boton_cerrar = Boton(config.ANCHO - 59, 0, "Imagenes/cerrar.png", "Imagenes/cerrarHover.png", "Imagenes/cerrar.png", "Imagenes/cerrarHover.png", 2/3)
boton_minimizar = Boton(config.ANCHO - 118, 0, "Imagenes/minimizar.png", "Imagenes/minimizarHover.png", "Imagenes/minimizar.png", "Imagenes/minimizarHover.png", 2/3)
boton_campo_electrico = Boton(600, 180, "Imagenes/campoElectricoBoton.png", "Imagenes/campoElectricoBotonHover.png", "Imagenes/campoElectricoBoton.png", "Imagenes/campoElectricoBotonHover.png", 0.6)
boton_campo_magnetico = Boton(600, 300, "Imagenes/campoMagneticoBoton.png", "Imagenes/campoMagneticoBotonHover.png", "Imagenes/campoMagneticoBoton.png", "Imagenes/campoMagneticoBotonHover.png", 0.6)
# Ciclo principal de eventos
def main():
    ejecutando = True
    while ejecutando:
        # Dibujar el fondo escalado
        pantalla.blit(fondo_menu_img, (0, 59))
        pantalla.blit(barra_img, (0,0))
        # Actualizar la pantalla

        # Comprobar eventos
        for event in pygame.event.get():
            if event.type == QUIT:
                ejecutando = False

            if boton_cerrar.controlar_eventos(event):
                ejecutando = False
            if boton_minimizar.controlar_eventos(event):
                ventana = gw.getActiveWindow()
                ventana.minimize()
            if boton_campo_electrico.controlar_eventos(event):
                Simulador_Electrico.main()
            if boton_campo_magnetico.controlar_eventos(event):
                Simulador_Magnetico.main()
            elif event.type == MOUSEBUTTONDOWN: 
                if boton_menu.collidepoint(event.pos): 
                    pass
                elif event.pos[1] < 59:
                    dragging = True
                    offset_x, offset_y = event.pos
                    ctypes.windll.user32.ReleaseCapture()
                    ctypes.windll.user32.SendMessageW(hwnd, 0xA1, 2, 0)  # Move window

            elif event.type == MOUSEBUTTONUP:
                dragging = True   

        boton_cerrar.dibujar(pantalla)
        boton_minimizar.dibujar(pantalla)
        boton_campo_electrico.dibujar(pantalla)
        boton_campo_magnetico.dibujar(pantalla)

        pygame.display.update()

    # Salir de Pygame
    pygame.quit()

if __name__ == "__main__":
    main()