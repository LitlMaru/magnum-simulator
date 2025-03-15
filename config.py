import pygame

ANCHO, ALTO = 800, 600
COLOR_FONDO = (0, 0, 0)

#Simulador de campo electrico

RADIO_CARGA = 15
K = 8.99e9  
PASO_TIEMPO = 0.0002 
FPS = 60
SEPARACION_PUNTOS = 20 
COLOR_CAMPO = (0, 255, 0)

#Estados
CARGA_PRUEBA = False
ANIMANDO = False

#Simulador de campo magnetico