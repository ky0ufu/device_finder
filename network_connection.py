from zeroconf import ServiceBrowser, Zeroconf, ServiceListener, ServiceInfo
import socket
import time

SERVICE_TYPE = "_https._tcp.local."

def register_service():
    service_name = "MyService"
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

    time.sleep(5)

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
        print(zeroconf)
        info = zeroconf.get_service_info(type_, name,timeout=5)
        print('\n', info)
        self.services[name] = {"port": 80}
        print(f"Service {name} added, address: {None}")
        self.show_services()

    
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")
    
    def show_services(self):
        print("\nList of available services:")
        for name, service in self.services.items():
            print("Service '{}', port={}".format(name, service["port"]))


register_service()

zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, SERVICE_TYPE, listener)

try:
    while True:
        command = input("Enter 'show' to display services, or press enter to exit: ")
        if command.lower() == "show":
            listener.show_services()
finally:
    zeroconf.close()