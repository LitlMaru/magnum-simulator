import pygame
import math
from Boton import Boton
from Carga import Carga
import config


# Inicialización de pygame
pygame.init()
pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
reloj = pygame.time.Clock()

cargas = []
carga_seleccionada = None

def campo_electrico(x, y, cargas):
    ex, ey = 0, 0
    for carga in cargas:
        dx = carga.x - x
        dy = carga.y - y
        r2 = dx**2 + dy**2
        if r2 == 0:
            continue
        r = math.sqrt(r2)
        magnitud_e = config.K * carga.q / r2
        ex += magnitud_e * dx / r
        ey += magnitud_e * dy / r
    return (ex, ey)

def dibujar_campo():
    for x in range(0, config.ANCHO, config.SEPARACION_PUNTOS):
        for y in range(0, config.ALTO, config.SEPARACION_PUNTOS):
            ex, ey = 0, 0
            for carga in cargas:
                dx, dy = x - carga.x, y - carga.y
                r2 = dx ** 2 + dy ** 2
                if r2 > 4:
                    e = config.K * carga.q / r2
                    angulo = math.atan2(dy, dx)
                    ex += e * math.cos(angulo)
                    ey += e * math.sin(angulo)
            magnitud = math.sqrt(ex ** 2 + ey ** 2)
            if magnitud > 0:
                ex, ey = ex / magnitud * 5, ey / magnitud * 5
                #dibujar_imagen(pantalla, "Imagenes/vector1.png", (x, y), 0.2, math.degrees(math.atan2(ex,ey)))
                pygame.draw.line(pantalla, config.COLOR_CAMPO, (x, y), (x + ex, y + ey), 1)

boton_dinamico = Boton(15, 15, "Imagenes/estaticoBoton.png", "Imagenes/estaticoBotonHover.png", "Imagenes/dinamicoBoton.png", "Imagenes/dinamicoBotonHover.png", 0.6)
boton_animar = Boton(15, 55, "Imagenes/iniciarAnimacionBoton.png", "Imagenes/iniciarAnimacionHover.png", "Imagenes/detenerAnimacionBoton.png", "Imagenes/detenerAnimacionHover.png", 0.6)
boton_resetear = Boton(15, 95, "Imagenes/resetearBoton.png", "Imagenes/resetearBotonHover.png", None, None, 0.6) 
boton_positivo = Boton(720, 15, "Imagenes/cargaPositivaBoton.png", "Imagenes/cargaPositivaBotonHover.png", None, None, 0.5)
boton_negativo = Boton(720, 75, "Imagenes/cargaNegativaBoton.png", "Imagenes/cargaNegativaBotonHover.png", None, None, 0.5)

ejecutando = True
while ejecutando:
    pantalla.fill(config.COLOR_FONDO)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not boton_animar.activo:
            mx, my = pygame.mouse.get_pos()
            for carga in cargas:
                if math.hypot(mx - carga.x, my - carga.y) < config.RADIO_CARGA:
                    carga_seleccionada = carga
                    print(carga_seleccionada)
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            carga_seleccionada = None
        elif event.type == pygame.MOUSEMOTION and carga_seleccionada and not boton_animar.activo:
            carga_seleccionada.x, carga_seleccionada.y = pygame.mouse.get_pos()
        #static_button.handle_event(event)

        if boton_dinamico.controlar_eventos(event):
            config.CARGA_PRUEBA = boton_dinamico.activo
        
        if boton_animar.controlar_eventos(event):
            config.ANIMANDO = boton_animar.activo

        if boton_resetear.controlar_eventos(event):
            cargas.clear()

        if boton_positivo.controlar_eventos(event):
            if config.CARGA_PRUEBA:
                cargas.append(Carga(config.ANCHO/2, config.ALTO/2, 1, True, pantalla))
            else:
                cargas.append(Carga(config.ANCHO/2, config.ALTO/2, 1, False, pantalla))
            print(len(cargas))

        if boton_negativo.controlar_eventos(event):
            if config.CARGA_PRUEBA:
                cargas.append(Carga(config.ANCHO/2, config.ALTO/2, -1, True, pantalla))
            else:
                cargas.append(Carga(config.ANCHO/2, config.ALTO/2, -1, False, pantalla))
            print(len(cargas))

    dibujar_campo()
    for carga in cargas:
        carga.actualizar(cargas)
    
    for carga in cargas:
        carga.dibujar()
    
    boton_dinamico.dibujar(pantalla)
    boton_animar.dibujar(pantalla)
    boton_resetear.dibujar(pantalla)
    boton_positivo.dibujar(pantalla)
    boton_negativo.dibujar(pantalla)

    pygame.display.flip()
    reloj.tick(config.FPS)

pygame.quit()
