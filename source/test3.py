import socket
ipaddress=socket.gethostbyname(socket.gethostname())
if ipaddress=="127.0.0.1":
    print("You are not connected to the internet!")
else:
    print("You are connected to the internet with the IP address of "+ ipaddress )