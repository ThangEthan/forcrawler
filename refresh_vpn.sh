#!/bin/zsh
timeout 30 nordvpn c $(shuf -n 1 ~/server.txt)
while [[ $? -eq 1 ]];
do
	timeout 30 nordvpn c $(shuf -n 1 ~/server.txt)
done
	
