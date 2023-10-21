# Chat Room with RSA Encryption

This is a simple chat room application implemented in Python using asyncio and RSA encryption. The chat room consists of a server and multiple clients. Messages sent between clients and the server are encrypted with RSA for secure communication.

## Features

- Server-client architecture for group messaging.
- RSA encryption for secure communication.
- Basic error handling.

## Requirements

- Python 3.7 or later.
- The `rsa` library. Install it using `pip install cryptography`.

## Installation

Clone the repository:

   ```shell
   git clone https://github.com/nihat123445/Chat-Room.git
   cd Chat-Room
```

## Usage

1. Run the server:

    ```shell
    pyhton server.py
    ```
    The server will start listening for incoming connections on 127.0.0.1:12345.

2. Run the client:

    ```shell
    python client.py
    ```
    - The client will prompt you to enter a message. Type your message and press Enter.
    - To exit the client, type "exit" and press Enter.
    - Messages are encrypted using RSA before being sent to the server.

## Configuration

- To modify the RSA key size or other parameters, you can update the relevant parts of the code in both the server and client scripts.
- Ensure the client has access to the server's public key for encryption.
- For production use, additional error handling and security measures are recommended.

## Contributing

1. Fork the repository on GitHub.
2. Clone your fork locally.
3. Create a new branch with a descriptive name.
4. Make your changes and commit them.
5. Push the changes to your fork on GitHub.
6. Create a pull request from your fork to the main repository.



