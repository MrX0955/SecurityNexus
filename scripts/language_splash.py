#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import math
from colorama import Fore, Style, Back, init
from core.config import load_config, save_config, config
from core.menu_theme import MenuTheme
from utils.helpers import clear

def select_language():
    """
    Program başlangıcında görünen modern ve animasyonlu dil seçme ekranı
    """
    init(autoreset=True)
    clear()
    
    # Terminal genişliğini al
    term_width = os.get_terminal_size().columns
    
    # Animasyonlu başlık
    title = "Tercih Edilen Dili Seç / Select Your Language"
    
    # Başlığı merkezle
    title_padding = (term_width - len(title)) // 2
    
    # 3D Efektli başlık
    sys.stdout.write("\n" + " " * title_padding)
    
    # Renk paleti
    colors = [Fore.CYAN, Fore.LIGHTCYAN_EX, Fore.BLUE]
    
    # Efektli başlık yazdırma
    for i, char in enumerate(title):
        # Renk seçimi
        color_index = i % len(colors)
        color = colors[color_index]
        
        # Yazı efekti
        if char == " ":
            sys.stdout.write(" ")
        else:
            sys.stdout.write(f"{color}{Style.BRIGHT}{char}")
        sys.stdout.flush()
        time.sleep(0.01)
    
    print("\n")
    
    # Dekoratif çizgi
    line_char = "─"
    line = line_char * (term_width - 20)
    line_padding = (term_width - len(line)) // 2
    
    # Çizgiyi animasyonlu göster
    sys.stdout.write(" " * line_padding)
    for char in line:
        sys.stdout.write(f"{Fore.BLUE}{char}")
        sys.stdout.flush()
        time.sleep(0.005)
    print("\n")
    
    # Dil seçenekleri
    languages = [
        {"code": "tr", "name": "Türkçe", "flag": "🇹🇷"},
        {"code": "en", "name": "English", "flag": "🇺🇸"}
    ]
    
    # Seçenekleri merkezde göster
    options_width = 40
    options_padding = (term_width - options_width) // 2
    
    # Seçenekler için kutular çiz
    for i, lang in enumerate(languages):
        # Kutunun başlangıcını çiz
        option_text = f"{lang['flag']} {lang['name']}"
        # Seçenekler arası boşluk
        print(" " * options_padding, end="")
        
        # Animasyonlu seçenek kutusu
        sys.stdout.write(f"{Fore.CYAN}{MenuTheme.BOX_TOP_LEFT}")
        for _ in range(options_width - 2):
            sys.stdout.write(f"{Fore.CYAN}{MenuTheme.BOX_HORIZONTAL}")
            sys.stdout.flush()
            time.sleep(0.002)
        sys.stdout.write(f"{Fore.CYAN}{MenuTheme.BOX_TOP_RIGHT}\n")
        
        # Kutunun orta kısmı
        print(f"{' ' * options_padding}{Fore.CYAN}{MenuTheme.BOX_VERTICAL}{Fore.RESET}{' ' * ((options_width - 2 - len(option_text)) // 2)}{Fore.WHITE}{Style.BRIGHT}{option_text}{Fore.RESET}{' ' * ((options_width - 2 - len(option_text) + 1) // 2)}{Fore.CYAN}{MenuTheme.BOX_VERTICAL}")
        
        # Kutunun alt kısmı
        print(f"{' ' * options_padding}{Fore.CYAN}{MenuTheme.BOX_BOTTOM_LEFT}", end="")
        for _ in range(options_width - 2):
            sys.stdout.write(f"{Fore.CYAN}{MenuTheme.BOX_HORIZONTAL}")
            sys.stdout.flush()
            time.sleep(0.002)
        print(f"{Fore.CYAN}{MenuTheme.BOX_BOTTOM_RIGHT}")
        
        # Seçenekler arası boşluk
        if i < len(languages) - 1:
            print("")
    
    print("\n")
    
    # Kullanıcı seçimi
    while True:
        choice = input(f"{Fore.GREEN}Seçiminizi yapın / Make your choice (tr/en): {Fore.RESET}").lower()
        
        for lang in languages:
            if choice == lang["code"]:
                # Config'i güncelle
                if "settings" not in config:
                    config["settings"] = {}
                
                config["settings"]["language"] = choice
                save_config()
                
                # Başarı mesajı
                clear()
                message = "Dil tercihiniz kaydedildi! / Your language preference has been saved!" if choice == "tr" else "Your language preference has been saved! / Dil tercihiniz kaydedildi!"
                
                # Animasyonlu başarı mesajı
                for i in range(3):
                    sys.stdout.write("\r" + " " * term_width)
                    sys.stdout.flush()
                    time.sleep(0.1)
                    
                    message_padding = (term_width - len(message)) // 2
                    sys.stdout.write("\r" + " " * message_padding + f"{Fore.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}")
                    sys.stdout.flush()
                    time.sleep(0.2)
                
                print("\n\n")
                time.sleep(0.5)
                
                # Yükleniyor animasyonu
                loading_text = "Yükleniyor... / Loading..." if choice == "tr" else "Loading... / Yükleniyor..."
                MenuTheme.loading_animation(loading_text, duration=2.0, style="modern")
                
                return choice
        
        # Geçersiz seçim
        print(f"{Fore.RED}Geçersiz seçim! / Invalid choice!{Fore.RESET}")

if __name__ == "__main__":
    # Config'i yükle
    load_config()
    # Dil seçimini göster
    select_language() 