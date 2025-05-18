import os
import requests
import datetime
import json
import time
from functools import lru_cache
from colorama import Fore
from string import Template
from core.config import config, translate, VERSION, save_to_history

# Global HTTP oturumu
_session = None

def get_session():
    global _session
    if _session is None:
        _session = requests.Session()
        # Varsayılan kullanıcı ajanı
        _session.headers.update({"User-Agent": "SecurityNexus"})
    return _session

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_validated_input(prompt, validation_func):
    while True:
        user_input = input(f"{translate(prompt)}: ").strip()
        if validation_func(user_input):
            return user_input
        else:
            print(f"{Fore.RED}{translate('invalid_input')}{Fore.RESET}")

@lru_cache(maxsize=64)
def make_request(url, params=None, data=None, headers=None, method="GET", timeout=10):
    try:
        print(f"{Fore.LIGHTYELLOW_EX}\n > {translate('waiting_results')}{Fore.LIGHTGREEN_EX}")
        
        print(f"{Fore.CYAN}[{translate('progress')}] {Fore.RESET}", end="", flush=True)
        for i in range(5):
            print("▓", end="", flush=True)
            time.sleep(0.1)
            
        # Giriş parametreleri ön-işleme
        request_headers = {"User-Agent": "SecurityNexus"}
        if headers:
            request_headers.update(headers)
            
        # Timeout değerini yapılandırma dosyasından al veya verilen değeri kullan
        timeout = config.get("settings", {}).get("default_timeout", timeout)
            
        # İstek yap
        session = get_session()
        if method == "GET":
            response = session.get(url, params=params, headers=request_headers, timeout=timeout)
        elif method == "POST":
            response = session.post(url, data=data, headers=request_headers, timeout=timeout)
                
        for i in range(5):
            print("▓", end="", flush=True)
            time.sleep(0.05)
        print(f" {Fore.GREEN}100%{Fore.RESET}")
            
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"{Fore.RED}{translate('error')}: {e}{Fore.RESET}")
        return None

