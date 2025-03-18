import pygame
import numpy as np

#Funcion para crear superficie rgba a partir de un 3d array con 4 canales de color
def make_surface_rgba(array):
    """Returns a surface made from a [w, h, 4] numpy array with per-pixel alpha
    """
    shape = array.shape
    if len(shape) != 3 and shape[2] != 4:
        raise ValueError("Array not RGBA")

    # Create a surface the same width and height as array and with
    # per-pixel alpha.
    surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)

    # Copy the rgb part of array to the new surface.
    pygame.pixelcopy.array_to_surface(surface, array[:,:,0:3])

    # Copy the alpha part of array to the surface using a pixels-alpha
    # view of the surface.
    surface_alpha = np.array(surface.get_view('A'), copy=False)
    surface_alpha[:,:] = array[:,:,3]

    return surface


def dibujar_imagen(pantalla, direccion, posicion, escala_x=None, escala_y=None, rotacion=0, alpha = None):
    imagen = pygame.image.load(direccion).convert_alpha() 
    if escala_x:
        imagen = pygame.transform.scale(imagen, (imagen.get_width() * escala_x, imagen.get_height()))
    if escala_y:
        imagen = pygame.transform.scale(imagen, (imagen.get_width(), imagen.get_height() * escala_y))

    if rotacion:
        imagen = pygame.transform.rotate(imagen, rotacion)

    if alpha:
        imagen.set_alpha(alpha)

    rect = imagen.get_rect(center=posicion) 
    pantalla.blit(imagen, rect)  
