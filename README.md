# Structure

/home/pi/kinect_patterns/

main.py

kinect_manager.py

pattern_generator.py

install.sh

README.md

# Installation

Copier les fichiers sur le Raspberry Pi 

Rendre le script d'installation exécutable
chmod +x install.sh

# Exécuter l'installation
sudo ./install.sh

# Créer un binding Python pour freenect (si nécessaire)
cd /opt/libfreenect/wrappers/python

sudo python3 setup.py install

# Lancement manuel
cd /home/pi/kinect_patterns

python3 main.py

# Ou si configuré en service
sudo systemctl start kinect-patterns.service

sudo systemctl status kinect-patterns.service

# Pour accès SSH distant
sudo systemctl enable ssh

# Configuration VNC pour interface graphique distante
sudo apt install realvnc-vnc-server

sudo systemctl enable vncserver-x11-serviced



# Instructions d'utilisation

Installation : Exécutez le script d'installation
Connexion : Branchez la Kinect avec son adaptateur secteur
Lancement : Démarrez l'application
Contrôles :
Bougez devant la Kinect pour générer des patterns
ESPACE : Changer de pattern
ECHAP : Quitter

# Dépannage
Erreurs communes :
"Kinect not found" : Vérifiez les connexions et les permissions USB
Performance lente : Réduisez la résolution et le nombre de particules
Import Error : Vérifiez l'installation de libfreenect

# Test de la Kinect
lsusb | grep "Xbox"

# Test des permissions
groups pi | grep plugdev

# Log des erreurs
journalctl -u kinect-patterns.service -f

Ce projet est maintenant prêt pour une Raspberry Pi 3B+ avec une carte SD 16Go. Il génère des patterns visuels réactifs au mouvement humain capté par la Kinect V1.
