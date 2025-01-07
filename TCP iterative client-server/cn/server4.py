import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ServerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Server")
        
        self.chat_display = scrolledtext.ScrolledText(master)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.message_entry = tk.Entry(master)
        self.message_entry.pack(padx=10, pady=10, fill=tk.X, expand=True)
        
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)
        
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
        self.server_socket.bind(('localhost', 12345))  # Replace with your server IP
        self.server_socket.listen(5)

        self.chat_display.tag_config('right', justify='right')
        self.chat_display.tag_config('left', justify='left')
        
        threading.Thread(target=self.accept_connections).start()
        
    def accept_connections(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, client_socket, client_address):
        self.chat_display.insert(tk.END, f"New connection from {client_address}\n", 'right')
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.chat_display.insert(tk.END, f"Client {client_address}: {message}\n", 'right')
                self.broadcast_message(message, client_socket)
            except:
                break
        client_socket.close()
        self.clients.remove(client_socket)
        self.chat_display.insert(tk.END, f"Connection with {client_address} closed.\n", 'right')
    
    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.message_entry.delete(0, tk.END)
            self.chat_display.insert(tk.END, f"Server: {message}\n", 'left')
            self.broadcast_message(f"Server: {message}")
    
    def broadcast_message(self, message, sender_socket=None):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.sendall(message.encode('utf-8'))
                except:
                    client.close()
                    self.clients.remove(client)

def main():
    root = tk.Tk()
    app = ServerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
