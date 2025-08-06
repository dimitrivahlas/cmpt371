import threading
from tkinter import *
import socket
from backend.server import run
def show_menu():
    """
    returns IP of user
    """
    def host_ip():
        temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp.connect(("8.8.8.8", 80)) # connect to google dns
        host_address = temp.getsockname()[0] # Get the local IP address
        temp.close() # Close the socket
        return host_address

    def show_window(frame):
        frame.tkraise()

    def back_ToMenu():
        show_window(menu_frame)

    def host_game():
        delete_msg()
        # print("Hosting game...")
        address_text.config(text="Your IP Address is: " + host_ip())
        address_text.pack(pady=10)
        show_window(host_frame)

        thread1 = threading.Thread(target=run, args=(host_ip(), 50558), daemon= True).start()

    def join_game():
        delete_msg()
        # print("Joining game...")
        join_ip.pack(pady=10)
        entered_ip.pack(pady=5)
        show_window(join_frame)

    def delete_msg():
        address_text.pack_forget()
        join_ip.pack_forget()
        entered_ip.pack_forget()
        entered_ip.delete(0, END)


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
    join_ip = Label(join_frame, text="Enter Host IP Address: ", font=("Arial", 16), bg="white", fg="black")
    join_ip.pack(pady=10)
    entered_ip = Entry(join_frame, font=("Arial", 16), bg="white", fg="black")
    entered_ip.pack(pady=5)

    back_button_join = Button(join_frame, text="Back to Menu", font=("Arial", 16), bg="white", fg="black", command=back_ToMenu)
    back_button_join.pack(pady=10)

    show_window(menu_frame)

    window.mainloop()