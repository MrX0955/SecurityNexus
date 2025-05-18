from colorama import Fore, Back, Style
import time
import sys
import os
import random
import math
from core.utils import clear
from core.config import translate, config

class MenuTheme:
    """
    MenuTheme class manages the colors, styles and visual design elements used in the menu system.
    """
    # Renk kodları ve stiller
    HEADING = Fore.CYAN + Style.BRIGHT
    TITLE_COLOR = Fore.CYAN
    ACTIVE_ITEM = Fore.LIGHTGREEN_EX
    ERROR = Fore.LIGHTRED_EX
    INFO = Fore.LIGHTBLUE_EX  
    SUCCESS = Fore.LIGHTGREEN_EX
    WARNING = Fore.LIGHTYELLOW_EX
    
    # Kutu çizim karakterleri - Modern görünüm
    BOX_HORIZONTAL = "─"
    BOX_VERTICAL = "│"
    BOX_TOP_LEFT = "╭"
    BOX_TOP_RIGHT = "╮"
    BOX_BOTTOM_LEFT = "╰"
    BOX_BOTTOM_RIGHT = "╯"
    
    # Animasyon için renkler
    ANIMATION_COLORS = [
        Fore.CYAN,
        Fore.LIGHTCYAN_EX,
        Fore.BLUE,
        Fore.LIGHTBLUE_EX,
        Fore.GREEN,
        Fore.LIGHTGREEN_EX,
        Fore.MAGENTA,
        Fore.LIGHTMAGENTA_EX
    ]
    
    # Modern buton stillerinde kullanılan semboller
    BUTTON_SYMBOLS = {
        "arrow": "→",
        "check": "✓",
        "cross": "✗",
        "star": "★",
        "warning": "⚠",
        "info": "ℹ",
        "lock": "🔒",
        "unlock": "🔓",
        "settings": "⚙",
        "power": "⏻",
        "accept": "✅",
        "deny": "❌",
        "sync": "↻",
    }
    
    @staticmethod
    def draw_box(width, title=None):
        """
        Belirtilen genişlikte başlık kutusu oluşturur - Gelişmiş animasyon efektiyle
        
        Args:
            width (int): Kutunun genişliği
            title (str, optional): Kutunun içine yazılacak başlık
        
        Returns:
            list: Kutu çizgilerini içeren liste
        """
        lines = []
        
        # Üst çizgi animasyonu - Gelişmiş dalga efekti
        top_line = f"{MenuTheme.BOX_TOP_LEFT}{MenuTheme.BOX_HORIZONTAL * (width - 2)}{MenuTheme.BOX_TOP_RIGHT}"
        
        # Renkli dalga efekti ile çizgi oluştur
        animated_line = ""
        for i, char in enumerate(top_line):
            # Dalga efekti için sin fonksiyonu
            wave_position = math.sin(i/5) + 1  # 0-2 arası değer
            color_index = int(wave_position * (len(MenuTheme.ANIMATION_COLORS)/2)) % len(MenuTheme.ANIMATION_COLORS)
            animated_line += f"{MenuTheme.ANIMATION_COLORS[color_index]}{char}{Style.RESET_ALL}"
        
        lines.append(animated_line)
        
        # Başlık varsa göster - Animasyonlu ve gölgeli
        if title:
            # Başlık için boşluk hesapla (ortala)
            title_length = len(title.replace('\033[0m', '').replace('\033[36m', '').replace('\033[1m', ''))
            padding_left = (width - 2 - title_length) // 2
            padding_right = width - 2 - title_length - padding_left
            
            # Animasyonlu dikey çizgiler - Parlama efekti
            left_border = f"{Fore.CYAN + Style.BRIGHT}{MenuTheme.BOX_VERTICAL}{Style.RESET_ALL}"
            right_border = f"{Fore.CYAN + Style.BRIGHT}{MenuTheme.BOX_VERTICAL}{Style.RESET_ALL}"
            
            # Başlık metni - Gölge efektli
            enhanced_title = ""
            for char in title.replace('\033[0m', '').replace('\033[36m', '').replace('\033[1m', ''):
                enhanced_title += f"{Fore.CYAN + Style.BRIGHT}{char}{Style.RESET_ALL}"
            
            title_line = f"{left_border}{' ' * padding_left}{enhanced_title}{' ' * padding_right}{right_border}"
            lines.append(title_line)
            
            # Başlık altı ayırıcı çizgi - Gelişmiş gradyan efekti
            separator = f"{MenuTheme.BOX_VERTICAL}{MenuTheme.BOX_HORIZONTAL * (width - 2)}{MenuTheme.BOX_VERTICAL}"
            
            # Renk gradyanı oluştur
            animated_separator = ""
            for i, char in enumerate(separator):
                # Pozisyon bazlı renk gradyanı
                pos_ratio = i / len(separator)  # 0-1 arası
                color_index = int(pos_ratio * len(MenuTheme.ANIMATION_COLORS)) % len(MenuTheme.ANIMATION_COLORS)
                animated_separator += f"{MenuTheme.ANIMATION_COLORS[color_index]}{char}{Style.RESET_ALL}"
            
            lines.append(animated_separator)
        
        return lines
    
    @staticmethod
    def draw_box_bottom(width):
        """
        Belirtilen genişlikte kutu alt kenarı oluşturur - Gelişmiş animasyon efektiyle
        
        Args:
            width (int): Kutunun genişliği
        
        Returns:
            str: Kutu alt kenarını temsil eden string
        """
        bottom_line = f"{MenuTheme.BOX_BOTTOM_LEFT}{MenuTheme.BOX_HORIZONTAL * (width - 2)}{MenuTheme.BOX_BOTTOM_RIGHT}"
        
        # Gelişmiş renk efekti - Tersine dalga
        animated_bottom = ""
        for i, char in enumerate(bottom_line):
            # Dalga efekti için cos fonksiyonu (sin'in tersi)
            wave_position = math.cos(i/5) + 1  # 0-2 arası değer
            color_index = int(wave_position * (len(MenuTheme.ANIMATION_COLORS)/2)) % len(MenuTheme.ANIMATION_COLORS)
            animated_bottom += f"{MenuTheme.ANIMATION_COLORS[color_index]}{char}{Style.RESET_ALL}"
        
        return animated_bottom
    
    @staticmethod
    def animate_text(text, colors, delay=0.03):
        """
        Renk geçişli animasyonlu metin görüntüler
        
        Args:
            text (str): Animasyonlu gösterilecek metin
            colors (list): Kullanılacak renk kodları listesi
            delay (float, optional): Animasyon gecikmesi
        """
        color_index = 0
        
        for char in text:
            # Karakter başına renk değiştir ve parlaklık ekle
            color = colors[color_index]
            sys.stdout.write(f"{color + Style.BRIGHT}{char}{Style.RESET_ALL}")
            sys.stdout.flush()
            
            # Renk indeksini döngüsel olarak değiştir
            color_index = (color_index + 1) % len(colors)
            
            # Rastgele hafif gecikme varyasyonu ekle (daha doğal görünüm)
            variation = random.uniform(0.8, 1.2)
            time.sleep(delay * variation)
        
        print()  # Yeni satır
    
    @staticmethod
    def loading_animation(message, duration=1.0, style="dots"):
        """
        Yükleme animasyonu gösterir - Modern ve gelişmiş efektlerle
        
        Args:
            message (str): Animasyon yanında gösterilecek mesaj
            duration (float): Animasyon süresi (saniye)
            style (str): Animasyon stili ("dots", "spinner", "bar", "pulse", "blocks", "modern")
        """
        # Gelişmiş animasyon kareleri
        frames = {
            "dots": ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
            "spinner": ["◐", "◓", "◑", "◒"],
            "bar": ["[▰▱▱▱▱▱▱▱▱▱]", "[▰▰▱▱▱▱▱▱▱▱]", "[▰▰▰▱▱▱▱▱▱▱]", "[▰▰▰▰▱▱▱▱▱▱]", 
                    "[▰▰▰▰▰▱▱▱▱▱]", "[▰▰▰▰▰▰▱▱▱▱]", "[▰▰▰▰▰▰▰▱▱▱]", "[▰▰▰▰▰▰▰▰▱▱]",
                    "[▰▰▰▰▰▰▰▰▰▱]", "[▰▰▰▰▰▰▰▰▰▰]"],
            "pulse": ["∙∙∙∙∙", "•∙∙∙∙", "∙•∙∙∙", "∙∙•∙∙", "∙∙∙•∙", "∙∙∙∙•", "∙∙∙∙∙"],
            "blocks": ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▁"],
            "modern": ["⢀⠀", "⡀⠀", "⠄⠀", "⢂⠀", "⡂⠀", "⠅⠀", "⢃⠀", "⡃⠀", "⠍⠀", "⢋⠀", "⡋⠀", "⠍⠁", "⢋⠁", "⡋⠁", "⠍⠉", "⠋⠉", "⠋⠉", "⠉⠙", "⠉⠙", "⠉⠩", "⠈⢙", "⠈⡙", "⢈⠩", "⡀⢙", "⠄⡙", "⢂⠩", "⡂⢘", "⠅⡘", "⢃⠨", "⡃⢐", "⠍⡐", "⢋⠠", "⡋⢀", "⠍⡁", "⢋⠁", "⡋⠁", "⠍⠉", "⠋⠉", "⠋⠉", "⠉⠙", "⠉⠙", "⠉⠩", "⠈⢙", "⠈⡙", "⠈⠩", "⠀⢙", "⠀⡙", "⠀⠩", "⠀⢘", "⠀⡘", "⠀⠨", "⠀⢐", "⠀⡐", "⠀⠠", "⠀⢀", "⠀⡀"]
        }
        
        # Animasyon stili yoksa default
        selected_style = style if style in frames else "dots"
        selected_frames = frames[selected_style]
        
        start_time = time.time()
        frame_index = 0
        
        # Başlık renkleri için index
        color_index = 0
        
        # Mesaj ön işleme
        if message:
            message = f" {message}"
            
        # Terminalde çıkış genişliği
        term_width = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80
        
        while (time.time() - start_time) < duration:
            frame = selected_frames[frame_index]
            # Her karedeki renk değişimi
            color = MenuTheme.ANIMATION_COLORS[color_index]
            
            # Özel animasyon stilleri için değişken içerik
            if style == "bar":
                # İlerleme çubuğu stili
                progress = int((time.time() - start_time) / duration * 100)
                progress_text = f" {progress}%"
                sys.stdout.write(f"\r{color}{frame}{progress_text}{message}{Style.RESET_ALL}")
            elif style == "blocks":
                # 3D blok animasyonu
                blocks = ""
                for i in range(10):
                    block_idx = (frame_index + i) % len(selected_frames)
                    block_color = MenuTheme.ANIMATION_COLORS[(color_index + i) % len(MenuTheme.ANIMATION_COLORS)]
                    blocks += f"{block_color}{selected_frames[block_idx]}{Style.RESET_ALL}"
                sys.stdout.write(f"\r{blocks}{message}{Style.RESET_ALL}")
            elif style == "modern":
                # Modern kaydırmalı animasyon
                loading_bar = ""
                for i in range(min(10, term_width // 4)):
                    idx = (frame_index + i * 2) % len(selected_frames)
                    bar_color = MenuTheme.ANIMATION_COLORS[(color_index + i) % len(MenuTheme.ANIMATION_COLORS)]
                    loading_bar += f"{bar_color}{selected_frames[idx]}{Style.RESET_ALL}"
                sys.stdout.write(f"\r{loading_bar}{message}{Style.RESET_ALL}")
            else:
                # Standart animasyonlar
                sys.stdout.write(f"\r{color}{frame}{message}{Style.RESET_ALL}")
                
            sys.stdout.flush()
            
            # Frame indeksini güncelle
            frame_index = (frame_index + 1) % len(selected_frames)
            color_index = (color_index + 1) % len(MenuTheme.ANIMATION_COLORS)
            
            # Yükleme hızı ayarları - stil bazlı
            if style == "blocks" or style == "modern":
                time.sleep(0.05)
            elif style == "bar":
                time.sleep(0.1)
            else:
                time.sleep(0.08)  # Standart animasyon hızı
            
        # Animasyon bitince temizle
        sys.stdout.write("\r" + " " * (term_width) + "\r")
        sys.stdout.flush()
    
    @staticmethod
    def typing_animation(text, delay=0.03, color=Fore.CYAN):
        """
        Yazı yazılıyormuş gibi bir animasyon gösterir - Geliştirilmiş 3D efektli
        
        Args:
            text (str): Animasyonla gösterilecek metin
            delay (float): Karakterler arası gecikme
            color (str): Metin rengi
        """
        # 3D efekti için renk paletleri
        palettes = {
            "blue": [Fore.LIGHTBLUE_EX, Fore.BLUE, Fore.CYAN],
            "green": [Fore.LIGHTGREEN_EX, Fore.GREEN, Fore.CYAN],
            "red": [Fore.LIGHTRED_EX, Fore.RED, Fore.YELLOW],
            "purple": [Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.BLUE],
            "gold": [Fore.YELLOW, Fore.LIGHTYELLOW_EX, Fore.WHITE]
        }
        
        # Giriş rengine göre palette seç
        palette_key = "blue"  # default
        if color == Fore.GREEN or color == Fore.LIGHTGREEN_EX:
            palette_key = "green"
        elif color == Fore.RED or color == Fore.LIGHTRED_EX:
            palette_key = "red"
        elif color == Fore.MAGENTA or color == Fore.LIGHTMAGENTA_EX:
            palette_key = "purple"
        elif color == Fore.YELLOW or color == Fore.LIGHTYELLOW_EX:
            palette_key = "gold"
            
        palette = palettes[palette_key]
        
        # 3D efekt için karakter yüksekliği ve gölge karakterleri
        shadows = ["▒", "░", "▓"]
        
        # Her karakter için
        for i, char in enumerate(text):
            # Rastgele hafif renk varyasyonu ekle
            if char != ' ':
                # 3D efekti için karakter ve gölgesi
                main_color = palette[0] + Style.BRIGHT
                
                # Özel karakterlerde daha belirgin efekt
                if char in ['.', ',', '!', '?', ';', ':', '"', "'", '(', ')', '[', ']', '{', '}']:
                    # 3D ışık efekti
                    sys.stdout.write(f"{palette[2]}{shadows[0]}")
                    sys.stdout.flush()
                    time.sleep(delay * 0.2)
                    sys.stdout.write(f"\b{palette[1]}{shadows[1]}")
                    sys.stdout.flush()
                    time.sleep(delay * 0.2)
                    sys.stdout.write(f"\b{main_color}{char}")
                else:
                    # Normal karakter 3D efekti
                    sys.stdout.write(f"{main_color}{char}")
            else:
                # Boşluklar için basit efekt
                sys.stdout.write(" ")
            
            sys.stdout.flush()
            
            # Gerçekçi yazma gecikmesi (bazı karakterlerde daha uzun)
            if char in ['.', ',', '!', '?', ';', ':']:
                char_delay = delay * 3
            elif char == ' ':
                char_delay = delay * 1.5
            else:
                # Rastgele hafif gecikme varyasyonu (daha doğal yazma)
                char_delay = delay * random.uniform(0.7, 1.3)
                
            time.sleep(char_delay)
                
        # 3D efekti tamamlamak için son bir gölge
        if len(text) > 0 and text[-1] != ' ':
            sys.stdout.write(f"{palette[1]}{Style.DIM}{shadows[2]}")
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write("\b ")
            
        print()  # Yeni satır
    
    @staticmethod
    def display_welcome_banner(version, lang):
        """
        Karşılama bannerını gösterir - Gelişmiş animasyonlu
        
        Args:
            version (str): Uygulama versiyonu
            lang (str): Seçilen dil kodu
        """
        # Terminal genişliğini al
        term_width = os.get_terminal_size().columns
        
        # SecurityNexus ASCII sanatı - Modernize edilmiş
        banner = [
            " ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗███████╗███╗   ██╗████████╗██████╗ ██╗   ██╗",
            "██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝",
            "██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝ ",
            "██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝  ",
            "╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║███████╗██║ ╚████║   ██║   ██║  ██║   ██║   ",
            " ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   "
        ]
        
        # Hoş geldiniz animasyonu - ilk önce ekranın ortasından genişleyen bir nokta efekti
        center_x = term_width // 2
        MenuTheme.loading_animation(translate("program_starting", lang), 1.0, "pulse")
        
        # Banner'ı ortala ve gelişmiş 3D benzeri efektlerle göster
        for line_idx, line in enumerate(banner):
            # Satır uzunluğunu hesapla
            padding = (term_width - len(line)) // 2
            
            # Derinlik efekti için satır gecikme ve renk seçimi
            depth_delay = 0.05 * (len(banner) - line_idx)  # Üst satırlar daha geç gelir
            time.sleep(depth_delay)
            
            # Her satır için farklı renk geçişi uygula - 3D efekti
            colored_line = ""
            for i, char in enumerate(line):
                if char == ' ':
                    colored_line += " "
                    continue
                    
                # 3D derinlik efekti için konuma göre renk seçimi
                pos_ratio = (i / len(line))
                # Işık efekti: Ortada daha parlak, kenarlarda daha koyu
                brightness = 1 - abs(pos_ratio - 0.5) * 1.5
                brightness = max(0.3, min(1.0, brightness))  # 0.3-1.0 arası sınırla
                
                if brightness > 0.8:
                    style = Style.BRIGHT
                elif brightness > 0.5:
                    style = ""
                else:
                    style = Style.DIM if hasattr(Style, 'DIM') else ""
                
                # Derinlik efekti için satır indeksine göre renk
                if line_idx < 2:
                    color = Fore.CYAN
                elif line_idx < 4:
                    color = Fore.LIGHTCYAN_EX
                else:
                    color = Fore.WHITE
                
                colored_line += f"{color}{style}{char}{Style.RESET_ALL}"
            
            # Kayma efekti: Satırı sola kaydırarak göster
            for offset in range(min(10, padding)):
                slide_padding = padding - offset
                sys.stdout.write("\r" + " " * slide_padding + colored_line)
                sys.stdout.flush()
                time.sleep(0.01)
            
            print()  # Satır sonu
        
        # Sürüm bilgisi - Yanıp sönen efekt
        version_text = f"v{version} | {translate('professional_edition', lang)}"
        version_padding = (term_width - len(version_text)) // 2
        
        # Yanıp sönme efekti
        for _ in range(3):
            sys.stdout.write("\r" + " " * term_width)  # Satırı temizle
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write("\r" + " " * version_padding + f"{Fore.CYAN + Style.BRIGHT}{version_text}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(0.2)
        
        print("\n")  # Extra boşluk
        
        # Slogan - Dalga efekti
        slogan = translate("cyber_banner_slogan", lang)
        slogan_padding = (term_width - len(slogan)) // 2
        
        time.sleep(0.3)  # Slogan öncesi kısa bekleme
        
        # Dalga efekti oluştur
        wave_slogan = ""
        for i, char in enumerate(slogan):
            # Sin fonksiyonu ile dalga efekti (karakter yüksekliği)
            wave_pos = math.sin(i / 2) 
            
            # Dalga yüksekliğine göre renk seçimi
            if wave_pos > 0.7:
                color = Fore.LIGHTGREEN_EX + Style.BRIGHT
            elif wave_pos > 0:
                color = Fore.GREEN
            elif wave_pos > -0.7:
                color = Fore.CYAN
            else:
                color = Fore.BLUE
                
            wave_slogan += f"{color}{char}{Style.RESET_ALL}"
        
        # Sloganı yazdır
        print(" " * slogan_padding + wave_slogan)
        
        time.sleep(0.5)  # Efektin okunması için bekleme
    
    @staticmethod
    def draw_button(text, style="primary", width=25):
        """
        Modern buton çizimi oluşturur
        
        Args:
            text (str): Buton metni
            style (str): Buton stili (primary, success, danger, warning)
            width (int): Buton genişliği
        
        Returns:
            str: Oluşturulan buton metni
        """
        # Stile göre renkleri belirle
        if style == "primary":
            bg_color = Back.BLUE
            fg_color = Fore.WHITE
            hover_color = Back.LIGHTBLUE_EX
        elif style == "success":
            bg_color = Back.GREEN
            fg_color = Fore.WHITE
            hover_color = Back.LIGHTGREEN_EX
        elif style == "danger":
            bg_color = Back.RED
            fg_color = Fore.WHITE
            hover_color = Back.LIGHTRED_EX
        elif style == "warning":
            bg_color = Back.YELLOW
            fg_color = Fore.BLACK
            hover_color = Back.LIGHTYELLOW_EX
        else:
            bg_color = Back.LIGHTBLACK_EX
            fg_color = Fore.WHITE
            hover_color = Back.WHITE
        
        # Buton metni uzunluğunu hesapla
        text_length = len(text)
        # Padding hesapla
        padding = max(width - text_length - 2, 0)
        left_padding = padding // 2
        right_padding = padding - left_padding
        
        # Buton oluştur
        button = f"{bg_color}{fg_color}▌{' ' * left_padding}{text}{' ' * right_padding}▐{Style.RESET_ALL}"
        
        return button
    
    @staticmethod
    def draw_pill(text, width=15, color=Fore.CYAN):
        """
        Pill stili etiket oluşturur
        
        Args:
            text (str): Etiket metni
            width (int): Etiket genişliği
            color (str): Etiket rengi
        
        Returns:
            str: Oluşturulan etiket metni
        """
        text_length = len(text)
        # Padding hesapla
        padding = max(width - text_length - 2, 0)
        left_padding = padding // 2
        right_padding = padding - left_padding
        
        pill = f"{color}⦿{' ' * left_padding}{text}{' ' * right_padding}⦿{Style.RESET_ALL}"
        
        return pill
    
    @staticmethod
    def draw_toggle(state=True, label=""):
        """
        Açma/kapama düğmesi oluşturur
        
        Args:
            state (bool): Açık/kapalı durumu
            label (str): Etiket metni
        
        Returns:
            str: Oluşturulan düğme metni
        """
        if state:
            toggle = f"{Back.GREEN}{Fore.WHITE} ON {Style.RESET_ALL}"
        else:
            toggle = f"{Back.RED}{Fore.WHITE} OFF {Style.RESET_ALL}"
        
        if label:
            toggle = f"{label}: {toggle}"
        
        return toggle
    
    @staticmethod
    def display_accept_button(text, width=30):
        """
        Modern kabul butonu gösterir - Geliştirilmiş 3D efekt ve animasyon ile
        
        Args:
            text (str): Buton içindeki metin
            width (int): Buton genişliği
        """
        # Seçilen dili al - varsayılan İngilizce
        selected_lang = "en"
        if "config" in globals() and hasattr(config, "get"):
            selected_lang = config.get("settings", {}).get("language", "en")
        
        # 3D Efekt için gölgeler
        top_shadow = f"{Fore.WHITE + Style.DIM}{MenuTheme.BOX_HORIZONTAL * (width + 4)}{Style.RESET_ALL}"
        side_shadow = f"{Fore.WHITE + Style.DIM}{MenuTheme.BOX_VERTICAL}{Style.RESET_ALL}"
        
        # Buton çerçevesi içi dolu - Gradyan efektli
        button_top = f"{Fore.CYAN + Style.BRIGHT}{MenuTheme.BOX_TOP_LEFT}{MenuTheme.BOX_HORIZONTAL * width}{MenuTheme.BOX_TOP_RIGHT}{Style.RESET_ALL}"
        button_bottom = f"{Fore.CYAN + Style.BRIGHT}{MenuTheme.BOX_BOTTOM_LEFT}{MenuTheme.BOX_HORIZONTAL * width}{MenuTheme.BOX_BOTTOM_RIGHT}{Style.RESET_ALL}"
        
        # Buton metni ortala ve tik işareti ekle
        check_icon = f"{Fore.GREEN + Style.BRIGHT}{MenuTheme.BUTTON_SYMBOLS['accept']}{Style.RESET_ALL}"
        text_length = len(text)
        padding = (width - text_length - 1) // 2
        
        # Animasyonlu gradyan buton metni
        enhanced_text = ""
        for i, char in enumerate(text):
            # Pozisyon bazlı renk geçişi
            pos_ratio = i / text_length
            if pos_ratio < 0.33:
                color = Fore.LIGHTGREEN_EX
            elif pos_ratio < 0.66:
                color = Fore.CYAN
            else:
                color = Fore.LIGHTYELLOW_EX
            enhanced_text += f"{color + Style.BRIGHT}{char}{Style.RESET_ALL}"
        
        button_text = f"{Fore.CYAN + Style.BRIGHT}{MenuTheme.BOX_VERTICAL}{Style.RESET_ALL}{' ' * padding}{check_icon} {enhanced_text}{' ' * (padding - 1)}{Fore.CYAN + Style.BRIGHT}{MenuTheme.BOX_VERTICAL}{Style.RESET_ALL}"
        
        # Terminal genişliğini al
        term_width = os.get_terminal_size().columns if hasattr(os, 'get_terminal_size') else 80
        
        # Butonun konumunu hesapla ve ortala
        left_padding = (term_width - width - 2) // 2
        
        # Buton çerçevesini çiz (gölgeli 3D efekt)
        print(f"{' ' * left_padding}{button_top}")
        print(f"{' ' * left_padding}{button_text}")
        print(f"{' ' * left_padding}{button_bottom}")
        
        # Buton altında animasyonlu yardımcı mesaj
        helper_text = f"{Fore.LIGHTBLUE_EX + Style.DIM}{translate('enter_to_continue', selected_lang)}{Style.RESET_ALL}"
        helper_padding = (term_width - len(helper_text.replace('\033[0m', '').replace('\033[36m', '').replace('\033[1m', ''))) // 2
        print(f"{' ' * helper_padding}{helper_text}")
        
        # Animasyonlu hareketli imleç efekti
        for _ in range(3):
            cursor_padding = left_padding + (width // 2)
            sys.stdout.write(f"\r{' ' * cursor_padding}▼")
            sys.stdout.flush()
            time.sleep(0.2)
            sys.stdout.write(f"\r{' ' * cursor_padding} ")
            sys.stdout.flush()
            time.sleep(0.1)
    
    @staticmethod
    def rainbow_effect(text):
        """
        Bir metni gökkuşağı renkleriyle ekrana yazdırır
        
        Args:
            text (str): Renklendirilecek metin
        """
        colors = [
            Fore.RED,
            Fore.YELLOW,
            Fore.GREEN,
            Fore.CYAN,
            Fore.BLUE,
            Fore.MAGENTA
        ]
        
        colored_text = ""
        for i, char in enumerate(text):
            color_index = i % len(colors)
            colored_text += f"{colors[color_index]}{char}"
            
        print(f"{colored_text}{Style.RESET_ALL}")
    
    @staticmethod
    def pulse_text(text, color=Fore.CYAN, repeat=1, delay=0.1):
        """
        Metni titreşen efektle gösterir
        
        Args:
            text (str): Gösterilecek metin
            color (str): Metin rengi
            repeat (int): Tekrar sayısı
            delay (float): Gecikme süresi
        """
        for _ in range(repeat):
            sys.stdout.write(f"\r{color + Style.BRIGHT}{text}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(delay)
            
            sys.stdout.write(f"\r{color}{text}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(delay)
            
        # Son tekrardan sonra parlak göster
        sys.stdout.write(f"\r{color + Style.BRIGHT}{text}{Style.RESET_ALL}")
        sys.stdout.flush()
        print()  # Yeni satır
    
    @staticmethod
    def draw_arrow_menu(options, title=None, box_width=80, selected_lang=None):
        """
        Yön tuşlarıyla seçilebilen modern menü çizer
        
        Args:
            options (list): (key, label) şeklinde menü seçenekleri listesi
            title (str): Menü başlığı
            box_width (int): Menü genişliği
            selected_lang (str): Seçili dil kodu
            
        Returns:
            str: Seçilen seçeneğin anahtarı
        """
        import inquirer
        from inquirer import themes
        from inquirer.render import ConsoleRender
        
        # Dil ayarını kontrol et, varsayılan İngilizce
        if selected_lang is None:
            selected_lang = config.get("settings", {}).get("language", "en")
        
        # Terminal genişliği hesapla
        term_width = os.get_terminal_size().columns
        box_width = min(box_width, term_width)
        
        # Özel bir renk teması oluştur
        class CyberTheme(themes.Default):
            def __init__(self):
                super(CyberTheme, self).__init__()
                self.Question.mark_color = Fore.CYAN
                self.Question.brackets_color = Fore.CYAN
                self.Question.default_color = Fore.CYAN
                self.List.selection_color = Fore.GREEN
                self.List.selection_cursor = "▶"
                self.List.unselected_color = Fore.WHITE
        
        # Menünün üst tarafını çiz
        clear()
        
        # Başlık çiz
        if title:
            title_box = MenuTheme.draw_box(box_width, title)
            for line in title_box:
                print(line)
        
        # Menü açıklaması
        desc_text = translate("arrow_usage", selected_lang) if selected_lang else "Use arrow keys to select and ENTER to confirm"
        print(f"\n{MenuTheme.INFO}ℹ️  {desc_text}{Style.RESET_ALL}\n")
        
        # Seçenekleri oluştur
        choices = []
        for option_key, option_text in options:
            if option_key == "back" or option_key == "exit":
                # Geri ve çıkış seçenekleri için özel renk
                option_text = f"{Fore.RED}{option_text}{Style.RESET_ALL}"
            choices.append(option_text)
        
        # inquirer ile ok tuşlu menü oluştur
        questions = [
            inquirer.List(
                'choice',
                message=translate("select_option", selected_lang),
                choices=choices,
            ),
        ]
        
        # inquirer'ı CyberTheme ile başlat
        answers = inquirer.prompt(questions, theme=CyberTheme(), render=ConsoleRender())
        
        if answers:
            selected_text = answers['choice']
            # Seçilen metni temizle ve anahtarı bul
            clean_selected = selected_text.replace(Fore.RED, "").replace(Style.RESET_ALL, "")
            
            for option_key, option_text in options:
                clean_option = option_text.replace(Fore.RED, "").replace(Style.RESET_ALL, "")
                if clean_option == clean_selected:
                    # Seçilen öğe efekti
                    print(f"\n{MenuTheme.SUCCESS}✓ {translate('selected', selected_lang)}: ", end="")
                    MenuTheme.animate_text(clean_option, [Fore.CYAN, Fore.GREEN, Fore.BLUE])
                    time.sleep(0.3)  # Kısa gecikme
                    return option_key
            
            return options[0][0]  # Varsayılan değer
        else:
            return options[0][0]  # İptal edilirse varsayılan değer 