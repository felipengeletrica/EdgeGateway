#!/bin/bash

# Check root
if [ "$(id -u)" -ne 0 ]; then
  echo "🥷  Please, execute as root"
  exit 1
fi

# Install depedencies
echo "Install depedencies"
sudo apt-get install libcairo2-dev libjpeg-dev libgif-dev
sudo apt-get install cmake
sudo apt-get install libgirepository1.0-dev
sudo apt-get install libdbus-1-dev
sudo apt-get install bluetooth libbluetooth-dev

# Check if directory exists
DIR="/usr/bin/datalogger"
if [ ! -d "$DIR" ]; then
  echo "Directory ${DIR} not found, creating.."$'\n'
  mkdir ${DIR}
  mkdir ${DIR}/logs 
fi

# Check if git is installed
echo "🏷️  Checking git version..."
if ! git --version ; then
    echo "git is not installed"
    exit 1
fi
echo "Done"$'\n'

# Install files in DIR
echo "🔧 Installing config files in ${DIR}..."

if [ -f ${0##*/} ]; then
    cp -r '../' ${DIR}
    cd ${DIR}
else
    echo "📁 Are you in folder of ${0##*/} file?"
    exit 1
fi
echo "Done"$'\n'

# Check if python is installed
echo "🐍 Checking python installed..."
if ! python3 --version ; then
    echo "Python3 is not installed"
    exit 1
fi
echo "Done"$'\n'

# Install virtual env for application
echo "💻 Install virtual env for application"
python3 -m venv env
echo "Done"$'\n'

echo "✅ Activate environment"
source env/bin/activate
echo "Done"$'\n'

# Install python requirements for application
echo "📥 Installing python requirements for application"
if ! python3 -m pip install -r requirements.txt; then
    exit 1
fi
echo "Done"$'\n'

echo "--- Service is ready to be installed ---"

# Confirm
while true; do
    read -p "Do you wish to install these services now? [y/n]: " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Copying services files
echo "🚫 Stoping all previous services"
sudo systemctl stop datalogger.service
echo "Done"$'\n'

echo "🔧 Installing services"
cp "./services/datalogger.service" "/etc/systemd/system/"

# Add systemd to run the service at startup
systemctl daemon-reload
systemctl enable datalogger.service 
systemctl start datalogger.service  &
echo "Services were installed successfully"$'\n'

# Status of services
while true; do
    read -p "🤩 Would you like to see the status of services? [y/n]: " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "Datalogger services installed"
echo "Done"$'\n'

systemctl status datalogger.service