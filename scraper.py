import requests
from bs4 import BeautifulSoup
import json
import re

# Renkli çıktı için
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def fetch_advanced_stats():
    """RealGM Advanced Stats çek"""
    url = "https://basketball.realgm.com/nba/team-stats/2026/Advanced_Stats/Team_Totals/Regular_Season"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"{Colors.BLUE}Advanced Stats çekiliyor...{Colors.END}")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"{Colors.RED}Hata: {e}{Colors.END}")
        return {}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Tabloyu bul
    table = soup.find('table', {'class': 'tablesaw'})
    if not table:
        print(f"{Colors.RED}Tablo bulunamadı{Colors.END}")
        return {}
    
    teams = {}
    
    # Satırları işle (ilk satır header)
    rows = table.find('tbody').find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 10:
            continue
        
        # Takım adı ve kodu
        team_cell = cols[1]
        team_name = team_cell.get_text(strip=True)
        team_link = team_cell.find('a')
        
        if team_link:
            # Linkten kısa kod çıkar (örn: /nba/teams/LAL/...)
            href = team_link.get('href', '')
            match = re.search(r'/nba/teams/([A-Z]{3})/', href)
            team_code = match.group(1) if match else team_name[:3].upper()
        else:
            team_code = team_name[:3].upper()
        
        # Stats
        try:
            ortg = float(cols[9].get_text(strip=True))  # ORtg
            drtg = float(cols[10].get_text(strip=True))  # DRtg
            pace = float(cols[8].get_text(strip=True))   # Pace
            gp = int(cols[3].get_text(strip=True))       # GP
        except:
            continue
        
        teams[team_code] = {
            'name': team_name,
            'ortg': ortg,
            'drtg': drtg,
            'pace': pace,
            'gp': gp,
            'mov': 0,    # Misc stats'tan gelecek
            'win': 0,    # Misc stats'tan gelecek
            'form': None # Flashscore'dan gelecek
        }
        
        print(f"{Colors.GREEN}✓ {team_code}: {team_name}{Colors.END}")
    
    return teams

def fetch_misc_stats(existing_teams):
    """RealGM Misc Stats çek (MOV, Win%)"""
    url = "https://basketball.realgm.com/nba/team-stats/2026/Misc_Stats/Team_Totals/Regular_Season"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print(f"\n{Colors.BLUE}Misc Stats çekiliyor...{Colors.END}")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        print(f"{Colors.RED}Hata: {e}{Colors.END}")
        return existing_teams
    
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'tablesaw'})
    
    if not table:
        print(f"{Colors.RED}Tablo bulunamadı{Colors.END}")
        return existing_teams
    
    rows = table.find('tbody').find_all('tr')
    
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 15:
            continue
        
        team_cell = cols[1]
        team_name = team_cell.get_text(strip=True)
        
        # Takımı bul
        team_code = None
        for code, data in existing_teams.items():
            if data['name'] == team_name:
                team_code = code
                break
        
        if not team_code:
            continue
        
        try:
            mov = float(cols[5].get_text(strip=True))   # MOV
            win_pct = float(cols[4].get_text(strip=True))  # Win%
        except:
            continue
        
        existing_teams[team_code]['mov'] = mov
        existing_teams[team_code]['win'] = win_pct
        
        print(f"{Colors.ORANGE}✓ {team_code}: MOV={mov}, Win%={win_pct}{Colors.END}")
    
    return existing_teams

def save_to_json(teams):
    import datetime
    
    output = {
        'last_updated': datetime.datetime.now().isoformat(),
        'teams': teams
    }
    
    with open('teams.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n{Colors.GREEN}✓ teams.json kaydedildi ({len(teams)} takım){Colors.END}")

def main():
    print(f"{Colors.GREEN}=== NBA Stats Scraper ==={Colors.END}\n")
    
    # Advanced Stats
    teams = fetch_advanced_stats()
    
    if not teams:
        print(f"{Colors.RED}Veri çekilemedi{Colors.END}")
        return
    
    # Misc Stats
    teams = fetch_misc_stats(teams)
    
    # Kaydet
    save_to_json(teams)
    
    print(f"\n{Colors.GREEN}Tamamlandı!{Colors.END}")

if __name__ == '__main__':
    main()
