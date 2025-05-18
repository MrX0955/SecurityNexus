#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import datetime

def create_module_template(module_name, operation_names):
    """
    Yeni modül için şablon dosyası oluşturur ve çoklu dil desteği ekler.
    
    Args:
        module_name (str): Modül adı (örn: "memory_forensics")
        operation_names (list): İşlem adları listesi (örn: ["memory_dump", "process_analysis"])
    
    Returns:
        dict: Oluşturulan modül şablonu (language.json'a eklenecek çeviriler)
    """
    translations = {}
    
    # Ana kategori adı
    category_key = f"category_{module_name}"
    translations[category_key] = {}
    
    # İşlemler için çeviri anahtarları
    for operation in operation_names:
        translations[operation] = {}
    
    # Desteklenen diller
    languages = ["tr", "en", "ru", "zh", "de", "az", "ja", "hi", "fr", "es", "ko", "la", "el"]
    
    # Örnek çeviriler oluştur (gerçek projede bunlar doldurulacak)
    for lang in languages:
        # Kategori adı
        translations[category_key][lang] = f"{module_name.replace('_', ' ').title()} [{lang}]"
        
        # İşlem adları
        for operation in operation_names:
            translations[operation][lang] = f"{operation.replace('_', ' ').title()} [{lang}]"
    
    return translations

def update_languages_file(new_translations):
    """
    Dil dosyasını yeni çevirilerle günceller
    
    Args:
        new_translations (dict): Eklenecek yeni çeviriler
    """
    languages_file = os.path.join("config", "languages.json")
    
    # Mevcut dil dosyasını yükle
    try:
        if os.path.exists(languages_file):
            with open(languages_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
        else:
            translations = {}
            for lang in ["tr", "en", "ru", "zh", "de", "az", "ja", "hi", "fr", "es", "ko", "la", "el"]:
                translations[lang] = {}
    except Exception as e:
        print(f"Dil dosyası yüklenirken hata: {e}")
        return False
    
    # Yeni çevirileri ekle
    for key, lang_dict in new_translations.items():
        for lang, value in lang_dict.items():
            if lang not in translations:
                translations[lang] = {}
            translations[lang][key] = value
    
    # Dil dosyasını kaydet
    try:
        with open(languages_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Dil dosyası kaydedilirken hata: {e}")
        return False

def create_module_file(module_name, operation_names):
    """
    Yeni bir modül dosyası oluşturur
    
    Args:
        module_name (str): Modül adı
        operation_names (list): İşlem adları listesi
    """
    module_file = os.path.join("modules", f"{module_name}.py")
    
    class_name = f"{module_name.title().replace('_', '')}Operations"
    
    # Modül şablonu
    module_content = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
from colorama import Fore, Style
from core.config import _, config
from utils.helpers import clear, print_info, print_success, print_error

class {class_name}:
    @staticmethod
    def menu():
        \"\"\"Modül menüsünü gösterir\"\"\"
        # Config'den dil ayarını al
        selected_lang = config.get("settings", {{}}).get("language", "tr")
        
        clear()
        print(f"{{Fore.CYAN}}{{_('category_{module_name}', selected_lang)}}{{Fore.RESET}}\\n")
        
"""
    
    # Her işlem için fonksiyon ekle
    for i, operation in enumerate(operation_names):
        module_content += f"""    @staticmethod
    def {operation}():
        \"\"\"
        {operation.replace('_', ' ').title()}
        \"\"\"
        # Config'den dil ayarını al
        selected_lang = config.get("settings", {{}}).get("language", "tr")
        
        clear()
        print(f"{{Fore.CYAN}}{{_('category_{module_name}', selected_lang)}} - {{_('{operation}', selected_lang)}}{{Fore.RESET}}\\n")
        
        # İşlem kodu buraya gelecek
        
        print(f"\\n{{Fore.YELLOW}}{{_('operation_completed', selected_lang)}}{{Fore.RESET}}")
        input(f"\\n{{_('continue_prompt', selected_lang)}}")
        
"""

    # Dosyayı yaz
    try:
        with open(module_file, 'w', encoding='utf-8') as f:
            f.write(module_content)
        print(f"Modül dosyası oluşturuldu: {module_file}")
        return True
    except Exception as e:
        print(f"Modül dosyası oluşturulurken hata: {e}")
        return False

def create_new_module():
    """Yeni bir modül oluşturmak için etkileşimli işlem"""
    print("=== Yeni Modül Oluşturma ===\n")
    
    module_name = input("Modül adı: ").strip().lower().replace(" ", "_")
    
    if not module_name:
        print("Modül adı boş olamaz.")
        return
    
    operations = []
    print("\nİşlem adlarını girin (boş bırakarak bitirin):")
    
    i = 1
    while True:
        operation = input(f"{i}. işlem: ").strip().lower().replace(" ", "_")
        if not operation:
            break
        operations.append(operation)
        i += 1
    
    if not operations:
        print("En az bir işlem eklemelisiniz.")
        return
    
    # Çevirileri oluştur
    translations = create_module_template(module_name, operations)
    
    # Dil dosyasını güncelle
    if update_languages_file(translations):
        print("\nDil dosyası güncellendi.")
    else:
        print("\nDil dosyası güncellenirken hata oluştu.")
    
    # Modül dosyasını oluştur  
    if create_module_file(module_name, operations):
        print("\nModül başarıyla oluşturuldu.")
    else:
        print("\nModül oluşturulurken hata oluştu.")

if __name__ == "__main__":
    create_new_module() 