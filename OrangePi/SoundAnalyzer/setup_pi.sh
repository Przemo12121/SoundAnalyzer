# tensorflow_lite runtime
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get -y update
sudo apt-get -y install python3-tflite-runtime

# i2c, smbus
sudo apt-get -y install i2c-tools
sudo apt-get -y install python3-smbus
if ! [ $(cat "/etc/modules" | grep "i2c-dev") ]; then
    echo "i2c-dev" >> /etc/modules
fi

# other required python packages
sudo apt-get -y install python3-pyaudio
python3 -m pip install python-dotenv
python3 -m pip install pydub

echo "Setup complete, reboot device using command 'reboot'"