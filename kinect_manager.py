#!/usr/bin/env python3
"""
Gestionnaire Kinect pour Raspberry Pi
"""

import freenect
import cv2
import numpy as np
import threading
import time

class KinectManager:
    def __init__(self):
        self.depth_data = None
        self.rgb_data = None
        self.running = False
        self.depth_threshold = 1000  # mm
        self.movement_threshold = 30
        self.previous_depth = None
        self.motion_mask = None
        
    def depth_callback(self, dev, depth, timestamp):
        """Callback pour les données de profondeur"""
        # Conversion en format utilisable
        depth_processed = depth.astype(np.uint8)
        
        # Detection de mouvement
        if self.previous_depth is not None:
            diff = cv2.absdiff(depth_processed, self.previous_depth)
            _, self.motion_mask = cv2.threshold(diff, self.movement_threshold, 255, cv2.THRESH_BINARY)
            
        self.previous_depth = depth_processed.copy()
        self.depth_data = depth_processed
        
    def rgb_callback(self, dev, rgb, timestamp):
        """Callback pour les données RGB"""
        self.rgb_data = rgb
        
    def start(self):
        """Démarre la capture Kinect"""
        self.running = True
        
        try:
            freenect.set_depth_callback(self.depth_callback)
            freenect.set_rgb_callback(self.rgb_callback)
            
            freenect.set_depth_mode(freenect.DEPTH_11BIT)
            freenect.set_rgb_mode(freenect.RGB_RGB)
            
            print("Kinect initialisée avec succès")
            
            # Boucle principale
            while self.running:
                freenect.process_events()
                time.sleep(0.01)
                
        except Exception as e:
            print(f"Erreur Kinect: {e}")
            
    def stop(self):
        """Arrête la capture Kinect"""
        self.running = False
        freenect.shutdown()
        
    def get_motion_data(self):
        """Retourne les données de mouvement"""
        if self.motion_mask is None:
            return None, 0, (0, 0)
            
        # Calcul du centre de masse du mouvement
        moments = cv2.moments(self.motion_mask)
        if moments["m00"] != 0:
            center_x = int(moments["m10"] / moments["m00"])
            center_y = int(moments["m01"] / moments["m00"])
        else:
            center_x, center_y = 320, 240
            
        # Intensité du mouvement
        motion_intensity = np.sum(self.motion_mask) / 255.0
        
        return self.motion_mask, motion_intensity, (center_x, center_y)
