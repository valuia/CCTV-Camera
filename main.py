import pickle
import socket
import struct
import threading
import webbrowser

import cv2
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRectangleFlatIconButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar


class ClientApp(MDApp):
    def __init__(self):
        super().__init__()

    def build(self):
        self.screen = MDScreen()  # Add the Screen

        self.main_layout = MDBoxLayout(orientation="vertical", spacing=5, padding=5,
                                       md_bg_color=(0, 0, 0, 1))  # make the main_layout

        self.top_bar = MDTopAppBar(title="CCTV-Camera App", )
        self.top_bar.left_action_items = [["chevron-left", lambda x: self.Quit_Window("")]]
        self.top_bar.right_action_items = [["help", lambda button: self.about("")]]
        self.top_bar.line_color = (0, 0, 0, 1)
        self.top_bar.specific_text_color = (0, 0, 0, 1)
        self.top_bar.md_bg_color = (1, 1, 1, 1)

        self.main_layout.add_widget(self.top_bar)

        start_btn = MDRectangleFlatIconButton(icon="camera-wireless", text='Start the CAMERA',
                                              halign="center", pos_hint={"center_x": 0.5},
                                              size_hint=(0.7, 0.1), icon_color=(0.7, 0.7, 0.2, 1),
                                              theme_text_color="Custom", text_color=(1, 1, 1, 1), font_size="30")
        start_btn.on_release = self.start_camera
        self.main_layout.add_widget(start_btn)

        lbl = MDLabel(text="----------Information----------", font_style="H4", theme_text_color="Custom",
                      text_color=(0.5, 0.5, 0.5, 1), halign="center", size_hint=(1, 0.05))
        self.main_layout.add_widget(lbl)

        self.n_btn = MDRaisedButton(pos_hint={"center_x": 0.5}, on_release=self.connection_show)

        self.main_layout.add_widget(self.n_btn)

        self.screen.add_widget(self.main_layout)  # paste the main_layout in the screen

        Clock.schedule_interval(callback=self.check_connection, timeout=0.75)

        return self.screen  # return the Screen.

    def Quit_Window(self, param):
        self.stop()

    def about(self, param):
        self.messagebox("Help - How to Connect",
                        "[b]Step 1[/b] : This Method Required the Same Wifi-Connection on both Device [i](Phone and the PC)[/i].\n[b]Step 2[/b] : Then See [i]\"You Are Connected\"[/i].\n[b]Step 3[/b] : Then Tap The [i]\"Start Camera\"[/i] Button",
                        "try: [b]Phone to Phone[/b]")

    def messagebox(self, title, text, cmd_btn_text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRectangleFlatIconButton(
                    text="Cancel",
                    icon="close",
                    md_bg_color=(0.7, .2, 0, 1),
                    on_release=self.close_message_box),
                MDRectangleFlatIconButton(
                    text=cmd_btn_text,
                    icon="check",
                    md_bg_color=(0.2, 1, 0.2, 1),
                    on_release=self.process_action
                ),
            ],
        )
        self.dialog.open()

    def process_action(self, instance):  # call the self.Delete_clicked_user and dismiss the msg box

        self.dialog.dismiss()
        if self.dialog.title == "Help - How to Connect":

            self.messagebox("[b]Help - [i]How to Connect Phone to Phone[/i][/b]",
                            "Sorry, We are working on it. [i]Check Updates on:[/i]\n1. [b]Github:[/b] valuia\n2. [b]Instagram:[/b] valuia.",
                            "[b]Check-Updates![/b]")
        elif "Phone to Phone" in self.dialog.title:
            webbrowser.open_new_tab("https://github.com/valuia")

    def close_message_box(self, instance):  # cose the messagebox
        # print(f"{instance} is not Deleted")
        toast("Canceled")

        self.dialog.dismiss()

    def get_wifi_info(self):
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Connect to a remote server (doesn't send any data, just obtains local IP)
            s.connect(('8.8.8.8', 80))

            # Get local IP address
            local_ip = s.getsockname()[0]

            # Close the socket
            s.close()

            return local_ip
        except Exception as e:
            print("Error:", e)
            return None

    def START_CAMERA(self):

        # Define the host and port to listen on
        # Get local IP address (which might be the IP address of the connected WiFi network)
        local_ip = self.get_wifi_info()

        if local_ip:
            try:
                print("Local IP Address:", local_ip)
                HOST = f'{local_ip}'  # Listen on all available network interfaces
                PORT = 12345  # Choose a port number

                # Create a socket object
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Bind the socket to the host and port
                server_socket.bind((HOST, PORT))

                # Listen for incoming connections
                server_socket.listen()

                print(f"Server listening on {HOST}:{PORT}")

                while True:
                    # Accept a new connection
                    client_socket, client_address = server_socket.accept()
                    print(f"Connection from {client_address}")

                    # Initialize OpenCV video capture
                    cap = cv2.VideoCapture(0)

                    while cap.isOpened():
                        ret, frame = cap.read()

                        # Serialize the frame
                        data = pickle.dumps(frame)

                        # Send the size of the serialized frame
                        client_socket.sendall(struct.pack(">L", len(data)))

                        # Send the serialized frame data
                        client_socket.sendall(data)

                        # Break the loop if the 'q' key is pressed
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    # Release the camera and close the connection with the client
                    cap.release()
                    client_socket.close()

                # Close the server socket
                server_socket.close()
            except Exception as e:
                print(e)
        else:
            print("Failed to retrieve local IP address.")

    def start_camera(self, *args):
        # Start camera in a separate thread
        threading.Thread(target=self.START_CAMERA).start()

    def check_connection(self, dt):
        con = self.get_wifi_info()
        if con:
            self.n_btn.text = f"You are Connected to : {con}"
            self.n_btn.md_bg_color = (0.5, 0.7, 0.2, 1)
        else:
            self.n_btn.text = "You are Not Connected!"
            self.n_btn.md_bg_color = (0.7, 0.5, 0.2, 1)

    def connection_show(self, instance):
        data = str(instance.text).strip().split(":")
        print(data)
        ip = data[1]
        toast(f"Your Wifi-Public IPV4 IP is : {ip}")


if __name__ == '__main__':
    ClientApp.title = "CCTV-Camera"
    ClientApp().run()
