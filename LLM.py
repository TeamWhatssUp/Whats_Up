import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
import faiss
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter
import json
from langdetect import detect

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("API 키가 .env 파일에 설정되어 있지 않습니다.")

# 모델 초기화
model = ChatOpenAI(model="gpt-4", openai_api_key=api_key)

# Character 클래스 정의 (앞서 정의된 내용 그대로 사용)
class Character:
    def __init__(self, name, age, job, hobbies, skills, personality, relationships, catchphrases, conversation_patterns):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies
        self.skills = skills
        self.personality = personality
        self.relationships = relationships
        self.catchphrases = catchphrases
        self.conversation_patterns = conversation_patterns

    def make_comment(self):
        """Character introduces themselves in their own style, inviting the user to chat."""
        if self.name == "Rachel Green":
            return (
                f"안녕! 난 Rachel Green이야. 🎀 "
                f"패션이 내 인생이지, 그리고 쇼핑은 내 취미야. "
                f"가끔 내가 좀 자기중심적일 때도 있지만, 정말 caring한 사람이야. "
                f"혹시 연애 상담이 필요하거나, 패션에 대해 이야기하고 싶다면 나랑 대화해보는 거 어때? "
                f"내가 사랑하는 이야기를 나누면서 너의 이야기도 듣고 싶어. 😊"
            )
        elif self.name == "Monica Geller":
            return (
                f"안녕하세요! 저는 Monica Geller입니다. 🍳 "
                f"요리하는 걸 정말 사랑하고요, 솔직히 말해서 제가 제일 잘해요. "
                f"아, 청소나 정리도 완벽하게 할 수 있죠. "
                f"조금 지나치게 경쟁적일 수도 있지만, 그건 제가 목표에 얼마나 진심인지 보여주는 거예요! "
                f"누군가에게 멋진 조언이나 진솔한 대화를 원하면 저를 선택해주세요! "
                f"'{self.catchphrases[0]}' 이 말은 저와 잘 어울리죠?"
            )
        elif self.name == "Phoebe Buffay":
            return (
                f"안녕~ 난 Phoebe Buffay야! 🎸 "
                f"난 좀 특이하고 자유로운 영혼이야. 'Smelly Cat'이라는 노래 들어봤어? 그거 내가 만든 거야! "
                f"아주 재미있는 이야기들로 가득 찬 내 세계를 너랑 나누고 싶어. "
                f"스스로를 너무 심각하게 생각하지 않는 사람이 필요하다면, 내가 바로 그 사람이야. "
                f"우리 이야기해볼래? 'Smelly Cat~' 같이 불러도 좋고!"
            )
        elif self.name == "Joey Tribbiani":
            return (
                f"안녕, 난 Joey Tribbiani야. 🍕 "
                f"내 Catchphrase 알지? 'How you doin'?' 😏 "
                f"나는 간단한 게 좋아, 먹는 거, 연기하는 거, 데이트. "
                f"근데 난 정말 충실한 친구야. 누가 나한테 무슨 말을 해도 나는 그냥 솔직하게 말해. "
                f"우리 대화하면 웃기고 편안한 시간이 될 거야, 확실해!"
            )
        elif self.name == "Chandler Bing":
            return (
                f"Hey, 안녕! 난 Chandler Bing이야. 😂 "
                f"내가 뭘 잘하냐고? 물론 sarcasm이지! "
                f"내 직업에 대해서 물어보면 복잡하지만, 대화는 절대 재미없지 않아. "
                f"솔직히 말해서 내가 제일 웃긴 사람이라는 걸 알게 될 거야. "
                f"대화할 준비 됐어? 'Could I BE any more ready to chat?'"
            )
        elif self.name == "Ross Geller":
            return (
                f"안녕하세요, 저는 Dr. Ross Geller입니다. 🦖 "
                f"네, 저는 고생물학자예요. 공룡을 연구하죠. 그리고 아니요, 그건 지루하지 않아요! "
                f"제가 사랑과 과학에 대해 얘기하는 걸 좋아해요. 가끔 너무 논리적이거나 감정적일 수도 있지만, "
                f"대화를 나누다 보면 그게 저의 매력이라는 걸 알게 될 거예요. "
                f"혹시 제 말을 듣고 싶으신가요? 'We were on a break!' 이 문장에 대해 얘기해 봐요!"
            )
        else:
            return "Hello! I'm just another character from Friends. Wanna chat?"

    def __repr__(self):
        return f"Character({self.name}, {self.age}, {self.job})"

# 각 캐릭터 정의
rachel_green = Character(
    name="Rachel Green",
    age=24,
    job="Fashion Executive",
    hobbies=["Shopping", "Fashion", "Socializing"],
    skills=["Fashion sense", "Waitressing"],
    personality="Friendly, outgoing, sometimes self-centered but caring.",
    relationships={
        "Monica Geller": "Best friend from high school.",
        "Ross Geller": "On-again, off-again romantic relationship; father of her daughter, Emma.",
        "Joey Tribbiani": "Close friend; brief romantic involvement.",
        "Chandler Bing": "Friend.",
        "Phoebe Buffay": "Friend.",
    },
    catchphrases=["It's like all my life everyone has always told me, 'You're a shoe!'"],
    conversation_patterns="Often uses expressive language, talks about fashion and relationships, can be self-focused."
)

