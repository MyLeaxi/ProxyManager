import socket
import threading
import http.client

proxies = [
    "62.112.11.200:11843:12557354-all-country-US:12557354-all-country-US",
    "109.236.80.210:12031:12557360-all-country-TR:12557360-all-country-TR"
]

local_host = '127.0.0.1'
local_port = 8888

def handle_client(client_socket):
    proxy = proxies.pop(0).split(':')
    proxy_ip = proxy[0]
    proxy_port = int(proxy[1])
    proxy_user = proxy[2]
    proxy_pass = proxy[3]

    proxy_connection = http.client.HTTPConnection(proxy_ip, proxy_port)

    try:
        while True:
            request = client_socket.recv(4096)

            if len(request) == 0:
                break

            proxy_connection.request("GET", "/", body=request)

            response = proxy_connection.getresponse()

            client_socket.send(response.read())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        proxy_connection.close()
        proxies.append(':'.join(proxy))

def start_proxy_server():
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.bind((local_host, local_port))
    proxy_server.listen(5)
    print(f"[+] Proxy Server Listening on {local_host}:{local_port}")

    while True:
        client_socket, addr = proxy_server.accept()
        print(f"[+] Accepted connection from {addr[0]}:{addr[1]}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_proxy_server()
