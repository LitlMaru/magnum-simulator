import pygame

pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 400, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Textbox Numérico")

# Cargar imagen de fondo
textbox_image = pygame.image.load("Imagenes/textboxFuerza.png")  
textbox_rect = textbox_image.get_rect(center=(WIDTH//2, HEIGHT//2))

# Configuración del textbox
input_box = pygame.Rect(10, 10, 140, 30)  # Posición y tamaño del área de entrada
font = pygame.font.Font(None, 32)
text = ""

running = True
while running:
    screen.fill((255, 255, 255))  # Fondo blanco
    screen.blit(textbox_image, textbox_rect)  # Dibujar imagen del textbox

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]  # Borrar último carácter
            elif event.unicode.isdigit() or (event.unicode == '.' and '.' not in text):
                text += event.unicode  # Agregar solo números o un solo punto decimal

    # Renderizar el texto dentro del textbox
    txt_surface = font.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

    pygame.display.flip()

pygame.quit()