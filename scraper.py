from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
import datetime
import re

def fetch_advanced_stats():
    """Selenium ile RealGM Advanced Stats çek"""
    
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
        time.sleep(5)  # JS render için bekle
        
        wait = WebDriverWait(driver, 30)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tablesaw")))
        
        print("Tablo bulundu, veriler çekiliyor...")
        
        teams = {}
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 11:
                continue
            
            team_cell = cols[1]
            team_name = team_cell.text.strip()
            
            try:
                team_link = team_cell.find_element(By.TAG_NAME, "a").get_attribute("href")
                match = re.search(r'/nba/teams/([A-Z]{3})/', team_link)
                team_code = match.group(1) if match else team_name[:3].upper()
            except:
                team_code = team_name[:3].upper()
            
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
        
        return teams
        
    except Exception as e:
        print(f"Hata: {e}")
        return {}
    finally:
        driver.quit()

def fetch_misc_stats(teams):
    """Selenium ile Misc Stats çek (MOV, Win%)"""
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://basketball.realgm.com/nba/team-stats/2026/Misc_Stats/Team_Totals/Regular_Season"
        print(f"\nMisc Stats yükleniyor: {url}")
        
        driver.get(url)
        time.sleep(5)
        
        wait = WebDriverWait(driver, 30)
        table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tablesaw")))
        
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) < 6:
                continue
            
            team_name = cols[1].text.strip()
            
            team_code = None
            for code, data in teams.items():
                if data["name"] == team_name:
                    team_code = code
                    break
            
            if not team_code:
                continue
            
            try:
                mov = float(cols[5].text.strip())
                win_pct = float(cols[4].text.strip())
                teams[team_code]["mov"] = mov
                teams[team_code]["win"] = win_pct
                print(f"✓ {team_code}: MOV={mov}, Win%={win_pct}")
            except:
                continue
        
        return teams
        
    except Exception as e:
        print(f"Misc Hata: {e}")
        return teams
    finally:
        driver.quit()

def main():
    print("=== NBA Stats Scraper (Selenium) ===\n")
    
    teams = fetch_advanced_stats()
    
    if not teams:
        print("Veri çekilemedi")
        return
    
    teams = fetch_misc_stats(teams)
    
    output = {
        "last_updated": datetime.datetime.now().isoformat(),
        "teams": teams
    }
    
    with open("teams.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ {len(teams)} takım kaydedildi")

if __name__ == "__main__":
    main()
