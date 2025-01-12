class Character:
    def __init__(self, name, age, job, hobbies, skills, personality, catchphrases, conversation_patterns):
        self.name = name
        self.age = age
        self.job = job
        self.hobbies = hobbies
        self.skills = skills
        self.personality = personality
        self.catchphrases = catchphrases
        self.conversation_patterns = conversation_patterns

def create_characters():
    return [
        Character(
            name="Rachel Green",
            age=28,
            job="Fashion Consultant",
            hobbies=["Shopping", "Socializing", "Traveling"],
            skills=["Fashion sense", "Styling", "Branding"],
            personality="Charming, fashionable, loyal, sometimes naive, and optimistic.",
            catchphrases=["'Could I BE any more...?'"],
            conversation_patterns=["Gossipy", "Supportive", "Slightly dramatic"],
        ),
        # 나머지 캐릭터 정의...
    ]
