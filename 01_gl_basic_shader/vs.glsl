#version 400

layout (location = 0) in vec3 vertexPosition;
layout (location = 1) in vec3 vertexColor;

uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;

out vec3 color;

void main()
{
    color = vertexColor;
    gl_Position =  projectionMatrix * modelViewMatrix * vec4(vertexPosition, 1.0);
}
