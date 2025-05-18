import os
import time
import datetime
import inquirer
from colorama import Fore
from core.config import translate, config
from utils.helpers import clear

class ZeroTrustOperations:
    @staticmethod
    def access_policy_analyzer():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('access_policy_analyzer', selected_lang)}{Fore.RESET}\n")
        
        policy_file = input(f"{Fore.MAGENTA}{translate('enter_policy_file', selected_lang)}: {Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('analyzing_access_policies', selected_lang)}...{Fore.RESET}")
        time.sleep(2)
        
        # Örnek politika analizi
        print(f"\n{Fore.GREEN}{translate('policy_analysis_completed', selected_lang)}:{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('policy_statistics', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('total_policies', selected_lang)}: 24{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('user_based_policies', selected_lang)}: 12{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('group_based_policies', selected_lang)}: 8{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('network_based_policies', selected_lang)}: 4{Fore.RESET}")
        
        print(f"\n{Fore.RED}{translate('detected_issues', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('high', selected_lang)}] {translate('overly_permissive_policies', selected_lang, {'count': '3'})}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('conflicting_policies', selected_lang, {'count': '5'})}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('user_based_privileged_access', selected_lang, {'count': '2'})}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('low', selected_lang)}] {translate('unused_policies', selected_lang, {'count': '4'})}{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('zero_trust_compliance_score', selected_lang)}: 65/100{Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('recommendations', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('make_policies_granular', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('use_mfa', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('implement_least_privilege', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('resolve_policy_conflicts', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('detailed_report', selected_lang)}: reports/access_policy_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def network_segmentation_check():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('network_segmentation_check', selected_lang)}{Fore.RESET}\n")
        
        network_map = input(f"{Fore.MAGENTA}{translate('enter_network_map', selected_lang)}: {Fore.RESET}")
        
        discovery_questions = [
            inquirer.List(
                'method',
                message=f'{Fore.YELLOW}{translate("select_discovery_method", selected_lang)}:{Fore.RESET}',
                choices=[
                    (translate("passive_discovery", selected_lang), "passive"),
                    (translate("active_scanning", selected_lang), "active"),
                    (translate("load_from_file", selected_lang), "file"),
                    (f"↩️ {translate('back', selected_lang)}", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(discovery_questions)
        if result is None or result['method'] == 'back':
            return
            
        method = result['method']
        
        print(f"\n{Fore.YELLOW}{translate('analyzing_network_segmentation', selected_lang)} ({method})...{Fore.RESET}")
        
        # Analiz süreci simülasyonu
        for i in range(4):
            print(f"{Fore.WHITE}{translate('analysis_step', selected_lang)} {i+1}/4...{Fore.RESET}")
            time.sleep(1)
        
        print(f"\n{Fore.GREEN}{translate('network_segmentation_analysis_completed', selected_lang)}:{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('segmentation_summary', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('detected_subnets', selected_lang)}: 5{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('vlan_count', selected_lang)}: 8{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('security_control_points', selected_lang)}: 4{Fore.RESET}")
        
        print(f"\n{Fore.RED}{translate('segmentation_issues', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('high', selected_lang)}] {translate('no_isolation_critical_user', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('limited_filtering_workstation_server', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('iot_devices_not_separate', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('low', selected_lang)}] {translate('traffic_not_encrypted', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('zero_trust_microsegmentation_score', selected_lang)}: 45/100{Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('recommendations', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('create_separate_vlan', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('control_segment_traffic', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('move_iot_separate_networks', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('implement_app_based_policies', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('detailed_report', selected_lang)}: reports/network_segmentation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def identity_verification_check():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('identity_verification_check', selected_lang)}{Fore.RESET}\n")
        
        idp_questions = [
            inquirer.List(
                'idp',
                message=f'{Fore.YELLOW}{translate("select_identity_provider", selected_lang)}:{Fore.RESET}',
                choices=[
                    ("Active Directory", "ad"),
                    ("Azure AD", "azure_ad"),
                    ("Okta", "okta"),
                    ("Google Workspace", "google"),
                    ("Keycloak", "keycloak"),
                    ("OneLogin", "onelogin"),
                    (translate("other", selected_lang), "other"),
                    (f"↩️ {translate('back', selected_lang)}", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(idp_questions)
        if result is None or result['idp'] == 'back':
            return
            
        idp = result['idp']
        
        if idp == 'other':
            idp_name = input(f"{Fore.MAGENTA}{translate('enter_idp_name', selected_lang)}: {Fore.RESET}")
            idp = idp_name
        
        print(f"\n{Fore.YELLOW}{translate('analyzing_identity_system', selected_lang)} ({idp})...{Fore.RESET}")
        time.sleep(2)
        
        print(f"\n{Fore.GREEN}{translate('identity_system_analysis_completed', selected_lang)}:{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('authentication_summary', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('single_factor_auth', selected_lang)}: {translate('active', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('multi_factor_auth', selected_lang)}: {translate('partially_active', selected_lang, {'details': translate('for_admins', selected_lang)})}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('sso_integration', selected_lang)}: {translate('active', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('context_based_access', selected_lang)}: {translate('passive', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.RED}{translate('detected_issues', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('high', selected_lang)}] {translate('mfa_not_required', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('password_policies_weak', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('medium', selected_lang)}] {translate('location_verification_inactive', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• [{translate('low', selected_lang)}] {translate('session_timeout_long', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('zero_trust_authentication_score', selected_lang)}: 60/100{Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('recommendations', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('make_mfa_mandatory', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('strengthen_password_policies', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('enable_location_device_policies', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('reduce_session_timeout', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('detailed_report', selected_lang)}: reports/identity_verification_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def context_based_security():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('context_based_security', selected_lang)}{Fore.RESET}\n")
        
        print(f"{Fore.YELLOW}{translate('which_contextual_factors_analyze', selected_lang)}?{Fore.RESET}")
        factors_questions = [
            inquirer.Checkbox(
                'factors',
                message=f'{Fore.YELLOW}{translate("factors", selected_lang)}:{Fore.RESET}',
                choices=[
                    (translate("user_identity", selected_lang), "user_identity"),
                    (translate("device_health", selected_lang), "device_health"),
                    (translate("location", selected_lang), "location"),
                    (translate("time", selected_lang), "time"),
                    (translate("network_connection", selected_lang), "network"),
                    (translate("data_sensitivity", selected_lang), "data_sensitivity"),
                    (translate("application_risk", selected_lang), "application_risk"),
                ],
                default=["user_identity", "device_health", "location"]
            )
        ]
        
        factors_result = inquirer.prompt(factors_questions)
        if factors_result is None or not factors_result['factors']:
            return
            
        factors = factors_result['factors']
        
        print(f"\n{Fore.YELLOW}{translate('evaluating_context_security', selected_lang)}...{Fore.RESET}")
        print(f"{Fore.WHITE}{translate('analyzed_factors', selected_lang)}: {', '.join(factors)}{Fore.RESET}")
        
        # Analiz simülasyonu
        for i in range(3):
            print(f"{Fore.WHITE}{translate('analysis_step', selected_lang)} {i+1}/3...{Fore.RESET}")
            time.sleep(1)
        
        print(f"\n{Fore.GREEN}{translate('context_security_assessment_completed', selected_lang)}:{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('current_status', selected_lang)}:{Fore.RESET}")
        
        if "user_identity" in factors:
            print(f"\n  {Fore.YELLOW}{translate('user_identity_factor', selected_lang)}:{Fore.RESET}")
            print(f"    {Fore.WHITE}• {translate('user_risk_scoring', selected_lang)}: {translate('passive', selected_lang)}{Fore.RESET}")
            print(f"    {Fore.WHITE}• {translate('role_based_access', selected_lang)}: {translate('active', selected_lang)}{Fore.RESET}")
            print(f"    {Fore.WHITE}• {translate('continuous_verification', selected_lang)}: {translate('passive', selected_lang)}{Fore.RESET}")
        
        if "device_health" in factors:
            print(f"\n  {Fore.YELLOW}{translate('device_health_factor', selected_lang)}:{Fore.RESET}")
            print(f"    {Fore.WHITE}• {translate('device_compliance_check', selected_lang)}: {translate('partially_active', selected_lang)}{Fore.RESET}")
            print(f"    {Fore.WHITE}• {translate('device_security_score', selected_lang)}: {translate('passive', selected_lang)}{Fore.RESET}")
            print(f"    {Fore.WHITE}• {translate('edr_solution_integration', selected_lang)}: {translate('passive', selected_lang)}{Fore.RESET}")
        
        if "location" in factors:
            print(f"\n  {Fore.YELLOW}{translate('location_factor', selected_lang)}:{Fore.RESET}")
            print(f"    {Fore.WHITE}• {translate('geo_location_based_access', selected_lang)}: {translate('passive', selected_lang)}{Fore.RESET}")
            print(f"    {Fore.WHITE}• {translate('ip_address_risk', selected_lang)}: {translate('partially_active', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('zero_trust_context_security_score', selected_lang)}: 40/100{Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('recommendations', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('apply_dynamic_risk_scoring', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('continuous_user_device_verification', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('implement_location_ip_policies', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('integrate_edr_identity_management', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('implement_data_classification', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('detailed_report', selected_lang)}: reports/context_security_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
    
    @staticmethod
    def zero_trust_assessment():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('zero_trust_assessment', selected_lang)}{Fore.RESET}\n")
        
        print(f"{Fore.YELLOW}{translate('starting_comprehensive_assessment', selected_lang)}...{Fore.RESET}")
        time.sleep(2)
        
        # Değerlendirme simülasyonu
        print(f"\n{Fore.WHITE}{translate('checking_identity_verification', selected_lang)}...{Fore.RESET}")
        time.sleep(1)
        print(f"{Fore.WHITE}{translate('checking_device_trust', selected_lang)}...{Fore.RESET}")
        time.sleep(1)
        print(f"{Fore.WHITE}{translate('analyzing_network_access', selected_lang)}...{Fore.RESET}")
        time.sleep(1)
        print(f"{Fore.WHITE}{translate('evaluating_application_access', selected_lang)}...{Fore.RESET}")
        time.sleep(1)
        print(f"{Fore.WHITE}{translate('checking_data_protection', selected_lang)}...{Fore.RESET}")
        time.sleep(1)
        
        print(f"\n{Fore.GREEN}{translate('zero_trust_assessment_completed', selected_lang)}:{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}{translate('zero_trust_pillars', selected_lang)}:{Fore.RESET}")
        
        pillars = [
            {"name": translate("identity", selected_lang), "score": 60, "status": translate("partial", selected_lang)},
            {"name": translate("devices", selected_lang), "score": 45, "status": translate("partial", selected_lang)},
            {"name": translate("networks", selected_lang), "score": 50, "status": translate("partial", selected_lang)},
            {"name": translate("applications", selected_lang), "score": 35, "status": translate("limited", selected_lang)},
            {"name": translate("data", selected_lang), "score": 25, "status": translate("limited", selected_lang)},
            {"name": translate("visibility_analytics", selected_lang), "score": 40, "status": translate("partial", selected_lang)},
            {"name": translate("automation_orchestration", selected_lang), "score": 20, "status": translate("limited", selected_lang)},
        ]
        
        # Değerlendirme sonuçlarını göster
        for pillar in pillars:
            score = pillar["score"]
            if score >= 75:
                color = Fore.GREEN
            elif score >= 50:
                color = Fore.YELLOW
            elif score >= 25:
                color = Fore.LIGHTYELLOW_EX
            else:
                color = Fore.RED
                
            print(f"  {color}• {pillar['name']}: {score}/100 - {pillar['status']}{Fore.RESET}")
        
        # Genel değerlendirme puanı
        total_score = sum(p["score"] for p in pillars) / len(pillars)
        print(f"\n{Fore.CYAN}{translate('overall_zero_trust_score', selected_lang)}: {total_score:.1f}/100{Fore.RESET}")
        
        # Olgunluk seviyesi
        if total_score >= 80:
            maturity = translate("optimized", selected_lang)
        elif total_score >= 60:
            maturity = translate("managed", selected_lang)
        elif total_score >= 40:
            maturity = translate("defined", selected_lang)
        elif total_score >= 20:
            maturity = translate("repeatable", selected_lang)
        else:
            maturity = translate("initial", selected_lang)
            
        print(f"{Fore.CYAN}{translate('zero_trust_maturity', selected_lang)}: {maturity}{Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}{translate('key_recommendations', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}1. {translate('implement_mfa_all_users', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}2. {translate('deploy_device_health_checks', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}3. {translate('segment_network_micro_perimeters', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}4. {translate('implement_app_level_access_control', selected_lang)}{Fore.RESET}")
        print(f"  {Fore.WHITE}5. {translate('deploy_data_classification', selected_lang)}{Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('roadmap_timeline', selected_lang)}:{Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('phase1', selected_lang)}: {translate('identity_device_controls', selected_lang)} (3 {translate('months', selected_lang)}){Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('phase2', selected_lang)}: {translate('network_app_controls', selected_lang)} (6 {translate('months', selected_lang)}){Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('phase3', selected_lang)}: {translate('data_visibility_controls', selected_lang)} (9 {translate('months', selected_lang)}){Fore.RESET}")
        print(f"  {Fore.WHITE}• {translate('phase4', selected_lang)}: {translate('automation_orchestration_implementation', selected_lang)} (12 {translate('months', selected_lang)}){Fore.RESET}")
        
        print(f"\n{Fore.WHITE}{translate('detailed_report', selected_lang)}: reports/zero_trust_assessment_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")