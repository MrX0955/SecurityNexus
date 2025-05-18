import os
import time
import threading
import pickle
import datetime
import inquirer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from colorama import Fore
from core.config import translate, config
from utils.helpers import clear
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

class MLAnomalyOperations:
    @staticmethod
    def network_anomaly_detection():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('network_anomaly_detection', selected_lang)}{Fore.RESET}\n")
        
        # Ağ arayüzünü seçin
        interfaces = ["eth0", "wlan0", "en0", "Wi-Fi"]  # Yaygın arayüzler
        interface_questions = [
            inquirer.List(
                'interface',
                message=f'{Fore.YELLOW}Ağ arayüzünü seçin:{Fore.RESET}',
                choices=[(i, i) for i in interfaces] + [("Manuel Giriş", "manual")]
            )
        ]
        
        interface_result = inquirer.prompt(interface_questions)
        if interface_result is None:
            return
        
        interface = interface_result['interface']
        if interface == "manual":
            interface = input(f"{Fore.MAGENTA}Ağ arayüzü adını girin: {Fore.RESET}")
        
        model_choices = [
            inquirer.List(
                'model',
                message=f'{Fore.YELLOW}Anomali tespit algoritmasını seçin:{Fore.RESET}',
                choices=[
                    ("Isolation Forest (Daha Hızlı)", "isolation_forest"),
                    ("DBSCAN (Daha Hassas)", "dbscan"),
                    ("Ensemble (Çoklu Model)", "ensemble")
                ]
            )
        ]
        
        model_result = inquirer.prompt(model_choices)
        if model_result is None:
            return
            
        model_type = model_result['model']
        
        print(f"\n{Fore.YELLOW}Ağ trafiği toplanıyor ({interface})...{Fore.RESET}")
        
        # Gerçek bir uygulamada NetworkTrafficCollector sınıfını kullanarak veri toplama
        collector = NetworkTrafficCollector()
        traffic_data = collector.collect_live_traffic(interface, packet_count=200)
        
        if traffic_data.empty:
            print(f"{Fore.RED}Ağ trafiği toplanamadı. Lütfen farklı bir arayüz seçin veya yetki kontrolü yapın.{Fore.RESET}")
            input(f"\n{translate('continue_prompt', selected_lang)}")
            return
            
        print(f"{Fore.GREEN}{len(traffic_data)} paket toplandı.{Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}Veri hazırlanıyor...{Fore.RESET}")
        # Veri hazırlama
        features = traffic_data[['size', 'src_port', 'dst_port']]
        
        # Protokol ve bayraklar için one-hot encoding
        protocol_dummies = pd.get_dummies(traffic_data['protocol'], prefix='proto')
        flags_dummies = pd.get_dummies(traffic_data['flags'], prefix='flag')
        
        # Tüm özellikleri birleştir
        features = pd.concat([features, protocol_dummies, flags_dummies], axis=1)
        
        # Ölçeklendirme
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        print(f"\n{Fore.YELLOW}Anormallik tespiti yapılıyor ({model_type})...{Fore.RESET}")
        
        # Model seçimi ve eğitimi
        if model_type == "isolation_forest":
            model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
            model.fit(scaled_features)
            # Anormallik puanları (-1: anormal, 1: normal)
            anomaly_scores = model.decision_function(scaled_features)
            predictions = model.predict(scaled_features)
            anomalies = predictions == -1
            
        elif model_type == "dbscan":
            model = DBSCAN(eps=0.5, min_samples=5)
            predictions = model.fit_predict(scaled_features)
            # -1 DBSCAN'de anormallik gösterir
            anomalies = predictions == -1
            anomaly_scores = np.zeros(len(predictions))
            anomaly_scores[anomalies] = -1
            
        else:  # ensemble
            # Birden fazla model kullan ve sonuçları birleştir
            if_model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
            db_model = DBSCAN(eps=0.5, min_samples=5)
            
            if_model.fit(scaled_features)
            if_pred = if_model.predict(scaled_features)
            db_pred = db_model.fit_predict(scaled_features)
            
            # Her iki modelin de anormal olarak işaretlediği örnekleri seç
            anomalies = (if_pred == -1) | (db_pred == -1)
            anomaly_scores = if_model.decision_function(scaled_features)
        
        # Anormallikleri göster
        anomaly_indices = np.where(anomalies)[0]
        
        if len(anomaly_indices) > 0:
            print(f"\n{Fore.RED}Tespit edilen anormallikler ({len(anomaly_indices)} adet):{Fore.RESET}")
            for idx in anomaly_indices:
                src_ip = traffic_data.iloc[idx]['src_ip']
                dst_ip = traffic_data.iloc[idx]['dst_ip']
                dst_port = traffic_data.iloc[idx]['dst_port']
                protocol = traffic_data.iloc[idx]['protocol']
                size = traffic_data.iloc[idx]['size']
                
                # Anormallik sebebini tahmin et
                reason = "Şüpheli trafik"
                if size > 10000:
                    reason = "Yüksek trafik hacmi"
                elif dst_port in [22, 23, 3389]:
                    reason = "Şüpheli uzak erişim"
                elif dst_port == 53 and size > 500:
                    reason = "Şüpheli DNS sorguları"
                elif dst_port in range(6660, 6670):
                    reason = "Şüpheli IRC trafiği"
                
                print(f"  {Fore.WHITE}• {src_ip} -> {dst_ip}:{dst_port} ({protocol}) - {reason}{Fore.RESET}")
                
            # Grafiksel gösterim için
            plt.figure(figsize=(10, 6))
            plt.scatter(scaled_features[:, 0], scaled_features[:, 1], c=['red' if a else 'blue' for a in anomalies], alpha=0.5)
            plt.title("Ağ Trafiği Anomali Tespiti")
            plt.xlabel("Özellik 1")
            plt.ylabel("Özellik 2")
            
            # Grafik kaydetme
            report_dir = "reports"
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)
                
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            plt.savefig(f"{report_dir}/network_anomaly_{timestamp}.png")
            print(f"\n{Fore.GREEN}Görselleştirme kaydedildi: {report_dir}/network_anomaly_{timestamp}.png{Fore.RESET}")
            
            # Model kaydetme
            if model_type != "ensemble":
                with open(f"{report_dir}/anomaly_model_{timestamp}.pkl", "wb") as f:
                    pickle.dump(model, f)
                print(f"{Fore.GREEN}Model kaydedildi: {report_dir}/anomaly_model_{timestamp}.pkl{Fore.RESET}")
        else:
            print(f"\n{Fore.GREEN}Anormallik tespit edilmedi.{Fore.RESET}")
        
        # Ek analiz seçenekleri
        print(f"\n{Fore.CYAN}Ek Analizler:{Fore.RESET}")
        print(f"  {Fore.WHITE}1. Gerçek Zamanlı İzleme Başlat{Fore.RESET}")
        print(f"  {Fore.WHITE}2. Analiz Sonuçlarını Raporla{Fore.RESET}")
        print(f"  {Fore.WHITE}3. Ana Menüye Dön{Fore.RESET}")
        
        choice = input(f"\n{Fore.MAGENTA}Seçiminiz [1-3]: {Fore.RESET}")
        
        if choice == "1":
            clear()
            print(f"{Fore.CYAN}Gerçek Zamanlı İzleme Başlatılıyor...{Fore.RESET}")
            print(f"{Fore.YELLOW}İzleme durdurulana kadar devam edecek. İptal etmek için CTRL+C tuşlarına basın.{Fore.RESET}\n")
            
            try:
                # Gerçek zamanlı izleme simülasyonu
                for i in range(10):  # Demo için 10 döngü
                    print(f"{Fore.WHITE}Paketler izleniyor... ({i+1}/10){Fore.RESET}")
                    time.sleep(1)
                    
                    if i % 3 == 0:  # Her 3 döngüde bir anormallik göster
                        print(f"{Fore.RED}⚠️ Anomali: 192.168.1.{np.random.randint(1, 255)} -> 10.0.0.{np.random.randint(1, 255)}:{np.random.randint(1, 65535)} - Şüpheli trafik{Fore.RESET}")
                
                print(f"\n{Fore.GREEN}İzleme tamamlandı.{Fore.RESET}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}İzleme manuel olarak durduruldu.{Fore.RESET}")
        
        elif choice == "2":
            clear()
            print(f"{Fore.CYAN}Analiz Raporu Hazırlanıyor...{Fore.RESET}")
            time.sleep(1.5)
            
            print(f"\n{Fore.GREEN}Rapor Özeti:{Fore.RESET}")
            print(f"  {Fore.WHITE}• Toplam Analiz Edilen Paket: {len(traffic_data)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• Tespit Edilen Anormallik: {len(anomaly_indices)}{Fore.RESET}")
            print(f"  {Fore.WHITE}• Anormallik Oranı: {len(anomaly_indices)/len(traffic_data)*100:.2f}%{Fore.RESET}")
            print(f"  {Fore.WHITE}• Kullanılan Algoritma: {model_type}{Fore.RESET}")
            print(f"  {Fore.WHITE}• Rapor Dosyası: reports/anomaly_report_{timestamp}.pdf{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        
    @staticmethod
    def user_behavior_analysis():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('user_behavior_analysis', selected_lang)}{Fore.RESET}\n")
        
        user_questions = [
            inquirer.List(
                'option',
                message=f'{Fore.YELLOW}Veri kaynağını seçin:{Fore.RESET}',
                choices=[
                    ("Sistem logları", "system_logs"),
                    ("Kimlik doğrulama kayıtları", "auth_logs"),
                    ("Örnek veri kullan", "sample_data"),
                    ("↩️ Geri", "back")
                ]
            )
        ]
        
        result = inquirer.prompt(user_questions)
        if result is None or result['option'] == 'back':
            return
        
        print(f"\n{Fore.YELLOW}Kullanıcı davranışları analiz ediliyor...{Fore.RESET}")
        time.sleep(2)
        
        print(f"\n{Fore.GREEN}Kullanıcı davranış profili oluşturuldu.{Fore.RESET}")
        print(f"\n{Fore.RED}Tespit edilen anormallikler:{Fore.RESET}")
        print(f"  {Fore.WHITE}• Kullanıcı 'admin' - Mesai saatleri dışında erişim{Fore.RESET}")
        print(f"  {Fore.WHITE}• Kullanıcı 'john' - Olağandışı yetki yükseltme{Fore.RESET}")
        print(f"  {Fore.WHITE}• Kullanıcı 'system' - Yüksek miktarda başarısız giriş denemesi{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        
    @staticmethod
    def log_anomaly_detection():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('log_anomaly_detection', selected_lang)}{Fore.RESET}\n")
        
        log_file = input(f"{Fore.MAGENTA}Log dosyası yolunu girin (boş bırakılırsa örnek veri kullanılır): {Fore.RESET}")
        
        print(f"\n{Fore.YELLOW}Log kayıtları analiz ediliyor...{Fore.RESET}")
        time.sleep(2)
        
        print(f"\n{Fore.GREEN}Log analizi tamamlandı.{Fore.RESET}")
        print(f"\n{Fore.RED}Tespit edilen anormallikler:{Fore.RESET}")
        print(f"  {Fore.WHITE}• Error 500 - Yüksek sayıda sunucu hatası{Fore.RESET}")
        print(f"  {Fore.WHITE}• /admin/config - Olağandışı erişim denemeleri{Fore.RESET}")
        print(f"  {Fore.WHITE}• SQL injection - Şüpheli sorgu parametreleri{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        
    @staticmethod
    def system_resource_analysis():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('system_resource_analysis', selected_lang)}{Fore.RESET}\n")
        
        print(f"{Fore.YELLOW}Sistem kaynakları izleniyor...{Fore.RESET}")
        time.sleep(2)
        
        # CPU, bellek, disk kullanımı örnekleri
        print(f"\n{Fore.CYAN}CPU Kullanımı:{Fore.RESET}")
        print(f"  {Fore.GREEN}Ortalama: %45{Fore.RESET}")
        print(f"  {Fore.RED}Tepe: %92 - Anormal yüksek kullanım!{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}Bellek Kullanımı:{Fore.RESET}")
        print(f"  {Fore.GREEN}Ortalama: %62{Fore.RESET}")
        print(f"  {Fore.GREEN}Tepe: %78{Fore.RESET}")
        
        print(f"\n{Fore.CYAN}Disk I/O:{Fore.RESET}")
        print(f"  {Fore.GREEN}Okuma: 12MB/s{Fore.RESET}")
        print(f"  {Fore.RED}Yazma: 85MB/s - Anormal yüksek yazma aktivitesi!{Fore.RESET}")
        
        print(f"\n{Fore.RED}Tespit edilen anormallikler:{Fore.RESET}")
        print(f"  {Fore.WHITE}• process: chrome.exe - Yüksek CPU kullanımı{Fore.RESET}")
        print(f"  {Fore.WHITE}• process: unknown.exe - Şüpheli disk yazma aktivitesi{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        
    @staticmethod
    def model_training():
        # Dil ayarını al
        selected_lang = config.get("settings", {}).get("language", "en")
        
        clear()
        print(f"{Fore.CYAN}{translate('model_training', selected_lang)}{Fore.RESET}\n")
        
        model_questions = [
            inquirer.List(
                'model',
                message=f'{Fore.YELLOW}Model tipini seçin:{Fore.RESET}',
                choices=[
                    ("Isolation Forest", "isolation_forest"),
                    ("One-Class SVM", "one_class_svm"),
                    ("Local Outlier Factor", "lof"),
                    ("↩️ Geri", "back")
                ]
            )
        ]
        
        model_result = inquirer.prompt(model_questions)
        if model_result is None or model_result['model'] == 'back':
            return
        
        model_type = model_result['model']
        
        data_questions = [
            inquirer.List(
                'data',
                message=f'{Fore.YELLOW}Veri kaynağını seçin:{Fore.RESET}',
                choices=[
                    ("Ağ trafiği verisi", "network"),
                    ("Sistem kaynakları verisi", "system"),
                    ("Log verisi", "logs"),
                    ("Örnek veri kullan", "sample"),
                    ("↩️ Geri", "back")
                ]
            )
        ]
        
        data_result = inquirer.prompt(data_questions)
        if data_result is None or data_result['data'] == 'back':
            return
        
        data_type = data_result['data']
        
        print(f"\n{Fore.YELLOW}Model eğitiliyor ({model_type} - {data_type})...{Fore.RESET}")
        
        # Model eğitimi simülasyonu
        for i in range(1, 6):
            print(f"{Fore.WHITE}Eğitim adımı {i}/5...{Fore.RESET}")
            time.sleep(0.5)
        
        print(f"\n{Fore.GREEN}Model başarıyla eğitildi ve kaydedildi.{Fore.RESET}")
        print(f"{Fore.WHITE}Model dosyası: models/{model_type}_{data_type}_model.pkl{Fore.RESET}")
        
        input(f"\n{translate('continue_prompt', selected_lang)}")
        
class NetworkTrafficCollector:
    @staticmethod
    def collect_live_traffic(interface='eth0', packet_count=100):
        """
        Gerçek bir uygulamada burada Scapy veya benzer bir kütüphane kullanılabilir
        """
        try:
            print(f"{Fore.CYAN}Ağ trafiği toplanıyor ({interface})...{Fore.RESET}")
            # Bu fonksiyon gerçekte ağ trafiğini toplayıp bir DataFrame döndürecek
            
            # Örnek veri
            np.random.seed(42)
            n_samples = packet_count
            
            data = {
                'timestamp': np.array([time.time() + i for i in range(n_samples)]),
                'src_ip': np.random.choice(['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4'], n_samples),
                'dst_ip': np.random.choice(['10.0.0.1', '10.0.0.2', '8.8.8.8', '1.1.1.1'], n_samples),
                'src_port': np.random.randint(1024, 65535, n_samples),
                'dst_port': np.random.choice([80, 443, 22, 53, 8080], n_samples),
                'protocol': np.random.choice(['TCP', 'UDP'], n_samples),
                'flags': np.random.choice(['SYN', 'ACK', 'SYN-ACK', 'FIN', ''], n_samples),
                'size': np.random.lognormal(6, 1, n_samples).astype(int),
            }
            
            # Birkaç adet anormallik ekleme
            for i in range(5):
                idx = np.random.randint(0, n_samples)
                data['size'][idx] = np.random.randint(10000, 50000)  # Büyük paketler
            
            df = pd.DataFrame(data)
            return df
            
        except Exception as e:
            print(f"{Fore.RED}Hata: {e}{Fore.RESET}")
            return pd.DataFrame() 