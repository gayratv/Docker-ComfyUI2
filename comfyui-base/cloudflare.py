import subprocess
import threading
import time
import socket
import urllib.request

def iframe_thread(port):
  while True:
      time.sleep(0.5)
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      result = sock.connect_ex(('127.0.0.1', port))
      if result == 0:
        break
      sock.close()
  # print("\nComfyUI finished loading, trying to launch cloudflared (if it gets stuck here cloudflared is having issues)\n")

  red_bold = "\033[1;31m"
  blue_bold = "\033[1;34m"
  reset_format = "\033[0m"
  text = "\nComfyUI finished loading, trying to launch cloudflared (if it gets stuck here cloudflared is having issues)\n"
  print(f"{blue_bold}{text}{reset_format}")

  p = subprocess.Popen(["cloudflared", "tunnel", "--url", "http://127.0.0.1:{}".format(port)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  for line in p.stderr:
    l = line.decode()
    if "trycloudflare.com " in l:
        http_link=l[l.find("http"):]
        end = ''
        print(f"{red_bold}This is the URL to access ComfyUI: {http_link}{reset_format}")
        # print("This is the URL to access ComfyUI:", l[l.find("http"):], end='')

# threading.Thread(target=iframe_thread, daemon=True, args=(8188,)).start()
#
# !python main.py --dont-print-server

if __name__ == "__main__":
    threading.Thread(target=iframe_thread, daemon=True, args=(8188,)).start()

    # Replace this with the appropriate way to run main.py based on your project setup.
    # If main.py is in the same directory and can be executed directly:
    subprocess.run(["python3", "main.py", "--dont-print-server"])

    # Alternatively, if you're within the project and want to run main.py as a module:
    # import main
    # main.main(['--dont-print-server'])
