import tkinter as tk
from tkinter import ttk
from zeroconf import ServiceBrowser, Zeroconf, ServiceListener, ServiceInfo
import socket
import time
import platform

SERVICE_TYPE = "_devicees._tcp.local."

def get_ip_address():
    return socket.gethostbyname(socket.gethostname())

def register_service():
    ip_address = get_ip_address()
    service_name = f"{platform.system()}-{ip_address}"

    service_type = SERVICE_TYPE
    service_port = 8080

    info = ServiceInfo(
        type_=service_type,
        name="{}.{}".format(service_name, service_type),
        addresses=[ip_address],
        port=service_port,
        weight=0,
        priority=0,
        properties={"info": None}
    )

    zeroconf = Zeroconf()
    zeroconf.register_service(info, allow_name_change=True)
    info = zeroconf.get_service_info(SERVICE_TYPE, "{}.{}".format(service_name, service_type))

    time.sleep(1)

    return zeroconf


class MyListener(ServiceListener):

    def __init__(self):
        self.services = {}


    def remove_service(self, zeroconf, type, name):
        print(f"Service {name} removed")
        if name in self.services:
            del self.services[name]
        self.show_services()


    def add_service(self, zeroconf, type_, name):
        info = zeroconf.get_service_info(type_, name)

        ip = socket.inet_ntoa(info.addresses[0])
        self.services[name] = {"port": info.port, "ip": ip}

        print(f"Service {name} added")
        self.show_services()


    def update_service(self, zeroconf, type_, name):
        print(f"Service {name} updated")
    

    def show_services(self):
        tree.delete(*tree.get_children())
        for name, service in self.services.items():
            if service["ip"] == get_ip_address():
                continue
            tree.insert("", "end", values=(name.split('._')[0].split('-')[0], service["ip"]))



root = tk.Tk()
root.title("Service Browser")

tree = ttk.Treeview(root, columns=("Platform", "IP"), show="headings")
tree.heading("Platform", text="Platform")
tree.heading("IP", text="IP")
tree.pack(padx=10, pady=10)


zeroconf = register_service()
listener = MyListener()

browser = ServiceBrowser(zeroconf, SERVICE_TYPE, listener)

root.mainloop()

zeroconf.close()