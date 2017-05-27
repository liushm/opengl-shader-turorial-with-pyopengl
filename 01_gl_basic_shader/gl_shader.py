#!/bin/env python
# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from numpy import *
from PIL import Image

import sys
import time

program = None
locMVM = None
locPrM = None
vbo = None
vao = None
vertices = [1.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
colors = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

def InitShader():
    global program, locMVM, locPrM
    program = compileProgram(
        compileShader(open('vs.glsl').read(), GL_VERTEX_SHADER),
        compileShader(open('fs.glsl').read(), GL_FRAGMENT_SHADER), )
    locMVM = glGetUniformLocation(program, 'modelViewMatrix')
    locPrM = glGetUniformLocation(program, 'projectionMatrix')

def InitBuffers():
    global vbo, vao
    vbo = glGenBuffers(2)
    # vertex buffer
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, 4 * len(vertices), (ctypes.c_float*len(vertices))(*vertices), GL_STATIC_DRAW)
    # color buffer for each vertex
    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glBufferData(GL_ARRAY_BUFFER, 4 * len(colors), (ctypes.c_float*len(colors))(*colors), GL_STATIC_DRAW)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

def PrintVersion():
    print glGetString(GL_RENDERER)
    print glGetString(GL_VENDOR)
    print glGetString(GL_VERSION)
    # print glGetString(GL_EXTENSIONS)

def InitGL(width,height):
    glClearColor(0.5, 0.5, 0.5, 0.1)
    glClearDepth(1.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    PrintVersion()
    InitShader()
    InitBuffers()
    # glEnableClientState(GL_VERTEX_ARRAY)

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # rotate alone Y-axis, 30 deg/sec
    glRotatef(30 * time.time() % 360.0, 0, 1.0, 0.0)

    glUseProgram(program)
    # print glGetFloatv(GL_MODELVIEW_MATRIX)
    # print glGetFloatv(GL_PROJECTION_MATRIX)
    glUniformMatrix4fv(locMVM, 1, GL_FALSE, glGetFloatv(GL_MODELVIEW_MATRIX))
    glUniformMatrix4fv(locPrM, 1, GL_FALSE, glGetFloatv(GL_PROJECTION_MATRIX))

    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    glutSwapBuffers()

def MouseButton(button, mode, x, y):
    if button == 3 and mode == 0:
        glMatrixMode(GL_PROJECTION)
        glScalef(1.1, 1.1, 1.1)
    elif button == 4 and mode == 0:
        glMatrixMode(GL_PROJECTION)
        glScalef(1/1.1, 1/1.1, 1/1.1)
    pass

def ReSizeGLScene(Width, Height):
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

def main():
    w, h = 800, 450

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutInitWindowPosition(400, 300)
    glutCreateWindow("opengl")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutMouseFunc(MouseButton)

    InitGL(w, h)

    glutMainLoop()

main()
