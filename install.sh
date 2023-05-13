#!/bin/bash

# Install Scapy and its dependencies
sudo apt update
sudo apt install python3-pip libpcap-dev libpq-dev -y
sudo pip3 install scapy

# Check if Scapy is installed
if ! type "scapy" > /dev/null 2>&1; then
    echo "Scapy installation failed. Exiting..."
    exit 1
fi

echo "Scapy installation completed successfully."
