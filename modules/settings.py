import os
import json
import datetime
import inquirer
from colorama import Fore, Style
from core.config import translate, config, save_config, load_config, load_translations
from utils.helpers import clear
from core.menu_theme import MenuTheme

class SettingsOperations:
    @staticmethod
    def settings_menu():
        # Get language setting from config
        selected_lang = config.get("settings", {}).get("language", "en")
        
        # Get terminal width
        term_width = os.get_terminal_size().columns
        box_width = min(80, term_width)
        
        # Menu title
        category_title = translate("settings_menu", selected_lang)
        
        # Submenu options
        settings_options = [
            ('language', f'🌐 {translate("change_language", selected_lang)}'),
            ('api_keys', f'🔑 {translate("api_keys", selected_lang)}'),
            ('reports', f'📊 {translate("report_settings", selected_lang)}'),
            ('threat_intel', f'🔍 {translate("threat_intel_settings", selected_lang)}'),
            ('about', f'ℹ️ {translate("about", selected_lang)}'),
            ('back', f'↩️ {translate("back_to_main", selected_lang)}')
        ]
        
        # Use the new arrow key menu
        return MenuTheme.draw_arrow_menu(settings_options, category_title, box_width, selected_lang)
    
    @staticmethod
    def change_language():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}=== {translate('change_language', selected_lang)} ==={Fore.RESET}")
        
        # Mevcut dili ve dil seçeneklerini al
        language_options = config.get("language_options", ["en", "tr"])
        
        # Config yapısını kontrol et ve gerekirse oluştur
        if "settings" not in config:
            config["settings"] = {}
            
        # Mevcut dil ayarını al
        current_language = config.get("settings", {}).get("language", "en")
        
        choices = []
        for lang in language_options:
            if lang == current_language:
                choices.append(f"🔹 {lang} ({translate('current', selected_lang)})")
            else:
                choices.append(lang)
        
        questions = [
            inquirer.List(
                'language',
                message=f'{Fore.CYAN}{translate("select_language", selected_lang)}:{Fore.RESET}',
                choices=choices
            )
        ]
        
        result = inquirer.prompt(questions)
        
        if result is None:
            return
            
        selected_lang = result['language']

        if "🔹" in selected_lang:
            selected_lang = selected_lang.split()[1]
        
        if selected_lang != current_language:
            # Config yapısını kontrol et ve gerekirse oluştur
            if "settings" not in config:
                config["settings"] = {}
                
            config["settings"]["language"] = selected_lang
            save_config()
            load_translations()
            print(f"{Fore.GREEN}{translate('language_changed', selected_lang)}{Fore.RESET}")
        else:
            print(f"{Fore.YELLOW}{translate('same_language_selected', selected_lang)}{Fore.RESET}")
        
        input(f"{translate('press_enter', selected_lang)}")
    
    @staticmethod
    def api_keys():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}=== {translate('api_keys', selected_lang)} ==={Fore.RESET}")
        
        api_keys = config.get("api_keys", {})

        print(f"{Fore.YELLOW}{translate('current_api_keys', selected_lang)}{Fore.RESET}")
        for service, key in api_keys.items():
            if key:
                masked_key = f"{key[:4]}{'*' * (len(key) - 8)}{key[-4:]}" if len(key) > 8 else "****"
                print(f"  {Fore.GREEN}✓ {service}: {masked_key}{Fore.RESET}")
            else:
                print(f"  {Fore.RED}✗ {service}: {translate('not_set', selected_lang)}{Fore.RESET}")
        
        print("")
        services = list(api_keys.keys())
        
        choices = [(service, service) for service in services]
        choices.append((translate("back", selected_lang), "back"))
        
        questions = [
            inquirer.List(
                'service',
                message=f'{Fore.CYAN}{translate("select_api_to_update", selected_lang)}:{Fore.RESET}',
                choices=choices
            )
        ]
        
        result = inquirer.prompt(questions)
        
        if result is None or result['service'] == "back":
            return
        
        service = result['service']
        current_key = api_keys.get(service, "")
        
        print(f"{Fore.CYAN}{translate('updating_api_key', selected_lang)}: {service}{Fore.RESET}")
        if current_key:
            print(f"{Fore.YELLOW}{translate('current_value', selected_lang)}: {current_key[:4]}{'*' * (len(current_key) - 8)}{current_key[-4:]}{Fore.RESET}")
        
        new_key = input(f"{Fore.MAGENTA}{translate('enter_new_api_key', selected_lang)} ({translate('empty_to_cancel', selected_lang)}): {Fore.RESET}")
        
        if new_key:
            config["api_keys"][service] = new_key
            save_config()
            print(f"{Fore.GREEN}{translate('api_key_updated', selected_lang)}: {service}{Fore.RESET}")
        else:
            print(f"{Fore.YELLOW}{translate('operation_cancelled', selected_lang)}{Fore.RESET}")
        
        input(translate('press_enter', selected_lang))
        SettingsOperations.api_keys()
    
    @staticmethod
    def report_settings():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}=== {translate('report_settings', selected_lang)} ==={Fore.RESET}")
        
        settings = config.get("settings", {})
        
        save_reports = settings.get("save_reports", True)
        report_format = settings.get("report_format", "html")
        reports_folder = settings.get("reports_folder", "reports")
        
        print(f"{Fore.YELLOW}{translate('current_report_settings', selected_lang)}{Fore.RESET}")
        print(f"  {translate('save_reports', selected_lang)}: {Fore.GREEN if save_reports else Fore.RED}{save_reports}{Fore.RESET}")
        print(f"  {translate('report_format', selected_lang)}: {Fore.CYAN}{report_format}{Fore.RESET}")
        print(f"  {translate('reports_folder', selected_lang)}: {Fore.CYAN}{reports_folder}{Fore.RESET}")
        
        options = [
            (translate("toggle_save_reports", selected_lang), "toggle_save"),
            (translate("change_report_format", selected_lang), "change_format"),
            (translate("change_reports_folder", selected_lang), "change_folder"),
            (translate("back", selected_lang), "back")
        ]
        
        questions = [
            inquirer.List(
                'option',
                message=f'{Fore.CYAN}{translate("make_selection", selected_lang)}:{Fore.RESET}',
                choices=[(name, value) for name, value in options]
            )
        ]
        
        result = inquirer.prompt(questions)
        
        if result is None or result['option'] == "back":
            return
        
        option = result['option']
        
        if option == "toggle_save":
            config["settings"]["save_reports"] = not save_reports
            save_config()
            print(f"{Fore.GREEN}{translate('save_reports_set_to', selected_lang)} {not save_reports}{Fore.RESET}")
        
        elif option == "change_format":
            format_options = ["html", "json", "txt"]
            
            format_questions = [
                inquirer.List(
                    'format',
                    message=f'{Fore.CYAN}{translate("select_report_format", selected_lang)}:{Fore.RESET}',
                    choices=format_options
                )
            ]
            
            format_result = inquirer.prompt(format_questions)
            
            if format_result:
                new_format = format_result['format']
                config["settings"]["report_format"] = new_format
                save_config()
                print(f"{Fore.GREEN}{translate('report_format_set_to', selected_lang)} {new_format}{Fore.RESET}")
        
        elif option == "change_folder":
            new_folder = input(f"{Fore.MAGENTA}{translate('enter_reports_folder', selected_lang)} ({translate('current', selected_lang)}: {reports_folder}): {Fore.RESET}")
            
            if new_folder:

                if not os.path.exists(new_folder):
                    try:
                        os.makedirs(new_folder)
                        print(f"{Fore.GREEN}{translate('created_folder', selected_lang)}: {new_folder}{Fore.RESET}")
                    except Exception as e:
                        print(f"{Fore.RED}{translate('error_creating_folder', selected_lang)}: {e}{Fore.RESET}")
                        input(translate('press_enter', selected_lang))
                        SettingsOperations.report_settings()
                        return
                
                config["settings"]["reports_folder"] = new_folder
                save_config()
                print(f"{Fore.GREEN}{translate('reports_folder_set_to', selected_lang)} {new_folder}{Fore.RESET}")
        
        input(translate('press_enter', selected_lang))
        SettingsOperations.report_settings()
    
    @staticmethod
    def threat_intel_settings():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}=== {translate('threat_intel_settings', selected_lang)} ==={Fore.RESET}")
        
        threat_intel = config.get("threat_intelligence", {})
        
        misp_url = threat_intel.get("misp_url", "")
        otx_pulse_days = threat_intel.get("otx_pulse_days", 30)
        
        print(f"{Fore.YELLOW}{translate('current_threat_intel_settings', selected_lang)}{Fore.RESET}")
        print(f"  MISP URL: {Fore.CYAN}{misp_url if misp_url else translate('not_set', selected_lang)}{Fore.RESET}")
        print(f"  OTX Pulse Days: {Fore.CYAN}{otx_pulse_days}{Fore.RESET}")
        
        options = [
            (translate("set_misp_url", selected_lang), "set_misp_url"),
            (translate("set_otx_pulse_days", selected_lang), "set_otx_pulse_days"),
            (translate("back", selected_lang), "back")
        ]
        
        questions = [
            inquirer.List(
                'option',
                message=f'{Fore.CYAN}{translate("make_selection", selected_lang)}:{Fore.RESET}',
                choices=[(name, value) for name, value in options]
            )
        ]
        
        result = inquirer.prompt(questions)
        
        if result is None or result['option'] == "back":
            return
        
        option = result['option']
        
        if option == "set_misp_url":
            new_url = input(f"{Fore.MAGENTA}{translate('enter_misp_url', selected_lang)} ({translate('current', selected_lang)}: {misp_url}): {Fore.RESET}")
            
            if new_url:
                if not "threat_intelligence" in config:
                    config["threat_intelligence"] = {}
                
                config["threat_intelligence"]["misp_url"] = new_url
                save_config()
                print(f"{Fore.GREEN}MISP URL {translate('set_to', selected_lang)} {new_url}{Fore.RESET}")
        
        elif option == "set_otx_pulse_days":
            try:
                new_days = int(input(f"{Fore.MAGENTA}{translate('enter_otx_pulse_days', selected_lang)} ({translate('current', selected_lang)}: {otx_pulse_days}): {Fore.RESET}"))
                
                if new_days > 0:
                    if not "threat_intelligence" in config:
                        config["threat_intelligence"] = {}
                    
                    config["threat_intelligence"]["otx_pulse_days"] = new_days
                    save_config()
                    print(f"{Fore.GREEN}OTX Pulse Days {translate('set_to', selected_lang)} {new_days}{Fore.RESET}")
                else:
                    print(f"{Fore.RED}{translate('must_be_positive_number', selected_lang)}{Fore.RESET}")
            except ValueError:
                print(f"{Fore.RED}{translate('must_be_valid_number', selected_lang)}{Fore.RESET}")
        
        input(translate('press_enter', selected_lang))
        SettingsOperations.threat_intel_settings()
    
    @staticmethod
    def about():
        from core.config import VERSION
        
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}=== {translate('about', selected_lang)} ==={Fore.RESET}")
        
        print(f"{Fore.GREEN}SecurityNexus v{VERSION}{Fore.RESET}")
        print(f"{Fore.CYAN}Advanced Network Intelligence Suite{Fore.RESET}")
        print("")
        print(f"{Fore.YELLOW}© {datetime.datetime.now().year} SecurityNexus{Fore.RESET}")
        print("")
        print(f"{Fore.MAGENTA}GitHub:{Fore.RESET} https://github.com/MrX0955/SecurityNexus")
        print("")
        print(f"{Fore.CYAN}Features:{Fore.RESET}")
        print("  • DNS & Network Operations")
        print("  • Security Analysis")
        print("  • Threat Intelligence")
        print("  • Vulnerability Assessment")
        print("  • OSINT Tools")
        print("")
        print(f"{Fore.YELLOW}License: MIT{Fore.RESET}")
        
        input(translate('press_enter', selected_lang)) 