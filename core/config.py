import os
import json
import datetime
import re
from colorama import Fore
from functools import lru_cache

CONFIG_DIR = "config"
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
LANGUAGES_FILE = os.path.join(CONFIG_DIR, "languages.json")
VERSION = "2.0.0"

config = {}
current_language = "en"  # Default language is English
translations = {}

# Helper function to clean ANSI style codes
def strip_ansi_codes(text):
    """Clean ANSI style codes from text"""
    # Most common ANSI code pattern: \033[...m
    if not text:
        return ""
        
    # Faster cleaning with regex
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def load_config():
    global config, current_language, translations
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                current_language = config.get("settings", {}).get("language", "en")
                
                for folder in ["reports", "history"]:
                    folder_path = config.get("settings", {}).get(f"{folder}_folder", folder)
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                
                load_translations()
                return True
        else:
            print(f"{Fore.YELLOW}Configuration file not found. Creating default configuration...{Fore.RESET}")
            create_default_config()
            return load_config()
    except Exception as e:
        print(f"{Fore.RED}Error loading configuration: {e}{Fore.RESET}")
        return False

def create_default_config():
    default_config = {
        "settings": {
            "language": "en",  # Default language is English
            "save_reports": True,
            "report_format": "html",
            "reports_folder": "reports",
            "history_folder": "history",
            "auto_update": True,
            "update_check_interval_days": 7,
            "default_timeout": 10,
            "max_concurrent_tasks": 3
        },
        "api_keys": {
            "hackertarget": "",
            "hibp": "",
            "misp": "",
            "otx": "",
            "threatfox": "",
            "shodan": ""
        },
        "threat_intelligence": {
            "misp_url": "",
            "otx_pulse_days": 30
        },
        "last_update_check": datetime.datetime.now().strftime("%Y-%m-%d"),
        "language_options": ["en", "tr"],
        "first_run": True  # İlk çalıştırma kontrolü
    }
    
    try:
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
            
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
            print(f"{Fore.GREEN}Default configuration created.{Fore.RESET}")
            
        for folder in ["reports", "history"]:
            if not os.path.exists(folder):
                os.makedirs(folder)
    except Exception as e:
        print(f"{Fore.RED}Error creating default configuration: {e}{Fore.RESET}")

def save_config():
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving configuration: {e}{Fore.RESET}")
        return False

@lru_cache(maxsize=1)
def load_translations():
    global translations
    try:
        # Try to load the languages.json file
        if os.path.exists(LANGUAGES_FILE):
            with open(LANGUAGES_FILE, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                return
        else:
            print(f"{Fore.YELLOW}Language file not found. Using default translations.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error loading translations: {e}{Fore.RESET}")
        translations = {
            "en": {
                "menu_title": "SecurityNexus - Advanced Network Intelligence Suite",
                "github": "GitHub",
                "exit": "Exit SecurityNexus",
            }
        }

@lru_cache(maxsize=256)
def _(text_id, lang=None):
    """
    Translation function - easy to understand
    """
    global translations
    if not translations:
        load_translations()
        
    try:
        if lang is None:
            lang = config.get("settings", {}).get("language", "en")
            
        if lang in translations and text_id in translations[lang]:
            return translations[lang][text_id]
        elif "en" in translations and text_id in translations["en"]:
            # Fallback to English if not found in selected language
            return translations["en"][text_id]
        else:
            # Return text_id if not found in any language
            return text_id
    except:
        return text_id

# Create alias for translate function
translate = _

class Settings:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Content-Type": "application/json",
    }

def save_to_history(action_type, data):
    try:
        history_folder = config.get("settings", {}).get("history_folder", "history")
        
        if not os.path.exists(history_folder):
            os.makedirs(history_folder)
        
        today = datetime.datetime.now().strftime("%Y%m%d")
        history_file = f"{history_folder}/history_{today}.json"
        
        history_data = []
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                try:
                    history_data = json.load(f)
                except:
                    history_data = []
        
        history_data.append({
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action_type,
            "data": data
        })
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=4)
        
        return True
    
    except Exception as e:
        print(f"{Fore.RED}Error saving to history: {e}{Fore.RESET}")
        return False 