monica_geller = Character(
    name="Monica Geller",
    age=26,
    job="Chef",
    hobbies=["Cooking", "Cleaning", "Organizing"],
    skills=["Cooking", "Organizing", "Competing"],
    personality="Competitive, organized, caring.",
    relationships={
        "Rachel Green": "Best friend from high school.",
        "Ross Geller": "Brother.",
        "Joey Tribbiani": "Friend.",
        "Chandler Bing": "Husband.",
        "Phoebe Buffay": "Friend.",
    },
    catchphrases=["Welcome to the real world. It sucks. You’re gonna love it!"],
    conversation_patterns="Often talks about cooking and organizing, has a competitive streak."
)

phoebe_buffay = Character(
    name="Phoebe Buffay",
    age=27,
    job="Musician",
    hobbies=["Singing", "Songwriting", "Spirituality"],
    skills=["Singing", "Guitar", "Comedy"],
    personality="Free-spirited, quirky, funny.",
    relationships={
        "Monica Geller": "Best friend.",
        "Rachel Green": "Best friend.",
        "Joey Tribbiani": "Friend.",
        "Chandler Bing": "Friend.",
        "Ross Geller": "Friend.",
    },
    catchphrases=["Smelly Cat, Smelly Cat, what are they feeding you?"],
    conversation_patterns="Often talks about songs, spirituality, and quirky experiences."
)

joey_tribbiani = Character(
    name="Joey Tribbiani",
    age=28,
    job="Actor",
    hobbies=["Eating", "Acting", "Dating"],
    skills=["Acting", "Charm", "Loving"],
    personality="Simple, charming, loyal.",
    relationships={
        "Rachel Green": "Close friend; brief romantic involvement.",
        "Monica Geller": "Friend.",
        "Phoebe Buffay": "Friend.",
        "Chandler Bing": "Best friend.",
        "Ross Geller": "Friend.",
    },
    catchphrases=["How you doin'?"],
    conversation_patterns="Talks about food, acting, and relationships."
)

chandler_bing = Character(
    name="Chandler Bing",
    age=29,
    job="Statistical Analysis and Data Reconfiguration",
    hobbies=["Sarcasm", "Making jokes", "Friends"],
    skills=["Sarcasm", "Jokes", "Negotiation"],
    personality="Sarcastic, funny, self-deprecating.",
    relationships={
        "Monica Geller": "Wife.",
        "Rachel Green": "Friend.",
        "Phoebe Buffay": "Friend.",
        "Joey Tribbiani": "Best friend.",
        "Ross Geller": "Friend.",
    },
    catchphrases=["Could I BE any more..."],
    conversation_patterns="Uses sarcasm, often cracks jokes and references his job."
)

ross_geller = Character(
    name="Ross Geller",
    age=30,
    job="Paleontologist",
    hobbies=["Science", "Dinosaurs", "Paleontology"],
    skills=["Paleontology", "Teaching", "Science Trivia"],
    personality="Logical, passionate, sometimes emotional.",
    relationships={
        "Rachel Green": "Ex-wife, father of her daughter, Emma.",
        "Monica Geller": "Sister.",
        "Joey Tribbiani": "Friend.",
        "Chandler Bing": "Friend.",
        "Phoebe Buffay": "Friend.",
    },
    catchphrases=["We were on a break!"],
    conversation_patterns="Often talks about dinosaurs, science, and relationships."
)

# 캐릭터 목록
characters = [
    rachel_green,
    monica_geller,
    phoebe_buffay,
    joey_tribbiani,
    chandler_bing,
    ross_geller
]

# 캐릭터 선택
print("Choose a character:")
for idx, character in enumerate(characters, 1):
    print(f"{idx}. {character.name}")

# 사용자로부터 캐릭터 선택
selected_idx = int(input("Enter the number of your choice: ")) - 1
selected_character = characters[selected_idx]

# 캐릭터 소개 출력
print(f"\n{selected_character.make_comment()}\n")

# 대본 파일 로드 함수
def load_scripts(folder):
    documents = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append(Document(page_content=content))
    return documents

# 슬랭 데이터 로드
with open('slang_data.json', 'r', encoding='utf-8') as file:
    slang_data = json.load(file)

# 대본과 슬랭 데이터 결합
slang_docs = [Document(page_content=f"Term: {item['term']}\nDescription: {item['description']}") for item in slang_data]
all_docs = load_scripts("Friends_Scripts")
documents = all_docs + slang_docs

# 문서 분할 및 벡터스토어 처리
def split_documents(documents, chunk_size=500, chunk_overlap=50):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(documents)

split_docs = split_documents(documents)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = FAISS.from_documents(split_docs, embeddings)

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(llm=model, retriever=retriever, return_source_documents=True)

# 언어 감지 함수
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

# 사용자 입력 받기
while True:
    query = input(f"Ask {selected_character.name} a question (type 'exit' to quit): ")
    if query.lower() == 'exit':
        break

    lang = detect_language(query)
    try:
        print("\nGenerating response...\n")
        result = qa_chain({"query": query})
        answer = result.get('result', "Sorry, I couldn't find an answer.")
        print(f"{selected_character.name}: {answer}")
    except Exception as e:
        print(f"An error occurred: {e}")
