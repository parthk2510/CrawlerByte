import requests
import socks
import socket

def connect_to_tor():
    # Set up Tor proxy
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)  # Tor proxy address and port
    socket.socket = socks.socksocket

    # Check if Tor is working properly
    try:
        response = requests.get("https://check.torproject.org/")
        if "Congratulations. This browser is configured to use Tor." in response.text:
            print("Connected to Tor successfully.")
        else:
            print("Failed to connect to Tor.")
            raise ConnectionError("Failed to connect to Tor.")
    except Exception as e:
        print("Error connecting to Tor:", e)
        raise e

# Call this function to connect to Tor before starting the crawler
connect_to_tor()
