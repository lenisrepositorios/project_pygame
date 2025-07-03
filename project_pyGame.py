import pygame
import sys

pygame.init()

#Configuración pantalla
ancho_pantalla, alto_pantalla = 800, 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Camino peligroso")

#Colores
aqua = (189, 255, 245)
negro = (0, 0, 0)
blanco = (255, 255, 255)

fuente = pygame.font.SysFont(None, 40)
reloj = pygame.time.Clock()
imagen_player = pygame.image.load("player.png")
imagen_meta = pygame.image.load("flag.png")

def texto_centrado(texto, y):
    t = fuente.render(texto, True, negro)
    pantalla.blit(t, (ancho_pantalla // 2 - t.get_width() // 2, y))

def dibujar_boton(texto, rect, color):
    pygame.draw.rect(pantalla, color, rect)
    t = fuente.render(texto, True, negro)
    pantalla.blit(t, (rect.x + 10, rect.y + 10))

def menu_inicio():
    while True:
        pantalla.fill(aqua)
        texto_centrado("Presiona ESPACIO para comenzar", 250)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                return

def menu_niveles():
    while True:
        pantalla.fill(aqua)
        texto_centrado("Selecciona un nivel:", 150)
        boton1 = pygame.Rect(300, 220, 200, 50)
        boton2 = pygame.Rect(300, 300, 200, 50)
        boton3 = pygame.Rect(300, 380, 200, 50)
        dibujar_boton("Nivel 1", boton1, blanco)
        dibujar_boton("Nivel 2", boton2, blanco)
        dibujar_boton("Nivel 3", boton3, blanco)
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton1.collidepoint(evento.pos):
                    return 1
                if boton2.collidepoint(evento.pos):
                    return 2
                if boton3.collidepoint(evento.pos):
                    return 3

def pantalla_final(mensaje):
    while True:
        pantalla.fill(aqua)
        texto_centrado(mensaje, 200)
        boton_reiniciar = pygame.Rect(300, 300, 200, 50)
        boton_salir = pygame.Rect(300, 380, 200, 50)
        dibujar_boton("Reiniciar", boton_reiniciar, blanco)
        dibujar_boton("Salir", boton_salir, blanco)
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(evento.pos):
                    return True
                if boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

def jugar_nivel(n):
    #Jugador
    jugador = pygame.Rect(50, 50, 40, 40)
    velocidad = 5
    meta = pygame.Rect(700, 500, 50, 50)

    #Obstáculos y enemigos por nivel
    if n == 1:
        imagen_enemigo = pygame.image.load("enemigo1.png")
        obstaculos = [pygame.Rect(200, 150, 100, 20), pygame.Rect(400, 300, 150, 20)]
        enemigos = [pygame.Rect(300, 100, 40, 40)]
        direcciones = [1]
    elif n == 2:
        imagen_enemigo = pygame.image.load("enemigo2.png")
        obstaculos = [pygame.Rect(50, 200, 300, 20), pygame.Rect(300, 400, 150, 20), pygame.Rect(600, 250, 100, 20)]
        enemigos = [pygame.Rect(500, 100, 40, 40), pygame.Rect(200, 350, 40, 40)]
        direcciones = [1, -1]
    elif n == 3:
        imagen_enemigo = pygame.image.load("enemigo3.png")
        obstaculos = [pygame.Rect(150, 100, 100, 20), pygame.Rect(400, 200, 150, 20), pygame.Rect(250, 350, 200, 20), 
                      pygame.Rect(500, 450, 100, 20), pygame.Rect(500, 450, 20, 120)]
        enemigos = [pygame.Rect(100, 300, 40, 40), pygame.Rect(600, 400, 40, 40), pygame.Rect(350, 100, 40, 40)]
        direcciones = [1, -1, 1]

    #Bucle del nivel
    while True:
        reloj.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]: jugador.x -= velocidad
        if teclas[pygame.K_RIGHT]: jugador.x += velocidad
        if teclas[pygame.K_UP]: jugador.y -= velocidad
        if teclas[pygame.K_DOWN]: jugador.y += velocidad

        #Movimiento enemigos
        for i, enemigo in enumerate(enemigos):
            enemigo.x += direcciones[i] * 3
            if enemigo.left <= 0 or enemigo.right >= ancho_pantalla:
                direcciones[i] *= -1

        #Colisiones
        for obs in obstaculos:
            if jugador.colliderect(obs):
                jugador.x = 50
                jugador.y = 50
        for enemigo in enemigos:
            if jugador.colliderect(enemigo):
                return "¡Perdiste!"
        if jugador.colliderect(meta):
            return "¡Ganaste!"

        pantalla.fill(aqua)
        pantalla.blit(imagen_meta, meta.center)
        pantalla.blit(imagen_player, jugador.topleft)
        for obs in obstaculos:
            pygame.draw.rect(pantalla, negro, obs)
        for enemigo in enemigos:
            pantalla.blit(imagen_enemigo, enemigo.topleft)
        pygame.display.flip()

#Ejecución
while True:
    menu_inicio()
    nivel = menu_niveles()
    resultado = jugar_nivel(nivel)
    reiniciar = pantalla_final(resultado)
    if not reiniciar:
        break
