import requests
import socket
import cv2
import struct
import pickle

webhook_url = 'https://discordapp.com/api/webhooks/1279650252411899934/CMbqErpb4X_V8Tge84hrbip9mNcfZouev6MaqUEyJ4g3v0qRHptUJZ0_E5FRqE-p4hX6'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('<server ip address>', 6000)
client_socket.connect(server_address)
print(f'Connected to server at {server_address}')

message = {"content": "不審者？検出"}
data = b""
info_size = struct.calcsize("Q")
try:
    while True:
        while len(data) < info_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        
        info = data[:info_size]
        data = data[info_size:]
        data_size = struct.unpack("Q", info)[0]

        while len(data) < data_size:
            data += client_socket.recv(4096)
        frame_data = data[:data_size]
        data = data[data_size:]

        frame = pickle.loads(frame_data)
        if frame['detect']:
            response = requests.post(webhook_url, json=message)
            if response.status_code == 204:
                print("Message sent successfully")
            else:
                print(f"Failed to send message: {response.status_code} - {response.text}")

            cv2.imwrite('camera-image.jpg', frame['camera'])
            with open('camera-image.jpg', 'rb') as file:
                response = requests.post(webhook_url, data=message, files={'file': file})
            if response.status_code == 200:
                print("Image sent successfully")
            else:
                print(f"Failed to send image: {response.status_code} - {response.text}")

        cv2.imshow('Received Image', frame['camera'])

except (ConnectionResetError, ConnectionResetError, BrokenPipeError, TimeoutError) as e:
     print('Connection error: {e}')

finally:
    client_socket.close()
    cv2.destroyAllWindows()
