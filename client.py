import socket
import threading
import sys
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


if len(sys.argv) != 3:
        print("Usage: python script.py <ip_address> <port>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])



# Generation of RSA key pair for encryption
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# It is function to send encrypted messages
def send_encrypted_message(client_socket):
    while True:
        message = input("")
        ciphertext = public_key.encrypt(
            message.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        client_socket.send(ciphertext)

# This is function to receive and display decrypted messages from the server
def receive_decrypted_messages(client_socket):
    while True:
        ciphertext = client_socket.recv(2048)
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        ).decode('utf-8')
        print(">", plaintext)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Here we create threads for sending and receiving messages
send_thread = threading.Thread(target=send_encrypted_message, args=(client,))
send_thread.start()

receive_thread = threading.Thread(target=receive_decrypted_messages, args=(client,))
receive_thread.start()
