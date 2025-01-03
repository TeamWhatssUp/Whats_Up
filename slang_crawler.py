import requests
from bs4 import BeautifulSoup
import json

def fetch_popular_slangs():
    url = "https://www.urbandictionary.com/"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    # 인기 슬랭 단어를 찾기
    slang_elements = soup.find_all('a', class_='word')  # 수정된 부분
    slangs = [element.text.strip() for element in slang_elements]

    return slangs

def fetch_slang_definition(term):
    url = f"https://www.urbandictionary.com/define.php?term={term}"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    definitions = soup.find_all('div', class_='meaning')
    examples = soup.find_all('div', class_='example')

    results = []
    
    for definition, example in zip(definitions, examples):
        results.append({
            'term': term,
            'definition': definition.text.strip(),
            'example': example.text.strip()
        })
    
    return results

def save_to_json(data, filename='slang_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 인기 슬랭 단어 자동 수집
    popular_slangs = fetch_popular_slangs()
    all_results = []

    for slang in popular_slangs:
        results = fetch_slang_definition(slang)
        all_results.extend(results)

    # 결과를 JSON 파일에 저장
    save_to_json(all_results)

    print(f"{len(all_results)}개의 슬랭 정보가 저장되었습니다.")
