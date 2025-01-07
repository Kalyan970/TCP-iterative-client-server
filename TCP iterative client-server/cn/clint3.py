import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ClientApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Client")
        
        self.chat_display = scrolledtext.ScrolledText(master)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.message_entry = tk.Entry(master)
        self.message_entry.pack(padx=10, pady=10, fill=tk.X, expand=True)
        
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=10)
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.23.51', 12345))  # Replace with your server IP
        
        threading.Thread(target=self.receive_messages).start()
    
    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.chat_display.insert(tk.END, f"Server: {message}\n")
            except:
                break
        self.client_socket.close()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.message_entry.delete(0, tk.END)
            self.client_socket.sendall(message.encode('utf-8'))
            self.chat_display.insert(tk.END, f"Client: {message}\n")

def main():
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