def process_and_print_request(url, params=None, data=None, headers=None, method="GET"):
    # Dil ayarını al
    selected_lang = config.get("settings", {}).get("language", "en")
    
    response = make_request(url, params, data, headers, method)
    if response:
        result = response
        print(f"\n{result}\n| >> {translate('continue_prompt', selected_lang)}.")
        
        save_to_history("api_request", {
            "url": url,
            "method": method,
            "response": result
        })
        
        if config.get("settings", {}).get("save_reports", True):
            save_report("api_request", {
                "url": url,
                "method": method,
                "response": result,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    
    input()
    clear()

@lru_cache(maxsize=32)
def _load_report_template():
    template_path = os.path.join("templates", "report_template.html")
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as template_file:
            return template_file.read()
    return None

def save_report(report_type, data):
    # Dil ayarını al
    selected_lang = config.get("settings", {}).get("language", "en")
    
    try:
        reports_folder = config.get("settings", {}).get("reports_folder", "reports")
        report_format = config.get("settings", {}).get("report_format", "html")
        
        # Dizin yolu yoksa oluştur
        if not os.path.exists(reports_folder):
            try:
                os.makedirs(reports_folder, exist_ok=True)
                print(f"{Fore.GREEN}{translate('created_folder', selected_lang)}: {reports_folder}{Fore.RESET}")
            except Exception as mkdir_err:
                print(f"{Fore.RED}{translate('error_creating_folder', selected_lang)}: {mkdir_err}{Fore.RESET}")
                reports_folder = "reports"  # Fallback olarak varsayılan "reports" klasörünü kullan
                if not os.path.exists(reports_folder):
                    os.makedirs(reports_folder, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{reports_folder}/{report_type}_{timestamp}.{report_format}"
        
        # Dosyanın yazılacağı dizini kontrol et
        report_dir = os.path.dirname(filename)
        if not os.path.exists(report_dir):
            os.makedirs(report_dir, exist_ok=True)
        
        def clean_css_vars(value):
            if isinstance(value, str):
                if '--' in value:
                    value = value.replace('--', '\\-\\-')
                if value.strip().startswith('--'):
                    value = '\\' + value
            return value
            
        def deep_clean_dict(obj):
            if isinstance(obj, dict):
                return {k: deep_clean_dict(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [deep_clean_dict(i) for i in obj]
            elif isinstance(obj, str):
                return clean_css_vars(obj)
            else:
                return obj
        
        clean_data = deep_clean_dict(data)
        
        if report_format == "html":
            html_formatted_data = ""
            if "response" in clean_data:
                response_text = clean_data.get("response", "")
                if isinstance(response_text, str):
                    response_text = response_text.replace('<', '&lt;').replace('>', '&gt;')
                html_formatted_data = response_text
            else:
                try:
                    html_formatted_data = json.dumps(clean_data, indent=4, ensure_ascii=False, default=str)
                except Exception as json_err:
                    print(f"{Fore.YELLOW}{translate('json_conversion_error', selected_lang)}: {json_err}{Fore.RESET}")
                    html_formatted_data = str(clean_data)
            
            html_template = _load_report_template()
            if html_template:
                current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                current_year = datetime.datetime.now().year
                
                try:
                    report_data_json = json.dumps(clean_data, ensure_ascii=False, default=str)
                except Exception as e:
                    print(f"{Fore.YELLOW}{translate('js_data_preparation_error', selected_lang)}: {e}{Fore.RESET}")
                    report_data_json = "{}"
                
                try:
                    template_obj = Template(html_template)
                    html_content = template_obj.safe_substitute(
                        report_type=report_type,
                        timestamp=clean_data.get("timestamp", current_timestamp),
                        version=VERSION,
                        year=current_year,
                        html_formatted_data=html_formatted_data,
                        report_data_json=report_data_json
                    )
                except Exception as format_err:
                    print(f"{Fore.RED}{translate('html_template_format_error', selected_lang)}: {format_err}{Fore.RESET}")
                    html_content = f"""
                    <!DOCTYPE html>
                    <html lang="tr">
                    <head><title>SecurityNexus Report</title></head>
                    <body>
                        <h1>{report_type} {translate('report', selected_lang)}</h1>
                        <p>{translate('date', selected_lang)}: {current_timestamp}</p>
                        <pre>{html_formatted_data}</pre>
                    </body>
                    </html>
                    """
            else:
                html_content = f"""
                <!DOCTYPE html>
                <html lang="tr">
                <head>
                    <title>SecurityNexus Report - {report_type}</title>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        body {{ font-family: sans-serif; }}
                        pre {{ background: #f0f0f0; padding: 10px; }}
                    </style>
                </head>
                <body>
                    <h1>SecurityNexus Report - {report_type}</h1>
                    <p>{translate('date', selected_lang)}: {clean_data.get("timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}</p>
                    <h2>{translate('results', selected_lang)}</h2>
                    <pre>{html_formatted_data}</pre>
                </body>
                </html>
                """
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            except Exception as write_err:
                print(f"{Fore.RED}{translate('error', selected_lang)} {translate('file_writing_error', selected_lang)}: {write_err}{Fore.RESET}")
                alt_filename = f"{reports_folder}/emergency_{report_type}_{timestamp}.html"
                with open(alt_filename, 'w', encoding='utf-8') as f:
                    f.write("<html><body><h1>Acil Durum Raporu</h1><pre>" + str(clean_data) + "</pre></body></html>")
                filename = alt_filename
        
        elif report_format == "json":
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(clean_data, f, indent=4, default=str)
        
        elif report_format == "txt":
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"SecurityNexus Report - {report_type}\n")
                f.write(f"{translate('date', selected_lang)}: {clean_data.get('timestamp', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}\n\n")
                
                if "response" in clean_data:
                    f.write(f"{translate('results', selected_lang)}:\n{clean_data.get('response', '')}")
                else:
                    try:
                        f.write(f"{translate('results', selected_lang)}:\n{json.dumps(clean_data, indent=4, ensure_ascii=False, default=str)}")
                    except:
                        f.write(f"{translate('results', selected_lang)}:\n{str(clean_data)}")
        
        print(f"{Fore.GREEN}{translate('report_saved', selected_lang)}: {filename}{Fore.RESET}")
        return filename
    
    except Exception as e:
        print(f"{Fore.RED}{translate('error', selected_lang)}: {e}{Fore.RESET}")
        try:
            emergency_file = f"reports/emergency_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(emergency_file, 'w', encoding='utf-8') as f:
                f.write(f"EMERGENCY BACKUP\n\n{translate('error', selected_lang)}: {str(e)}\n\nData: {str(data)}")
            print(f"{Fore.YELLOW}{translate('emergency_backup_created', selected_lang)}: {emergency_file}{Fore.RESET}")
        except:
            pass
        return None