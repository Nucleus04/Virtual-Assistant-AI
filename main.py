import socket
import pyaudio
from llm import groq_api
import json
# Connect to server
with open('config.json') as f:
        config = json.load(f)

piper_socket_address = ('localhost', int(config["tts"]["piper"]["port"]))
piper_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Connecting to stt", piper_socket_address)
piper_socket.connect(piper_socket_address)

coqui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', int(config["stt"]["coqui"]["port"]))
print(f"Connecting to tts at {server_address}")
coqui_socket.connect(server_address)


pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)


try:
    groq = groq_api.GroqAPI()
    while True:
        data = coqui_socket.recv(1024)
        if data:
            # print(f"User: {data.decode()}")
            # message = input("Enter text to synthesize (or 'exit' to quit): ")

            print("User: ", data.decode())
            response = groq.request(data.decode())
            print("Ai", response)

            piper_socket.sendall(response.encode('utf-8'))

            while True:
                try:
                    chunk = piper_socket.recv(1024)
                    stream.write(chunk)
                    if len(chunk) < 1024:
                        break
                except Exception as e:
                    print(f"Error occurred during stream write: {e}")
                    break
            if response.lower() == 'exit':
                break

            print("Finished playing audio.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Close the connection and clean up
    piper_socket.close()
    stream.stop_stream()
    stream.close()
    pa.terminate()
