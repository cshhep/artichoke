# "plane" flying

# you're hallucinating if you see errors ;) 

import pygame
from pygame.locals import *
from OpenGL import GL
from OpenGL.GLU import *

from OpenGL import GL

GL.glEnable(GL.GL_LIGHTING)

from OpenGL import GL

# starting
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -10)

# Ball properties
ball_pos = [0, 0, 0]
ball_speed = [0.02, 0.03, 0.04]
ball_radius = 1

glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, (2, 2, 2, 0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT, GL_DIFFUSE)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Ball movement
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]
    ball_pos[2] += ball_speed[2]

    for i in range(3):
        if ball_pos[i] > 4.5 - ball_radius or ball_pos[i] < -4.5 + ball_radius:
            ball_speed[i] = -ball_speed[i]

    glColor3f(0.5, 0.5, 0.5)
    glPushMatrix()  
    glTranslatef(ball_pos[0], ball_pos[1], ball_pos[2])
    quad = gluNewQuadric()
    gluSphere(quad, ball_radius, 50, 50)
    glPopMatrix() 

    pygame.display.flip()
    pygame.time.wait(10)
