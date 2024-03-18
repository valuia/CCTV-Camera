import socket
import cv2
import pickle
import struct
import ex2

# Define the server host and port
SERVER_HOST = ex2.get_wifi_info()  # Replace 'server_ip_address' with the IP address of the server
SERVER_PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))

# OpenCV window to display the received video
cv2.namedWindow("Video")

while True:
    # Receive the size of the serialized frame
    data_size = client_socket.recv(4)
    if not data_size:
        break

    # Unpack the size of the serialized frame
    data_size = struct.unpack(">L", data_size)[0]

    # Receive the serialized frame data
    data = b""
    while len(data) < data_size:
        packet = client_socket.recv(data_size - len(data))
        if not packet:
            break
        data += packet

    # Deserialize the frame
    frame = pickle.loads(data)

    # Display the received frame
    cv2.imshow("Video", frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the OpenCV window and the connection with the server
cv2.destroyAllWindows()
client_socket.close()
