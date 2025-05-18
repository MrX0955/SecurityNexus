import socket
import json
import time
import datetime
import re
import requests
from colorama import Fore
from core.config import _, config, Settings
from utils.helpers import clear, process_and_print_request, save_to_history, save_report

class OSINTOperations:
    @staticmethod
    def whois_lookup():
        clear()
        print(f"{Fore.CYAN}{_('whois_lookup')}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
        
        if domain:
            try:
                # Doğrudan API'den sorgu yerine Python WHOIS kütüphanesi kullanım seçeneği ekleyin
                import whois
                print(f"{Fore.YELLOW}WHOIS sorgusu yapılıyor: {domain}{Fore.RESET}")
                
                try:
                    # Python WHOIS kütüphanesiyle sorgu yapalım
                    result = whois.whois(domain)
                    
                    # Unhashable type: 'dict' hatasını önlemek için
                    # Sözlük türündeki alanlarda işlem yapmadan önce kontrol ekleyelim
                    print(f"\n{Fore.GREEN}WHOIS Bilgileri:{Fore.RESET}")
                    
                    # Değerleri string şekilde gösterelim
                    for key, value in result.items():
                        # Boş değerleri ve sözlük anahtar/değer çiftlerini atlayalım
                        if value is not None and not isinstance(value, dict):
                            print(f"{Fore.YELLOW}{key}:{Fore.RESET} {value}")
                    
                    # Kayıt bilgilerini ve geçmiş verilerini saklayalım
                    save_to_history("whois_lookup", {
                        "domain": domain,
                        "result": str(result)  # Sözlük yerine string olarak kaydet
                    })
                    
                    # İsteğe bağlı olarak rapor da kaydedilebilir
                    save_report("whois_lookup", {
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "domain": domain,
                        "result": str(result)  # Sözlük yerine string olarak kaydet
                    })
                    
                except Exception as e:
                    # Python whois kütüphanesiyle ilgili hatayı göster
                    print(f"{Fore.RED}WHOIS sorgusu sırasında hata oluştu: {e}{Fore.RESET}")
                    
                    # Alternatif olarak API'yi kullanmayı deneyelim
                    print(f"\n{Fore.YELLOW}Alternatif kaynak kullanılıyor...{Fore.RESET}")
                    url = f"https://api.hackertarget.com/whois/?q={domain}"
                    process_and_print_request(url, headers={"User-Agent": "SecurityNexus"})
                    return
                
            except ImportError:
                # Python whois kütüphanesi yüklü değilse API'yi kullanın
                print(f"{Fore.YELLOW}Python WHOIS modülü bulunamadı, API kullanılıyor...{Fore.RESET}")
                url = f"https://api.hackertarget.com/whois/?q={domain}"
                process_and_print_request(url, headers={"User-Agent": "SecurityNexus"})
            
            input(f"\n{_('continue_prompt')}")
            clear()

    @staticmethod
    def subdomain_finder():
        clear()
        print(f"{Fore.CYAN}{_('subdomain_finder')}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
        
        if domain:
            url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
            process_and_print_request(url, headers={"User-Agent": "SecurityNexus"})

    @staticmethod
    def email_finder():
        clear()
        print(f"{Fore.CYAN}{_('email_finder')}{Fore.RESET}\n")
        domain = input(f"{Fore.MAGENTA}{_('enter_domain')}: {Fore.RESET}")
        
        if domain:
            print(f"{Fore.YELLOW}Domainle ilgili e-posta adresleri aranıyor: {domain}{Fore.RESET}")
            
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

                url = f"https://{domain}"
                response = requests.get(url, headers=headers, timeout=config.get("settings", {}).get("default_timeout", 10))
                html_content = response.text

                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = set(re.findall(email_pattern, html_content))
                
                if emails:
                    print(f"\n{Fore.GREEN}Bulunan e-posta adresleri:{Fore.RESET}")
                    for email in emails:
                        if domain in email:
                            print(f"{Fore.CYAN}  - {email}{Fore.RESET}")
                        else:
                            print(f"  - {email}")
                else:
                    print(f"\n{Fore.YELLOW}Ana sayfada e-posta adresi bulunamadı.{Fore.RESET}")
                
                save_to_history("email_finder", {
                    "domain": domain,
                    "emails": list(emails)
                })
                
            except Exception as e:
                print(f"{Fore.RED}Hata: {e}{Fore.RESET}")
            
            input(f"\n{_('continue_prompt')}")
            clear()

    @staticmethod
    def social_media_finder():
        clear()
        print(f"{Fore.CYAN}{_('social_media_finder')}{Fore.RESET}\n")
        target = input(f"{Fore.MAGENTA}{_('enter_username_or_company')}: {Fore.RESET}")
        
        if target:
            print(f"{Fore.YELLOW}Sosyal medya profilleri aranıyor: {target}{Fore.RESET}")
            time.sleep(1)
            
            platforms = {
                "Facebook": f"https://facebook.com/{target}",
                "Twitter": f"https://twitter.com/{target}",
                "Instagram": f"https://instagram.com/{target}",
                "LinkedIn": f"https://linkedin.com/in/{target}",
                "LinkedIn (Company)": f"https://linkedin.com/company/{target}",
                "GitHub": f"https://github.com/{target}",
                "YouTube": f"https://youtube.com/@{target}",
                "Reddit": f"https://reddit.com/user/{target}",
                "TikTok": f"https://tiktok.com/@{target}",
                "Pinterest": f"https://pinterest.com/{target}",
                "Medium": f"https://medium.com/@{target}"
            }
            
            results = []
            print(f"\n{Fore.GREEN}Platformlarda aranıyor...{Fore.RESET}")
            
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                
                for platform, url in platforms.items():
                    print(f"  {Fore.YELLOW}Kontrol ediliyor: {platform}...{Fore.RESET}", end="", flush=True)
                    try:
                        response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
                        
                        if response.status_code == 200 and target.lower() in response.url.lower():
                            print(f"{Fore.GREEN} BULUNDU ✓{Fore.RESET}")
                            results.append({
                                "platform": platform,
                                "url": url,
                                "status": "found"
                            })
                        else:
                            print(f"{Fore.RED} BULUNAMADI ✗{Fore.RESET}")
                            results.append({
                                "platform": platform,
                                "url": url,
                                "status": "not_found"
                            })
                    except:
                        print(f"{Fore.RED} HATA ✗{Fore.RESET}")
                        results.append({
                            "platform": platform,
                            "url": url,
                            "status": "error"
                        })
                
                found_platforms = [r for r in results if r["status"] == "found"]
                
                if found_platforms:
                    print(f"\n{Fore.GREEN}Bulunan profiller:{Fore.RESET}")
                    for platform in found_platforms:
                        print(f"  {Fore.CYAN}{platform['platform']}:{Fore.RESET} {platform['url']}")
                else:
                    print(f"\n{Fore.YELLOW}Hiçbir sosyal medya profili bulunamadı.{Fore.RESET}")
                
                save_to_history("social_media_finder", {
                    "target": target,
                    "results": results
                })
                
            except Exception as e:
                print(f"{Fore.RED}Hata: {e}{Fore.RESET}")
            
            input(f"\n{_('continue_prompt')}")
            clear()

    @staticmethod
    def leaked_data_checker():
        clear()
        print(f"{Fore.CYAN}{_('leaked_data_checker')}{Fore.RESET}\n")
        email = input(f"{Fore.MAGENTA}{_('enter_email')}: {Fore.RESET}")
        
        if email:
            api_key = config.get("api_keys", {}).get("hibp", "")
            
            if not api_key:
                print(f"{Fore.YELLOW}Bu özellik Have I Been Pwned API anahtarı gerektirir.{Fore.RESET}")
                print(f"{Fore.YELLOW}Lütfen API anahtarınızı config.json dosyasına ekleyin.{Fore.RESET}")
                input(f"\n{_('continue_prompt')}")
                clear()
                return
            
            print(f"{Fore.YELLOW}Sızıntı veritabanlarında kontrol ediliyor: {email}{Fore.RESET}")
            
            try:
                headers = {
                    "hibp-api-key": api_key,
                    "User-Agent": "SecurityNexus"
                }
                
                url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
                response = requests.get(url, headers=headers, timeout=config.get("settings", {}).get("default_timeout", 10))
                
                if response.status_code == 200:
                    breaches = response.json()
                    
                    print(f"\n{Fore.RED}⚠️ E-posta adresi {len(breaches)} veri sızıntısında bulundu!{Fore.RESET}")
                    
                    for idx, breach in enumerate(breaches):
                        print(f"\n{Fore.RED}Sızıntı Bilgileri:{Fore.RESET}")
                        print(f"  {Fore.YELLOW}Tarih:{Fore.RESET} {breach['BreachDate']}")
                        print(f"  {Fore.YELLOW}Açıklama:{Fore.RESET} {breach['Description'][:100]}...")
                        print(f"  {Fore.YELLOW}Etkilenen hesap sayısı:{Fore.RESET} {breach['PwnCount']:,}")
                        
                        compromised_data = ", ".join(breach['DataClasses'])
                        print(f"  {Fore.YELLOW}Ele geçirilen veriler:{Fore.RESET} {compromised_data}")
                    
                    print(f"\n{Fore.RED}Bu e-posta adresinin şifresini değiştirmeniz ve herhangi bir yerde aynı şifreyi kullanıyorsanız, onları da değiştirmeniz önerilir.{Fore.RESET}")
                    
                    save_to_history("leaked_data_check", {
                        "email": email,
                        "breaches": breaches
                    })
                    
                    save_report("leaked_data", {
                        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "email": email,
                        "breaches": breaches
                    })
                    
                elif response.status_code == 404:
                    print(f"\n{Fore.GREEN}✅ İyi haber! E-posta adresi bilinen veri sızıntılarında bulunamadı.{Fore.RESET}")
                else:
                    print(f"{Fore.RED}API hatası: {response.status_code} - {response.text}{Fore.RESET}")
            
            except Exception as e:
                print(f"{Fore.RED}Hata: {e}{Fore.RESET}")
            
            input(f"\n{_('continue_prompt')}")
            clear()

    @staticmethod
    def pastebin_scraper():
        clear()
        print(f"{Fore.CYAN}{_('pastebin_scraper')}{Fore.RESET}\n")
        keyword = input(f"{Fore.MAGENTA}{_('enter_keyword')}: {Fore.RESET}")
        
        if keyword:
            print(f"{Fore.YELLOW}Pastebin'de aranıyor: {keyword}{Fore.RESET}")
            print(f"{Fore.RED}Bu özellik şu anda doğrudan Pastebin API kısıtlamaları nedeniyle tam olarak çalışmıyor.{Fore.RESET}")
            print(f"{Fore.YELLOW}Pastebin arama için Pastebin Pro hesabı gereklidir.{Fore.RESET}")
            
            time.sleep(2)

            print(f"\n{Fore.GREEN}Benzer arama sonuçları:{Fore.RESET}")
            print(f"  {Fore.CYAN}Google Dorks kullanarak web'de arayın:{Fore.RESET}")
            print(f"  site:pastebin.com {keyword}")
            
            input(f"\n{_('continue_prompt')}")
            clear() 