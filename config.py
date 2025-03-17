import pygame

ANCHO, ALTO = 1142, 720
COLOR_FONDO = (0, 0, 0)

#Simulador de campo electrico

RADIO_CARGA = 25
K = 8.99e9  
PASO_TIEMPO = 0.0002 
FPS = 60
SEPARACION_PUNTOS = 40 
COLOR_CAMPO = (255, 255, 255)

#Estados
CARGA_PRUEBA = False
ANIMANDO = False

#Simulador de campo magnetico