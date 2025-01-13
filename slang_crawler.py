import requests
from bs4 import BeautifulSoup
import json  # JSON 저장을 위한 라이브러리 임포트

def fetch_slang_definitions(page_count):
    base_url = "https://www.urbandictionary.com/?page="
    slang_data = []  # 단어와 설명을 저장할 리스트

    for page in range(1, page_count + 1):
        url = f"{base_url}{page}"
        response = requests.get(url)
        response.raise_for_status()  # 오류 발생 시 예외 발생

        soup = BeautifulSoup(response.text, 'html.parser')

        # 슬랭 단어와 설명 추출
        entries = soup.find_all('div', class_='meaning')  # 슬랭 단어와 설명이 있는 div
        
        for entry in entries:
            term_element = entry.find_previous('a', class_='word')
            if term_element:
                term = term_element.text.strip()
                description = entry.text.strip()
                slang_data.append({'term': term, 'description': description})

    return slang_data

def save_to_json(data, filename='slang_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  # JSON 파일로 저장

if __name__ == "__main__":
    page_count = int(input("크롤링할 페이지 수를 입력하세요 (각 페이지마다 7개의 슬랭 단어가 있습니다): "))
    results = fetch_slang_definitions(page_count)

    # 결과를 JSON 파일에 저장
    save_to_json(results)
    print(f"{len(results)}개의 슬랭 정보가 'slang_data.json' 파일에 저장되었습니다.")
