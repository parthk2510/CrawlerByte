from stem import Signal
from stem.control import Controller
from selenium import webdriver
import time

# Start Tor service
tor_process = None

try:
    from stem.process import launch_tor_with_config

    tor_process = launch_tor_with_config(
        tor_cmd=r'C:\Users\kpart\Desktop\Tor Browser\Browser\firefox.exe',
        config={
            'SocksPort': '9050',
        },
    )
except ImportError:
    print("Please make sure 'stem' library is installed.")

PROXY = "socks5://localhost:9050"  # IP:PORT or HOST:PORT
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % PROXY)
driver = webdriver.Chrome(
    chrome_options=options, executable_path=r'C:\Users\kpart\Desktop\Codewithharrycrawler'
)
driver.get("https://httplib2.readthedocs.io/en/latest/libhttplib2.html#http-objects")

# Pause for a few seconds to give the page time to load and display the result
time.sleep(5)

# Check if the page contains the text "Congratulations."
if "Congratulations" in driver.page_source:
    print("Tor is working with Chrome.")
else:
    print("Tor is NOT working with Chrome.")

# Close the browser
driver.quit()

# Stop Tor service
if tor_process:
    tor_process.kill()
