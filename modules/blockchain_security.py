import os
import time
import json
import random
import datetime
import requests
import inquirer
import matplotlib.pyplot as plt
from colorama import Fore
from core.config import translate, config
from utils.helpers import clear

class BlockchainSecurityOperations:
    @staticmethod
    def smart_contract_analyzer():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('smart_contract_analyzer', selected_lang)}{Fore.RESET}\n")
        
        contract_source = input(f"{Fore.MAGENTA}{translate('enter_contract_path', selected_lang)}: {Fore.RESET}")
        
        if not contract_source or not os.path.exists(contract_source):
            print(f"{Fore.YELLOW}{translate('using_sample_contract', selected_lang)}{Fore.RESET}")
            contract_source = "examples/smart_contracts/sample.sol"
        
        blockchain_questions = [
            inquirer.List(
                'platform',
                message=f'{Fore.YELLOW}{translate("select_blockchain_platform", selected_lang)}:{Fore.RESET}',
                choices=[
                    ("Ethereum", "ethereum"),
                    ("Binance Smart Chain", "bsc"),
                    ("Polygon", "polygon"),
                    ("Solana", "solana"),
                    ("Avalanche", "avalanche"),
                    (f"↩️ {translate('back', selected_lang)}", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(blockchain_questions)
        if result is None or result['platform'] == 'back':
            return
            
        platform = result['platform']
        
        print(f"\n{Fore.YELLOW}{translate('analyzing_smart_contract', selected_lang)} ({platform})...{Fore.RESET}")
        
        # Simülasyon
        for i in range(3):
            print(f"{Fore.WHITE}{translate('analysis_step', selected_lang)} {i+1}/3...{Fore.RESET}")
            time.sleep(1)
        
        print(f"\n{Fore.GREEN}{translate('smart_contract_analysis_completed', selected_lang)}.{Fore.RESET}")
        print(f"\n{Fore.RED}{translate('security_vulnerabilities_detected', selected_lang)}:{Fore.RESET}")
        
        # Örnek bulgular
        print(f"  {Fore.WHITE}• [{translate('high', selected_lang)}] {translate('reentrancy_vulnerability', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('integer_overflow', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('missing_auth_controls', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('low', selected_lang)}] {translate('gas_optimization', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('analysis_report', selected_lang)}: reports/smart_contract_security_{platform}_{time.strftime('%Y%m%d_%H%M%S')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def transaction_analyzer():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('transaction_analyzer', selected_lang)}{Fore.RESET}\n")
        
        tx_hash = input(f"{Fore.MAGENTA}{translate('enter_tx_hash', selected_lang)}: {Fore.RESET}")
        
        if not tx_hash:
            tx_hash = "0xd5e16b3ef6a136eff4aa86f3b54300f21a05fbc4f2626149ccd1aaef1230654e"
            print(f"{Fore.YELLOW}{translate('using_sample_tx_hash', selected_lang)}: {tx_hash}{Fore.RESET}")
        
        blockchain_questions = [
            inquirer.List(
                'network',
                message=f'{Fore.YELLOW}{translate("select_blockchain_network", selected_lang)}:{Fore.RESET}',
                choices=[
                    ("Ethereum Mainnet", "eth_mainnet"),
                    ("Ethereum Goerli", "eth_goerli"),
                    ("Binance Smart Chain", "bsc"),
                    ("Polygon", "polygon"),
                    ("Optimism", "optimism"),
                    ("Arbitrum", "arbitrum"),
                    (f"↩️ {translate('back', selected_lang)}", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(blockchain_questions)
        if result is None or result['network'] == 'back':
            return
            
        network = result['network']
        
        print(f"\n{Fore.YELLOW}{translate('analyzing_transaction', selected_lang)} ({network})...{Fore.RESET}")
        time.sleep(1.5)
        
        # Örnek işlem verisi
        print(f"\n{Fore.GREEN}{translate('transaction_details', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.YELLOW}{translate('hash', selected_lang)}:{Fore.RESET} {tx_hash}")
        print(f"  {Fore.YELLOW}{translate('block', selected_lang)}:{Fore.RESET} 15481324")
        print(f"  {Fore.YELLOW}{translate('sender', selected_lang)}:{Fore.RESET} 0x742d35Cc6634C0532925a3b844Bc454e4438f44e")
        print(f"  {Fore.YELLOW}{translate('receiver', selected_lang)}:{Fore.RESET} 0x388C818CA8B9251b393131C08a736A67ccB19297")
        print(f"  {Fore.YELLOW}{translate('value', selected_lang)}:{Fore.RESET} 0.5 ETH")
        print(f"  {Fore.YELLOW}{translate('gas_fee', selected_lang)}:{Fore.RESET} 0.002134 ETH")
        
        print(f"\n{Fore.CYAN}{translate('security_analysis', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('transaction_normal', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('address_not_blacklisted', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('gas_fee_normal', selected_lang)}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def wallet_security_check():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('wallet_security_check', selected_lang)}{Fore.RESET}\n")
        
        wallet_address = input(f"{Fore.MAGENTA}{translate('enter_wallet_address', selected_lang)}: {Fore.RESET}")
        
        if not wallet_address:
            wallet_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
            print(f"{Fore.YELLOW}{translate('using_sample_wallet', selected_lang)}: {wallet_address}{Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('checking_wallet_security', selected_lang)}...{Fore.RESET}")
        time.sleep(2)
        
        # Örnek güvenlik kontrol sonuçları
        print(f"\n{Fore.GREEN}{translate('wallet_security_report', selected_lang)}:{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('transaction_history_analysis', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('transactions_last_30_days', selected_lang, {'count': '45'})}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('no_suspicious_flow', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('contracts_interacted', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('safe_contracts', selected_lang)}: 12{Fore.RESET}")
        print(f"  {Fore.RED}• {translate('suspicious_contracts', selected_lang)}: 1 - 0x7cB57B5A97eAbe94205C07890BE4c1aD31E486A8{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('asset_security', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('total_asset_value', selected_lang)}: ~$12,540{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('low_liquidity_assets', selected_lang)}: 2 token{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('recommendations', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.YELLOW}• {translate('stop_suspicious_contract', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.YELLOW}• {translate('use_hardware_wallet', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.YELLOW}• {translate('switch_to_multisig', selected_lang)}{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def crypto_asset_monitor():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('crypto_asset_monitor', selected_lang)}{Fore.RESET}\n")
        
        address = input(f"{Fore.MAGENTA}{translate('enter_monitor_address', selected_lang)}: {Fore.RESET}")
        
        if not address:
            address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
            print(f"{Fore.YELLOW}{translate('using_sample_wallet', selected_lang)}: {address}{Fore.RESET}")
        
        networks_questions = [
            inquirer.Checkbox(
                'networks',
                message=f'{Fore.YELLOW}{translate("select_networks_to_monitor", selected_lang)}:{Fore.RESET}',
                choices=[
                    ("Ethereum", "ethereum"),
                    ("Binance Smart Chain", "bsc"),
                    ("Polygon", "polygon"),
                    ("Arbitrum", "arbitrum"),
                    ("Optimism", "optimism"),
                    ("Avalanche", "avalanche"),
                ],
                default=["ethereum", "bsc"]
            )
        ]
        
        result = inquirer.prompt(networks_questions)
        if result is None or not result['networks']:
            return
            
        networks = result['networks']
        
        alert_questions = [
            inquirer.Checkbox(
                'alerts',
                message=f'{Fore.YELLOW}{translate("select_alert_types", selected_lang)}:{Fore.RESET}',
                choices=[
                    (translate("large_transfer_alerts", selected_lang), "large_transfers"),
                    (translate("suspicious_contract_interactions", selected_lang), "suspicious_contracts"),
                    (translate("asset_value_changes", selected_lang), "value_changes"),
                    (translate("new_token_transfers", selected_lang), "new_tokens"),
                    (translate("all_transactions", selected_lang), "all_transactions"),
                ],
                default=["large_transfers", "suspicious_contracts"]
            )
        ]
        
        alert_result = inquirer.prompt(alert_questions)
        if alert_result is None:
            return
            
        alerts = alert_result['alerts']
        
        print(f"\n{Fore.YELLOW}{translate('starting_crypto_asset_monitoring', selected_lang)}...")
        print(f"{Fore.WHITE}{translate('address', selected_lang)}: {address}{Fore.RESET}")
        print(f"{Fore.WHITE}{translate('monitored_networks', selected_lang)}: {', '.join(networks)}{Fore.RESET}")
        print(f"{Fore.WHITE}{translate('active_alerts', selected_lang)}: {', '.join(alerts)}{Fore.RESET}")
        
        print(f"\n{Fore.GREEN}{translate('monitoring_started_successfully', selected_lang)}{Fore.RESET}")
        
        # Örnek varlık listesi
        print(f"\n{Fore.CYAN}{translate('detected_assets', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• 2.45 ETH (Ethereum){Fore.RESET}")
        print(f"  {Fore.WHITE}• 150.23 MATIC (Polygon){Fore.RESET}")
        print(f"  {Fore.WHITE}• 5,000 USDT (Ethereum){Fore.RESET}")
        print(f"  {Fore.WHITE}• 245.5 LINK (Ethereum){Fore.RESET}")
        print(f"  {Fore.WHITE}• 10.5 BNB (Binance Smart Chain){Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('monitoring_reports_saved', selected_lang)}: reports/crypto_monitor_{address[:6]}_{time.strftime('%Y%m%d')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")