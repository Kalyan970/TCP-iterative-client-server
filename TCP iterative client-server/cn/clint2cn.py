import socket
import threading

def handle_receive(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Received from server: {message}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        client_socket.close()

def handle_send(client_socket):
    try:
        while True:
            message = input("Enter message to send: ")
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode('utf-8'))
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        client_socket.close()

def main():
    server_address = ('192.168.23.51', 12345)  # Replace with your server machine's actual IP address
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(server_address)
        print(f"Connected to server at {server_address}")

        receive_thread = threading.Thread(target=handle_receive, args=(client_socket,))
        send_thread = threading.Thread(target=handle_send, args=(client_socket,))
        receive_thread.start()
        send_thread.start()
        
        receive_thread.join()
        send_thread.join()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
