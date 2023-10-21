import socket
import threading
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Client configuration
HOST = '127.0.0.1'
PORT = 12345
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

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

send_thread = threading.Thread(target=send_encrypted_message, args=(client,))
send_thread.start()

receive_thread = threading.Thread(target=receive_decrypted_messages, args=(client,))
receive_thread.start()
