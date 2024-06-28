import socket
import pyaudio
import groq_api
# Connect to server
server_address = ('localhost', 12343)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print(f"Connecting to producer at {server_address}")
sock.connect(server_address)
# Initialize PyAudio for audio playback
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)

try:
    groq = groq_api.GroqAPI()
    while True:
        data = sock.recv(1024)
        if data:
            # print(f"User: {data.decode()}")
            # message = input("Enter text to synthesize (or 'exit' to quit): ")

            print("User: ", data.decode())
            response = groq.request(data.decode())
            print("Ai", response)

            client_socket.sendall(response.encode('utf-8'))

            while True:
                try:
                    chunk = client_socket.recv(1024)
                    stream.write(chunk)
                    if len(chunk) < 1024:
                        break
                except Exception as e:
                    print(f"Error occurred during stream write: {e}")
                    break
            if response.lower() == 'exit':
                break

            print("Finished playing audio.")
    
    print("Exiting the program.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Close the connection and clean up
    client_socket.close()
    stream.stop_stream()
    stream.close()
    pa.terminate()
