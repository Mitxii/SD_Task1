#!/bin/bash

# Obtenir port del servidor
port=50000
while true
do 
    netstat -tuln | grep $port &> /dev/null
    if [ $? -eq 0 ]; then
        echo "El port $port ja està ocupat."
        port=$((port+1))
    else
        break
    fi
done

# Obtenir IP del servidor
ip=$(hostname -I | awk '{print $1}')

# Guardar variables al fitxer config
echo "server_ip: $ip" > config.yaml
echo "server_port: $port" >> config.yaml

# Agregar directori 'proto' al sys.path
PROTO_ABS_DIR=$(realpath "./proto")
export PYTHONPATH="$PROTO_ABS_DIR:$PYTHONPATH"

# Engegar servidor
gnome-terminal --title="SERVER" -- python3 server/server.py 2> /dev/null
#python3 server/server.py