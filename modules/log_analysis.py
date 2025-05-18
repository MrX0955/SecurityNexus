import os
import time
import datetime
import re
import inquirer
import pandas as pd
from colorama import Fore
from core.config import translate, config
from utils.helpers import clear

class LogAnalysisOperations:
    @staticmethod
    def log_collector():
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('log_collector', selected_lang)}{Fore.RESET}\n")
        
        collector_questions = [
            inquirer.List(
                'source',
                message=f'{Fore.YELLOW}{translate("select_log_source", selected_lang)}:{Fore.RESET}',
                choices=[
                    (translate("system_logs", selected_lang), "system"),
                    (translate("app_logs", selected_lang), "application"),
                    (translate("web_server_logs", selected_lang), "webserver"),
                    (translate("security_logs", selected_lang), "security"),
                    (translate("from_local_file", selected_lang), "file"),
                    (f"↩️ {translate('back', selected_lang)}", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(collector_questions)
        if result is None or result['source'] == 'back':
            return
        
        source = result['source']
        
        if source == 'file':
            log_file = input(f"{Fore.MAGENTA}{translate('enter_log_file_path', selected_lang)}: {Fore.RESET}")
            if not os.path.exists(log_file):
                print(f"{Fore.RED}{translate('error_file_not_found', selected_lang)}!{Fore.RESET}")
                time.sleep(1.5)
                return
            
            print(f"\n{Fore.YELLOW}{translate('collecting_logs_from_file', selected_lang)}...{Fore.RESET}")
        else:
            print(f"\n{Fore.YELLOW}{translate('collecting_logs', selected_lang)} ({source})...{Fore.RESET}")
        
        # Simülasyonlu log toplama
        time.sleep(2)
        
        print(f"\n{Fore.GREEN}{translate('logs_collected_successfully', selected_lang)}.{Fore.RESET}")
        print(f"{Fore.WHITE}{translate('total', selected_lang)}: 1,245 {translate('log_records', selected_lang)}{Fore.RESET}")
        print(f"{Fore.WHITE}{translate('saved_file', selected_lang)}: logs/{source}_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def log_parser():
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('log_parser', selected_lang)}{Fore.RESET}\n")
        
        parser_questions = [
            inquirer.List(
                'format',
                message=f'{Fore.YELLOW}{translate("select_log_format", selected_lang)}:{Fore.RESET}',
                choices=[
                    ("Apache Access Logs", "apache"),
                    ("Nginx Logs", "nginx"),
                    ("Windows Event Logs", "windows"),
                    ("Syslog", "syslog"),
                    (translate("json_format", selected_lang), "json"),
                    (translate("auto_detect", selected_lang), "auto"),
                    (f"↩️ {translate('back', selected_lang)}", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(parser_questions)
        if result is None or result['format'] == 'back':
            return
            
        format_type = result['format']
        
        log_file = input(f"{Fore.MAGENTA}{translate('enter_log_file_path_or_empty', selected_lang)}: {Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('parsing_logs', selected_lang)} ({format_type})...{Fore.RESET}")
        time.sleep(2)
        
        print(f"\n{Fore.GREEN}{translate('logs_parsed_successfully', selected_lang)}.{Fore.RESET}")
        print(f"{Fore.WHITE}{translate('parsed_fields', selected_lang)}:{Fore.RESET}")
        
        if format_type == "apache" or format_type == "nginx" or format_type == "auto":
            print(f"  {Fore.YELLOW}• {translate('ip_address', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• {translate('timestamp', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• {translate('http_method', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• URI{Fore.RESET}")
            print(f"  {Fore.YELLOW}• {translate('status_code', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• {translate('byte_count', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• Referrer{Fore.RESET}")
            print(f"  {Fore.YELLOW}• User-Agent{Fore.RESET}")
        elif format_type == "windows":
            print(f"  {Fore.YELLOW}• {translate('timestamp', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• {translate('event_id', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• {translate('source', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• {translate('level', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.YELLOW}• {translate('message', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('output_file', selected_lang)}: parsed_logs/{format_type}_parsed_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def correlation_engine():
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('correlation_engine', selected_lang)}{Fore.RESET}\n")
        
        print(f"{Fore.YELLOW}{translate('select_log_sources_multiple', selected_lang)}:{Fore.RESET}")
        sources_questions = [
            inquirer.Checkbox(
                'sources',
                message=f'{Fore.YELLOW}{translate("sources", selected_lang)}:{Fore.RESET}',
                choices=[
                    (translate("firewall_logs", selected_lang), "firewall"),
                    (translate("ids_ips_logs", selected_lang), "ids"),
                    (translate("auth_logs", selected_lang), "auth"),
                    (translate("web_server_logs", selected_lang), "web"),
                    (translate("database_logs", selected_lang), "database"),
                ],
                default=["firewall", "ids"]
            )
        ]
        
        sources_result = inquirer.prompt(sources_questions)
        if sources_result is None or not sources_result['sources']:
            return
            
        sources = sources_result['sources']
        
        rules_questions = [
            inquirer.Checkbox(
                'rules',
                message=f'{Fore.YELLOW}{translate("select_correlation_rules", selected_lang)}:{Fore.RESET}',
                choices=[
                    (translate("brute_force_detection", selected_lang), "brute_force"),
                    (translate("lateral_movement", selected_lang), "lateral_movement"),
                    (translate("data_exfiltration", selected_lang), "data_exfiltration"),
                    (translate("malware_activity", selected_lang), "malware"),
                    (translate("suspicious_login", selected_lang), "suspicious_login"),
                ],
                default=["brute_force", "malware"]
            )
        ]
        
        rules_result = inquirer.prompt(rules_questions)
        if rules_result is None or not rules_result['rules']:
            return
            
        rules = rules_result['rules']
        
        print(f"\n{Fore.YELLOW}{translate('running_correlation_analysis', selected_lang)}...")
        print(f"{Fore.WHITE}{translate('sources', selected_lang)}: {', '.join(sources)}{Fore.RESET}")
        print(f"{Fore.WHITE}{translate('rules', selected_lang)}: {', '.join(rules)}{Fore.RESET}")
        
        # Korelasyon analizi simülasyonu
        for i in range(5):
            print(f"{Fore.WHITE}{translate('analysis_step', selected_lang)} {i+1}/5...{Fore.RESET}")
            time.sleep(0.8)
        
        print(f"\n{Fore.GREEN}{translate('correlation_analysis_completed', selected_lang)}.{Fore.RESET}")
        print(f"\n{Fore.RED}{translate('detected_events', selected_lang)}:{Fore.RESET}")
        
        if "brute_force" in rules:
            print(f"  {Fore.WHITE}• [{translate('high', selected_lang)}] {translate('brute_force_attack_detected', selected_lang)} - 10.2.3.4 IP {translate('address_login_attempts', selected_lang)}{Fore.RESET}")
        
        if "malware" in rules:
            print(f"  {Fore.WHITE}• [{translate('high', selected_lang)}] {translate('trojan_activity_detected', selected_lang)} - workstation3 {translate('suspicious_connections', selected_lang)}{Fore.RESET}")
        
        if "lateral_movement" in rules and "suspicious_login" in rules:
            print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('lateral_movement_suspected', selected_lang)} - 192.168.1.55 {translate('to', selected_lang)} 192.168.2.30 {translate('unusual_access', selected_lang)}{Fore.RESET}")
        
        if "data_exfiltration" in rules:
            print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('potential_data_exfiltration', selected_lang)} - 172.16.5.12 {translate('high_dns_traffic', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('report', selected_lang)}: reports/correlation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def event_visualization():
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('event_visualization', selected_lang)}{Fore.RESET}\n")
        
        viz_questions = [
            inquirer.List(
                'type',
                message=f'{Fore.YELLOW}{translate("select_visualization_type", selected_lang)}:{Fore.RESET}',
                choices=[
                    (translate("timeline", selected_lang), "timeline"),
                    (translate("network_graph", selected_lang), "network_graph"),
                    (translate("heatmap", selected_lang), "heatmap"),
                    (translate("statistics_graphs", selected_lang), "statistics"),
                    (f"↩️ {translate('back', selected_lang)}", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(viz_questions)
        if result is None or result['type'] == 'back':
            return
            
        viz_type = result['type']
        
        print(f"\n{Fore.YELLOW}{translate('analyzing_event_data', selected_lang)}...{Fore.RESET}")
        time.sleep(1.5)
        
        print(f"\n{Fore.GREEN}{translate('visualization_prepared', selected_lang)}: {viz_type}{Fore.RESET}")
        
        if viz_type == "timeline":
            print(f"\n{Fore.CYAN}{translate('timeline_events', selected_lang)}:{Fore.RESET}")
            print(f"  {Fore.WHITE}• 08:45:22 - {translate('auth_error', selected_lang)} ({translate('user', selected_lang)}: admin){Fore.RESET}")
            print(f"  {Fore.WHITE}• 08:46:15 - {translate('multiple_failed_logins', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• 08:52:08 - {translate('successful_login', selected_lang)} ({translate('user', selected_lang)}: admin){Fore.RESET}")
            print(f"  {Fore.WHITE}• 09:03:45 - {translate('privilege_escalation', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• 09:10:32 - {translate('suspicious_file_access', selected_lang)}{Fore.RESET}")
        elif viz_type == "network_graph":
            print(f"\n{Fore.CYAN}{translate('network_graph_summary', selected_lang)}:{Fore.RESET}")
            print(f"  {Fore.WHITE}• 25 {translate('nodes', selected_lang)}, 43 {translate('connections', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• 3 {translate('suspicious_nodes_detected', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• {translate('heaviest_traffic', selected_lang)}: 192.168.1.5 -> 192.168.1.1{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('visualization_saved', selected_lang)}: reports/viz_{viz_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def log_analyzer():
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('log_analyzer', selected_lang)}{Fore.RESET}\n")
        
        analysis_questions = [
            inquirer.List(
                'type',
                message=f'{Fore.YELLOW}{translate("select_analysis_type", selected_lang)}:{Fore.RESET}',
                choices=[
                    (translate("anomaly_detection", selected_lang), "anomaly"),
                    (translate("attack_pattern_analysis", selected_lang), "attack_pattern"),
                    (translate("security_events", selected_lang), "security_events"),
                    (translate("performance_analysis", selected_lang), "performance"),
                    (translate("usage_statistics", selected_lang), "usage"),
                    (f"↩️ {translate('back', selected_lang)}", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(analysis_questions)
        if result is None or result['type'] == 'back':
            return
            
        analysis_type = result['type']
        
        log_file = input(f"{Fore.MAGENTA}{translate('enter_log_file_path_or_empty', selected_lang)}: {Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('analyzing_logs', selected_lang)} ({analysis_type})...{Fore.RESET}")
        time.sleep(2)
        
        print(f"\n{Fore.GREEN}{translate('log_analysis_completed', selected_lang)}.{Fore.RESET}")
        
        if analysis_type == "anomaly":
            print(f"\n{Fore.CYAN}{translate('detected_anomalies', selected_lang)}:{Fore.RESET}")
            print(f"  {Fore.WHITE}• {translate('unusual_access_times', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• {translate('multiple_failed_login_attempts', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• {translate('abnormal_url_requests', selected_lang)}{Fore.RESET}")
        elif analysis_type == "attack_pattern":
            print(f"\n{Fore.CYAN}{translate('detected_attack_patterns', selected_lang)}:{Fore.RESET}")
            print(f"  {Fore.WHITE}• {translate('sql_injection_attempts', selected_lang)} (12 {translate('events', selected_lang)}){Fore.RESET}")
            print(f"  {Fore.WHITE}• {translate('xss_attack_attempts', selected_lang)} (8 {translate('events', selected_lang)}){Fore.RESET}")
            print(f"  {Fore.WHITE}• {translate('directory_traversal_attempts', selected_lang)} (5 {translate('events', selected_lang)}){Fore.RESET}")
        elif analysis_type == "security_events":
            print(f"\n{Fore.CYAN}{translate('important_security_events', selected_lang)}:{Fore.RESET}")
            print(f"  {Fore.WHITE}• 3 {translate('successful_admin_logins', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• 1 {translate('account_lockout_event', selected_lang)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• 5 {translate('permission_change_events', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('analysis_report', selected_lang)}: reports/log_analysis_{analysis_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")

class LogParser:
    @staticmethod
    def parse_apache_log(log_line):
        """
        Apache/Nginx access log format parser
        Example format: 127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
        """
        pattern = r'(\S+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+)'
        match = re.match(pattern, log_line)
        
        if match:
            ip, identity, user, timestamp, request, status, size = match.groups()
            
            # Parse HTTP method, URI and protocol
            request_parts = request.split()
            method = request_parts[0] if len(request_parts) > 0 else ""
            uri = request_parts[1] if len(request_parts) > 1 else ""
            protocol = request_parts[2] if len(request_parts) > 2 else ""
            
            return {
                'ip': ip,
                'timestamp': timestamp,
                'method': method,
                'uri': uri,
                'protocol': protocol,
                'status': status,
                'size': size
            }
        return None
    
    @staticmethod
    def parse_windows_event(log_line):
        """
        Windows Event Log format parser (simplified)
        """
        # Windows Event Log parsing implementation
        # May require parsing XML formatted event records
        return None 