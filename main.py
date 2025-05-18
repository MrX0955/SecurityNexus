#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import sys
from colorama import Fore, init, Style, Back
from core.config import load_config, save_config, translate, config, VERSION
from utils.helpers import clear
from modules.menu import MenuSystem
from modules.dns import DNSOperations
from modules.network import NetworkOperations
from modules.security import SecurityOperations
from modules.threat_intel import ThreatIntelligence
from modules.vulnerability import VulnerabilityOperations
from modules.osint import OSINTOperations
from modules.settings import SettingsOperations
from modules.additional import AdditionalOperations
from modules.ml_anomaly import MLAnomalyOperations
from modules.log_analysis import LogAnalysisOperations
from modules.blockchain_security import BlockchainSecurityOperations
from modules.zero_trust import ZeroTrustOperations
from core.menu_theme import MenuTheme
from scripts.language_splash import select_language

# Config yapısını kontrol et ve gerekirse oluştur
def ensure_config_structure():
    """Config yapısının doğru olduğundan emin ol"""
    # Dil ayarını al
    selected_lang = config.get("settings", {}).get("language", "en")
    
    if "settings" not in config:
        config["settings"] = {}
    
    if "language" not in config["settings"]:
        config["settings"]["language"] = "en"
    
    # Dizinlerin varlığını kontrol et
    for folder in ["reports", "history"]:
        folder_path = config.get("settings", {}).get(f"{folder}_folder", folder)
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                print(f"{Fore.GREEN}{translate('folder_created', selected_lang)}: '{folder_path}'{Fore.RESET}")
            except Exception as e:
                print(f"{Fore.RED}{translate('folder_create_error', selected_lang)}: '{folder_path}' - {e}{Fore.RESET}")
    
    save_config()

def accept_license_agreement():
    clear()
    
    # Dil ayarını al
    selected_lang = config.get("settings", {}).get("language", "en")
    
    # Başlık için 3D efektli animasyon başlığı
    title = f"{MenuTheme.HEADING}{translate('license_agreement', selected_lang)}{Style.RESET_ALL}"
    
    # Terminal genişliğini al ve modern görünüm uygula
    width = min(os.get_terminal_size().columns, 100)
    padding = (width - len(title) - len(MenuTheme.HEADING) - len(Style.RESET_ALL)) // 2
    
    # Geliştirilmiş üst başlık
    print("\n" + " " * padding + title + "\n")
    
    # Animasyonlu kutu üst kısmı - genişleyen dalga efektiyle
    box_top = MenuTheme.draw_box(width)
    for line in box_top:
        print(line)
    
    # Dil seçimine göre lisans dosyasını seç
    license_file = "LICENSE"
    if selected_lang == "en":
        if os.path.exists("LICENSE.en"):
            license_file = "LICENSE.en"
    
    # License dosyasını oku
    try:
        with open(license_file, "r", encoding="utf-8") as f:
            license_text = f.read()
        
        # Lisans metnini ekranda daha okunaklı göstermek için işleme
        sections = license_text.split("\n\n")
        processed_sections = []
        
        for section in sections:
            lines = section.split('\n')
            processed_lines = []
            
            for line in lines:
                if line.strip().startswith("SecurityNexus"):
                    # Başlık satırları için iyileştirilmiş stil
                    processed_lines.append(f"{Fore.CYAN + Style.BRIGHT}{line}{Style.RESET_ALL}")
                elif line.strip().startswith("Copyright"):
                    # Telif hakkı için özel parlak stil
                    processed_lines.append(f"{Fore.YELLOW + Style.BRIGHT}{line}{Style.RESET_ALL}")
                elif line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")):
                    # Numaralı maddeler için özel renk ve efekt
                    prefix, rest = line.split(".", 1) if "." in line else (line, "")
                    processed_lines.append(f"{Fore.MAGENTA + Style.BRIGHT}{prefix}.{Fore.LIGHTGREEN_EX}{rest}{Style.RESET_ALL}")
                elif any(keyword in line.lower() for keyword in ["illegal", "yasak", "yasadışı", "prohibited", "unlawful"]):
                    # Yasak/illegal ifadeleri için dikkat çekici stil
                    processed_lines.append(f"{Fore.LIGHTRED_EX}{line}{Style.RESET_ALL}")
                elif any(keyword in line.lower() for keyword in ["sorumlu", "sorumluluk", "responsibility", "liable", "liability"]):
                    # Sorumluluk belirten satırlar için özel renk ve ikon
                    processed_lines.append(f"{Fore.LIGHTYELLOW_EX}⚠ {line}{Style.RESET_ALL}")
                else:
                    processed_lines.append(f"{Fore.WHITE}{line}{Style.RESET_ALL}")
            
            processed_sections.append("\n".join(processed_lines))
        
        # Bölümleri göster
        for section in processed_sections:
            print(section)
            print()  # Bölümler arası boşluk
        
        # Animasyonlu kutu alt kısmı
        bottom_box = MenuTheme.draw_box_bottom(width)
        print(bottom_box)
        
        # Kabul butonu için metin
        accept_text = translate("accept_agreement", selected_lang)
        
        # Kabul işlemi
        accepted = False
        while not accepted:
            print("\n")  # Boşluk bırak
            
            # Yeni modern 3D buton görünümü
            MenuTheme.display_accept_button(accept_text, width=50)
            
            key = input()
            accepted = True
            
        # Özel onay animasyonu
        sys.stdout.write("\r" + " " * width + "\r")  # Satırı temizle
        success_msg = translate("agreement_accepted", selected_lang)
        
        # Başarı mesajını renk geçişiyle göster
        colored_success = ""
        for i, char in enumerate(success_msg):
            # Yeşilden maviye kademeli geçiş
            ratio = i / len(success_msg)
            if ratio < 0.33:
                color = Fore.LIGHTGREEN_EX
            elif ratio < 0.66:
                color = Fore.GREEN
            else:
                color = Fore.CYAN
                
            colored_success += f"{color + Style.BRIGHT}{char}{Style.RESET_ALL}"
            
        print(f"\n{colored_success}")
        
        # Başarı animasyonu ekle
        MenuTheme.loading_animation(translate("starting", selected_lang), duration=2.0, style="modern")
        
        # Lisans kabul edildi işaretlemesi
        config['license_accepted'] = True
        save_config()
        
        return True
        
    except Exception as e:
        # Hata oluşursa daha görsel bir hata mesajı göster
        error_border = f"{Fore.RED}{'!' * 50}{Style.RESET_ALL}"
        print(f"\n{error_border}")
        print(f"{Fore.RED + Style.BRIGHT}  {translate('error', selected_lang)}: {e}{Style.RESET_ALL}")
        print(f"{error_border}")
        time.sleep(3)
        return False

