#!/bin/bash

# Agregar directori 'proto' al sys.path
PROTO_ABS_DIR=$(realpath "./proto")
export PYTHONPATH="$PROTO_ABS_DIR:$PYTHONPATH"

# Funció per comprovar si un port està lliure
port_is_free() {
    netstat -tuln | grep ":$1 " > /dev/null
    return $?
}

# Funció per obtenir un port aleatori
get_random_port() {
    local port
    while true; do
        port=$((RANDOM % 65536))
        port_is_free $port
        if [ $? -eq 1 ]; then
            echo $port
            break
        fi
    done
}

# Funció per iniciar RabbitMQ si no està en execució
start_rabbitmq() {
    docker ps | grep rabbitmq > /dev/null
    if [ $? -ne 0 ]; then
        gnome-terminal --title RabbitMQ -e "docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management" 2> /dev/null
    fi
}

# Obtenir IP
ip=$(hostname -I | awk '{print $1}')

# Generar port aleatori
port=$(get_random_port)

# Iniciar RabbitMQ
start_rabbitmq

# Engegar client
gnome-terminal -- python3 client/client.py --ip $ip --port $port 2> /dev/null
#python3 client/client.py --ip $ip --port $port