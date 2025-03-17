class Inference:
    def __init__(self, skills) -> None:
        skills[0] += 0.05
        skills[1] -= 0.03
        skills[2] += 0.02
        skills[3] += 0.02
        skills[4] -= 0.12
        skills[5] += 0.06
        self.skills= {}

        for l, v in zip(["리더십", "매력", "신뢰도", "피지컬", "예술", "지능"], skills):
            # default_point = random.randint(40, 60)
            self.skills[l] = min(v*450, 100)

    def calc_values(self):
        self.careers = {
            # 🎭 예술 & 창작 직군 (매력 & 예술 최우선, 신뢰도 & 피지컬 낮음)
            "🎭 배우, 모델, 인플루언서": self.skills["매력"] * 4.8 + self.skills["예술"] * 3.5 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.1 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 0.5,
            "🎨 디자이너, 일러스트레이터, 화가": self.skills["매력"] * 0.5 + self.skills["예술"] * 7.1 + self.skills["신뢰도"] * 2.25 + self.skills["리더십"] * 0.15 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 0.3,
            "🎤 가수, 성우, 연예인": self.skills["매력"] *4.3 + self.skills["예술"] * 3.7 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.1 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 0.8,

            # 💼 경영 & 리더십 직군 (리더십 & 신뢰도 최우선, 예술 & 피지컬 낮음)
            "📢 CEO, 정치가, 경영자": self.skills["매력"] * 0.3 + self.skills["예술"] * 0.05 + self.skills["신뢰도"] * 0.8 + self.skills["리더십"] * 4.0 + self.skills["지능"] * 4.8 + self.skills["피지컬"] * 0.05,
            "📊 마케터, 광고기획자": self.skills["매력"] * 1.5 + self.skills["예술"] * 3.5 + self.skills["신뢰도"] * 2.0 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 2.0 + self.skills["피지컬"] * 0.5,
            "🏛️ 외교관, 공무원, 행정가": self.skills["매력"] * 0.15 + self.skills["예술"] * 0.15 + self.skills["신뢰도"] * 4.5 + self.skills["리더십"] * 2.0 + self.skills["지능"] * 3.0 + self.skills["피지컬"] * 0.2,

            # 🏋️‍♂️ 스포츠 & 육체 직군 (피지컬 최우선, 지능 & 예술 낮음)
            "⚽ 운동선수, 트레이너": self.skills["매력"] * 1.5 + self.skills["예술"] * 0.1 + self.skills["신뢰도"] * 0.3 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 7.0,
            "🚔 경찰, 군인, 소방관": self.skills["매력"] * 0.1 + self.skills["예술"] * 0.1 + self.skills["신뢰도"] * 2.0 + self.skills["리더십"] * 1.1 + self.skills["지능"] * 1.2 + self.skills["피지컬"] * 5.5,
            "🚀 파일럿, 레이서": self.skills["매력"] * 1.0 + self.skills["예술"] * 1.0 + self.skills["신뢰도"] * 1.7 + self.skills["리더십"] * 1.5 + self.skills["지능"] * 0.8 + self.skills["피지컬"] * 4.0,

            # 🧠 학문 & 기술 직군 (지능 최우선, 피지컬 & 예술 낮음)
            "🔬 과학자, 교수, 연구원": self.skills["매력"] * 0.15 + self.skills["예술"] * 0.05 + self.skills["신뢰도"] * 1.5 + self.skills["리더십"] * 1.4 + self.skills["지능"] * 6.0 + self.skills["피지컬"] * 0.4,
            "💻 프로그래머, 데이터 과학자": self.skills["매력"] * 0.3 + self.skills["예술"] * 1.2 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.3 + self.skills["지능"] * 7.0 + self.skills["피지컬"] * 0.2,
            "⚖️ 변호사, 판사": self.skills["매력"] * 0.7 + self.skills["예술"] * 0.2 + self.skills["신뢰도"] * 4.0 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 4.0 + self.skills["피지컬"] * 0.1,

            # 🌍 서비스 & 커뮤니케이션 직군 (매력 & 신뢰도 최우선, 피지컬 낮음)
            "🎙️ 기자, 아나운서, 방송인": self.skills["매력"] * 3.5 + self.skills["예술"] * 0.5 + self.skills["신뢰도"] * 3.5 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 1.5 + self.skills["피지컬"] * 0.5,
            "🛫 호텔리어, 승무원, 바텐더": self.skills["매력"] * 6.0 + self.skills["예술"] * 0.6 + self.skills["신뢰도"] * 1.5 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 0.4 + self.skills["피지컬"] * 1.0,
        }

        self.animal = {
            # 🦁 리더십 & 피지컬이 강한 동물
            "🐅 호랑이": self.skills["매력"] * 0.8 + self.skills["예술"] * 0.4 + self.skills["신뢰도"] * 1.2 + self.skills["리더십"] * 4.0 + self.skills["지능"] * 0.5 + self.skills["피지컬"] * 3.1,
            "🦁 사자": self.skills["매력"] * 1.5 + self.skills["예술"] * 0.3 + self.skills["신뢰도"] * 2.0 + self.skills["리더십"] * 4.5 + self.skills["지능"] * 0.3 + self.skills["피지컬"] * 1.4,
            "🐺 늑대": self.skills["매력"] * 1.2 + self.skills["예술"] * 0.4 + self.skills["신뢰도"] * 2.5 + self.skills["리더십"] * 3.5 + self.skills["지능"] * 1.0 + self.skills["피지컬"] * 1.4,

            # 🦉 지능이 높은 동물 (인기 있는 동물로 변경)
            "🦉 올빼미": self.skills["매력"] * 0.5 + self.skills["예술"] * 0.3 + self.skills["신뢰도"] * 1.5 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 5.5 + self.skills["피지컬"] * 1.2,
            "🐬 돌고래": self.skills["매력"] * 1.0 + self.skills["예술"] * 1.5 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 4.5 + self.skills["피지컬"] * 1.0,
            "🐱 고양이": self.skills["매력"] * 3.5 + self.skills["예술"] * 1.0 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 3.0 + self.skills["피지컬"] * 1.0,

            # 🦜 매력과 예술성이 높은 동물
            "🦚 공작새": self.skills["매력"] * 5.0 + self.skills["예술"] * 4.5 + self.skills["신뢰도"] * 0.2 + self.skills["리더십"] * 0.1 + self.skills["지능"] * 0.1 + self.skills["피지컬"] * 0.1,
            "🦜 앵무새": self.skills["매력"] * 4.5 + self.skills["예술"] * 3.5 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 0.5 + self.skills["피지컬"] * 0.0,
            "🦋 나비": self.skills["매력"] * 6.0 + self.skills["예술"] * 3.0 + self.skills["신뢰도"] * 0.3 + self.skills["리더십"] * 0.2 + self.skills["지능"] * 0.3 + self.skills["피지컬"] * 0.2,

            # 🐕 신뢰도가 높은 동물
            "🐶 강아지": self.skills["매력"] * 2.5 + self.skills["예술"] * 0.5 + self.skills["신뢰도"] * 4.0 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 1.5 + self.skills["피지컬"] * 0.5,
            "🐘 코끼리": self.skills["매력"] * 0.5 + self.skills["예술"] * 0.2 + self.skills["신뢰도"] * 2.5 + self.skills["리더십"] * 1.5 + self.skills["지능"] * 1.8 + self.skills["피지컬"] * 3.5,
            "🐴 말": self.skills["매력"] * 1.5 + self.skills["예술"] * 0.5 + self.skills["신뢰도"] * 4.5 + self.skills["리더십"] * 2.0 + self.skills["지능"] * 1.0 + self.skills["피지컬"] * 0.5,

            # 🦅 피지컬이 뛰어난 동물
            "🦅 독수리": self.skills["매력"] * 1.0 + self.skills["예술"] * 0.5 + self.skills["신뢰도"] * 2.0 + self.skills["리더십"] * 2.5 + self.skills["지능"] * 0.8 + self.skills["피지컬"] * 3.2,
            "🐻 곰": self.skills["매력"] * 1.2 + self.skills["예술"] * 0.5 + self.skills["신뢰도"] * 2.0 + self.skills["리더십"] * 1.5 + self.skills["지능"] * 1.8 + self.skills["피지컬"] * 3.0,
            "🐢 거북이": self.skills["매력"] * 1.0 + self.skills["예술"] * 0.2 + self.skills["신뢰도"] * 4.5 + self.skills["리더십"] * 1.5 + self.skills["지능"] * 1.5 + self.skills["피지컬"] * 1.3,

            # 🌍 균형 잡힌 동물 (귀엽고 인기 많은 동물 포함)
            "🐼 판다": self.skills["매력"] * 3.5 + self.skills["예술"] * 1.5 + self.skills["신뢰도"] * 2.0 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 1.0 + self.skills["피지컬"] * 1.0,
            "🦊 여우": self.skills["매력"] * 4.5 + self.skills["예술"] * 2.0 + self.skills["신뢰도"] * 0.0 + self.skills["리더십"] * 1.0 + self.skills["지능"] * 2.5 + self.skills["피지컬"] * 0.5,
            "🐿️ 다람쥐": self.skills["매력"] * 3.0 + self.skills["예술"] * 2.5 + self.skills["신뢰도"] * 1.0 + self.skills["리더십"] * 0.5 + self.skills["지능"] * 2.5 + self.skills["피지컬"] * 0.5,
        }

    def infer_careers(self):
        self.calc_values()
        sorted_careers = sorted(self.careers.items(), key=lambda x: x[1], reverse=True)
        sorted_animals = sorted(self.animal.items(), key=lambda x: x[1], reverse=True)

        careers = []
        animals = []

        for i in range(3) :
            careers.append(sorted_careers[i][0])
            animals.append(sorted_animals[i][0])

        return careers, animals  

