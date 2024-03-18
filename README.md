# CCTV Camera App

This repository contains a CCTV camera application built using Python. It consists of two main components:

- `main.py`: Sender application for the camera device using KivyMD.
- `cli.py`: Receiver application for the PC device.

## Installation

To run the CCTV camera application, ensure you have Python installed on your system. Then, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/valuia/CCTV-Camera.git
    ```

2. Navigate to the project directory:

    ```bash
    cd CCTV-Camera
    ```

3. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Sender (Camera Device)

Run `main.py` to start the sender application on the camera device. This application uses KivyMD for the user interface.

```bash
python main.py
```

### Receiver (PC Device)

Run `cli.py` to start the receiver application on the PC device.

```bash
python cli.py
```

## Requirements

- pickle
- socket
- struct
- threading
- webbrowser
- kivy
- kivymd

## License

This project is not licensed.

## Disclaimer

This CCTV camera application is developed for educational purposes. Use it responsibly and ensure compliance with local laws and regulations regarding surveillance and privacy. The developers hold no responsibility for any misuse of this software.
