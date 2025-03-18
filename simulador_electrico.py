import pygame
import numpy as np
import math
from Boton import Boton
from Carga import Carga
import config
from Utilidades import make_surface_rgba, dibujar_imagen

pygame.init()
pantalla = pygame.display.set_mode((config.ANCHO, config.ALTO))
reloj = pygame.time.Clock()
fuente = pygame.font.Font(None, 25)

#Imagen para el indicador de potencial
meter_img = pygame.image.load("Imagenes/medidorPotencial.png").convert_alpha()
meter_img = pygame.transform.scale(meter_img, (128, 132))
meter_rect = meter_img.get_rect()

cargas = []
carga_seleccionada = None
carga_a_eliminar = None
mostrar_potencial = False
mostrar_voltaje = False

id_carga = 0

#Dibujar el indicador de potencial
def dibujar_potencial(texto_potencial):

    pantalla.blit(meter_img, meter_rect)
    rect_texto = texto_potencial.get_rect(center = (mx, my + 85))
    pantalla.blit(texto_potencial, rect_texto)


def potencial_en(cargas, x, y):
    V = 0
    for carga in cargas:
        r = (x - carga.x)**2 + (y - carga.y)**2
        if r > 0:
            V += config.K * carga.q / (np.sqrt(r) * 10**7 *5)
    return V
    
def calcular_campo_potencial(cargas, ancho, alto):
    x = np.arange(ancho)
    y = np.arange(alto)
    xx, yy = np.meshgrid(x, y)

    V = np.zeros((alto, ancho), dtype=float)

    for carga in cargas:
        x_q, y_q, q = carga.x, carga.y, carga.q
        r2 = (xx - x_q)**2 + (yy - y_q)**2
        r2[r2 == 0] = 1e-10
        V += config.K * q / (np.sqrt(r2) * 10**7 *5)

    return V

def obtener_color_potencial(potencial):
    potencial_max = 7.0
    alpha = np.clip(abs(potencial) / potencial_max, 0, 1) * 255 
    rojo = np.where(potencial > 0, 255, 0)  
    azul = np.where(potencial < 0, 255, 0) 
    verde = np.zeros_like(potencial)
    rgba = np.dstack((rojo, verde, azul, alpha)).astype(np.uint8)

    return rgba

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
                ex, ey = ex * magnitud / config.K, ey * magnitud / config.K
                factor = min(magnitud ** (3/5) / 1000, 1.4)
                dibujar_imagen(pantalla, "Imagenes/vectorSmall.png", (x, y), 0.4, 0.4*factor, 180 + math.degrees(math.atan2(ex,ey)))
                #pygame.draw.line(pantalla, config.COLOR_CAMPO, (x, y), (x + ex, y + ey), 1)

#Creacion de botones
boton_dinamico = Boton(15, 15, "Imagenes/estaticoBoton.png", "Imagenes/estaticoBotonHover.png", "Imagenes/dinamicoBoton.png", "Imagenes/dinamicoBotonHover.png", 0.6)
boton_animar = Boton(15, 55, "Imagenes/iniciarAnimacionBoton.png", "Imagenes/iniciarAnimacionHover.png", "Imagenes/detenerAnimacionBoton.png", "Imagenes/detenerAnimacionHover.png", 0.6)
boton_resetear = Boton(15, 100, "Imagenes/resetearBoton.png", "Imagenes/resetearBotonHover.png", None, None, 0.6) 
boton_positivo = Boton(900, 15, "Imagenes/cargaPositivaBoton.png", "Imagenes/cargaPositivaBotonHover.png", None, None, 0.5)
boton_negativo = Boton(900, 75, "Imagenes/cargaNegativaBoton.png", "Imagenes/cargaNegativaBotonHover.png", None, None, 0.5)
checkbox_potencial = Boton(860, 140, "Imagenes/checkboxPotencial.png", "Imagenes/checkboxPotencial.png", "Imagenes/checkboxPotencialVerde.png", "Imagenes/checkboxPotencialVerde.png", 0.6)
checkbox_voltaje = Boton(860, 190, "Imagenes/Voltaje.png", "Imagenes/Voltaje.png", "Imagenes/VoltajeVerde.png", "Imagenes/VoltajeVerde.png", 0.55)

