import asyncio
import rsa

async def handle_client(reader, writer):
    while True:
        # Prompt the user for a message to send
        message = input("Enter a message to send to the server: ")
        if message.lower() == "exit":
            break

        # Encrypt the message using the server's public key (obtained securely)
        encrypted_message = rsa.encrypt(message.encode(), server_public_key)

        # Send the encrypted message to the server
        writer.write(encrypted_message)
        await writer.drain()

async def main():
    client = await asyncio.open_connection('127.0.0.1', 8888)

    reader, writer = client

    while True:
        data = await reader.read(100)

        # Decrypt the received message using the client's private key
        decrypted_message = rsa.decrypt(data, client_private_key).decode()
        print(f"Received from server: {decrypted_message}")

    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    # Load your RSA key pair for the client (private_key, public_key)
    client_private_key, client_public_key = rsa.newkeys(512)

    # The server's public key should be obtained securely.
    # Load it here (server_public_key) or share it from a secure source.

    asyncio.run(main())
