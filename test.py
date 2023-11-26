import socket

HOST = 'localhost'  # This is the server's IP address
PORT = 8081         # This is the port number you want to use

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific IP address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f'Server running on {HOST}:{PORT}')

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()

    # Receive the client's request
    request = client_socket.recv(1024).decode()

    # Split the request into lines
    request_lines = request.split('\r\n')

    # Get the request method
    method, path, version = request_lines[0].split()

    # Print the request line
    print(f'{method} {path} {version}')

    # Send the response
    response_body = '''
<!DOCTYPE html>
<html>
<body>

<h1>My First Heading</h1>

<p>My first paragraph.</p>

</body>
</html>
'''
    response_headers = [
        'HTTP/1.1 200 OK',
        'Content-Type: text/html; charset=utf-8',
        f'Content-Length: {len(response_body)}',
        'Connection: close',
    ]
    response = '\r\n'.join(response_headers) + '\r\n\r\n' + response_body
    client_socket.sendall(response.encode())

    # Close the connection
    client_socket.close()
