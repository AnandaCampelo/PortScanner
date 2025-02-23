import socket
import argparse
import sys
import ipaddress

# Dicionário de portas conhecidas e serviços
WELL_KNOWN_PORTS = {
    20: "FTP (Data)",
    21: "FTP (Control)",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    # Adicione mais portas conforme necessário
}

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            return "Open"
        else:
            return "Closed"
    except Exception as e:
        return f"Filtered ({e})"
    finally:
        sock.close()

def scan_udp_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.5)
        sock.sendto(b'', (ip, port))
        data, addr = sock.recvfrom(1024)
        return "Open"
    except socket.timeout:
        return "Closed"
    except Exception as e:
        return f"Filtered ({e})"
    finally:
        sock.close()

def detect_os(ip):
    try:
        # Tenta se conectar a portas comuns e capturar banners
        banners = {}
        common_ports = [21, 22, 80, 443]  # Portas comuns para banner grabbing

        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect((ip, port))
                sock.send(b"GET / HTTP/1.1\r\n\r\n")  # Envia uma solicitação HTTP (para portas 80/443)
                banner = sock.recv(1024).decode().strip()
                banners[port] = banner
                sock.close()
            except:
                continue

        # Analisa os banners para tentar identificar o sistema operacional
        if 22 in banners and "SSH" in banners[22]:
            return "Linux/Unix (SSH)"
        elif 80 in banners and "Apache" in banners[80]:
            return "Linux/Unix (Apache)"
        elif 80 in banners and "IIS" in banners[80]:
            return "Windows (IIS)"
        elif 21 in banners and "FTP" in banners[21]:
            return "Possivelmente Linux/Unix (FTP)"
        else:
            return "Sistema operacional não identificado"
    except Exception as e:
        return f"Erro ao detectar sistema operacional: {e}"

def main():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument("target", help="Target IP address or network (CIDR notation)")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000) or single port (e.g., 80)", default="1-1024")
    parser.add_argument("-u", "--udp", help="Scan UDP ports", action="store_true")
    parser.add_argument("-6", "--ipv6", help="Enable IPv6 support", action="store_true")
    parser.add_argument("-o", "--os", help="Detect operating system", action="store_true")
    args = parser.parse_args()

    try:
        # Verifica se o alvo é uma rede CIDR ou um IP único
        if '/' in args.target:
            network = ipaddress.ip_network(args.target, strict=False)
            targets = network.hosts()
        else:
            targets = [ipaddress.ip_address(args.target)]
    except ValueError:
        print("Invalid IP address or network")
        sys.exit(1)

    # Verifica se o intervalo de portas é único ou um intervalo
    if '-' in args.ports:
        start_port, end_port = map(int, args.ports.split('-'))
        single_port = False
    else:
        start_port = end_port = int(args.ports)
        single_port = True

    for target in targets:
        print(f"\nScanning target: {target}")
        print(f"Port range: {start_port}-{end_port}")
        print(f"Protocol: {'UDP' if args.udp else 'TCP'}")
        print("=" * 40)

        for port in range(start_port, end_port + 1):
            if args.udp:
                status = scan_udp_port(str(target), port)
            else:
                status = scan_port(str(target), port)

            # Exibe a porta se for única ou se estiver aberta
            if single_port or status == "Open":
                service = WELL_KNOWN_PORTS.get(port, "Unknown")
                print(f"Port {port}: {status} - {service}")

        # Detecção de sistema operacional
        if args.os:
            print("\nDetecting operating system...")
            os_info = detect_os(str(target))
            print(f"Detected OS: {os_info}")

if __name__ == "__main__":
    main()