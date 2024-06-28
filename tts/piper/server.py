import socket
import json
import custom_piper_lib
import onnxruntime


with open('../../config.json') as f:
    config = json.load(f) 
# Server configuration
HOST = 'localhost'  # Server IP address or 'localhost'
PORT = int(config["tts"]["piper"]["port"])       # Port to listen on

def start_server():
    onnx_model_path = 'en_US-ryan-high.onnx'
    options = onnxruntime.SessionOptions()
    options.enable_mem_reuse = False
    session = onnxruntime.InferenceSession(onnx_model_path, options)
    
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Enable server to accept connections
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            while True:
                # Receive data from client
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # Decode received data
                received_msg = data.decode('utf-8')
                print(f"Received from client: {received_msg}")
                
                # Perform inference to get audio data
                audio_output = custom_piper_lib.synthesized(session, received_msg, onnx_model_path)
                
                # Check if audio_output is bytes
                if isinstance(audio_output, bytes):
                    # Send audio data back to client
                    print("sending bytes to client")
                    client_socket.sendall(audio_output)
                else:
                    print("Error: Audio data not in expected bytes format.")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close client connection
            client_socket.close()

    # Close the server socket (unreachable in this example)
    server_socket.close()

if __name__ == '__main__':
    start_server()
