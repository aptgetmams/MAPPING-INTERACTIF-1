# Configuration et lancement

Structure des fichiers : 

/home/pi/kinect_patterns/

main.py

kinect_manager.py

pattern_generator.py

install.sh

README.md

2. Installation

# Copier les fichiers sur le Raspberry Pi + Rendre le script d'installation exécutable
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
