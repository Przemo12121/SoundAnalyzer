# tensorflow_lite runtime
echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update
sudo apt-get install python3-tflite-runtime

# i2c, smbus
sudo apt-get install i2c-tools
sudo apt-get install python3-smbus
if ! [ $(cat "/etc/modules" | grep "i2c-dev") ]; then
    echo "i2c-dev" >> /etc/modules
fi

echo "Setup complete, reboot device using command 'reboot'"