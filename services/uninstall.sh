#!/bin/bash

# Check root
if [ "$(id -u)" -ne 0 ]; then
  echo "🥷  Please, execute as root"
  exit 1
fi

# Check if python is installed
echo "🐍 Checking python version..."
if ! python3 --version ; then
    echo "Python3 is not installed"
    exit 1
fi
echo "Done"$'\n'

# Removing python requirements
DIR="/usr/bin/datalogger"
cd ${DIR}
echo "🗑  Removing python requirements"
if ! python3 -m pip uninstall -y -r requirements.txt; then
    exit 1
fi
echo "Done"$'\n'

# Removing files in DIR
echo "🗑  Removing config files in ${DIR}..."
rm -drf ${DIR}
echo "Done"$'\n'

# Stoping services
echo "🛑 Stoping all previous services"
sudo systemctl stop datalogger.service file-server.service hotspot.service pfi.service
echo "Done"$'\n'

# Removing services
echo "🗑  Removing services"
rm -f "/etc/systemd/system/datalogger.service"

# Reload daemon and display status
systemctl daemon-reload
systemctl status datalogger.service file-server.service hotspot.service pfi.service
echo "Done"$'\n'

echo "✅ Service was uninstalled successfully"$'\n'
