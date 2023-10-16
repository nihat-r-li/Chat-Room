import asyncio
import rsa

# Generate an RSA key pair for the server
private_key, public_key = rsa.newkeys(512)

# List to store connected clients
clients = []

async def handle_client(reader, writer):
    remote_address = writer.get_extra_info('peername')
    print(f"New connection from {remote_address}")

    # Add the client's writer to the list of clients
    clients.append(writer)

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break

            # Received data from a client
            message = data.decode()

            # Encrypt the received message using the server's public key
            encrypted_message = rsa.encrypt(message.encode(), public_key)
            print(f"Received: {message} from {remote_address}")

            # Send the encrypted message to all connected clients
            for client in clients:
                if client != writer:
                    client.write(encrypted_message)

            await writer.drain()

    except asyncio.CancelledError:
        pass

    finally:
        print(f"Connection closed from {remote_address}")

        # Remove the client's writer from the list of clients
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
