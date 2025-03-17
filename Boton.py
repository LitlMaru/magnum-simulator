import pygame

class Boton:
    def __init__(self, x, y, direccion_imagen_normal, direccion_imagen_hover=None, direccion_imagen_activo=None, direccion_imagen_activo_hover=None, scale=1):
        self.imagen_normal = pygame.image.load(direccion_imagen_normal).convert_alpha()
        self.imagen_hover = pygame.image.load(direccion_imagen_hover).convert_alpha() if direccion_imagen_hover else None
        self.imagen_activo = pygame.image.load(direccion_imagen_activo).convert_alpha() if direccion_imagen_activo else None
        self.imagen_activo_hover = pygame.image.load(direccion_imagen_activo_hover).convert_alpha() if direccion_imagen_activo_hover else None
        
        # Scale images
        self.imagen_normal = pygame.transform.scale(self.imagen_normal, (int(self.imagen_normal.get_width() * scale), int(self.imagen_normal.get_height() * scale)))
        if self.imagen_hover:
            self.imagen_hover = pygame.transform.scale(self.imagen_hover, (int(self.imagen_hover.get_width() * scale), int(self.imagen_hover.get_height() * scale)))
        if self.imagen_activo:
            self.imagen_activo = pygame.transform.scale(self.imagen_activo, (int(self.imagen_activo.get_width() * scale), int(self.imagen_activo.get_height() * scale)))
        if self.imagen_activo_hover:
            self.imagen_activo_hover = pygame.transform.scale(self.imagen_activo_hover, (int(self.imagen_activo_hover.get_width() * scale), int(self.imagen_activo_hover.get_height() * scale)))
        
        self.imagen = self.imagen_normal  # Default image
        self.rect = self.imagen.get_rect(topleft=(x, y))
        self.activo = False

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

    def controlar_eventos(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.activo:
                if self.rect.collidepoint(event.pos) and self.imagen_activo_hover:
                    self.imagen = self.imagen_activo_hover
                elif self.imagen_activo:
                    self.imagen = self.imagen_activo
            else:
                if self.rect.collidepoint(event.pos) and self.imagen_hover:
                    self.imagen = self.imagen_hover
                else:
                    self.imagen = self.imagen_normal

        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.activo = not self.activo  # Toggle state

            # **IMMEDIATELY UPDATE THE IMAGE**
            if self.activo:
                self.imagen = self.imagen_activo if self.imagen_activo else self.imagen_normal
            else:
                self.imagen = self.imagen_hover if self.rect.collidepoint(event.pos) and self.imagen_hover else self.imagen_normal

            return True  # Button was clicked

        return False  # No action