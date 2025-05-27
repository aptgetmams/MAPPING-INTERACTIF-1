#!/usr/bin/env python3
"""
Application principale - Patterns génératifs réactifs Kinect
"""

import sys
import time
import threading
import signal
from kinect_manager import KinectManager
from pattern_generator import PatternGenerator

class KinectPatternApp:
    def __init__(self):
        self.kinect = KinectManager()
        self.pattern_gen = PatternGenerator(800, 600)
        self.running = False
        self.kinect_thread = None
        
    def signal_handler(self, signum, frame):
        """Gestionnaire pour arrêt propre"""
        print("\nArrêt en cours...")
        self.stop()
        sys.exit(0)
        
    def kinect_loop(self):
        """Boucle de traitement Kinect dans un thread séparé"""
        try:
            self.kinect.start()
        except Exception as e:
            print(f"Erreur dans le thread Kinect: {e}")
            
    def start(self):
        """Démarre l'application"""
        print("Démarrage de l'application...")
        
        # Configuration des signaux pour arrêt propre
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.running = True
        
        # Démarrage du thread Kinect
        self.kinect_thread = threading.Thread(target=self.kinect_loop)
        self.kinect_thread.daemon = True
        self.kinect_thread.start()
        
        print("Kinect démarrée, lancement des patterns...")
        
        # Boucle principale d'affichage
        clock = time.time()
        
        try:
            while self.running:
                # Récupération des données de mouvement
                motion_mask, motion_intensity, motion_center = self.kinect.get_motion_data()
                
                # Mise à jour du générateur de patterns
                if motion_mask is not None:
                    # Adaptation des coordonnées Kinect (640x480) vers écran (800x600)
                    adjusted_center = (
                        int(motion_center[0] * 800 / 640),
                        int(motion_center[1] * 600 / 480)
                    )
                    self.pattern_gen.update_motion_data(adjusted_center, motion_intensity)
                else:
                    # Pas de mouvement détecté, centre par défaut
                    self.pattern_gen.update_motion_data((400, 300), 0)
                
                # Mise à jour et affichage des patterns
                self.pattern_gen.update_and_draw()
                
                # Gestion des événements
                if not self.pattern_gen.handle_events():
                    break
                    
                # Limitation du framerate
                current_time = time.time()
                frame_time = current_time - clock
                if frame_time < 1/60:  # 60 FPS max
                    time.sleep(1/60 - frame_time)
                clock = time.time()
                
        except Exception as e:
            print(f"Erreur dans la boucle principale: {e}")
            
        finally:
            self.stop()
            
    def stop(self):
        """Arrête l'application proprement"""
        print("Arrêt de l'application...")
        self.running = False
        
        if self.kinect:
            self.kinect.stop()
            
        if self.pattern_gen:
            self.pattern_gen.cleanup()
            
        print("Application arrêtée.")

def main():
    """Point d'entrée principal"""
    print("=== Kinect Generative Patterns ===")
    print("Appuyez sur ESPACE pour changer de pattern")
    print("Appuyez sur ECHAP pour quitter")
    print("===================================")
    
    app = KinectPatternApp()
    
    try:
        app.start()
    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"Erreur fatale: {e}")
    finally:
        app.stop()

if __name__ == "__main__":
    main()
