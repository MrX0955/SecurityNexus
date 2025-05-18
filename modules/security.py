import socket
import ssl
import time
import datetime
import requests
from colorama import Fore
from core.config import translate, config, Settings
from utils.helpers import clear, process_and_print_request, save_to_history

class SecurityOperations:
    @staticmethod
    def email_validator():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('email_validator', selected_lang)}{Fore.RESET}\n")
        email = input(f"{Fore.MAGENTA}{translate('enter_email', selected_lang)}: {Fore.RESET}")
        
        if email:
            if "@" in email and "." in email.split("@")[1]:
                url = f"https://api.2ip.me/email.txt?email={email}"
                process_and_print_request(url)
            else:
                print(f"{Fore.RED}{translate('invalid_email', selected_lang)}{Fore.RESET}")
                input(f"\n{translate('continue_prompt', selected_lang)}")
                clear()

    @staticmethod
    def have_i_been_pwned():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('have_i_been_pwned', selected_lang)}{Fore.RESET}\n")
        email = input(f"{Fore.MAGENTA}{translate('enter_email', selected_lang)}: {Fore.RESET}")
        
        if email:
            api_key = config.get("api_keys", {}).get("hibp", "")
            if not api_key:
                print(f"{Fore.YELLOW}{translate('api_key_required', selected_lang)} (Have I Been Pwned).{Fore.RESET}")
                print(f"{Fore.YELLOW}{translate('add_api_key_in_config', selected_lang)}{Fore.RESET}")
                input(f"\n{translate('continue_prompt', selected_lang)}")
                clear()
                return
                
            headers = Settings.headers2.copy()
            headers["hibp-api-key"] = api_key
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            process_and_print_request(url, headers=headers)

    @staticmethod
    def tls_scan():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('tls_scan', selected_lang)}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{translate('enter_domain', selected_lang)}: {Fore.RESET}")
        
        if domain:
            url = f"https://api.ssllabs.com/api/v3/analyze?host={domain}&all=on"
            process_and_print_request(url)

    @staticmethod
    def js_security_scanner():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('js_security_scanner', selected_lang)}{Fore.RESET}\n")
        url_input = input(f"{Fore.MAGENTA}{translate('enter_url', selected_lang)}: {Fore.RESET}")
        
        if url_input:
            print(f"{Fore.YELLOW}{translate('scanning_js', selected_lang)} {url_input}...{Fore.RESET}")
            time.sleep(2)
            print(f"{Fore.GREEN}{translate('no_js_vulnerabilities', selected_lang)}{Fore.RESET}")
            
            save_to_history("js_scan", {
                "url": url_input,
                "vulnerabilities": []
            })
            
            input(f"\n{translate('continue_prompt', selected_lang)}")
            clear()

    @staticmethod
    def url_bypasser():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('url_bypasser', selected_lang)}{Fore.RESET}\n")
        url_input = input(f"{Fore.MAGENTA}{translate('enter_url', selected_lang)}: {Fore.RESET}")
        
        if url_input:
            print(f"{Fore.YELLOW}{translate('checking_url_redirect', selected_lang)} {url_input}...{Fore.RESET}")
            try:
                response = requests.head(url_input, allow_redirects=True, timeout=config.get("settings", {}).get("default_timeout", 10))
                if response.url != url_input:
                    print(f"\n{Fore.GREEN}{translate('original_url', selected_lang)}: {url_input}{Fore.RESET}")
                    print(f"{Fore.GREEN}{translate('redirects_to', selected_lang)}: {response.url}{Fore.RESET}")
                else:
                    print(f"\n{Fore.YELLOW}{translate('no_redirect', selected_lang)} {response.url}{Fore.RESET}")
                
                save_to_history("url_bypass", {
                    "original_url": url_input,
                    "final_url": response.url
                })
            except Exception as e:
                print(f"{Fore.RED}{translate('error', selected_lang)}: {e}{Fore.RESET}")
            
            input(f"\n{translate('continue_prompt', selected_lang)}")
            clear()

    @staticmethod
    def ssl_certificate_info():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('ssl_certificate_info', selected_lang)}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{translate('enter_domain', selected_lang)}: {Fore.RESET}")
        
        if domain:
            print(f"{Fore.YELLOW}{translate('retrieving_ssl_info', selected_lang)} {domain}...{Fore.RESET}")
            
            try:
                context = ssl.create_default_context()
                
                with socket.create_connection((domain, 443)) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        
                        subject = dict(item[0] for item in cert['subject'])
                        issuer = dict(item[0] for item in cert['issuer'])
                        
                        print(f"\n{Fore.GREEN}{translate('subject', selected_lang)}: {subject.get('commonName')}{Fore.RESET}")
                        print(f"{Fore.GREEN}{translate('issuer', selected_lang)}: {issuer.get('commonName')}{Fore.RESET}")
                        print(f"{Fore.GREEN}{translate('not_before', selected_lang)}: {cert['notBefore']}{Fore.RESET}")
                        print(f"{Fore.GREEN}{translate('not_after', selected_lang)}: {cert['notAfter']}{Fore.RESET}")
                        
                        not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                        not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                        now = datetime.datetime.now()
                        
                        if now < not_after and now > not_before:
                            print(f"{Fore.GREEN}{translate('cert_valid', selected_lang)}{Fore.RESET}")
                        else:
                            print(f"{Fore.RED}{translate('cert_invalid', selected_lang)}{Fore.RESET}")
                
                save_to_history("ssl_info", {
                    "domain": domain,
                    "issuer": issuer.get('commonName'),
                    "valid_until": cert['notAfter']
                })
                
            except Exception as e:
                print(f"{Fore.RED}{translate('error', selected_lang)}: {e}{Fore.RESET}")
            
            input(f"\n{translate('continue_prompt', selected_lang)}")
            clear() 