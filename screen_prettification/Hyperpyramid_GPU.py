import math
import sys
import os
import json
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
import ctypes
import time

class GPU4DHyperpyramidViewer:
    def __init__(self):
        # Hyperpyramid parameters
        self.point_count = 250000
        self.edge_resolution = 100  # Points per edge
        self.face_density = 50  # Points per face unit area
        self.volume_density = 300  # Points per volume unit
        self.hypervolume_density = 200  # Points per hypervolume unit
        self.render_mode = 'full'  # 'vertices', 'edges', 'faces', 'volumes', 'full'
        
        # 4D rotation angles and position
        self.w_angle = 0.0
        self.w_position = 0.0
        self.xw_rotation_speed = 0.5
        self.yz_rotation_speed = 0.3
        self.zw_rotation_speed = 0.2
        self.xy_rotation_speed = 0.4
        self.xz_rotation_speed = 0.35
        self.yw_rotation_speed = 0.25
        self.auto_rotate_4d = False
        
        # 3D camera settings
        self.camera_pos = [0, 0, 4]
        self.rotation = [0, 0, 0]
        self.auto_rotate_3d = False
        self.auto_rotate_speed = [0.5, 0.5]
        
        # Display settings
        self.width = 1280
        self.height = 1280
        self.base_point_size = 1.0
        self.color_mode = 0  # 0: structure-based, 1: w-coordinate, 2: distance-based
        
        # Animation
        self.pulse_phase = 0.0
        self.pulse_speed = 0.02
        
        # OpenGL objects
        self.shader_program = None
        self.vao = None
        self.vbo = None
        self.vertex_count = 0

    def initialize_pygame_and_opengl(self):
        """Initialize Pygame and create OpenGL context"""
        pygame.init()
        
        # Set OpenGL attributes
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
        
        # Create window
        display = (self.width, self.height)
        screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("GPU 4D Hyperpyramid (5-Cell) Viewer")
        
        # Force context creation
        pygame.display.flip()
        time.sleep(0.1)
        
        # Verify context
        try:
            version = glGetString(GL_VERSION)
            if version:
                print(f"OpenGL Version: {version.decode()}")
                print(f"GLSL Version: {glGetString(GL_SHADING_LANGUAGE_VERSION).decode()}")
                print(f"Renderer: {glGetString(GL_RENDERER).decode()}")
            else:
                raise Exception("Failed to get OpenGL version")
        except Exception as e:
            print(f"OpenGL context verification failed: {e}")
            raise

    def create_shaders(self):
        """Create vertex and fragment shaders for 4D hyperpyramid rendering"""
        vertex_shader = """
        #version 330 core
        
        layout(location = 0) in float index;
        
        uniform mat4 projection;
        uniform mat4 view;
        uniform mat4 model;
        uniform float time;
        uniform float point_count;
        uniform int render_mode;
        uniform float edge_resolution;
        uniform float face_density;
        uniform float volume_density;
        uniform float hypervolume_density;
        uniform float w_angle;
        uniform float w_position;
        uniform float xw_speed;
        uniform float yz_speed;
        uniform float zw_speed;
        uniform float xy_speed;
        uniform float xz_speed;
        uniform float yw_speed;
        uniform float base_point_size;
        uniform float pulse_phase;
        
        out vec3 FragPos;
        out vec4 PyramidCoord4D;
        out float WCoord;
        out float StructureType;  // 0=vertex, 1=edge, 2=face, 3=volume, 4=hypervolume
        out float DistFromCenter;
        
        const float PI = 3.14159265359;
        const float SQRT2 = 1.41421356237;
        const float SQRT3 = 1.73205080757;
        const float SQRT5 = 2.2360679775;
        
        // 5-cell vertices in 4D (regular pentachoron)
        const vec4 vertices[5] = vec4[5](
            vec4(1.0, 1.0, 1.0, -1.0/SQRT5),
            vec4(1.0, -1.0, -1.0, -1.0/SQRT5),
            vec4(-1.0, 1.0, -1.0, -1.0/SQRT5),
            vec4(-1.0, -1.0, 1.0, -1.0/SQRT5),
            vec4(0.0, 0.0, 0.0, SQRT5 - 1.0/SQRT5)
        );
        
        vec4 generate_hyperpyramid_point(float idx) {
            vec4 point4d;
            float used_points = 0.0;
            
            // Mode 0: Just vertices
            if (render_mode == 0 || (render_mode == 4 && idx < 5.0)) {
                int vertex_idx = int(mod(idx, 5.0));
                point4d = vertices[vertex_idx];
                StructureType = 0.0;
                return point4d;
            }
            
            used_points = 5.0;
            
            // Mode 1 or 4: Edges (10 edges in a 5-cell)
            float edge_points = 10.0 * edge_resolution;
            if (render_mode == 1 || (render_mode == 4 && idx < used_points + edge_points)) {
                float edge_idx = idx - used_points;
                int edge_num = int(edge_idx / edge_resolution);
                float t = mod(edge_idx, edge_resolution) / edge_resolution;
                
                // Define edge connections
                int v1, v2;
                if (edge_num == 0) { v1 = 0; v2 = 1; }
                else if (edge_num == 1) { v1 = 0; v2 = 2; }
                else if (edge_num == 2) { v1 = 0; v2 = 3; }
                else if (edge_num == 3) { v1 = 0; v2 = 4; }
                else if (edge_num == 4) { v1 = 1; v2 = 2; }
                else if (edge_num == 5) { v1 = 1; v2 = 3; }
                else if (edge_num == 6) { v1 = 1; v2 = 4; }
                else if (edge_num == 7) { v1 = 2; v2 = 3; }
                else if (edge_num == 8) { v1 = 2; v2 = 4; }
                else { v1 = 3; v2 = 4; }
                
                point4d = mix(vertices[v1], vertices[v2], t);
                StructureType = 1.0;
                
                if (render_mode == 1) return point4d;
            }
            
            used_points += edge_points;
            
            // Mode 2 or 4: Faces (10 triangular faces)
            float face_points = 10.0 * face_density * face_density;
            if (render_mode == 2 || (render_mode == 4 && idx < used_points + face_points)) {
                float face_idx = idx - used_points;
                int face_num = int(face_idx / (face_density * face_density));
                float face_local = mod(face_idx, face_density * face_density);
                
                // Barycentric coordinates for triangle
                float u = mod(face_local, face_density) / face_density;
                float v = floor(face_local / face_density) / face_density;
                
                if (u + v > 1.0) {
                    u = 1.0 - u;
                    v = 1.0 - v;
                }
                float w = 1.0 - u - v;
                
                // Define face vertices
                int v1, v2, v3;
                if (face_num == 0) { v1 = 0; v2 = 1; v3 = 2; }
                else if (face_num == 1) { v1 = 0; v2 = 1; v3 = 3; }
                else if (face_num == 2) { v1 = 0; v2 = 1; v3 = 4; }
                else if (face_num == 3) { v1 = 0; v2 = 2; v3 = 3; }
                else if (face_num == 4) { v1 = 0; v2 = 2; v3 = 4; }
                else if (face_num == 5) { v1 = 0; v2 = 3; v3 = 4; }
                else if (face_num == 6) { v1 = 1; v2 = 2; v3 = 3; }
                else if (face_num == 7) { v1 = 1; v2 = 2; v3 = 4; }
                else if (face_num == 8) { v1 = 1; v2 = 3; v3 = 4; }
                else { v1 = 2; v2 = 3; v3 = 4; }
                
                point4d = vertices[v1] * u + vertices[v2] * v + vertices[v3] * w;
                StructureType = 2.0;
                
                if (render_mode == 2) return point4d;
            }
            
            used_points += face_points;
            
            // Mode 3 or 4: Volumes (5 tetrahedral cells)
            float volume_points = 5.0 * volume_density * volume_density * volume_density;
            if (render_mode == 3 || (render_mode == 4 && idx < used_points + volume_points)) {
                float vol_idx = idx - used_points;
                int cell_num = int(vol_idx / (volume_density * volume_density * volume_density));
                float cell_local = mod(vol_idx, volume_density * volume_density * volume_density);
                
                // Generate point inside tetrahedron
                float r1 = fract(sin(cell_local * 12.9898) * 43758.5453);
                float r2 = fract(sin(cell_local * 78.233) * 43758.5453);
                float r3 = fract(sin(cell_local * 45.164) * 43758.5453);
                
                // Transform to barycentric coordinates
                float s = pow(r1, 1.0/3.0);
                float t = sqrt(r2) * s;
                float u = r3 * t;
                
                float a = 1.0 - s;
                float b = s * (1.0 - t);
                float c = s * t * (1.0 - u);
                float d = s * t * u;
                
                // Get cell vertices (each cell excludes one vertex)
                vec4 v[4];
                if (cell_num == 0) { // Excludes vertex 0
                    v[0] = vertices[1]; v[1] = vertices[2]; v[2] = vertices[3]; v[3] = vertices[4];
                } else if (cell_num == 1) { // Excludes vertex 1
                    v[0] = vertices[0]; v[1] = vertices[2]; v[2] = vertices[3]; v[3] = vertices[4];
                } else if (cell_num == 2) { // Excludes vertex 2
                    v[0] = vertices[0]; v[1] = vertices[1]; v[2] = vertices[3]; v[3] = vertices[4];
                } else if (cell_num == 3) { // Excludes vertex 3
                    v[0] = vertices[0]; v[1] = vertices[1]; v[2] = vertices[2]; v[3] = vertices[4];
                } else { // Excludes vertex 4
                    v[0] = vertices[0]; v[1] = vertices[1]; v[2] = vertices[2]; v[3] = vertices[3];
                }
                
                point4d = v[0] * a + v[1] * b + v[2] * c + v[3] * d;
                StructureType = 3.0;
                
                if (render_mode == 3) return point4d;
            }
            
            // Mode 4: Fill the hypervolume
            if (render_mode == 4) {
                // Random point inside the entire 5-cell
                float r1 = fract(sin(idx * 12.9898) * 43758.5453);
                float r2 = fract(sin(idx * 78.233) * 43758.5453);
                float r3 = fract(sin(idx * 45.164) * 43758.5453);
                float r4 = fract(sin(idx * 94.673) * 43758.5453);
                
                // Barycentric coordinates for 5 vertices
                float t1 = sqrt(sqrt(r1));
                float t2 = sqrt(sqrt(r2)) * (1.0 - t1);
                float t3 = sqrt(r3) * (1.0 - t1 - t2);
                float t4 = r4 * (1.0 - t1 - t2 - t3);
                float t5 = 1.0 - t1 - t2 - t3 - t4;
                
                point4d = vertices[0] * t1 + vertices[1] * t2 + vertices[2] * t3 + 
                         vertices[3] * t4 + vertices[4] * t5;
                StructureType = 4.0;
            }
            
            return point4d;
        }
        
        vec3 project_4d_to_3d(vec4 point4d) {
            // Apply multiple 4D rotations for complex movement
            float total_angle = w_angle;
            if (time > 0.0) {
                total_angle += time * 0.001;
            }
            
            // XW rotation
            float cos_xw = cos(total_angle * xw_speed);
            float sin_xw = sin(total_angle * xw_speed);
            float new_x = point4d.x * cos_xw - point4d.w * sin_xw;
            float new_w = point4d.x * sin_xw + point4d.w * cos_xw;
            point4d.x = new_x;
            point4d.w = new_w;
            
            // YZ rotation
            float cos_yz = cos(total_angle * yz_speed * 0.5);
            float sin_yz = sin(total_angle * yz_speed * 0.5);
            float new_y = point4d.y * cos_yz - point4d.z * sin_yz;
            float new_z = point4d.y * sin_yz + point4d.z * cos_yz;
            point4d.y = new_y;
            point4d.z = new_z;
            
            // ZW rotation
            float cos_zw = cos(total_angle * zw_speed * 0.3);
            float sin_zw = sin(total_angle * zw_speed * 0.3);
            new_z = point4d.z * cos_zw - point4d.w * sin_zw;
            new_w = point4d.z * sin_zw + point4d.w * cos_zw;
            point4d.z = new_z;
            point4d.w = new_w;
            
            // XY rotation
            float cos_xy = cos(total_angle * xy_speed * 0.7);
            float sin_xy = sin(total_angle * xy_speed * 0.7);
            new_x = point4d.x * cos_xy - point4d.y * sin_xy;
            new_y = point4d.x * sin_xy + point4d.y * cos_xy;
            point4d.x = new_x;
            point4d.y = new_y;
            
            // XZ rotation
            float cos_xz = cos(total_angle * xz_speed * 0.4);
            float sin_xz = sin(total_angle * xz_speed * 0.4);
            new_x = point4d.x * cos_xz - point4d.z * sin_xz;
            new_z = point4d.x * sin_xz + point4d.z * cos_xz;
            point4d.x = new_x;
            point4d.z = new_z;
            
            // YW rotation
            float cos_yw = cos(total_angle * yw_speed * 0.6);
            float sin_yw = sin(total_angle * yw_speed * 0.6);
            new_y = point4d.y * cos_yw - point4d.w * sin_yw;
            new_w = point4d.y * sin_yw + point4d.w * cos_yw;
            point4d.y = new_y;
            point4d.w = new_w;
            
            // Apply W-axis translation
            point4d.w += w_position;
            
            // Store W coordinate for coloring
            WCoord = point4d.w;
            
            // Calculate distance from center
            DistFromCenter = length(point4d);
            
            // Apply pulsing effect to the structure
            float pulse = 1.0 + sin(pulse_phase) * 0.1;
            point4d *= pulse;
            
            // Perspective projection from 4D to 3D
            float projection_factor = 2.0 / (2.0 - point4d.w * 0.3);
            
            vec3 point3d;
            point3d.x = point4d.x * projection_factor;
            point3d.y = point4d.y * projection_factor;
            point3d.z = point4d.z * projection_factor;
            
            return point3d;
        }
        
        void main()
        {
            // Generate 4D hyperpyramid point
            vec4 point4d = generate_hyperpyramid_point(index);
            PyramidCoord4D = point4d;
            
            // Project to 3D
            vec3 pos = project_4d_to_3d(point4d);
            FragPos = pos;
            
            // Apply transformations
            gl_Position = projection * view * model * vec4(pos, 1.0);
            
            // Dynamic point size based on structure type
            float size_mult = 1.0;
            if (StructureType == 0.0) size_mult = 3.0;      // Vertices are larger
            else if (StructureType == 1.0) size_mult = 2.0; // Edges are medium
            else if (StructureType == 2.0) size_mult = 1.5; // Faces are smaller
            else if (StructureType == 3.0) size_mult = 1.0; // Volume points are small
            else size_mult = 0.8;                           // Hypervolume points are tiny
            
            gl_PointSize = base_point_size * size_mult * (1.0 + sin(pulse_phase) * 0.2);
        }
        """
        
        fragment_shader = """
        #version 330 core
        
        in vec3 FragPos;
        in vec4 PyramidCoord4D;
        in float WCoord;
        in float StructureType;
        in float DistFromCenter;
        
        uniform int color_mode;
        uniform float time;
        
        out vec4 FragColor;
        
        vec3 hsv_to_rgb(vec3 hsv) {
            float h = hsv.x;
            float s = hsv.y;
            float v = hsv.z;
            
            float c = v * s;
            float x = c * (1.0 - abs(mod(h / 60.0, 2.0) - 1.0));
            float m = v - c;
            
            vec3 rgb;
            if (h < 60.0) rgb = vec3(c, x, 0.0);
            else if (h < 120.0) rgb = vec3(x, c, 0.0);
            else if (h < 180.0) rgb = vec3(0.0, c, x);
            else if (h < 240.0) rgb = vec3(0.0, x, c);
            else if (h < 300.0) rgb = vec3(x, 0.0, c);
            else rgb = vec3(c, 0.0, x);
            
            return rgb + m;
        }
        
        void main()
        {
            vec3 color;
            
            if (color_mode == 0) {  // Structure-based coloring
                if (StructureType == 0.0) {
                    // Vertices - bright white
                    color = vec3(1.0, 1.0, 1.0);
                } else if (StructureType == 1.0) {
                    // Edges - cyan
                    color = vec3(0.0, 1.0, 1.0);
                } else if (StructureType == 2.0) {
                    // Faces - yellow
                    color = vec3(1.0, 1.0, 0.0);
                } else if (StructureType == 3.0) {
                    // Volumes - magenta
                    color = vec3(1.0, 0.0, 1.0);
                } else {
                    // Hypervolume - blue to red gradient based on position
                    float t = (WCoord + 2.0) / 4.0;
                    color = mix(vec3(0.0, 0.0, 1.0), vec3(1.0, 0.0, 0.0), t);
                }
                
            } else if (color_mode == 1) {  // W-coordinate rainbow
                float hue = (WCoord + 2.0) * 90.0;
                float saturation = 0.8;
                float value = 0.9;
                color = hsv_to_rgb(vec3(mod(hue, 360.0), saturation, value));
                
            } else {  // Distance-based with animation
                float hue = DistFromCenter * 120.0 + time * 0.02;
                float saturation = 0.7 + StructureType * 0.05;
                float value = 0.6 + 0.4 * sin(DistFromCenter * 5.0 + time * 0.001);
                color = hsv_to_rgb(vec3(mod(hue, 360.0), saturation, value));
            }
            
            // Add brightness variation based on structure type
            float brightness = 0.7 + 0.3 * (4.0 - StructureType) / 4.0;
            color *= brightness;
            
            // Depth shading
            float depth = gl_FragCoord.z;
            color *= (1.2 - depth * 0.2);
            
            FragColor = vec4(color, 1.0);
        }
        """
        
        try:
            # Compile shaders
            vs = shaders.compileShader(vertex_shader, GL_VERTEX_SHADER)
            fs = shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
            self.shader_program = shaders.compileProgram(vs, fs)
            print("4D Hyperpyramid GPU shaders compiled successfully!")
        except Exception as e:
            print(f"Shader compilation error: {e}")
            raise

    def create_vertex_buffer(self):
        """Create vertex buffer with point indices"""
        # Create array of indices
        indices = np.arange(self.point_count, dtype=np.float32)
        
        # Create VAO and VBO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        # Set vertex attributes
        glVertexAttribPointer(0, 1, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        glBindVertexArray(0)
        
        self.vertex_count = len(indices)
        print(f"Created vertex buffer with {self.vertex_count} points")

    def init_gl(self):
        """Initialize OpenGL settings"""
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        # Enable point size control from shaders
        glEnable(GL_PROGRAM_POINT_SIZE)
        
        # Enable blending
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Create shaders and vertex buffer
        self.create_shaders()
        self.create_vertex_buffer()
        
        print("GPU initialization complete")

    def get_projection_matrix(self):
        """Get perspective projection matrix"""
        fov = 45.0
        aspect = self.width / self.height
        near = 0.1
        far = 50.0
        
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        matrix = np.array([
            [f/aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)
        
        return matrix

    def get_view_matrix(self):
        """Get view matrix from camera position and rotation"""
        # Create translation matrix
        translation = np.eye(4, dtype=np.float32)
        translation[0, 3] = -self.camera_pos[0]
        translation[1, 3] = -self.camera_pos[1]
        translation[2, 3] = -self.camera_pos[2]
        
        # Create rotation matrices
        rx = math.radians(self.rotation[0])
        ry = math.radians(self.rotation[1])
        rz = math.radians(self.rotation[2])
        
        # X rotation
        rot_x = np.eye(4, dtype=np.float32)
        rot_x[1, 1] = math.cos(rx)
        rot_x[1, 2] = -math.sin(rx)
        rot_x[2, 1] = math.sin(rx)
        rot_x[2, 2] = math.cos(rx)
        
        # Y rotation
        rot_y = np.eye(4, dtype=np.float32)
        rot_y[0, 0] = math.cos(ry)
        rot_y[0, 2] = math.sin(ry)
        rot_y[2, 0] = -math.sin(ry)
        rot_y[2, 2] = math.cos(ry)
        
        # Z rotation
        rot_z = np.eye(4, dtype=np.float32)
        rot_z[0, 0] = math.cos(rz)
        rot_z[0, 1] = -math.sin(rz)
        rot_z[1, 0] = math.sin(rz)
        rot_z[1, 1] = math.cos(rz)
        
        # Combine transformations
        view = translation @ rot_x @ rot_y @ rot_z
        return view

    def display(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Use shader program
        glUseProgram(self.shader_program)
        
        # Get current time for animations
        current_time = pygame.time.get_ticks() if self.auto_rotate_4d else 0
        
        # Update pulse phase
        self.pulse_phase += self.pulse_speed
        
        # Set uniforms
        uniforms = {
            'projection': glGetUniformLocation(self.shader_program, "projection"),
            'view': glGetUniformLocation(self.shader_program, "view"),
            'model': glGetUniformLocation(self.shader_program, "model"),
            'time': glGetUniformLocation(self.shader_program, "time"),
            'point_count': glGetUniformLocation(self.shader_program, "point_count"),
            'render_mode': glGetUniformLocation(self.shader_program, "render_mode"),
            'edge_resolution': glGetUniformLocation(self.shader_program, "edge_resolution"),
            'face_density': glGetUniformLocation(self.shader_program, "face_density"),
            'volume_density': glGetUniformLocation(self.shader_program, "volume_density"),
            'hypervolume_density': glGetUniformLocation(self.shader_program, "hypervolume_density"),
            'w_angle': glGetUniformLocation(self.shader_program, "w_angle"),
            'w_position': glGetUniformLocation(self.shader_program, "w_position"),
            'xw_speed': glGetUniformLocation(self.shader_program, "xw_speed"),
            'yz_speed': glGetUniformLocation(self.shader_program, "yz_speed"),
            'zw_speed': glGetUniformLocation(self.shader_program, "zw_speed"),
            'xy_speed': glGetUniformLocation(self.shader_program, "xy_speed"),
            'xz_speed': glGetUniformLocation(self.shader_program, "xz_speed"),
            'yw_speed': glGetUniformLocation(self.shader_program, "yw_speed"),
            'base_point_size': glGetUniformLocation(self.shader_program, "base_point_size"),
            'pulse_phase': glGetUniformLocation(self.shader_program, "pulse_phase"),
            'color_mode': glGetUniformLocation(self.shader_program, "color_mode")
        }
        
        # Set matrices
        projection = self.get_projection_matrix()
        view = self.get_view_matrix()
        model = np.eye(4, dtype=np.float32)
        
        glUniformMatrix4fv(uniforms['projection'], 1, GL_TRUE, projection)
        glUniformMatrix4fv(uniforms['view'], 1, GL_TRUE, view)
        glUniformMatrix4fv(uniforms['model'], 1, GL_TRUE, model)
        
        # Set other uniforms
        glUniform1f(uniforms['time'], current_time)
        glUniform1f(uniforms['point_count'], self.point_count)
        
        # Render mode: 0=vertices, 1=edges, 2=faces, 3=volumes, 4=full
        mode_map = {'vertices': 0, 'edges': 1, 'faces': 2, 'volumes': 3, 'full': 4}
        glUniform1i(uniforms['render_mode'], mode_map.get(self.render_mode, 4))
        
        glUniform1f(uniforms['edge_resolution'], self.edge_resolution)
        glUniform1f(uniforms['face_density'], self.face_density)
        glUniform1f(uniforms['volume_density'], self.volume_density)
        glUniform1f(uniforms['hypervolume_density'], self.hypervolume_density)
        
        glUniform1f(uniforms['w_angle'], self.w_angle)
        glUniform1f(uniforms['w_position'], self.w_position)
        glUniform1f(uniforms['xw_speed'], self.xw_rotation_speed)
        glUniform1f(uniforms['yz_speed'], self.yz_rotation_speed)
        glUniform1f(uniforms['zw_speed'], self.zw_rotation_speed)
        glUniform1f(uniforms['xy_speed'], self.xy_rotation_speed)
        glUniform1f(uniforms['xz_speed'], self.xz_rotation_speed)
        glUniform1f(uniforms['yw_speed'], self.yw_rotation_speed)
        glUniform1f(uniforms['base_point_size'], self.base_point_size)
        glUniform1f(uniforms['pulse_phase'], self.pulse_phase)
        glUniform1i(uniforms['color_mode'], self.color_mode)
        
        # Draw
        glBindVertexArray(self.vao)
        glDrawArrays(GL_POINTS, 0, self.vertex_count)
        glBindVertexArray(0)
        
        pygame.display.flip()

    def run(self):
        """Main loop"""
        # Initialize
        self.initialize_pygame_and_opengl()
        self.init_gl()
        
        print("\nGPU 4D Hyperpyramid (5-Cell) Viewer")
        print("\nControls:")
        print("  Arrow keys: Rotate 3D view")
        print("  Page Up/Down: Zoom in/out")
        print("  W/S: Rotate in 4D (W dimension)")
        print("  T/G: Pan along W axis (4th dimension)")
        print("  Q/E: Decrease/Increase point size")
        print("  A: Toggle 3D auto-rotation")
        print("  D: Toggle 4D auto-rotation")
        print("  C: Cycle color modes")
        print("  M: Cycle render modes (vertices/edges/faces/volumes/full)")
        print("  P: Toggle pulse animation")
        print("  1-6: Adjust individual 4D rotation speeds")
        print("  R: Reset view")
        print("  ESC: Quit")
        
        clock = pygame.time.Clock()
        running = True
        pulse_enabled = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        # Reset view
                        self.camera_pos = [0, 0, -5]
                        self.rotation = [0, 0, 0]
                        self.w_angle = 0.0
                        self.w_position = 0.0
                        self.base_point_size = 2.0
                        print("View reset")
                    elif event.key == pygame.K_PAGEUP:
                        self.camera_pos[2] += 0.5
                    elif event.key == pygame.K_PAGEDOWN:
                        self.camera_pos[2] -= 0.5
                    elif event.key == pygame.K_q:
                        self.base_point_size = max(0.5, self.base_point_size - 0.5)
                        print(f"Point size: {self.base_point_size:.1f}")
                    elif event.key == pygame.K_e:
                        self.base_point_size = min(10.0, self.base_point_size + 0.5)
                        print(f"Point size: {self.base_point_size:.1f}")
                    elif event.key == pygame.K_a:
                        self.auto_rotate_3d = not self.auto_rotate_3d
                        print(f"3D Auto-rotation: {'ON' if self.auto_rotate_3d else 'OFF'}")
                    elif event.key == pygame.K_d:
                        self.auto_rotate_4d = not self.auto_rotate_4d
                        print(f"4D Auto-rotation: {'ON' if self.auto_rotate_4d else 'OFF'}")
                    elif event.key == pygame.K_c:
                        self.color_mode = (self.color_mode + 1) % 3
                        modes = ['Structure-based', 'W-coordinate', 'Distance-animated']
                        print(f"Color mode: {modes[self.color_mode]}")
                    elif event.key == pygame.K_m:
                        modes = ['vertices', 'edges', 'faces', 'volumes', 'full']
                        current_idx = modes.index(self.render_mode)
                        self.render_mode = modes[(current_idx + 1) % 5]
                        print(f"Render mode: {self.render_mode}")
                    elif event.key == pygame.K_p:
                        pulse_enabled = not pulse_enabled
                        if not pulse_enabled:
                            self.pulse_speed = 0
                        else:
                            self.pulse_speed = 0.02
                        print(f"Pulse animation: {'ON' if pulse_enabled else 'OFF'}")
                    elif event.key == pygame.K_1:
                        self.xw_rotation_speed *= 1.2
                        print(f"XW rotation speed: {self.xw_rotation_speed:.2f}")
                    elif event.key == pygame.K_2:
                        self.yz_rotation_speed *= 1.2
                        print(f"YZ rotation speed: {self.yz_rotation_speed:.2f}")
                    elif event.key == pygame.K_3:
                        self.zw_rotation_speed *= 1.2
                        print(f"ZW rotation speed: {self.zw_rotation_speed:.2f}")
                    elif event.key == pygame.K_4:
                        self.xy_rotation_speed *= 1.2
                        print(f"XY rotation speed: {self.xy_rotation_speed:.2f}")
                    elif event.key == pygame.K_5:
                        self.xz_rotation_speed *= 1.2
                        print(f"XZ rotation speed: {self.xz_rotation_speed:.2f}")
                    elif event.key == pygame.K_6:
                        self.yw_rotation_speed *= 1.2
                        print(f"YW rotation speed: {self.yw_rotation_speed:.2f}")
            
            # Handle continuous rotation and movement
            keys = pygame.key.get_pressed()
            
            if self.auto_rotate_3d:
                self.rotation[0] += self.auto_rotate_speed[0]
                self.rotation[1] += self.auto_rotate_speed[1]
            else:
                if keys[pygame.K_LEFT]:
                    self.rotation[1] -= 2
                if keys[pygame.K_RIGHT]:
                    self.rotation[1] += 2
                if keys[pygame.K_UP]:
                    self.rotation[0] -= 2
                if keys[pygame.K_DOWN]:
                    self.rotation[0] += 2
            
            # Continuous W-dimension controls
            if keys[pygame.K_w]:
                self.w_angle += 0.02
            if keys[pygame.K_s]:
                self.w_angle -= 0.02
            if keys[pygame.K_t]:
                self.w_position += 0.02
            if keys[pygame.K_g]:
                self.w_position -= 0.02
            
            self.display()
            clock.tick(60)
        
        # Cleanup
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
        if self.shader_program:
            glDeleteProgram(self.shader_program)
        
        pygame.quit()

def main():
    try:
        viewer = GPU4DHyperpyramidViewer()
        viewer.run()
    except Exception as e:
        print(f"Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure PyOpenGL is installed: pip install PyOpenGL PyOpenGL_accelerate")
        print("2. Check your graphics drivers are up to date")
        print("3. Try reducing point_count if performance is poor")

if __name__ == "__main__":
    main()