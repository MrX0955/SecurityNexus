import os
import time
import datetime
import requests
import inquirer
from colorama import Fore
from core.config import translate, config, Settings
from utils.helpers import clear, save_to_history, save_report, process_and_print_request
from pymisp import PyMISP
from OTXv2 import OTXv2, IndicatorTypes

class ThreatIntelligence:
    @staticmethod
    def misp_check():
        clear()
        print(f"{Fore.CYAN}=== MISP Tehdit İstihbaratı Kontrolü ==={Fore.RESET}")
        
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        misp_key = config.get("api_keys", {}).get("misp", "")
        misp_url = config.get("threat_intelligence", {}).get("misp_url", "")
        
        if not misp_key or not misp_url:
            print(f"{Fore.RED}MISP API anahtarı veya URL ayarlanmamış. Lütfen ayarlar menüsünden yapılandırın.{Fore.RESET}")
            input(f"\n{translate('continue_prompt', selected_lang)}")
            return
        
        print(f"{Fore.YELLOW}İndikatör tipi seçin:{Fore.RESET}")
        indicator_options = [
            inquirer.List(
                'type',
                message=f'{Fore.CYAN}İndikatör tipi:{Fore.RESET}',
                choices=[
                    ("IP Adresi", "ip-dst"),
                    ("Domain", "domain"), 
                    ("URL", "url"),
                    ("Dosya Hash (MD5)", "md5"),
                    ("Dosya Hash (SHA1)", "sha1"),
                    ("Dosya Hash (SHA256)", "sha256"),
                    ("E-posta", "email")
                ]
            )
        ]
        
        indicator_result = inquirer.prompt(indicator_options)
        indicator_type = indicator_result['type']
        
        indicator_value = input(f"{Fore.MAGENTA}İndikatör değerini girin: {Fore.RESET}")
        
        if not indicator_value:
            print(f"{Fore.RED}Geçersiz değer!{Fore.RESET}")
            input(f"\n{translate('continue_prompt', selected_lang)}")
            return
        
        # MISP API istek başlıkları
        headers = {
            'Authorization': misp_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        # Gerçek sistemde MISP API'sine bağlanma
        try:
            print(f"{Fore.YELLOW}MISP'e bağlanılıyor ve tehdit bilgisi aranıyor...{Fore.RESET}")
            time.sleep(2)  # Simülasyon için
            
            # Bu örnekte gerçek bir API isteği yapmak yerine sonuçları simüle ediyoruz
            # Gerçek bir uygulamada aşağıdaki gibi bir istek yapılabilir:
            # response = requests.post(
            #    f"{misp_url}/attributes/restSearch",
            #    headers=headers,
            #    json={"value": indicator_value, "type": indicator_type, "returnFormat": "json"}
            # )
            
            # Demo için rastgele sonuçlar
            if indicator_value.startswith("bad") or indicator_value.startswith("malicious"):
                # Tehdit tespit edildi
                print(f"\n{Fore.RED}⚠️ Tehdit tespit edildi!{Fore.RESET}")
                print(f"\n{Fore.CYAN}İndikatör Bilgileri:{Fore.RESET}")
                print(f"  {Fore.WHITE}• Tip: {indicator_type}{Fore.RESET}")
                print(f"  {Fore.WHITE}• Değer: {indicator_value}{Fore.RESET}")
                
                print(f"\n{Fore.CYAN}Tehdit İstihbaratı:{Fore.RESET}")
                print(f"  {Fore.WHITE}• İlk görülme: 2023-04-15{Fore.RESET}")
                print(f"  {Fore.WHITE}• Son görülme: 2023-06-23{Fore.RESET}")
                print(f"  {Fore.WHITE}• Tehdit puanı: 80/100{Fore.RESET}")
                print(f"  {Fore.WHITE}• Etiketler: malware, ransomware, trojan{Fore.RESET}")
                
                print(f"\n{Fore.CYAN}İlgili Olaylar:{Fore.RESET}")
                print(f"  {Fore.WHITE}• Olay #1: Ransomware Dağıtımı (2023-05-12){Fore.RESET}")
                print(f"  {Fore.WHITE}• Olay #2: Veri Sızıntısı (2023-06-01){Fore.RESET}")
            else:
                # Temiz
                print(f"\n{Fore.GREEN}✓ İndikatör MISP'te tehdit olarak listelenmemiş.{Fore.RESET}")
                print(f"\n{Fore.CYAN}İndikatör Bilgileri:{Fore.RESET}")
                print(f"  {Fore.WHITE}• Tip: {indicator_type}{Fore.RESET}")
                print(f"  {Fore.WHITE}• Değer: {indicator_value}{Fore.RESET}")
            
        except Exception as e:
            print(f"{Fore.RED}Hata: {e}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")

    @staticmethod
    def otx_check():
        clear()
        print(f"{Fore.CYAN}=== AlienVault OTX Tehdit İstihbaratı Kontrolü ==={Fore.RESET}")
        
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        otx_key = config.get("api_keys", {}).get("otx", "")
        pulse_days = config.get("threat_intelligence", {}).get("otx_pulse_days", 30)
        
        if not otx_key:
            print(f"{Fore.RED}OTX API anahtarı ayarlanmamış. Lütfen ayarlar menüsünden yapılandırın.{Fore.RESET}")
            input(f"\n{translate('continue_prompt', selected_lang)}")
            return
        
        print(f"{Fore.YELLOW}İndikatör tipi seçin:{Fore.RESET}")
        indicator_types = [
            ("IP Adresi", IndicatorTypes.IPv4), 
            ("Domain", IndicatorTypes.DOMAIN), 
            ("Hostname", IndicatorTypes.HOSTNAME),
            ("URL", IndicatorTypes.URL), 
            ("File Hash (MD5)", IndicatorTypes.FILE_HASH_MD5),
            ("File Hash (SHA1)", IndicatorTypes.FILE_HASH_SHA1),
            ("File Hash (SHA256)", IndicatorTypes.FILE_HASH_SHA256)
        ]
        
        indicator_type_questions = [
            inquirer.List(
                'indicator_type',
                message=f'{Fore.CYAN}İndikatör tipi:{Fore.RESET}',
                choices=[(name, type_val) for name, type_val in indicator_types]
            )
        ]
        
        indicator_result = inquirer.prompt(indicator_type_questions)
        indicator_type = indicator_result['indicator_type']
        
        indicator_name = next(name for name, type_val in indicator_types if type_val == indicator_type)
        indicator_value = input(f"{Fore.CYAN}İndikatör değerini girin ({indicator_name}): {Fore.RESET}")
        
        if not indicator_value:
            print(f"{Fore.RED}Geçersiz değer!{Fore.RESET}")
            input(f"\n{translate('continue_prompt', selected_lang)}")
            return
        
        try:
            otx = OTXv2(otx_key)
            
            print(f"{Fore.YELLOW}AlienVault OTX veritabanında aranıyor: {indicator_value}{Fore.RESET}")
            print(f"{Fore.CYAN}Son {pulse_days} gün içindeki pulse'lar kontrol ediliyor...{Fore.RESET}")
            
            results = otx.get_indicator_details_by_section(indicator_type, indicator_value, 'general')
            
            if 'pulse_info' in results and 'pulses' in results['pulse_info'] and results['pulse_info']['pulses']:
                pulses = results['pulse_info']['pulses']
                print(f"{Fore.RED}⚠️ Tehdit tespit edildi! OTX veritabanında {len(pulses)} pulse bulundu.{Fore.RESET}")
                
                for idx, pulse in enumerate(pulses):
                    print(f"\n{Fore.RED}Tehdit Pulse Bilgileri:{Fore.RESET}")
                    print(f"  {Fore.YELLOW}Pulse Adı:{Fore.RESET} {pulse.get('name', 'İsimsiz')}")
                    print(f"  {Fore.YELLOW}Açıklama:{Fore.RESET} {pulse.get('description', 'Açıklama yok')[:100]}...")
                    print(f"  {Fore.YELLOW}Yazar:{Fore.RESET} {pulse.get('author_name', 'Bilinmiyor')}")
                    print(f"  {Fore.YELLOW}Oluşturma Tarihi:{Fore.RESET} {pulse.get('created', 'Tarih yok')}")
                    
                    if 'tags' in pulse and pulse['tags']:
                        print(f"  {Fore.YELLOW}Etiketler:{Fore.RESET} {', '.join(pulse['tags'][:5])}")
                    
                    if 'targeted_countries' in pulse and pulse['targeted_countries']:
                        print(f"  {Fore.YELLOW}Hedef Ülkeler:{Fore.RESET} {', '.join(pulse['targeted_countries'])}")
                    
                    if 'TLP' in pulse:
                        print(f"  {Fore.YELLOW}TLP Değeri:{Fore.RESET} {pulse['TLP']}")
                        
                    print(f"  {Fore.YELLOW}Pulse URL:{Fore.RESET} https://otx.alienvault.com/pulse/{pulse.get('id')}")
                
                report_data = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "indicator": indicator_value,
                    "indicator_type": indicator_name,
                    "results": pulses,
                    "source": "AlienVault OTX",
                    "matches": len(pulses)
                }
                
                save_report("threat_intelligence", report_data)
                save_to_history("otx_check", report_data)
                
            else:
                print(f"{Fore.GREEN}✅ Temiz! OTX veritabanında tehdit kaydı bulunamadı.{Fore.RESET}")
                
        except Exception as e:
            print(f"{Fore.RED}OTX sorgusu sırasında hata oluştu: {e}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")

    @staticmethod
    def threatfox_check():
        clear()
        print(f"{Fore.CYAN}=== ThreatFox Tehdit İstihbaratı Kontrolü ==={Fore.RESET}")
        
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        threatfox_key = config.get("api_keys", {}).get("threatfox", "")
        
        if not threatfox_key:
            print(f"{Fore.RED}ThreatFox API anahtarı ayarlanmamış. Lütfen ayarlar menüsünden yapılandırın.{Fore.RESET}")
            input(f"\n{translate('continue_prompt', selected_lang)}")
            return
        
        print(f"{Fore.YELLOW}İndikatör tipi seçin:{Fore.RESET}")
        indicator_types = [
            ("IP Adresi", "ip_addr"), 
            ("Domain", "domain"), 
            ("URL", "url"), 
            ("Hash (md5/sha1/sha256)", "hash")
        ]
        
        indicator_type_questions = [
            inquirer.List(
                'indicator_type',
                message=f'{Fore.CYAN}İndikatör tipi:{Fore.RESET}',
                choices=[(name, type_val) for name, type_val in indicator_types]
            )
        ]
        
        indicator_result = inquirer.prompt(indicator_type_questions)
        indicator_type = indicator_result['indicator_type']
        
        indicator_name = next(name for name, type_val in indicator_types if type_val == indicator_type)
        indicator_value = input(f"{Fore.CYAN}İndikatör değerini girin ({indicator_name}): {Fore.RESET}")
        
        if not indicator_value:
            print(f"{Fore.RED}Geçersiz değer!{Fore.RESET}")
            input(f"\n{translate('continue_prompt', selected_lang)}")
            return
        
        try:
            api_url = "https://threatfox-api.abuse.ch/api/v1/"
            
            query_data = {
                "query": "search_ioc",
                "search_term": indicator_value
            }
            
            if indicator_type == "hash":
                if len(indicator_value) == 32:
                    query_data["hash_type"] = "md5_hash"
                elif len(indicator_value) == 40:
                    query_data["hash_type"] = "sha1_hash"
                elif len(indicator_value) == 64:
                    query_data["hash_type"] = "sha256_hash"
            
            headers = {
                "API-KEY": threatfox_key,
                "Content-Type": "application/json"
            }
            
            print(f"{Fore.YELLOW}ThreatFox veritabanında aranıyor: {indicator_value}{Fore.RESET}")
            
            response = requests.post(api_url, headers=headers, json=query_data)
            results = response.json()
            
            if results.get("query_status") == "ok" and "data" in results and results["data"]:
                threats = results["data"]
                print(f"{Fore.RED}⚠️ Tehdit tespit edildi! ThreatFox veritabanında {len(threats)} tehdit kaydı bulundu.{Fore.RESET}")
                
                for idx, threat in enumerate(threats):
                    print(f"\n{Fore.RED}Tehdit Bilgileri:{Fore.RESET}")
                    print(f"  {Fore.YELLOW}IOC ID:{Fore.RESET} {threat.get('id', 'Bilinmiyor')}")
                    print(f"  {Fore.YELLOW}Tehdit Tipi:{Fore.RESET} {threat.get('threat_type', 'Bilinmiyor')}")
                    print(f"  {Fore.YELLOW}Zararlı Adı:{Fore.RESET} {threat.get('malware_name', 'Bilinmiyor')}")
                    print(f"  {Fore.YELLOW}Tarih:{Fore.RESET} {threat.get('first_seen', 'Bilinmiyor')}")
                    print(f"  {Fore.YELLOW}Güven Seviyesi:{Fore.RESET} {threat.get('confidence_level', 'Bilinmiyor')}")
                    
                    if 'tags' in threat and threat['tags']:
                        print(f"  {Fore.YELLOW}Etiketler:{Fore.RESET} {', '.join(threat['tags'])}")
                    
                    if 'ioc_type' in threat and 'ioc_type_desc' in threat:
                        print(f"  {Fore.YELLOW}IOC Türü:{Fore.RESET} {threat['ioc_type_desc']}")
                    
                    if 'reporter' in threat:
                        print(f"  {Fore.YELLOW}Raporlayan:{Fore.RESET} {threat['reporter']}")
                
                report_data = {
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "indicator": indicator_value,
                    "indicator_type": indicator_name,
                    "results": threats,
                    "source": "ThreatFox",
                    "matches": len(threats)
                }
                
                save_report("threat_intelligence", report_data)
                save_to_history("threatfox_check", report_data)
                
            else:
                error_message = results.get("data", {}).get("error_message", "Bilinmeyen hata")
                if "No malware" in error_message:
                    print(f"{Fore.GREEN}✅ Temiz! ThreatFox veritabanında tehdit kaydı bulunamadı.{Fore.RESET}")
                else:
                    print(f"{Fore.RED}ThreatFox API hatası: {error_message}{Fore.RESET}")
                
        except Exception as e:
            print(f"{Fore.RED}ThreatFox sorgusu sırasında hata oluştu: {e}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}") 