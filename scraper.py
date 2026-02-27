from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def fetch_with_selenium():
    """Selenium ile RealGM'den çek"""
    
    # Chrome ayarları (headless)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://basketball.realgm.com/nba/team-stats/2026/Advanced_Stats/Team_Totals/Regular_Season"
        print(f"Sayfa yükleniyor: {url}")
        
        driver.get(url)
        
        # Tablo yüklenene kadar bekle
        wait = WebDriverWait(driver, 30)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tablesaw")))
        
        print("Tablo bulundu, veriler çekiliyor...")
        
        # Verileri çek
        teams = {}
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        for row in rows[1:]:  # İlk satır header
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 10:
                continue
            
            team_name = cols[1].text.strip()
            team_link = cols[1].find_element(By.TAG_NAME, "a").get_attribute("href")
            
            # Kısa kod çıkar
            import re
            match = re.search(r'/nba/teams/([A-Z]{3})/', team_link)
            team_code = match.group(1) if match else team_name[:3].upper()
            
            try:
                ortg = float(cols[9].text.strip())
                drtg = float(cols[10].text.strip())
                pace = float(cols[8].text.strip())
                gp = int(cols[3].text.strip())
            except:
                continue
            
            teams[team_code] = {
                "name": team_name,
                "ortg": ortg,
                "drtg": drtg,
                "pace": pace,
                "gp": gp,
                "mov": 0,
                "win": 0,
                "form": None
            }
            print(f"✓ {team_code}: {team_name}")
        
        driver.quit()
        return teams
        
    except Exception as e:
        print(f"Hata: {e}")
        driver.quit()
        return {}

# Çalıştır
if __name__ == "__main__":
    teams = fetch_with_selenium()
    
    if teams:
        import datetime
        output = {
            "last_updated": datetime.datetime.now().isoformat(),
            "teams": teams
        }
        
        with open("teams.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ {len(teams)} takım kaydedildi")
    else:
        print("\n✗ Veri çekilemedi")
