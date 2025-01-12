import requests
from bs4 import BeautifulSoup
import os

# 기본 URL
base_url = "https://www.livesinabox.com/friends/scripts.shtml?utm_source=chatgpt.com"

def fetch_season_links(season_number):
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to access {base_url}. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    episode_links = []

    # 에피소드 링크 수집 (입력된 시즌 번호에 따라)
    for link in soup.find_all('a', href=True):
        if f"season{season_number}/" in link['href']:
            episode_links.append(link['href'])

    return episode_links

def fetch_episode_script(episode_url):
    full_url = f"https://www.livesinabox.com/friends/{episode_url}"
    print(f"Accessing: {full_url}")  # URL 확인
    response = requests.get(full_url)
    if response.status_code != 200:
        print(f"Failed to access {full_url}. Status code: {response.status_code}")
        return ""
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 제목 추출
    title = soup.find('h1').get_text(strip=True)

    # 대사 추출
    script_lines = []
    for p in soup.find_all('p'):
        # 등장인물과 대사 구분
        if p.find('b'):
            character = p.find('b').get_text(strip=True)
            dialogue = p.get_text(strip=True).replace(character, '').strip()  # 등장인물 이름 제거
            script_lines.append(f"{character}: {dialogue}")

    # 제목과 대사를 합쳐서 하나의 문자열로 만듭니다.
    script_content = f"Title: {title}\n\n"
    script_content += "\n".join(script_lines)

    return script_content

def main():
    # 사용자로부터 크롤링할 시즌 번호 입력받기
    season_number = input("크롤링할 시즌 번호를 입력하세요 (1~9): ")

    if not season_number.isdigit() or not (1 <= int(season_number) <= 9):
        print("유효한 시즌 번호를 입력하세요.")
        return

    episode_links = fetch_season_links(season_number)
    
    if not episode_links:
        print("No episode links found.")
        return

    # 스크립트 저장 폴더 생성
    season_folder = f"Friends_Scripts/Season_{season_number.zfill(2)}"
    if not os.path.exists(season_folder):
        os.makedirs(season_folder)

    for i, episode_url in enumerate(episode_links):
        print(f"Fetching script for Episode {i + 1}...")
        script = fetch_episode_script(episode_url)
        if not script:
            print(f"Failed to fetch script for {episode_url}.")
            continue
        
        episode_title = episode_url.split('/')[-1].replace('-', '_').replace('.htm', '')
        file_path = f"{season_folder}/Episode_{i + 1:03d}_{episode_title}.txt"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(script)
    
    print(f"All scripts from Season {season_number} have been fetched and saved.")

if __name__ == "__main__":
    main()