ejecutando = True
while ejecutando:

    pantalla.fill(config.COLOR_FONDO)

    #Escribir potencial en el indicador de potencial
    mx, my = pygame.mouse.get_pos()
    meter_rect.topleft = (mx - 64, my - 22)

    V = potencial_en(cargas, mx, my)
    texto_potencial = fuente.render(f"{V:.2f} V", True, (255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False

        #Mover cargas usando el mouse
        elif event.type == pygame.MOUSEBUTTONDOWN and not boton_animar.activo:
            mx, my = pygame.mouse.get_pos()
            for carga in cargas:
                if math.hypot(mx - carga.x, my - carga.y) < config.RADIO_CARGA:
                    carga_seleccionada = carga
                    break

            if event.button == 3:
                for carga in cargas: 
                    if math.hypot(mx - carga.x, my - carga.y) < config.RADIO_CARGA:
                        cargas = [carga for carga in cargas if carga.id != carga_seleccionada.id]
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            carga_seleccionada = None
        elif event.type == pygame.MOUSEMOTION and carga_seleccionada and not boton_animar.activo:
            carga_seleccionada.x, carga_seleccionada.y = pygame.mouse.get_pos()
        
        #Manejar eventos de botones
        if boton_dinamico.controlar_eventos(event):
            config.CARGA_PRUEBA = boton_dinamico.activo
        
        if boton_animar.controlar_eventos(event):
            config.ANIMANDO = boton_animar.activo

        if boton_resetear.controlar_eventos(event):
            cargas.clear()

        if boton_positivo.controlar_eventos(event):
            id_carga+=1
            if config.CARGA_PRUEBA:
                cargas.append(Carga(config.ANCHO/2, config.ALTO/2, 1, True, pantalla))
                cargas[-1].id = id_carga
            else:
                cargas.append(Carga(config.ANCHO/2, config.ALTO/2, 1, False, pantalla))
                cargas[-1].id = id_carga

        if boton_negativo.controlar_eventos(event):
            id_carga+=1
            if config.CARGA_PRUEBA:
                cargas.append(Carga(config.ANCHO/2, config.ALTO/2, -1, True, pantalla))
                cargas[-1].id = id_carga
            else:
                cargas.append(Carga(config.ANCHO/2, config.ALTO/2, -1, False, pantalla))
                cargas[-1].id = id_carga

        if checkbox_potencial.controlar_eventos(event):
            mostrar_potencial = not mostrar_potencial

        if checkbox_voltaje.controlar_eventos(event):
            mostrar_voltaje = not mostrar_voltaje

    #Dibujar gradiente de voltaje
        
    if not config.ANIMANDO and mostrar_voltaje and len(cargas) >= 1:
        campo_potencial = calcular_campo_potencial(cargas, config.ANCHO, config.ALTO)

        campo_colores = obtener_color_potencial(campo_potencial.T)
        
        gradiente = make_surface_rgba(campo_colores)

        # Draw the surface onto the screen
        pantalla.blit(gradiente, (0, 0))

    #Cambiar mouse por indicador de potencial
    if mostrar_potencial:
        pygame.mouse.set_visible(False)
    else: pygame.mouse.set_visible(True)

    #Dibujar campo y cargas
    dibujar_campo()
    for carga in cargas:
        carga.actualizar(cargas)
    
    for carga in cargas:
        carga.dibujar()

    fps = reloj.get_fps()

    fps_text = fuente.render(f"FPS: {int(fps)}", True, (255, 255, 255))
    pantalla.blit(fuente.render(f"Cargas: {len(cargas)}", True, (255, 255, 255)), (1000, 680))
    pantalla.blit(fps_text, (1000, 700))

    #Dibujar botones
    boton_dinamico.dibujar(pantalla)
    boton_animar.dibujar(pantalla)
    boton_resetear.dibujar(pantalla)
    boton_positivo.dibujar(pantalla)
    boton_negativo.dibujar(pantalla)
    checkbox_potencial.dibujar(pantalla)
    checkbox_voltaje.dibujar(pantalla)

    if mostrar_potencial: dibujar_potencial(texto_potencial)

    pygame.display.flip()
    reloj.tick(config.FPS)

pygame.quit()
