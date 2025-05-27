# Configuration adaptée au Raspberry Pi 3B+
PERFORMANCE_CONFIG = {
    'resolution': (640, 480),  # Résolution réduite pour de meilleures performances
    'max_particles': 50,       # Moins de particules
    'fps_target': 30,          # 30 FPS au lieu de 60
    'depth_sample_rate': 2,    # Échantillonnage de profondeur réduit
    'motion_blur_samples': 3,  # Moins d'échantillons pour le flou de mouvement
}

# Usage dans pattern_generator.py
def __init__(self, width=640, height=480):
    # Utiliser la configuration optimisée
    pass
