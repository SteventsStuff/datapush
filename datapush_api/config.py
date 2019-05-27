import socket


class Config:
    SDA_HOST = "172.21.0.2"
    SDA_PORT = 5001
    SDA_CONNECT = socket.gethostbyname(socket.gethostname())

    SERVICE_HOST = "0.0.0.0"
    SERVICE_PORT = 18000
