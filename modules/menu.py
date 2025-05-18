import os
import sys
import time
import random
import inquirer
from colorama import Fore, Style
from core.config import translate, config, VERSION
from core.menu_theme import MenuTheme
from core.utils import clear

class MenuSystem:
    @staticmethod
    def main_menu():
        """Display main menu with modern design"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Modern menu title - with 3D effect
        title_text = translate("menu_title", selected_lang)
        
        # Category buttons - Modern, interactive design
        categories = [
            ("dns", f'🧬 {translate("category_dns", selected_lang)}'),
            ("network", f'🌐 {translate("category_network", selected_lang)}'),
            ("security", f'🔒 {translate("category_security", selected_lang)}'),
            ("threat_intel", f'🔍 {translate("category_threat_intel", selected_lang)}'),
            ("vulnerability", f'🔎 {translate("category_vulnerability", selected_lang)}'),
            ("osint", f'🕵️ {translate("category_osint", selected_lang)}'),
            ("ml_anomaly", f'🤖 {translate("category_ml_anomaly", selected_lang)}'),
            ("log_analysis", f'📊 {translate("category_log_analysis", selected_lang)}'),
            ("blockchain_security", f'⛓️ {translate("category_blockchain_security", selected_lang)}'),
            ("zero_trust", f'🔐 {translate("category_zero_trust", selected_lang)}'),
            ("additional", f'✒️ {translate("category_additional", selected_lang)}'),
            ("settings", f'⚙️ {translate("category_settings", selected_lang)}'),
            ("exit", f'❌ {translate("category_exit", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(categories, title_text, box_width, selected_lang)
    
    @staticmethod
    def dns_menu():
        """DNS menu - modernized view"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_dns", selected_lang)
        
        # Submenu options
        dns_options = [
            (1, f'🔎 {translate("reverse_dns", selected_lang)}'),
            (2, f'🌐 {translate("dns_lookup", selected_lang)}'),
            (3, f'↔️ {translate("zone_transfer", selected_lang)}'),
            (4, f'📋 {translate("dns_host_records", selected_lang)}'),
            (5, f'📝 {translate("dns_records", selected_lang)}'),
            (6, f'📧 {translate("dmarc_lookup", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(dns_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def network_menu():
        """Network menu - modernized view"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_network", selected_lang)
        
        # Submenu options
        network_options = [
            (1, f'🌍 {translate("geolocation_ip", selected_lang)}'),
            (2, f'🔄 {translate("reverse_ip_lookup", selected_lang)}'),
            (3, f'🔢 {translate("asn_lookup", selected_lang)}'),
            (4, f'🔒 {translate("privacy_api", selected_lang)}'),
            (5, f'🔍 {translate("port_scanner", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(network_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def security_menu():
        """Security menu - modernized view"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_security", selected_lang)
        
        # Submenu options
        security_options = [
            (1, f'📧 {translate("email_validator", selected_lang)}'),
            (2, f'🔍 {translate("have_i_been_pwned", selected_lang)}'),
            (3, f'🔒 {translate("tls_scan", selected_lang)}'),
            (4, f'📝 {translate("js_security_scanner", selected_lang)}'),
            (5, f'🔄 {translate("url_bypasser", selected_lang)}'),
            (6, f'🛡️ {translate("ssl_certificate_info", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(security_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def threat_intel_menu():
        """Threat intelligence menu - modernized view"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_threat_intel", selected_lang)
        
        # Submenu options
        threat_intel_options = [
            (1, f'🔍 {translate("misp_check", selected_lang)}'),
            (2, f'👁️ {translate("otx_check", selected_lang)}'),
            (3, f'🦊 {translate("threatfox_check", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(threat_intel_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def vulnerability_menu():
        """Vulnerability menu - modernized view"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_vulnerability", selected_lang)
        
        # Submenu options
        vulnerability_options = [
            (1, f'🔍 {translate("cve_lookup", selected_lang)}'),
            (2, f'🔎 {translate("vulnerability_scanner", selected_lang)}'),
            (3, f'🌐 {translate("web_vulnerability_scanner", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(vulnerability_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def osint_menu():
        """OSINT menu - modernized view"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_osint", selected_lang)
        
        # Submenu options
        osint_options = [
            (1, f'🔍 {translate("whois_lookup", selected_lang)}'),
            (2, f'🌐 {translate("subdomain_finder", selected_lang)}'),
            (3, f'📧 {translate("email_finder", selected_lang)}'),
            (4, f'📱 {translate("social_media_finder", selected_lang)}'),
            (5, f'💾 {translate("leaked_data_checker", selected_lang)}'),
            (6, f'📋 {translate("pastebin_scraper", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(osint_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def additional_menu():
        """Additional features menu - modernized view"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_additional", selected_lang)
        
        # Submenu options
        additional_options = [
            (1, f'⚡ {translate("performance_test", selected_lang)}'),
            (2, f'🔐 {translate("encryption_tools", selected_lang)}'),
            (3, f'🎲 {translate("random_generator", selected_lang)}'),
            (4, f'🔄 {translate("converter_tools", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(additional_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def ml_anomaly_menu():
        """Machine learning anomaly detection menu"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_ml_anomaly", selected_lang)
        
        # Submenu options
        ml_anomaly_options = [
            (1, f'🌐 {translate("network_anomaly", selected_lang)}'),
            (2, f'👤 {translate("user_behavior", selected_lang)}'),
            (3, f'📊 {translate("log_anomaly", selected_lang)}'),
            (4, f'💻 {translate("system_resource", selected_lang)}'),
            (5, f'🧠 {translate("model_training", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(ml_anomaly_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def log_analysis_menu():
        """Log analysis menu"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_log_analysis", selected_lang)
        
        # Submenu options
        log_analysis_options = [
            (1, f'📥 {translate("log_collector", selected_lang)}'),
            (2, f'🔍 {translate("log_parser", selected_lang)}'),
            (3, f'🔗 {translate("correlation_engine", selected_lang)}'),
            (4, f'📋 {translate("event_visualization", selected_lang)}'),
            (5, f'📈 {translate("log_analyzer", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(log_analysis_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def blockchain_security_menu():
        """Blockchain security menu"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_blockchain_security", selected_lang)
        
        # Submenu options
        blockchain_options = [
            (1, f'🤖 {translate("smart_contract_analyzer", selected_lang)}'),
            (2, f'💱 {translate("transaction_analyzer", selected_lang)}'),
            (3, f'👛 {translate("wallet_security_check", selected_lang)}'),
            (4, f'💰 {translate("crypto_asset_monitor", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(blockchain_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def zero_trust_menu():
        """Zero Trust security menu"""
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("category_zero_trust", selected_lang)
        
        # Submenu options
        zero_trust_options = [
            (1, f'📝 {translate("access_policy_analyzer", selected_lang)}'),
            (2, f'🔄 {translate("network_segmentation_check", selected_lang)}'),
            (3, f'🔐 {translate("identity_verification_check", selected_lang)}'),
            (4, f'🧩 {translate("context_based_security", selected_lang)}'),
            (5, f'📊 {translate("zero_trust_assessment", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(zero_trust_options, category_title, box_width, selected_lang)