def main():
    init(autoreset=True)
    clear()
    
    if not load_config():
        print(f"{Fore.RED}{translate('config_error', 'en')}{Fore.RESET}")
        exit(1)
    
    # İlk çalıştırmada dil seçim ekranını göster
    first_run = config.get("first_run", True)
    if first_run:
        selected_lang = select_language()
        config["first_run"] = False
        save_config()
    else:
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
    
    # Animasyonlu karşılama bannerı göster
    MenuTheme.display_welcome_banner(VERSION, selected_lang)
    time.sleep(1)
    
    # Kullanım sözleşmesi kontrolü
    if not config.get('license_accepted', False):
        if not accept_license_agreement():
            exit(0)
    
    print(f"{Fore.GREEN}{translate('starting', selected_lang)}{Fore.RESET}")
    # Yükleme animasyonu göster
    MenuTheme.loading_animation(translate('initializing', selected_lang), duration=1.5, style="dots")
    
    while True:
        clear()
        category = MenuSystem.main_menu()
        
        if category == 'exit':
            print(f"{Fore.CYAN}{translate('closing', selected_lang)}!{Fore.RESET}")
            time.sleep(1)
            break
        
        elif category == 'dns':
            dns_choice = MenuSystem.dns_menu()
            
            if dns_choice == 1:
                DNSOperations.reverse_dns()
            elif dns_choice == 2:
                DNSOperations.dns_lookup()
            elif dns_choice == 3:
                DNSOperations.zone_transfer()
            elif dns_choice == 4:
                DNSOperations.dns_host_records()
            elif dns_choice == 5:
                DNSOperations.dns_records()
            elif dns_choice == 6:
                DNSOperations.dmarc_lookup()
        
        elif category == 'network':
            network_choice = MenuSystem.network_menu()
            
            if network_choice == 1:
                NetworkOperations.geoip()
            elif network_choice == 2:
                NetworkOperations.reverseip()
            elif network_choice == 3:
                NetworkOperations.asn_lookup()
            elif network_choice == 4:
                NetworkOperations.ip_privacy()
            elif network_choice == 5:
                NetworkOperations.port_scanner()
        
        elif category == 'security':
            security_choice = MenuSystem.security_menu()
            
            if security_choice == 1:
                SecurityOperations.email_validator()
            elif security_choice == 2:
                SecurityOperations.have_i_been_pwned()
            elif security_choice == 3:
                SecurityOperations.tls_scan()
            elif security_choice == 4:
                SecurityOperations.js_security_scanner()
            elif security_choice == 5:
                SecurityOperations.url_bypasser()
            elif security_choice == 6:
                SecurityOperations.ssl_certificate_info()
        
        elif category == 'threat_intel':
            threat_intel_choice = MenuSystem.threat_intel_menu()
            
            if threat_intel_choice == 1:
                ThreatIntelligence.misp_check()
            elif threat_intel_choice == 2:
                ThreatIntelligence.otx_check()
            elif threat_intel_choice == 3:
                ThreatIntelligence.threatfox_check()
        
        elif category == 'vulnerability':
            vulnerability_choice = MenuSystem.vulnerability_menu()
            
            if vulnerability_choice == 1:
                VulnerabilityOperations.cve_lookup()
            elif vulnerability_choice == 2:
                VulnerabilityOperations.vulnerability_scanner()
            elif vulnerability_choice == 3:
                VulnerabilityOperations.web_vulnerability_scanner()
        
        elif category == 'osint':
            osint_choice = MenuSystem.osint_menu()
            
            if osint_choice == 1:
                OSINTOperations.whois_lookup()
            elif osint_choice == 2:
                OSINTOperations.subdomain_finder()
            elif osint_choice == 3:
                OSINTOperations.email_finder()
            elif osint_choice == 4:
                OSINTOperations.social_media_finder()
            elif osint_choice == 5:
                OSINTOperations.leaked_data_checker()
            elif osint_choice == 6:
                OSINTOperations.pastebin_scraper()
        
        elif category == 'additional':
            additional_choice = MenuSystem.additional_menu()
            
            if additional_choice == 1:
                AdditionalOperations.performance_test()
            elif additional_choice == 2:
                AdditionalOperations.encryption_tools()
            elif additional_choice == 3:
                AdditionalOperations.random_generator()
            elif additional_choice == 4:
                AdditionalOperations.converter_tools()
        
        elif category == 'settings':
            settings_choice = SettingsOperations.settings_menu()
            
            if settings_choice == 'language':
                SettingsOperations.change_language()
            elif settings_choice == 'api_keys':
                SettingsOperations.api_keys()
            elif settings_choice == 'reports':
                SettingsOperations.report_settings()
            elif settings_choice == 'threat_intel':
                SettingsOperations.threat_intel_settings()
            elif settings_choice == 'about':
                SettingsOperations.about()
        
        elif category == 'ml_anomaly':
            ml_anomaly_choice = MenuSystem.ml_anomaly_menu()
            
            if ml_anomaly_choice == 1:
                MLAnomalyOperations.network_anomaly_detection()
            elif ml_anomaly_choice == 2:
                MLAnomalyOperations.user_behavior_analysis()
            elif ml_anomaly_choice == 3:
                MLAnomalyOperations.log_anomaly_detection()
            elif ml_anomaly_choice == 4:
                MLAnomalyOperations.system_resource_analysis()
            elif ml_anomaly_choice == 5:
                MLAnomalyOperations.model_training()
        
        elif category == 'log_analysis':
            log_analysis_choice = MenuSystem.log_analysis_menu()
            
            if log_analysis_choice == 1:
                LogAnalysisOperations.log_collector()
            elif log_analysis_choice == 2:
                LogAnalysisOperations.log_parser()
            elif log_analysis_choice == 3:
                LogAnalysisOperations.correlation_engine()
            elif log_analysis_choice == 4:
                LogAnalysisOperations.event_visualization()
            elif log_analysis_choice == 5:
                LogAnalysisOperations.log_analyzer()
        
        elif category == 'blockchain_security':
            blockchain_choice = MenuSystem.blockchain_security_menu()
            
            if blockchain_choice == 1:
                BlockchainSecurityOperations.smart_contract_analyzer()
            elif blockchain_choice == 2:
                BlockchainSecurityOperations.transaction_analyzer()
            elif blockchain_choice == 3:
                BlockchainSecurityOperations.wallet_security_check()
            elif blockchain_choice == 4:
                BlockchainSecurityOperations.crypto_asset_monitor()
        
        elif category == 'zero_trust':
            zero_trust_choice = MenuSystem.zero_trust_menu()
            
            if zero_trust_choice == 1:
                ZeroTrustOperations.access_policy_analyzer()
            elif zero_trust_choice == 2:
                ZeroTrustOperations.network_segmentation_check()
            elif zero_trust_choice == 3:
                ZeroTrustOperations.identity_verification_check()
            elif zero_trust_choice == 4:
                ZeroTrustOperations.context_based_security()
            elif zero_trust_choice == 5:
                ZeroTrustOperations.zero_trust_assessment()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        print(f"\n{Fore.CYAN}{translate('closing', selected_lang)}!{Fore.RESET}")
        exit(0)
    except Exception as e:
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        print(f"{Fore.RED}{translate('unexpected_error', selected_lang)}: {e}{Fore.RESET}")
        exit(1)
