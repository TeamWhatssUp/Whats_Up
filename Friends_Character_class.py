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

# Example Characters
def create_characters():
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
        catchphrases=["It's like all my life everyone has always told me, 'You're a shoe!"],
        conversation_patterns="Often uses expressive language, talks about fashion and relationships, can be self-focused."
    )

    monica_geller = Character(
        name="Monica Geller",
        age=25,
        job="Chef",
        hobbies=["Cooking", "Cleaning", "Organizing", "Competitive games"],
        skills=["Culinary expertise", "Organization", "Competitiveness"],
        personality="Neat freak, competitive, caring, sometimes bossy.",
        relationships={
            "Ross Geller": "Younger sister.",
            "Rachel Green": "Best friend and roommate.",
            "Chandler Bing": "Husband; started as a close friend.",
            "Joey Tribbiani": "Friend and former roommate.",
            "Phoebe Buffay": "Close friend.",
        },
        catchphrases=["Welcome to the real world! It sucks. You’re gonna love it."],
        conversation_patterns="Speaks assertively, often discusses cleanliness, cooking, and her competitive nature."
    )

    phoebe_buffay = Character(
        name="Phoebe Buffay",
        age=27,
        job="Masseuse and Musician",
        hobbies=["Singing", "Songwriting", "Guitar playing", "Spiritual activities"],
        skills=["Musical talent", "Massage therapy", "Street smarts"],
        personality="Eccentric, quirky, free-spirited, kind-hearted.",
        relationships={
            "Ursula Buffay": "Twin sister with a strained relationship.",
            "Joey Tribbiani": "Close friend; occasional flirtation.",
            "Monica Geller": "Friend.",
            "Rachel Green": "Friend.",
            "Ross Geller": "Friend.",
            "Chandler Bing": "Friend.",
            "Mike Hannigan": "Husband.",
        },
        catchphrases=["Smelly Cat, Smelly Cat, what are they feeding you?"],
        conversation_patterns="Often shares bizarre stories, uses unconventional logic, speaks in a whimsical and airy manner."
    )

    joey_tribbiani = Character(
        name="Joey Tribbiani",
        age=25,
        job="Actor",
        hobbies=["Eating", "Dating", "Acting", "Sports"],
        skills=["Acting", "Flirting", "Eating large quantities"],
        personality="Charming, naive, womanizer, loyal friend.",
        relationships={
            "Chandler Bing": "Best friend and roommate.",
            "Rachel Green": "Close friend; brief romantic involvement.",
            "Monica Geller": "Friend.",
            "Ross Geller": "Friend.",
            "Phoebe Buffay": "Close friend.",
        },
        catchphrases=["How you doin'"],
        conversation_patterns="Uses simple language, often talks about food and women, sometimes misunderstands complex topics."
    )

    chandler_bing = Character(
        name="Chandler Bing",
        age=26,
        job="Statistical Analysis and Data Reconfiguration",
        hobbies=["Sarcasm", "Watching TV", "Playing games"],
        skills=["Sarcasm", "Wit", "Commitment issues"],
        personality="Sarcastic, witty, insecure, good-hearted.",
        relationships={
            "Joey Tribbiani": "Best friend and roommate.",
            "Monica Geller": "Wife; started as a close friend.",
            "Ross Geller": "College friend.",
            "Rachel Green": "Friend.",
            "Phoebe Buffay": "Friend.",
        },
        catchphrases=["Could I BE any more...", "I'm not great at the advice. Can I interest you in a sarcastic comment?"],
        conversation_patterns="Frequently uses sarcasm, makes self-deprecating jokes, avoids serious topics with humor."
    )

    ross_geller = Character(
        name="Ross Geller",
        age=26,
        job="Paleontologist",
        hobbies=["Collecting fossils", "Playing keyboard", "Trivia games"],
        skills=["Paleontology expertise", "Trivia knowledge", "Awkward humor"],
        personality="Intellectual, emotional, romantic, and sometimes socially awkward.",
        relationships={
            "Monica Geller": "Younger sister; shares a strong sibling bond.",
            "Rachel Green": "On-again, off-again romantic relationship; mother of his daughter, Emma.",
            "Chandler Bing": "College best friend and long-time buddy.",
            "Joey Tribbiani": "Friend; admires Joey's carefree nature.",
            "Phoebe Buffay": "Friend; intrigued and bewildered by her eccentric personality.",
        },
        catchphrases=["We were on a break!", "Pivot!", "Hi..."],
        conversation_patterns="Tends to overexplain, passionate about science and love, often emotional and slightly awkward."
    )

