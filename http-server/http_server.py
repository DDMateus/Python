import socket  # Networking
import threading  # concurrency
import os  # File operations
import sys  # CLI args
import gzip  # Compression

# Constants for HTTP status lines
STATUS_200 = "HTTP/1.1 200 OK\r\n"
STATUS_201 = "HTTP/1.1 201 Created\r\n\r\n"
STATUS_404 = "HTTP/1.1 404 Not Found\r\n\r\n"

ENCODING_AVAILABLE = "gzip"

class HTTPServer:
    """
    A simple HTTP server to handle multiple HTTP requests
    """
    
    def __init__(self, address, port):
        """
        Initialize the server with an address and port 
        """
        self.address = address
        self.port = port
    
    def start(self):
        """
        Start TCP server socket to listen for incoming requests
        """
        socket_server = socket.create_server((self.address, self.port))
        print(f"Server is listening on {self.address}:{self.port}")
        
        while True:
            # Accept incoming connection
            (connection_socket, address) = socket_server.accept()
            print(f"Received connection from {address}")
            
            # Handle each connection in a new thread
            connection_thread = threading.Thread(target=self.handle_connection, args=(connection_socket, address))
            connection_thread.start()
    
    def handle_connection(self, connection_socket, address):
        """
        Handle the incoming client connection
        """
        try:
            # Receive and decode request data
            request_data = connection_socket.recv(4096).decode()
            print(f"Received request:\n{request_data}")
            
            # Parse the HTTP request data
            method, request_target, headers, request_body = self.parse_request(request_data)
            print(method, request_target)
            # Route requests to the proper handler
            if request_target == "/":
                self.send_response(connection_socket, "HTTP/1.1 200 OK\r\n\r\n")
            elif request_target.startswith("/user-agent"):
                self.handle_user_agent(connection_socket, headers)
            elif request_target.startswith("/echo"):
                self.handle_echo(connection_socket, request_target, headers)
            elif request_target.startswith("/files") and method == "GET":
                self.handle_get_files(connection_socket, request_target)
            elif request_target.startswith("/files") and method == "POST":
                self.handle_post_files(connection_socket, request_target, request_body)
            else:
                self.send_response(connection_socket, STATUS_404)
        except Exception as e:
            print(f"Error handling connection: {e}")
            self.send_response(connection_socket, STATUS_404)
        finally:
            connection_socket.close()
            
    def parse_request(self, request_data):
        """
        Parse the HTTP request and return the method, target, headers, and body
        """
        # Split request into lines
        lines = request_data.split("\r\n")
        print(lines)
        start_line = lines[0]
        method, request_target, http_version = start_line.split(" ")
        
        # Parse headers
        headers = {}
        for header in lines[1:-2]:
            if header == "":
                break
            key, value = header.split(": ")
            headers[key] = value
        
        # POST method comes with body
        request_body = lines[-1]
        return method, request_target, headers, request_body
    
    def send_response(self, connection_socket, status_line):
        """
        Send a simple HTTP response with the given status line
        """
        connection_socket.sendall(status_line.encode())    
        
    def handle_user_agent(self, connection_socket, headers):
        """
        Handles requests to the /user-agent endpoint
        """
        user_agent = headers.get("User-Agent", "Unknown")
        response_body = (
            f"{STATUS_200}" 
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(user_agent)}\r\n"
            "\r\n"
            f"{user_agent}"
        )
        connection_socket.sendall(response_body.encode())
    
    def handle_echo(self, connection_socket, request_target, headers):
        """
        Handles requests to the /echo endpoint
        """
        endpoint = request_target.split("/")[-1]
        if "Accept-Encoding" in headers and ENCODING_AVAILABLE in headers["Accept-Encoding"]:
            gzip_endpoint = gzip.compress(endpoint.encode())
            response = (
                f"{STATUS_200}" 
                f"Content-Encoding: {ENCODING_AVAILABLE}\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(gzip_endpoint)}\r\n"
                "\r\n"
            )
            connection_socket.sendall(response.encode() + gzip_endpoint)
        else:
            response = (
                f"{STATUS_200}" 
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(endpoint)}\r\n"
                "\r\n"
                f"{endpoint}"
            )
            connection_socket.sendall(response.encode())
            
    def handle_get_files(self, connection_socket, request_target):
        """
        Handle GET requests to the /files endpoint
        """
        filename = request_target.split("/")[2]
        directory = sys.argv[2] 
        file_path = "".join([directory, filename])
        
        # Check if file existsand is a file:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "rb") as file:
                content = file.read()
                response = (
                    f"{STATUS_200}" 
                    "Content-Type: application/octet-stream\r\n"
                    f"Content-Length: {len(content)}\r\n"
                    "\r\n"
                )
                
                connection_socket.sendall(response.encode() + content)
        else:
            self.send_response(connection_socket, STATUS_404)
    
    def handle_post_files(self, connection_socket, request_target, request_body):
        """
        Handle POST requests to the /file endpoint
        """
        filename = request_target.split("/")[2]
        directory = sys.argv[2] 
        
        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)
        
        file_path = "".join([directory, filename])
        
        # Write the request body to the file
        with open(file_path, "w") as file:
            file.write(request_body)
            
        self.send_response(connection_socket, STATUS_201)
        
def main():
    """
    Main function to start server
    """
    server = HTTPServer("localhost", 4221)
    server.start()

if __name__ == "__main__":
    main()
