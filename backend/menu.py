import threading
# import socket
import requests
from tkinter import *
from backend.server import run
from backend import server
from backend.client import run_client2

def show_menu():

    def host_ip():
        try:
            host_addr = requests.get('https://api.ipify.org')
            return host_addr.text
        except requests.RequestException:
            return "Unable to retrieve public IP"
    # def host_ip():
    #     temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     temp.connect(("8.8.8.8", 80)) # connect to google dns
    #     host_address = temp.getsockname()[0] # Get the local IP address
    #     temp.close() # Close the socket
    #     return host_address

    host_address = host_ip()

    def show_window(frame):
        frame.tkraise()

    def back_ToMenu():
        server.stop_server()
        show_window(menu_frame)

    def host_game():
        delete_msg()
        # print("Hosting game...")
        address_text.config(text="Your IP Address is: " + host_address)
        address_text.pack(pady=10)
        show_window(host_frame)
        thread1 = threading.Thread(target=run, args=("0.0.0.0", 50558), daemon= True).start()

    def join_game():
        delete_msg()
        # print("Joining game...")
        back_button_join.pack(pady=10)
        join_ip.pack(pady=10)
        entered_ip.pack(pady=10)
        connect_button.pack(pady=20)
        show_window(join_frame)

    def connect_client():
        ip = entered_ip.get()
        connected_label.config("text=Connected. Waiting for host to start.")
        connected_label.pack(pady=10)
        run_client2(ip, 50558)

    def delete_msg():
        address_text.pack_forget()
        join_ip.pack_forget()
        entered_ip.pack_forget()
        entered_ip.delete(0, END)
        connect_button.pack_forget()
        back_button_join.pack_forget()
        connected_label.pack_forget()

    window = Tk()

    window.title("Deny and Conquer")
    window.geometry("1280x720")

    menu_frame = Frame(window, bg="white")
    host_frame = Frame(window, bg="white")
    join_frame = Frame(window, bg="white")

    for frame in (menu_frame, host_frame, join_frame):
        frame.place(relwidth=1, relheight=1)


    #  Main Menu UI
    host_button = Button(menu_frame, text="Host Game", font=("Arial",24, "bold"), bg="white", fg="black", command=host_game)
    host_button.pack(pady=80)

    join_button = Button(menu_frame, text="Join Game", font=("Arial", 24, "bold"), bg="white", fg="black", command=join_game)
    join_button.pack(pady=10)

    # Host User UI
    address_text = Label(host_frame, text="", font=("Arial", 16), bg="white", fg="black")
    address_text.pack(pady=10)

    back_button_host = Button(host_frame, text="Back to Menu", font=("Arial", 16), bg="white", fg="black", command=back_ToMenu)
    back_button_host.pack(pady=10)


    # Join User UI
    back_button_join = Button(join_frame, text="Back to Menu", font=("Arial", 16), bg="white", fg="black", command=back_ToMenu)

    join_ip = Label(join_frame, text="Enter Host IP Address: ", font=("Arial", 16), bg="white", fg="black")

    entered_ip = Entry(join_frame, font=("Arial", 16), bg="white", fg="black")

    connect_button = Button(join_frame, text="Connect", font=("Arial", 16), bg="white", fg="black",
                            command=connect_client)

    connected_label = Label(join_frame, text="", font=("Arial", 16), bg = "white", fg="green")



    show_window(menu_frame)

    window.mainloop()