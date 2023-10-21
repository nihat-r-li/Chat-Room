import socket
import threading
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

HOST = '127.0.0.1'
PORT = 12345
clients = []  # List to store connected client sockets

# Generation of RSA key pair for encryption
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# This is function to multicast encrypted messages to connected clients
def multicast_encrypted_message(client_socket, message):
    for client in clients:
        if client != client_socket:
            try:
                # Here we encrypt and send message
                ciphertext = client.encrypt(
                    message.encode('utf-8'),
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                )
                client.send(ciphertext)
            except:
                # Remove client in case of an error
                client.close()
                remove_client(client)

# This is function to handle a client's messages
def handle_client(client_socket):
    while True:
        try:
            # Here we receive and decrypt message
            ciphertext = client_socket.recv(2048)
            if ciphertext:
                plaintext = private_key.decrypt(
                    ciphertext,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None,
                    ),
                ).decode('utf-8')
                multicast_encrypted_message(client_socket, plaintext)
            else:
                remove_client(client_socket)
        except:
            continue

# This is function to remove a client from list
def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)
        client_socket.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("Chat server is running on port " + str(PORT))

# Here we create threads to handle them
while True:
    client_socket, client_addr = server.accept()
    clients.append(client_socket)
    print("Client connected from " + str(client_addr))
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
