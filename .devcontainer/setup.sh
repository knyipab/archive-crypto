#!/usr/bin/env bash

sudo apt update
sudo apt upgrade -y
# curl -s -L https://raw.githubusercontent.com/microsoft/vscode-dev-containers/main/script-library/desktop-lite-debian.sh | sudo bash

pip install -r requirements.txt
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb -y
rm google-chrome-stable_current_amd64.deb
version=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget "https://chromedriver.storage.googleapis.com/$version/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip chromedriver
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
rm chromedriver_linux64.zip
