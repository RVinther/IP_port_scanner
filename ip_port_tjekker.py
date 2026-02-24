import subprocess
import platform
import socket
import ipaddress

class Device:

    def __init__(self, ip, ports=None):
        self.ip = ip
        self.ports = ports or []

    def ping(self):
        os_name = platform.system().lower()
        flag = "-n" if os_name == "windows" else "-c"
        result = subprocess.run(["ping", flag, "1", self.ip], capture_output=True, text=True)
        status = "ONLINE" if result.returncode == 0 else "OFFLINE"
        print(f"IP {self.ip} er {status}!")

    def scan_ports(self):
        for p in self.ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                r = sock.connect_ex((self.ip, p))
                status = "ÅBEN" if r == 0 else "LUKKET"
                print(f"Port {p} på IP {self.ip} er {status}!")

def val_port():
    ports = []
    while True:
        try:
            port = input("Indtast port(e) ('done' for at afslutte) > ").strip().lower()

            if port == "done":
                return ports

            if not port:
                raise ValueError("Ingen port eller 'done' indtastet!")
            else:
                port = int(port)
                if not 1 <= port <=65535:
                    raise ValueError(f"Porten {port} er ikke i det gyldige interval (1-65535)!")
                elif port in ports:
                    raise ValueError(f"Porten {port} er allerede på scan-listen!")
        except ValueError as e:
            print(f"Fejl: {e}")
            continue
        else:
            ports.append(port)
            print(f"Porten {port} tilføjet til scan-liste!")

def val_ip():
    while True:
        try:
            ip = input("Indtast IP > ").strip()
            if not ip:
                raise ValueError("Du har ikke indtastet noget!")
            ipaddress.ip_address(ip)
        except ValueError as e:
            print(f"Fejl: {e}")
            continue
        else:
            return ip
        
def main():
    print("Starter program...")
    while True:
        print("=== MENU ===")
        print("1. Ping IP")
        print("2. Scan port(e)")
        print("3. Afslut")
        
        valg = input("Vælg > ").strip()

        if valg == "1":
            resultat = val_ip()
            d = Device(ip=resultat)
            d.ping()

        elif valg == "2":
            resultat1 = val_ip()
            print(f"IP {resultat1} tilføjet!")
            resultat2 = val_port()
            d = Device(ip=resultat1, ports=resultat2)
            d.scan_ports()

        elif valg == "3":
            print("Afslutter program...")
            break

        else:
            print("Ugyldigt input. Prøv igen!")

if __name__ == "__main__":
    main()