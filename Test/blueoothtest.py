import bluetooth 
import time

def start_server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) 
    port = 22
    server_sock.bind(("", port)) 
    server_sock.listen(1) 
    print("Esperando conexión Bluetooth...")
    client_sock, address = server_sock.accept() 
    print("Conexión realizada con:", address) 
    return server_sock, client_sock

def main():
    server_sock, client_sock = start_server()
    
    while True:
        try:
            recvdata = client_sock.recv(1024)
            if not recvdata:
                print("El cliente se ha desconectado.")
                client_sock.close()
                server_sock.close()
                time.sleep(1)
                server_sock, client_sock = start_server()
                continue
            
            print("Información recibida:", recvdata.decode())
            if recvdata.decode() == "Q":
                print("Finalizado.")
                break
        except bluetooth.btcommon.BluetoothError as e:
            print("Error de Bluetooth:", e)
            print("Intentando reconectar...")
            client_sock.close()
            server_sock.close()
            time.sleep(1)
            server_sock, client_sock = start_server()

    client_sock.close()
    server_sock.close()

if __name__ == "__main__":
    main()

