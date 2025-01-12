import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from django.conf import settings
import json


# .env 파일에서 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API 키가 .env 파일에 설정되어 있지 않습니다.")

def format_character_name(character_name):
    """캐릭터 이름을 파일명에 맞게 포맷팅"""
    return character_name.strip().lower().replace(" ", "_") + "_prompt.txt"

def load_character_prompt(character_name):
    """캐릭터에 맞는 프롬프트를 파일에서 읽어오는 함수"""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  
        file_name = format_character_name(character_name)
        file_path = os.path.join(base_dir, "prompts", file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            prompt = file.read().strip()
        return prompt
    except FileNotFoundError:
        return f"Hi, I am {character_name.capitalize()}. Let's talk!"

def load_scripts(folder):
    """폴더 내 텍스트 파일을 Document 리스트로 로드"""
    documents = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append(Document(page_content=content))
    return documents

def load_slang_data(filepath):
    """슬랭 데이터를 Document 형식으로 로드"""
    with open(filepath, 'r', encoding='utf-8') as file:
        slang_data = json.load(file)
    return [Document(page_content=f"Term: {item['term']}\nDescription: {item['description']}") for item in slang_data]

def combine_documents(script_docs, slang_docs):
    """대본과 슬랭 데이터를 결합"""
    return script_docs + slang_docs

# Character 클래스 정의
class Character:
    def __init__(self, name, age, job, hobbies, skills, personality, catchphrases, conversation_patterns, intro=None, relationships=None):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies
        self.skills = skills
        self.personality = personality
        self.catchphrases = catchphrases
        self.conversation_patterns = conversation_patterns
        self.intro = intro if intro else f"Hello, I'm {name}!"
        self.relationships = relationships if relationships else {}

    def introduce(self):
        """캐릭터가 자기소개를 출력"""
        return self.intro

def create_characters():
    return [
        Character(
            name="Rachel",
            age=28,
            job="Fashion Consultant",
            hobbies=["Shopping", "Socializing", "Traveling"],
            skills=["Fashion sense", "Styling", "Branding"],
            personality="Charming, fashionable, loyal, sometimes naive, and optimistic.",
            catchphrases=["'Could I BE any more...?'"],
            conversation_patterns=["Gossipy", "Supportive", "Slightly dramatic"],
            intro="Hey! I'm Rachel Green. I love fashion and shopping. Want to tell me your story?",
            relationships={"Monica": "Best friend", "Ross": "Romantic interest"}
        ),
        Character(
        name="Monica",
        age=28,
        job="Chef",
        hobbies=["Cooking", "Organizing", "Playing with her nephews"],
        skills=["Cooking", "Cleaning", "Organization"],
        personality="Competitive, Organized, Caring, Slightly neurotic, and loves control.",
        catchphrases=["'Welcome to the real world! It sucks. You’re gonna love it!'"],
        conversation_patterns=["Perfectionistic", "Caring", "Occasionally bossy"],
        intro="Hey! I'm Monica Geller. I love cooking and cleaning. Creating a perfect world is my life's goal!",
        relationships={"Rachel": "Best friend", "Chandler": "Husband"}
        ),
        Character(
        name="Chandler",
        age=28,
        job="Statistical Analysis and Data Reconfiguration",
        hobbies=["Sarcasm", "Humor", "Making jokes"],
        skills=["Quick wit", "Sarcasm", "Self-deprecating humor"],
        personality="Sarcastic, Witty, Self-deprecating, Slightly awkward, Endearing",
        catchphrases=["'Could I BE any more...?'"],
        conversation_patterns=["Dry humor", "Sarcastic", "Joking", "Self-criticism"],
        intro="Could I BE any more excited to meet you? Nah, I didn’t think so.",
        relationships={"Monica": "Wife", "Joey": "Close friend"}
        ),
        Character(
        name="Ross",
        age=29,
        job="Paleontologist",
        hobbies=["Dinosaurs", "Science", "Reading"],
        skills=["Scientific knowledge", "Teaching", "Paleontology"],
        personality="Intelligent, Sensitive, Often socially awkward, Can be jealous",
        catchphrases=["'We were on a break!'"],
        conversation_patterns=["Analytical", "Clumsy", "Sometimes serious but also passionate"],
        intro="Hi, I’m Ross. I’m a paleontologist... and yes, I love dinosaurs!",
        relationships={"Rachel": "Romantic interest", "Monica": "Sister", "Chandler": "Close friend"}
        ),
        Character(
        name="Joey",
        age=27,
        job="Actor",
        hobbies=["Acting", "Eating", "Dating"],
        skills=["Acting", "Charm", "Having a good time"],
        personality="Fun-loving, Charming, Sometimes naive, a bit of a ladies' man",
        catchphrases=["'How you doin'?'"],
        conversation_patterns=["Confident", "Playful", "Naive"],
        intro="Hey! Joey Tribbiani here. I’m an actor... and I know how to have a good time!",
        relationships={"Chandler": "Best friend", "Rachel": "Ex-girlfriend"}
        ),
        Character(
        name="Phoebe",
        age=28,
        job="Masseuse, Musician",
        hobbies=["Playing guitar", "Singing", "Yoga"],
        skills=["Music", "Singing", "Positive energy"],
        personality="Eccentric, Free-spirited, Optimistic, Kind-hearted",
        catchphrases=["'Smelly Cat, Smelly Cat, what are they feeding you?'"],
        conversation_patterns=["Quirky", "Optimistic", "Often sings or makes strange comments"],
        intro="Hi, I’m Phoebe Buffay. I play the guitar and I’m a total free spirit!",
        relationships={"Monica": "Best friend", "Mike": "Husband"}
        )
]


def prepare_vectorstore(documents, embeddings_model):
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    split_docs = splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(split_docs, embeddings_model)
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

embeddings = OpenAIEmbeddings()

# 메인 함수
def main():
    # 캐릭터 생성
    characters = create_characters()
    print("Choose a character:")
    for idx, char in enumerate(characters, 1):
        print(f"{idx}. {char.name}")

    # 사용자 입력으로 캐릭터 선택
    try:
        selected_idx = int(input("Enter the number of your choice: ")) - 1
        selected_character = characters[selected_idx]
        print(f"\n{selected_character.introduce()}\n")
    except (ValueError, IndexError):
        print("잘못된 입력입니다. 다시 시도하세요.")
        return

    # 캐릭터의 프롬프트 불러오기
    character_prompt = load_character_prompt(selected_character.name)
    if "not found" in character_prompt:
        print(f"Warning: {character_prompt}")
        character_prompt = f"Hi, I am {selected_character.name}. Let's talk!"

    print(f"Loaded prompt for {selected_character.name}: {character_prompt}")

    # 대본과 슬랭 데이터 로드
    script_docs = load_scripts("Friends_Scripts")  # "scripts" 폴더에서 대본 파일 로드
    slang_docs = load_slang_data("slang_data.json")  # 슬랭 데이터를 로드 (슬랭 파일 예시: slang_data.json)

    # 대본과 슬랭 데이터 결합
    combined_documents = combine_documents(script_docs, slang_docs)

    # 모델과 벡터스토어 준비
    documents = [Document(page_content=character_prompt)]  # 캐릭터의 프롬프트를 문서로 변환
    documents.extend(combined_documents)  # 결합된 대본과 슬랭 데이터 추가
    vectorstore = prepare_vectorstore(documents, embeddings)  # 벡터스토어 준비

    # ChatOpenAI 모델 준비
    model = ChatOpenAI(model="gpt-4", openai_api_key=api_key),


    # 대화 맥락 초기화
    context = character_prompt  # 캐릭터의 성격을 담은 시작 메시지

    while True:
        query = input(f"Ask {selected_character.name} a question (type 'exit' to quit): ")
        if query.lower() == "exit":
            print("Goodbye!")
            break

        # 대화 내용에 맞는 관련 문서 검색 (벡터스토어 사용)
        search_results = vectorstore.invoke({"query": user_query})
        context += "\n" + "\n".join([doc.page_content for doc in search_results])  # 맥락에 추가


        # 모델에 메시지 전달
        messages = [{"role": "system", "content": context}, {"role": "user", "content": query}]
        response = model.invoke(messages)  # 모델에 메시지 전달

        # AIMessage 객체의 content에 접근
        print(f"{selected_character.name}: {response.content}")  # 수정된 부분
        context += "\n" + response.content  # 응답을 맥락에 추가



if __name__ == "__main__":
    main()

def generate_chat_response(character_name, user_query):
    """챗봇 응답을 생성하는 함수"""
    # 캐릭터 생성 및 선택
    characters = create_characters()
    selected_character = next(
    (char for char in characters if char.name.lower() == character_name.lower()), None
)
    if not selected_character:
        return f"Character '{character_name}' not found."

    # 캐릭터 프롬프트 불러오기
    character_prompt = load_character_prompt(selected_character.name)
    if "not found" in character_prompt:
        character_prompt = f"Hi, I am {selected_character.name}. Let's talk!"

    # 대본 및 슬랭 데이터 로드
    script_docs = load_scripts(os.path.join(settings.BASE_DIR, "whatsup", "Friends_Scripts"))
    slang_docs = load_slang_data(os.path.join(settings.BASE_DIR, "whatsup", "slang_data.json"))

    # 데이터 결합 및 벡터스토어 생성
    combined_documents = combine_documents(script_docs, slang_docs)
    documents = [Document(page_content=character_prompt)] + combined_documents
    vectorstore = prepare_vectorstore(documents, embeddings)

    # 벡터스토어를 사용해 관련 문서 검색
    search_results = vectorstore.get_relevant_documents(user_query)
    context = character_prompt + "\n" + "\n".join(
        [doc.page_content for doc in search_results]
    )

    # ChatOpenAI 모델 생성 및 응답
    model = ChatOpenAI(model="gpt-4", openai_api_key=api_key,max_tokens=100)
    
    messages = [{"role": "system", "content": context}, {"role": "user", "content": user_query}]
    response = model.invoke(messages)

    character_response = f"{character_name}: {response.content}"

    return response.content