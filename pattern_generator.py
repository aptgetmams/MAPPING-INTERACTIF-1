#!/usr/bin/env python3
"""
Générateur de patterns génératifs réactifs
"""

import pygame
import numpy as np
import math
import time
from typing import Tuple, List

class PatternGenerator:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Kinect Generative Patterns")
        
        # Paramètres du pattern
        self.particles = []
        self.max_particles = 100
        self.colors = [
            (255, 100, 100),  # Rouge
            (100, 255, 100),  # Vert
            (100, 100, 255),  # Bleu
            (255, 255, 100),  # Jaune
            (255, 100, 255),  # Magenta
            (100, 255, 255),  # Cyan
        ]
        
        # État du système
        self.time_offset = 0
        self.motion_center = (width//2, height//2)
        self.motion_intensity = 0
        
        # Patterns disponibles
        self.pattern_mode = 0
        self.pattern_functions = [
            self._draw_spiral_pattern,
            self._draw_wave_pattern,
            self._draw_particle_system,
            self._draw_geometric_pattern
        ]
        
    def update_motion_data(self, motion_center: Tuple[int, int], intensity: float):
        """Met à jour les données de mouvement"""
        self.motion_center = motion_center
        self.motion_intensity = max(0, min(intensity / 10000.0, 1.0))  # Normalisation
        
    def _create_particle(self, x: int, y: int) -> dict:
        """Crée une nouvelle particule"""
        angle = np.random.uniform(0, 2 * np.pi)
        speed = np.random.uniform(1, 5)
        
        return {
            'x': x,
            'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'life': 100,
            'max_life': 100,
            'color_idx': np.random.randint(0, len(self.colors)),
            'size': np.random.uniform(2, 8)
        }
        
    def _update_particles(self):
        """Met à jour les particules"""
        # Ajouter de nouvelles particules basées sur le mouvement
        if self.motion_intensity > 0.1 and len(self.particles) < self.max_particles:
            for _ in range(int(self.motion_intensity * 10)):
                if len(self.particles) >= self.max_particles:
                    break
                    
                x = self.motion_center[0] + np.random.randint(-50, 50)
                y = self.motion_center[1] + np.random.randint(-50, 50)
                self.particles.append(self._create_particle(x, y))
        
        # Mettre à jour les particules existantes
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            
            # Gravité et friction
            particle['vy'] += 0.1
            particle['vx'] *= 0.99
            particle['vy'] *= 0.99
            
            # Supprimer les particules mortes
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def _draw_spiral_pattern(self, surface):
        """Pattern en spirale réactive"""
        center_x, center_y = self.motion_center
        
        for i in range(0, 360, 5):
            angle = math.radians(i + self.time_offset * 50)
            radius = (i / 5) * (1 + self.motion_intensity)
            
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            
            if 0 <= x < self.width and 0 <= y < self.height:
                color_intensity = int(255 * self.motion_intensity)
                color = (color_intensity, 100, 255 - color_intensity)
                pygame.draw.circle(surface, color, (int(x), int(y)), 3)
                
    def _draw_wave_pattern(self, surface):
        """Pattern d'ondes"""
        for x in range(0, self.width, 10):
            for y in range(0, self.height, 10):
                dist_to_motion = math.sqrt(
                    (x - self.motion_center[0])**2 + 
                    (y - self.motion_center[1])**2
                )
                
                wave = math.sin(dist_to_motion * 0.1 + self.time_offset * 5)
                wave += math.sin(x * 0.05 + self.time_offset * 3)
                wave += math.sin(y * 0.03 + self.time_offset * 2)
                
                intensity = (wave + 3) / 6 * self.motion_intensity
                if intensity > 0.3:
                    color_val = int(intensity * 255)
                    color = (color_val, color_val // 2, 255 - color_val)
                    pygame.draw.rect(surface, color, (x, y, 8, 8))
                    
    def _draw_particle_system(self, surface):
        """Système de particules"""
        self._update_particles()
        
        for particle in self.particles:
            life_ratio = particle['life'] / particle['max_life']
            color = list(self.colors[particle['color_idx']])
            
            # Fade out avec la vie
            for i in range(3):
                color[i] = int(color[i] * life_ratio)
                
            size = int(particle['size'] * life_ratio)
            if size > 0:
                pygame.draw.circle(
                    surface, 
                    color, 
                    (int(particle['x']), int(particle['y'])), 
                    size
                )
                
    def _draw_geometric_pattern(self, surface):
        """Pattern géométrique"""
        center_x, center_y = self.motion_center
        
        num_shapes = int(5 + self.motion_intensity * 10)
        
        for i in range(num_shapes):
            angle = (i / num_shapes) * 2 * math.pi + self.time_offset
            radius = 100 + self.motion_intensity * 200
            
            x = center_x + math.cos(angle) * radius
            y = center_y + math.sin(angle) * radius
            
            if 0 <= x < self.width and 0 <= y < self.height:
                size = int(20 + self.motion_intensity * 30)
                color = self.colors[i % len(self.colors)]
                
                # Dessiner des formes rotatives
                points = []
                for j in range(6):  # Hexagone
                    point_angle = angle + (j / 6) * 2 * math.pi
                    px = x + math.cos(point_angle) * size
                    py = y + math.sin(point_angle) * size
                    points.append((px, py))
                    
                if len(points) > 2:
                    pygame.draw.polygon(surface, color, points)
                    
    def update_and_draw(self):
        """Met à jour et dessine le pattern"""
        self.time_offset += 0.016  # ~60 FPS
        
        # Fond avec fade
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.set_alpha(50)
        fade_surface.fill((0, 0, 0))
        self.screen.blit(fade_surface, (0, 0))
        
        # Dessiner le pattern actuel
        self.pattern_functions[self.pattern_mode](self.screen)
        
        # Changer de pattern en fonction de l'intensité
        if self.motion_intensity > 0.8:
            self.pattern_mode = (self.pattern_mode + 1) % len(self.pattern_functions)
            
        pygame.display.flip()
        
    def handle_events(self):
        """Gère les événements pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.pattern_mode = (self.pattern_mode + 1) % len(self.pattern_functions)
                    
        return True
        
    def cleanup(self):
        """Nettoie les ressources"""
        pygame.quit()
