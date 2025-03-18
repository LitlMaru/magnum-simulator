import pygame
import math
import config
from Utilidades import dibujar_imagen
class Carga:
    def __init__(self, x, y, q, esCargaDePrueba, pantalla, masa = 1):
        self.x = x
        self.y = y
        self.q = q
        self.vx = 0
        self.vy = 0
        self.fx_total = 0
        self.fy_total = 0
        self.masa = masa
        self.pantalla = pantalla
        self.esCargaDePrueba = esCargaDePrueba
        self.id = None

    def fuerza_por(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        r2 = dx**2 + dy**2
        if r2 == 0:
            return (0, 0)
        r = math.sqrt(r2)
        magnitud_fuerza = - config.K * self.q * other.q / r2
        fuerza_x = magnitud_fuerza * dx / r
        fuerza_y = magnitud_fuerza * dy / r
        return (fuerza_x, fuerza_y)

    def actualizar(self, cargas):
        self.fx_total = 0
        self.fy_total = 0
        for other in cargas:
            if other is not self:
                fx, fy = self.fuerza_por(other)
                self.fx_total += fx
                self.fy_total += fy

        # Rebote elastico usando limites (cargas ademas desaceleran al acercarse al limite)
        limite_rebote = 0.7  

        if self.x <= 0 or self.x >= config.ANCHO:
            self.vx = -self.vx * limite_rebote  
            self.x = max(0, min(config.ANCHO, self.x))  

        if self.y <= 0 or self.y >= config.ALTO:
            self.vy = -self.vy * limite_rebote 
            self.y = max(0, min(config.ALTO, self.y))  

        margen = 50 
        factor_desaceleracion = 0.95  

        if self.x < margen or self.x > config.ANCHO - margen:
            self.vx *= factor_desaceleracion
        if self.y < margen or self.y > config.ALTO - margen:
            self.vy *= factor_desaceleracion
        

    def dibujar(self):
        if(self.esCargaDePrueba and config.ANIMANDO):
            ax = self.fx_total / self.masa
            ay = self.fy_total / self.masa
            self.vx += ax * config.PASO_TIEMPO
            self.vy += ay * config.PASO_TIEMPO
            self.x += self.vx * config.PASO_TIEMPO
            self.y += self.vy * config.PASO_TIEMPO
        if self.q > 0:
            dibujar_imagen(self.pantalla, "Imagenes/cargaPositiva.png", (int(self.x), int(self.y)), 0.12, 0.12)
        else:
            dibujar_imagen(self.pantalla, "Imagenes/cargaNegativa.png", (int(self.x), int(self.y)), 0.12, 0.12)
