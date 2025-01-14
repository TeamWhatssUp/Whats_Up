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

embeddings = OpenAIEmbeddings()


def format_character_name(character_name):
    """캐릭터 이름을 파일명에 맞게 포맷팅"""
    return character_name.strip().lower().replace(" ", "_") + "_prompt.txt"


def load_character_prompt(character_name):
    """캐릭터에 맞는 프롬프트를 파일에서 읽어오거나 기본값 반환"""
    try:
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "prompts",
            format_character_name(character_name),
        )
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
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


def prepare_vectorstore(documents):
    """벡터스토어 준비"""
    splitter = CharacterTextSplitter(chunk_size=900, chunk_overlap=90)
    split_docs = splitter.split_documents(documents)
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})


# 캐릭터 클래스 정의
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


def generate_chat_response(character_name, user_query, summary_threshold=500):
    """챗봇 응답을 생성하는 함수"""
    # 캐릭터 생성 및 선택
    characters = create_characters()
    selected_character = next(
        (char for char in characters if char.name.lower() == character_name.lower()), None
    )
    if not selected_character:
        return f"Character '{character_name}' not found."

    # 캐릭터 프롬프트 로드
    character_prompt = load_character_prompt(selected_character.name)

    # 캐릭터 프롬프트 생성 (캐릭터 클래스 포함)
    character_prompt = f"""
    You are {selected_character.name}, a {selected_character.job}. 
    Your personality: {selected_character.personality}.
    Your catchphrases: {" | ".join(selected_character.catchphrases)}.
    Your hobbies: {", ".join(selected_character.hobbies)}.
    You are having a conversation with a friend. Be {", ".join(selected_character.conversation_patterns)}.
    """

    # 대본 데이터 로드
    script_docs = load_scripts(os.path.join(settings.BASE_DIR, "whatsup", "Friends_Scripts"))

    # 벡터스토어 생성
    documents = [Document(page_content=character_prompt)] + script_docs
    vectorstore = prepare_vectorstore(documents)

    # 벡터스토어 검색
    search_results = vectorstore.get_relevant_documents(user_query)[:2]
    context = character_prompt + "\n" + "\n".join(doc.page_content for doc in search_results)

    # ChatOpenAI 모델 생성 및 호출
    model = ChatOpenAI(model="gpt-4", openai_api_key=api_key, max_tokens=100,temperature=0,)
    messages = [{"role": "system", "content": context}, {"role": "user", "content": user_query}]
    response = model.invoke(messages)

    return response.content

