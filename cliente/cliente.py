import socket
import sys
import uuid

mac_address = ':'.join(f'{(uuid.getnode() >> i) & 0xff:02x}' for i in range(0, 48, 8))
print(f"Dirección MAC de esta máquina: {mac_address}")

# Configuración del Proxy
PROXY_IP = sys.argv[1] if len(sys.argv) > 1 else "172.17.0.5"
PROXY_PORT = 4000
TERMINAL_IP = "172.17.0.2"
TERMINAL_PORT = 5001
PUERTO_ESPECIFICO = 5000

# Crear socket para enviar mensajes a la Terminal
terminal_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.bind(("0.0.0.0", PUERTO_ESPECIFICO))
    client_socket.connect((PROXY_IP, PROXY_PORT))

    proxy_response = client_socket.recv(1024).decode("utf-8")
    if "rechazada" in proxy_response.lower():
        print(proxy_response)
        terminal_socket.sendto(proxy_response.encode("utf-8"), (TERMINAL_IP, TERMINAL_PORT))
        client_socket.close()
        terminal_socket.close()
        sys.exit()

    print(proxy_response)

    client_name = input("Ingresa tu nombre: ")
    client_socket.sendall(client_name.encode("utf-8"))

    mensaje_terminal = f"{client_name} se ha conectado al proxy"
    terminal_socket.sendto(mensaje_terminal.encode("utf-8"), (TERMINAL_IP, TERMINAL_PORT))

    print(f"Conectado al proxy {PROXY_IP}:{PROXY_PORT}. Escribe 'exit' para salir.")

    while True:
        mensaje = input("Mensaje a enviar: ")
        client_socket.sendall(mensaje.encode("utf-8"))

        mensaje_terminal = f"{client_name}, ha enviado el mensaje '{mensaje}' al proxy"
        terminal_socket.sendto(mensaje_terminal.encode("utf-8"), (TERMINAL_IP, TERMINAL_PORT))

        if mensaje.lower() == "exit":
            break

        confirmacion = client_socket.recv(1024).decode("utf-8")
        print(f"-> Confirmación del servidor: {confirmacion}")

    client_socket.close()

except ConnectionRefusedError:
    mensaje_terminal = "Conexión rechazada: El proxy no está disponible o el puerto está bloqueado"
    print(mensaje_terminal)
    terminal_socket.sendto(mensaje_terminal.encode("utf-8"), (TERMINAL_IP, TERMINAL_PORT))

except OSError as e:
    mensaje_terminal = f"Error de conexión: {e}"
    print(mensaje_terminal)
    terminal_socket.sendto(mensaje_terminal.encode("utf-8"), (TERMINAL_IP, TERMINAL_PORT))

finally:
    terminal_socket.close()
    sys.exit()

