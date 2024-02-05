import tkinter as tk
from tkinter import ttk
from zeroconf import ServiceBrowser, Zeroconf, ServiceListener, ServiceInfo
import socket
import time

SERVICE_TYPE = "_https._tcp.local."

def get_ip_address():
    # Получаем IP-адрес устройства
    return socket.gethostbyname(socket.gethostname())

def register_service():
    ip_address = get_ip_address()
    service_name = ip_address
    service_type = SERVICE_TYPE
    service_port = 8080

    info = ServiceInfo(
        type_=service_type,
        name="{}.{}".format(service_name, service_type),
        port=service_port,
        properties={"info": "Additional information about the device"}
    )

    zeroconf = Zeroconf()
    zeroconf.register_service(info, allow_name_change=True)

    print("Service '{}' registered on port {}".format(service_name, service_port))

    time.sleep(2)

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
        info = zeroconf.get_service_info(type_, name, timeout=5)
        print('\n', info)
        self.services[name] = {"port": 80}
        print(f"Service {name} added")
        self.show_services()

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")
    
    def show_services(self):
        tree.delete(*tree.get_children())
        for name, service in self.services.items():
            tree.insert("", "end", values=(name, service["port"]))


print(socket.gethostname())
zeroconf = register_service()
listener = MyListener()


browser = ServiceBrowser(zeroconf, SERVICE_TYPE, listener)

# Создаем основное окно Tkinter
root = tk.Tk()
root.title("Service Browser")

# Создаем и размещаем виджет Treeview для отображения сервисов
tree = ttk.Treeview(root, columns=("Name", "Address", "Port"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Address", text="Address")
tree.heading("Port", text="Port")
tree.pack(padx=10, pady=10)

# Создаем кнопку "Show" для отображения сервисов
show_button = tk.Button(root, text="Show", command=listener.show_services())
show_button.pack(pady=10)

# Регистрируем сервис и создаем объект MyListener

# Создаем ServiceBrowser для поиска сервисов

# Запускаем главный цикл Tkinter
root.mainloop()

# Закрываем zeroconf при выходе из главного цикла
zeroconf.close()