import os
import time
import datetime
import inquirer
from colorama import Fore
from core.config import translate, config, VERSION
from utils.helpers import clear

class AdditionalOperations:
    @staticmethod
    def performance_test():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('performance_test', selected_lang)}{Fore.RESET}\n")
        
        print(f"{Fore.YELLOW}{translate('performance_testing', selected_lang)}...{Fore.RESET}")

        print(f"\n{Fore.CYAN}{translate('cpu_test', selected_lang)}:{Fore.RESET}")
        print(f"  {translate('computation_test_running', selected_lang)}...")
        
        start_time = time.time()
        result = 0
        for i in range(10000000):
            result += i
        end_time = time.time()
        
        cpu_time = end_time - start_time
        print(f"  {Fore.GREEN}{translate('cpu_score', selected_lang)}: {Fore.RESET}{10 / cpu_time:.2f}")

        print(f"\n{Fore.CYAN}{translate('memory_test', selected_lang)}:{Fore.RESET}")
        print(f"  {translate('memory_allocation_test_running', selected_lang)}...")
        
        start_time = time.time()
        test_data = []
        for i in range(100000):
            test_data.append("x" * 1000)
        test_data = None
        end_time = time.time()
        
        memory_time = end_time - start_time
        print(f"  {Fore.GREEN}{translate('memory_score', selected_lang)}: {Fore.RESET}{5 / memory_time:.2f}")

        print(f"\n{Fore.CYAN}{translate('network_test', selected_lang)}:{Fore.RESET}")
        print(f"  {translate('connection_test_running', selected_lang)}...")
        
        start_time = time.time()

        import socket
        for i in range(5):
            try:
                socket.create_connection(("www.google.com", 80), timeout=1)
            except:
                pass
        end_time = time.time()
        
        network_time = end_time - start_time
        print(f"  {Fore.GREEN}{translate('network_score', selected_lang)}: {Fore.RESET}{1 / network_time:.2f}")

        overall_score = (10 / cpu_time) * 0.6 + (5 / memory_time) * 0.3 + (1 / network_time) * 0.1
        print(f"\n{Fore.CYAN}{translate('overall_performance_score', selected_lang)}: {Fore.MAGENTA}{overall_score:.2f}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        clear()

    @staticmethod
    def encryption_tools():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('encryption_tools', selected_lang)}{Fore.RESET}\n")
        
        encryption_options = [
            inquirer.List(
                'option',
                message=f'{Fore.CYAN}{translate("make_selection", selected_lang)}:{Fore.RESET}',
                choices=[
                    ('1. ' + translate("hash_generator", selected_lang), 'hash_generator'),
                    ('2. ' + translate("text_encryptor", selected_lang), 'text_encryptor'),
                    ('3. ' + translate("text_decryptor", selected_lang), 'text_decryptor'),
                    ('↩️ ' + translate("back", selected_lang), 'back')
                ]
            )
        ]
        
        result = inquirer.prompt(encryption_options)
        
        if result is None or result['option'] == 'back':
            return
        
        option = result['option']
        
        if option == 'hash_generator':
            AdditionalOperations._hash_generator()
        elif option == 'text_encryptor':
            AdditionalOperations._text_encryptor()
        elif option == 'text_decryptor':
            AdditionalOperations._text_decryptor()
    
    @staticmethod
    def _hash_generator():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('hash_generator', selected_lang)}{Fore.RESET}\n")
        
        text = input(f"{Fore.MAGENTA}{translate('enter_text', selected_lang)}: {Fore.RESET}")
        
        if text:
            import hashlib
            
            md5 = hashlib.md5(text.encode()).hexdigest()
            sha1 = hashlib.sha1(text.encode()).hexdigest()
            sha256 = hashlib.sha256(text.encode()).hexdigest()
            sha512 = hashlib.sha512(text.encode()).hexdigest()
            
            print(f"\n{Fore.GREEN}{translate('hash_values', selected_lang)}:{Fore.RESET}")
            print(f"  {Fore.YELLOW}{translate('hash_md5', selected_lang)}:{Fore.RESET} {md5}")
            print(f"  {Fore.YELLOW}{translate('hash_sha1', selected_lang)}:{Fore.RESET} {sha1}")
            print(f"  {Fore.YELLOW}{translate('hash_sha256', selected_lang)}:{Fore.RESET} {sha256}")
            print(f"  {Fore.YELLOW}{translate('hash_sha512', selected_lang)}:{Fore.RESET} {sha512}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.encryption_tools()
    
    @staticmethod
    def _text_encryptor():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('text_encryptor', selected_lang)}{Fore.RESET}\n")
        
        text = input(f"{Fore.MAGENTA}{translate('enter_text', selected_lang)}: {Fore.RESET}")
        password = input(f"{Fore.MAGENTA}{translate('enter_password', selected_lang)}: {Fore.RESET}")
        
        if text and password:
            try:
                from cryptography.fernet import Fernet
                from cryptography.hazmat.primitives import hashes
                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
                import base64

                salt = b'SecurityNexus'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

                f = Fernet(key)
                encrypted_text = f.encrypt(text.encode()).decode()
                
                print(f"\n{Fore.GREEN}{translate('encrypted_text', selected_lang)}:{Fore.RESET}")
                print(f"{encrypted_text}")
                
                print(f"\n{Fore.YELLOW}{translate('save_encryption_key', selected_lang)}.{Fore.RESET}")
            except Exception as e:
                print(f"{Fore.RED}{translate('encryption_error', selected_lang)}: {e}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.encryption_tools()
    
    @staticmethod
    def _text_decryptor():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('text_decryptor', selected_lang)}{Fore.RESET}\n")
        
        encrypted_text = input(f"{Fore.MAGENTA}{translate('enter_encrypted_text', selected_lang)}: {Fore.RESET}")
        password = input(f"{Fore.MAGENTA}{translate('enter_password', selected_lang)}: {Fore.RESET}")
        
        if encrypted_text and password:
            try:
                from cryptography.fernet import Fernet, InvalidToken
                from cryptography.hazmat.primitives import hashes
                from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
                import base64

                salt = b'SecurityNexus'
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

                f = Fernet(key)
                try:
                    decrypted_text = f.decrypt(encrypted_text.encode()).decode()
                    print(f"\n{Fore.GREEN}{translate('decrypted_text', selected_lang)}:{Fore.RESET}")
                    print(f"{decrypted_text}")
                except InvalidToken:
                    print(f"\n{Fore.RED}{translate('decryption_error_invalid', selected_lang)}.{Fore.RESET}")
            except Exception as e:
                print(f"{Fore.RED}{translate('decryption_error', selected_lang)}: {e}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.encryption_tools()

    @staticmethod
    def random_generator():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('random_generator', selected_lang)}{Fore.RESET}\n")
        
        random_options = [
            inquirer.List(
                'option',
                message=f'{Fore.CYAN}{translate("make_selection", selected_lang)}:{Fore.RESET}',
                choices=[
                    ('1. ' + translate("password_generator", selected_lang), 'password_generator'),
                    ('2. ' + translate("uuid_generator", selected_lang), 'uuid_generator'),
                    ('3. ' + translate("random_number", selected_lang), 'random_number'),
                    ('↩️ ' + translate("back", selected_lang), 'back')
                ]
            )
        ]
        
        result = inquirer.prompt(random_options)
        
        if result is None or result['option'] == 'back':
            return
        
        option = result['option']
        
        if option == 'password_generator':
            AdditionalOperations._password_generator()
        elif option == 'uuid_generator':
            AdditionalOperations._uuid_generator()
        elif option == 'random_number':
            AdditionalOperations._random_number()
    
    @staticmethod
    def _password_generator():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('password_generator', selected_lang)}{Fore.RESET}\n")
        
        try:
            length = int(input(f"{Fore.MAGENTA}{translate('enter_password_length', selected_lang)} (8-64): {Fore.RESET}"))
            
            if length < 8 or length > 64:
                print(f"{Fore.RED}{translate('invalid_length', selected_lang)}.{Fore.RESET}")
            else:
                import random
                import string

                lowercase = string.ascii_lowercase
                uppercase = string.ascii_uppercase
                digits = string.digits
                special = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"

                use_lowercase = input(f"{Fore.MAGENTA}{translate('include_lowercase', selected_lang)}: {Fore.RESET}").upper() != "H"
                use_uppercase = input(f"{Fore.MAGENTA}{translate('include_uppercase', selected_lang)}: {Fore.RESET}").upper() != "H"
                use_digits = input(f"{Fore.MAGENTA}{translate('include_digits', selected_lang)}: {Fore.RESET}").upper() != "H"
                use_special = input(f"{Fore.MAGENTA}{translate('include_special', selected_lang)}: {Fore.RESET}").upper() != "H"

                char_pool = ""
                if use_lowercase:
                    char_pool += lowercase
                if use_uppercase:
                    char_pool += uppercase
                if use_digits:
                    char_pool += digits
                if use_special:
                    char_pool += special
                
                if not char_pool:
                    print(f"{Fore.RED}{translate('select_one_charset', selected_lang)}.{Fore.RESET}")
                else:

                    password = ''.join(random.choice(char_pool) for _ in range(length))
                    
                    print(f"\n{Fore.GREEN}{translate('generated_password', selected_lang)}:{Fore.RESET}")
                    print(f"{Fore.CYAN}{password}{Fore.RESET}")

                    strength = 0
                    if use_lowercase:
                        strength += 1
                    if use_uppercase:
                        strength += 1
                    if use_digits:
                        strength += 1
                    if use_special:
                        strength += 1
                    
                    strength = strength * (min(length, 32) / 8)
                    
                    strength_text = ""
                    if strength < 2:
                        strength_text = f"{Fore.RED}{translate('strength_weak', selected_lang)}{Fore.RESET}"
                    elif strength < 4:
                        strength_text = f"{Fore.YELLOW}{translate('strength_medium', selected_lang)}{Fore.RESET}"
                    elif strength < 6:
                        strength_text = f"{Fore.GREEN}{translate('strength_strong', selected_lang)}{Fore.RESET}"
                    else:
                        strength_text = f"{Fore.MAGENTA}{translate('strength_very_strong', selected_lang)}{Fore.RESET}"
                    
                    print(f"\n{Fore.YELLOW}{translate('password_strength', selected_lang)}: {strength_text}")
        except ValueError:
            print(f"{Fore.RED}{translate('invalid_input_numeric', selected_lang)}.{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.random_generator()
    
    @staticmethod
    def _uuid_generator():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('uuid_generator', selected_lang)}{Fore.RESET}\n")
        
        import uuid
        
        uuid_options = [
            inquirer.List(
                'option',
                message=f'{Fore.CYAN}{translate("select_uuid_version", selected_lang)}:{Fore.RESET}',
                choices=[
                    ('UUID v1 (zaman tabanlı)', 1),
                    ('UUID v4 (rastgele)', 4),
                    (translate("back", selected_lang), 'back')
                ]
            )
        ]
        
        result = inquirer.prompt(uuid_options)
        
        if result is None or result['option'] == 'back':
            AdditionalOperations.random_generator()
            return
        
        version = result['option']
        
        try:
            count = int(input(f"{Fore.MAGENTA}{translate('enter_uuid_count', selected_lang)} (1-10): {Fore.RESET}"))
            
            if count < 1 or count > 10:
                print(f"{Fore.RED}{translate('invalid_count_range_uuid', selected_lang)}.{Fore.RESET}")
            else:
                print(f"\n{Fore.GREEN}{translate('generated_uuids', selected_lang)}:{Fore.RESET}")
                
                for i in range(count):
                    if version == 1:
                        generated_uuid = uuid.uuid1()
                    else:
                        generated_uuid = uuid.uuid4()
                    
                    print(f"  {i+1}. {Fore.CYAN}{generated_uuid}{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}{translate('invalid_input_numeric', selected_lang)}.{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.random_generator()
    
    @staticmethod
    def _random_number():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('random_number', selected_lang)}{Fore.RESET}\n")
        
        try:
            min_val = int(input(f"{Fore.MAGENTA}{translate('minimum_value', selected_lang)}: {Fore.RESET}"))
            max_val = int(input(f"{Fore.MAGENTA}{translate('maximum_value', selected_lang)}: {Fore.RESET}"))
            
            if min_val >= max_val:
                print(f"{Fore.RED}{translate('min_smaller_max', selected_lang)}.{Fore.RESET}")
            else:
                import random
                
                count = int(input(f"{Fore.MAGENTA}{translate('random_count', selected_lang)}: {Fore.RESET}"))
                
                if count < 1 or count > 20:
                    print(f"{Fore.RED}{translate('invalid_count_range_random', selected_lang)}.{Fore.RESET}")
                else:
                    print(f"\n{Fore.GREEN}{translate('generated_random_numbers', selected_lang)} ({min_val} - {max_val}):{Fore.RESET}")
                    
                    for i in range(count):
                        random_num = random.randint(min_val, max_val)
                        print(f"  {i+1}. {Fore.CYAN}{random_num}{Fore.RESET}")
        except ValueError:
            print(f"{Fore.RED}{translate('invalid_input_numeric', selected_lang)}.{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.random_generator()

    @staticmethod
    def converter_tools():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('converter_tools', selected_lang)}{Fore.RESET}\n")
        
        converter_options = [
            inquirer.List(
                'option',
                message=f'{Fore.CYAN}{translate("make_selection", selected_lang)}:{Fore.RESET}',
                choices=[
                    ('1. ' + translate('base64_encoder', selected_lang), 'base64_encoder'),
                    ('2. ' + translate('base64_decoder', selected_lang), 'base64_decoder'),
                    ('3. ' + translate('url_encoder', selected_lang), 'url_encoder'),
                    ('4. ' + translate('url_decoder', selected_lang), 'url_decoder'),
                    ('5. ' + translate('hex_converter', selected_lang), 'hex_converter'),
                    ('↩️ ' + translate('back', selected_lang), 'back')
                ]
            )
        ]
        
        result = inquirer.prompt(converter_options)
        
        if result is None or result['option'] == 'back':
            return
        
        option = result['option']
        
        if option == 'base64_encoder':
            AdditionalOperations._base64_encoder()
        elif option == 'base64_decoder':
            AdditionalOperations._base64_decoder()
        elif option == 'url_encoder':
            AdditionalOperations._url_encoder()
        elif option == 'url_decoder':
            AdditionalOperations._url_decoder()
        elif option == 'hex_converter':
            AdditionalOperations._hex_converter()
    
    @staticmethod
    def _base64_encoder():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('base64_encoder', selected_lang)}{Fore.RESET}\n")
        
        text = input(f"{Fore.MAGENTA}{translate('enter_text', selected_lang)}: {Fore.RESET}")
        
        if text:
            import base64
            
            encoded = base64.b64encode(text.encode()).decode()
            
            print(f"\n{Fore.GREEN}{translate('base64_encoded_text', selected_lang)}:{Fore.RESET}")
            print(f"{Fore.CYAN}{encoded}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.converter_tools()
    
    @staticmethod
    def _base64_decoder():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('base64_decoder', selected_lang)}{Fore.RESET}\n")
        
        encoded_text = input(f"{Fore.MAGENTA}{translate('enter_encoded_text', selected_lang)}: {Fore.RESET}")
        
        if encoded_text:
            import base64
            
            try:
                decoded = base64.b64decode(encoded_text).decode()
                
                print(f"\n{Fore.GREEN}{translate('base64_decoded_text', selected_lang)}:{Fore.RESET}")
                print(f"{Fore.CYAN}{decoded}{Fore.RESET}")
            except Exception as e:
                print(f"{Fore.RED}{translate('decoding_error', selected_lang)}: {e}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.converter_tools()
    
    @staticmethod
    def _url_encoder():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('url_encoder', selected_lang)}{Fore.RESET}\n")
        
        text = input(f"{Fore.MAGENTA}{translate('enter_text', selected_lang)}: {Fore.RESET}")
        
        if text:
            import urllib.parse
            
            encoded = urllib.parse.quote_plus(text)
            
            print(f"\n{Fore.GREEN}{translate('url_encoded_text', selected_lang)}:{Fore.RESET}")
            print(f"{Fore.CYAN}{encoded}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.converter_tools()
    
    @staticmethod
    def _url_decoder():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('url_decoder', selected_lang)}{Fore.RESET}\n")
        
        encoded_text = input(f"{Fore.MAGENTA}{translate('enter_encoded_text', selected_lang)}: {Fore.RESET}")
        
        if encoded_text:
            import urllib.parse
            
            try:
                decoded = urllib.parse.unquote_plus(encoded_text)
                
                print(f"\n{Fore.GREEN}{translate('url_decoded_text', selected_lang)}:{Fore.RESET}")
                print(f"{Fore.CYAN}{decoded}{Fore.RESET}")
            except Exception as e:
                print(f"{Fore.RED}{translate('decoding_error', selected_lang)}: {e}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations.converter_tools()
    
    @staticmethod
    def _hex_converter():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('hex_converter', selected_lang)}{Fore.RESET}\n")
        
        converter_options = [
            inquirer.List(
                'option',
                message=f'{Fore.CYAN}{translate("select_conversion", selected_lang)}:{Fore.RESET}',
                choices=[
                    ('1. ' + translate('text_to_hex', selected_lang), 'text_to_hex'),
                    ('2. ' + translate('hex_to_text', selected_lang), 'hex_to_text'),
                    ('3. ' + translate('decimal_to_hex', selected_lang), 'decimal_to_hex'),
                    ('4. ' + translate('hex_to_decimal', selected_lang), 'hex_to_decimal'),
                    ('↩️ ' + translate('back', selected_lang), 'back')
                ]
            )
        ]
        
        result = inquirer.prompt(converter_options)
        
        if result is None or result['option'] == 'back':
            AdditionalOperations.converter_tools()
            return
        
        option = result['option']
        
        if option == 'text_to_hex':
            text = input(f"{Fore.MAGENTA}{translate('enter_text', selected_lang)}: {Fore.RESET}")
            if text:
                try:
                    hex_result = text.encode('utf-8').hex()
                    print(f"\n{Fore.GREEN}{translate('hex_value', selected_lang)}:{Fore.RESET}")
                    print(f"{Fore.CYAN}{hex_result}{Fore.RESET}")
                except Exception as e:
                    print(f"{Fore.RED}{translate('conversion_error', selected_lang)}: {e}{Fore.RESET}")
        
        elif option == 'hex_to_text':
            hex_text = input(f"{Fore.MAGENTA}{translate('enter_hex', selected_lang)}: {Fore.RESET}")
            if hex_text:
                try:
                    hex_text = hex_text.replace(" ", "")
                    if hex_text.startswith("0x"):
                        hex_text = hex_text[2:]
                    
                    text_result = bytes.fromhex(hex_text).decode('utf-8')
                    print(f"\n{Fore.GREEN}{translate('text', selected_lang)}:{Fore.RESET}")
                    print(f"{Fore.CYAN}{text_result}{Fore.RESET}")
                except Exception as e:
                    print(f"{Fore.RED}{translate('conversion_error', selected_lang)}: {e}{Fore.RESET}")
        
        elif option == 'decimal_to_hex':
            try:
                decimal = int(input(f"{Fore.MAGENTA}{translate('enter_decimal_number', selected_lang)}: {Fore.RESET}"))
                hex_result = hex(decimal)
                print(f"\n{Fore.GREEN}{translate('hex_value', selected_lang)}:{Fore.RESET}")
                print(f"{Fore.CYAN}{hex_result}{Fore.RESET}")
            except ValueError:
                print(f"{Fore.RED}{translate('invalid_number', selected_lang)}.{Fore.RESET}")
        
        elif option == 'hex_to_decimal':
            hex_text = input(f"{Fore.MAGENTA}{translate('enter_hex', selected_lang)} ({translate('optional_prefix', selected_lang)} 0x): {Fore.RESET}")
            if hex_text:
                try:
                    decimal_result = int(hex_text, 16)
                    print(f"\n{Fore.GREEN}{translate('decimal_value', selected_lang)}:{Fore.RESET}")
                    print(f"{Fore.CYAN}{decimal_result}{Fore.RESET}")
                except ValueError:
                    print(f"{Fore.RED}{translate('invalid_hex', selected_lang)}.{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        AdditionalOperations._hex_converter()