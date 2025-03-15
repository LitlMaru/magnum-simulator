import pygame

class Boton:
    def __init__(self, x, y, direccion_imagen_normal, direccion_imagen_hover=None, direccion_imagen_activo=None, direccion_imagen_activo_hover=None, scale=1):
        self.imagen_normal = pygame.image.load(direccion_imagen_normal).convert_alpha()
        if direccion_imagen_hover:
            self.imagen_hover = pygame.image.load(direccion_imagen_hover).convert_alpha()
        if direccion_imagen_activo:
            self.imagen_activo =  pygame.image.load(direccion_imagen_activo).convert_alpha()
        if direccion_imagen_activo_hover:
            self.imagen_activo_hover =  pygame.image.load(direccion_imagen_activo_hover).convert_alpha()
        
        # Scale images if needed
        self.imagen_normal = pygame.transform.scale(self.imagen_normal, 
                        (int(self.imagen_normal.get_width() * scale), int(self.imagen_normal.get_height() * scale)))
        if direccion_imagen_hover:
            self.imagen_hover = pygame.transform.scale(self.imagen_hover, 
                            (int(self.imagen_hover.get_width() * scale), int(self.imagen_hover.get_height() * scale)))
        if direccion_imagen_activo:
            self.imagen_activo = pygame.transform.scale(self.imagen_activo, 
                            (int(self.imagen_activo.get_width() * scale), int(self.imagen_activo.get_height() * scale)))
        if direccion_imagen_activo_hover:
            self.imagen_activo_hover = pygame.transform.scale(self.imagen_activo_hover, 
                            (int(self.imagen_activo_hover.get_width() * scale), int(self.imagen_activo_hover.get_height() * scale)))
        
        self.imagen = self.imagen_normal  # Default image
        self.rect = self.imagen.get_rect(topleft=(x, y))

        self.activo = False

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def controlar_eventos(self, event):
        if self.activo == False:
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.imagen = self.imagen_hover
                else:
                    self.imagen = self.imagen_normal
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if hasattr(self, "imagen_activo"):
                        self.activo = True
                    return True
            return False
        elif self.activo and hasattr(self, "imagen_activo"):
            if event.type == pygame.MOUSEMOTION:
                if self.rect.collidepoint(event.pos):
                    self.imagen = self.imagen_activo_hover
                else:
                    self.imagen = self.imagen_activo
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.activo = False
                    return True
            return False
