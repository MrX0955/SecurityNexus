import socket
from colorama import Fore
from core.config import translate, config
from utils.helpers import clear, process_and_print_request, save_to_history

class DNSOperations:
    @staticmethod
    def reverse_dns():
        # Get language setting
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('reverse_dns', selected_lang)}{Fore.RESET}\n")
        ip = input(f"{Fore.MAGENTA}{translate('enter_ip', selected_lang)}: {Fore.RESET}")
        
        if ip:

            api_key = config.get("api_keys", {}).get("hackertarget", "")
            if api_key:
                url = f"https://api.hackertarget.com/reversedns/?q={ip}&apikey={api_key}"
            else:
                url = f"https://api.hackertarget.com/reversedns/?q={ip}"
            process_and_print_request(url)

    @staticmethod
    def dns_lookup():
        # Get language setting
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('dns_lookup', selected_lang)}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{translate('enter_domain', selected_lang)}: {Fore.RESET}")
        
        if domain:

            api_key = config.get("api_keys", {}).get("hackertarget", "")
            if api_key:
                url = f"https://api.hackertarget.com/dnslookup/?q={domain}&apikey={api_key}"
            else:
                url = f"https://api.hackertarget.com/dnslookup/?q={domain}"
            process_and_print_request(url)

    @staticmethod
    def zone_transfer():
        # Get language setting
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('zone_transfer', selected_lang)}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{translate('enter_domain', selected_lang)}: {Fore.RESET}")
        
        if domain:

            api_key = config.get("api_keys", {}).get("hackertarget", "")
            if api_key:
                url = f"https://api.hackertarget.com/zonetransfer/?q={domain}&apikey={api_key}"
            else:
                url = f"https://api.hackertarget.com/zonetransfer/?q={domain}"
            process_and_print_request(url)

    @staticmethod
    def dns_host_records():
        # Get language setting
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('dns_host_records', selected_lang)}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{translate('enter_domain', selected_lang)}: {Fore.RESET}")
        
        if domain:

            api_key = config.get("api_keys", {}).get("hackertarget", "")
            if api_key:
                url = f"https://api.hackertarget.com/hostsearch/?q={domain}&apikey={api_key}"
            else:
                url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
            process_and_print_request(url)

    @staticmethod
    def dns_records():
        # Get language setting
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('dns_records', selected_lang)}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{translate('enter_domain', selected_lang)}: {Fore.RESET}")
        
        if domain:

            api_key = config.get("api_keys", {}).get("hackertarget", "")
            if api_key:
                url = f"https://api.hackertarget.com/dnslookup/?q={domain}&apikey={api_key}"
            else:
                url = f"https://api.hackertarget.com/dnslookup/?q={domain}"
            process_and_print_request(url)

    @staticmethod
    def dmarc_lookup():
        # Get language setting
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('dmarc_lookup', selected_lang)}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{translate('enter_domain', selected_lang)}: {Fore.RESET}")
        
        if domain:
            try:
                print(f"{Fore.LIGHTYELLOW_EX}\n > {translate('waiting_results', selected_lang)}{Fore.LIGHTGREEN_EX}")
                
                try:
                    answers = socket.getaddrinfo(f"_dmarc.{domain}", None)
                    has_dmarc = True
                except:
                    has_dmarc = False
                    
                if has_dmarc:
                    print(f"\n{Fore.GREEN}DMARC {translate('record_found', selected_lang)}: {domain}{Fore.RESET}")
                else:
                    print(f"\n{Fore.RED}DMARC {translate('record_not_found', selected_lang)}: {domain}{Fore.RESET}")
                    
                save_to_history("dmarc_lookup", {
                    "domain": domain,
                    "has_dmarc": has_dmarc
                })
                
                input(f"\n{translate('continue_prompt', selected_lang)}")
                clear()
            except Exception as e:
                print(f"{Fore.RED}{translate('error', selected_lang)}: {e}{Fore.RESET}")
                input(f"\n{translate('continue_prompt', selected_lang)}")
                clear()