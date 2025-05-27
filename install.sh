#!/bin/bash

echo "=== Installation Kinect Patterns pour Raspberry Pi ==="

# Vérification des droits root
if [ "$EUID" -ne 0 ]; then
    echo "Veuillez exécuter en tant que root (sudo)"
    exit 1
fi

# Mise à jour du système
echo "Mise à jour du système..."
apt update && apt upgrade -y

# Installation des dépendances système
echo "Installation des dépendances..."
apt install -y \
    build-essential \
    cmake \
    pkg-config \
    libusb-1.0-0-dev \
    python3-dev \
    python3-pip \
    python3-numpy \
    git \
    freeglut3-dev \
    libxmu-dev \
    libxi-dev

# Installation de libfreenect
echo "Installation de libfreenect..."
cd /opt
git clone https://github.com/OpenKinect/libfreenect.git
cd libfreenect
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j4
make install
ldconfig

# Configuration udev pour Kinect
echo "Configuration des permissions Kinect..."
cp ../platform/linux/udev/51-kinect.rules /etc/udev/rules.d/
udevadm control --reload-rules

# Installation des packages Python
echo "Installation des packages Python..."
pip3 install \
    opencv-python \
    pygame \
    Pillow \
    scipy

# Création du répertoire de travail
echo "Création du répertoire de travail..."
mkdir -p /home/mams/kinect_patterns
cd /home/mams/kinect_patterns

# Configuration de l'autostart (optionnel)
read -p "Voulez-vous configurer le démarrage automatique? (y/n): " -n 1 -r
echo
if [[  $ REPLY =~ ^[Yy] $  ]]; then
    echo "Configuration de l'autostart..."
    cat > /etc/systemd/system/kinect-patterns.service << EOF
[Unit]
Description=Kinect Patterns Generative
After=graphical.target

[Service]
Type=simple
User=mams
WorkingDirectory=/home/mams/kinect_patterns
ExecStart=/usr/bin/python3 main.py
Restart=always
Environment=DISPLAY=:0

[Install]
WantedBy=graphical.target
EOF

    systemctl enable kinect-patterns.service
fi

# Configuration GPU pour de meilleures performances
echo "Configuration GPU..."
if ! grep -q "gpu_mem=128" /boot/config.txt; then
    echo "gpu_mem=128" >> /boot/config.txt
fi

# Ajout de l'utilisateur au groupe plugdev
usermod -a -G plugdev mams

echo "Installation terminée!"
echo "Redémarrez le système et branchez votre Kinect"
echo "Les fichiers doivent être placés dans /home/pi/kinect_patterns/"
