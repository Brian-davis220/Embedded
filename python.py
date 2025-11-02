# joystick_3d_cube_bluetooth.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import serial
import time

# --- Bluetooth setup ---
# Replace 'COM5' with your Bluetooth COM port on Windows or '/dev/tty.HC-05-DevB' on Mac/Linux
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  # wait for BT to connect

# --- Pygame & OpenGL setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Cube Bluetooth Control")

glEnable(GL_DEPTH_TEST)
glClearColor(0.1, 0.1, 0.1, 1)
gluPerspective(45, WIDTH/HEIGHT, 0.1, 50.0)
glTranslatef(0, 0, -5)

vertices = [
    (1,1,-1), (1,-1,-1), (-1,-1,-1), (-1,1,-1),
    (1,1,1), (1,-1,1), (-1,-1,1), (-1,1,1)
]

edges = [
    (0,1),(1,2),(2,3),(3,0),
    (4,5),(5,6),(6,7),(7,4),
    (0,4),(1,5),(2,6),(3,7)
]

cube_pos = [0, 0, 0]

def draw_cube():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(cube_pos[0], cube_pos[1], cube_pos[2]-5)
    glBegin(GL_LINES)
    glColor3f(1,0,0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    pygame.display.flip()

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Read Bluetooth data ---
    try:
        line = ser.readline().decode().strip()
        if line:
            x_str, y_str = line.split(',')
            x = float(x_str)
            y = float(y_str)
            cube_pos[0] += x * 0.2
            cube_pos[1] += y * 0.2
    except:
        pass

    draw_cube()
    clock.tick(60)

ser.close()
pygame.quit()
