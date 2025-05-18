import socket
import time
import datetime
import concurrent.futures
import ipaddress
from colorama import Fore
from core.config import translate, config
from utils.helpers import clear, process_and_print_request, save_to_history, save_report, get_session

class NetworkOperations:
    @staticmethod
    def geoip():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('geolocation_ip', selected_lang)}{Fore.RESET}\n")
        ip = input(f"{Fore.MAGENTA}{translate('enter_ip', selected_lang)}: {Fore.RESET}")
        
        if ip:

            api_key = config.get("api_keys", {}).get("hackertarget", "")
            if api_key:
                url = f"https://api.hackertarget.com/geoip/?q={ip}&apikey={api_key}"
            else:
                url = f"https://api.hackertarget.com/geoip/?q={ip}"
            process_and_print_request(url)

    @staticmethod
    def reverseip():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('reverse_ip_lookup', selected_lang)}{Fore.RESET}\n")
        ip = input(f"{Fore.MAGENTA}{translate('enter_ip', selected_lang)}: {Fore.RESET}")
        
        if ip:

            api_key = config.get("api_keys", {}).get("hackertarget", "")
            if api_key:
                url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}&apikey={api_key}"
            else:
                url = f"https://api.hackertarget.com/reverseiplookup/?q={ip}"
            process_and_print_request(url)

    @staticmethod
    def asn_lookup():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('asn_lookup', selected_lang)}{Fore.RESET}\n")
        asn = input(f"{Fore.MAGENTA}{translate('enter_asn', selected_lang)}: {Fore.RESET}")
        
        if asn:

            api_key = config.get("api_keys", {}).get("hackertarget", "")
            if api_key:
                url = f"https://api.hackertarget.com/aslookup/?q={asn}&apikey={api_key}"
            else:
                url = f"https://api.hackertarget.com/aslookup/?q={asn}"
            process_and_print_request(url)

    @staticmethod
    def ip_privacy():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('privacy_api', selected_lang)}{Fore.RESET}\n")
        ip = input(f"{Fore.MAGENTA}{translate('enter_ip', selected_lang)}: {Fore.RESET}")
        
        if ip:
            url = f"http://ip-api.com/json/{ip}"
            process_and_print_request(url)

    @staticmethod
    def _scan_port(host, port, timeout=1):
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return {"port": port, "state": "open", "service": NetworkOperations._get_service_name(port)}
            else:
                return {"port": port, "state": "closed", "service": NetworkOperations._get_service_name(port)}
        except:
            return {"port": port, "state": "error", "service": NetworkOperations._get_service_name(port)}
    
    @staticmethod
    def _get_service_name(port):
        
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 
            80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 
            465: "SMTPS", 587: "SMTP/Submission", 993: "IMAPS", 995: "POP3S",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt",
            8443: "HTTPS-Alt", 1433: "MSSQL", 27017: "MongoDB"
        }
        return services.get(port, "Bilinmiyor")

    @staticmethod
    def port_scanner():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('port_scanner', selected_lang)}{Fore.RESET}\n")
        host = input(f"{Fore.MAGENTA}{translate('enter_ip_or_domain', selected_lang)}: {Fore.RESET}")
        
        if not host:
            return
            
        scan_type = input(f"{Fore.MAGENTA}{translate('scan_type', selected_lang)} (1={translate('common_ports', selected_lang)}, 2={translate('custom_port_range', selected_lang)}): {Fore.RESET}")
        timeout = config.get("settings", {}).get("default_timeout", 1)
        max_workers = config.get("settings", {}).get("max_concurrent_tasks", 10)
        
        ports = []
        if scan_type == "2":
            try:
                start_port = int(input(f"{Fore.MAGENTA}{translate('start_port', selected_lang)}: {Fore.RESET}"))
                end_port = int(input(f"{Fore.MAGENTA}{translate('end_port', selected_lang)}: {Fore.RESET}"))
                if 0 < start_port <= 65535 and 0 < end_port <= 65535 and start_port <= end_port:
                    ports = range(start_port, end_port + 1)
                else:
                    print(f"{Fore.RED}{translate('invalid_port_range', selected_lang)} (1-65535){Fore.RESET}")
                    input(f"\n{translate('continue_prompt', selected_lang)}")
                    clear()
                    return
            except ValueError:
                print(f"{Fore.RED}{translate('invalid_port_number', selected_lang)}{Fore.RESET}")
                input(f"\n{translate('continue_prompt', selected_lang)}")
                clear()
                return
        else:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 587, 993, 995, 1433, 3306, 3389, 5432, 8080, 8443, 27017]
        
        try:

            try:
                ipaddress.ip_address(host)

            except ValueError:

                host_ip = socket.gethostbyname(host)
                print(f"{Fore.YELLOW}{translate('hostname_resolved', selected_lang)}: {host} -> {host_ip}{Fore.RESET}")
            
            print(f"{Fore.YELLOW}{translate('scanning_ports', selected_lang)}: {host}...{Fore.RESET}")
            start_time = time.time()

            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_port = {
                    executor.submit(NetworkOperations._scan_port, host, port, timeout): port 
                    for port in ports
                }
                
                done = 0
                total = len(future_to_port)
                for future in concurrent.futures.as_completed(future_to_port):
                    done += 1
                    print(f"\r{translate('progress_info', selected_lang)}: {done}/{total} port tarandı ({int(done/total*100)}%)...", end="", flush=True)
                    result = future.result()
                    results.append(result)
            
            print("\n")
            end_time = time.time()
            scan_time = end_time - start_time

            open_ports = [r for r in results if r["state"] == "open"]
            print(f"{Fore.GREEN}{translate('open_ports', selected_lang)} ({len(open_ports)}):{Fore.RESET}")
            if open_ports:
                for port in sorted(open_ports, key=lambda x: x["port"]):
                    print(f"{Fore.GREEN}  - Port {port['port']}: {port['service']}{Fore.RESET}")
            else:
                print(f"{Fore.YELLOW}  {translate('no_open_ports', selected_lang)}{Fore.RESET}")
            
            print(f"\n{Fore.CYAN}{translate('scan_completed', selected_lang)} {scan_time:.2f} {translate('seconds', selected_lang)}.{Fore.RESET}")

            scan_data = {
                "host": host,
                "ports_scanned": len(ports),
                "open_ports": len(open_ports),
                "scan_time": f"{scan_time:.2f} sn",
                "results": results
            }
            
            save_to_history("port_scan", scan_data)
            
            if config.get("settings", {}).get("save_reports", True):
                save_report("port_scan", {
                    **scan_data,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
        except socket.gaierror:
            print(f"{Fore.RED}{translate('hostname_resolution_failed', selected_lang)}{Fore.RESET}")
        except socket.error as e:
            print(f"{Fore.RED}{translate('connection_failed', selected_lang)}: {e}{Fore.RESET}")
        except Exception as e:
            print(f"{Fore.RED}{translate('error', selected_lang)}: {e}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        clear() 