class Inference:
    def __init__(self, skills) -> None:
        print(skills)
        skills[0] += 0.05
        skills[1] -= 0.015
        skills[2] += 0.025
        skills[3] += 0.02
        skills[4] -= 0.13
        skills[5] += 0.05

        self.inf_skills= {
            "매력": 90,
            "신뢰도": 70,
            "리더십": 80,            
            "지능": 85,
            "피지컬": 75, 
            "예술": 95,
        }

        self.result_info = """
                <style>
                    p { line-height: 140%; }  /* 🔹 줄 간격 140% 설정 */
                </style>
                <p><b>피지컬:</b> 신체적 능력과 활동적인 역량</p>
                <p><b>예술:</b> 창의적 감각과 표현력을 바탕으로 한 미적 감성</p>
                <p><b>매력:</b> 사람을 끌어당기는 호감과 사회적 영향력</p>
                <p><b>신뢰도:</b> 믿음을 주고 신뢰를 형성하는 안정적인 성향</p>
                <p><b>리더십:</b> 조직을 이끌고 조율하는 능력과 지도력</p>
                <p><b>지능:</b> 논리적 사고와 문제 해결 능력을 포함한 인지적 역량</p>
                """
        self.careers_info = """
                    <style>
                        p {{ 
                            line-height: 140%;
                            text-align: center;
                        }}
                        .title {{ font-size: 26px; }}  /* 🥇 금메달 */
                        .gold {{ font-size: 24px; }}  /* 🥇 금메달 */
                        .silver {{ font-size: 20px; }} /* 🥈 은메달 */
                        .bronze {{ font-size: 18px; }} /* 🥉 동메달 */
                    </style>
                    <p class="title"><b>🔥 추천 직업 🔥</b></p>
                    <p class="gold">🥇 <b>{}점 : {}</b></p>
                    <p class="silver">🥈 <b>{}점 </b>: {}</p>
                    <p class="bronze">🥉 <b>{}점 </b>: {}</p>
                """
        
        self.animals_info = """
                    <style>
                        p {{ 
                            line-height: 140%;
                            text-align: center;
                        }}
                        .title {{ font-size: 26px; }}  /* 🥇 금메달 */
                        .gold {{ font-size: 24px; }}  /* 🥇 금메달 */
                        .silver {{ font-size: 20px; }} /* 🥈 은메달 */
                        .bronze {{ font-size: 18px; }} /* 🥉 동메달 */
                    </style>
                    <p class="title"><b>나와 닮은 동물</b></p>
                    <p class="gold">🥇 <b>{}점 : {}</b></p>
                    <p class="silver">🥈 <b>{}점 </b>: {}</p>
                    <p class="bronze">🥉 <b>{}점 </b>: {}</p>
                """

        for l, v in zip(["리더십", "매력", "신뢰도", "피지컬", "예술", "지능"], skills):
            # default_point = random.randint(40, 60)
            self.inf_skills[l] = min(v*450, 100)

    def calc_values(self):
        self.careers = {
            # 🎭 예술 & 창작 직군 (매력 & 예술 최우선, 신뢰도 & 피지컬 낮음)
            "🎭 배우, 모델, 인플루언서": self.inf_skills["매력"] * 4.8 + self.inf_skills["예술"] * 3.5 + self.inf_skills["신뢰도"] * 1.0 + self.inf_skills["리더십"] * 0.1 + self.inf_skills["지능"] * 0.1 + self.inf_skills["피지컬"] * 0.5,
            "🎨 디자이너, 일러스트레이터, 화가": self.inf_skills["매력"] * 0.5 + self.inf_skills["예술"] * 7.1 + self.inf_skills["신뢰도"] * 2.25 + self.inf_skills["리더십"] * 0.15 + self.inf_skills["지능"] * 0.1 + self.inf_skills["피지컬"] * 0.3,
            "🎤 가수, 성우, 연예인": self.inf_skills["매력"] *4.3 + self.inf_skills["예술"] * 3.7 + self.inf_skills["신뢰도"] * 1.0 + self.inf_skills["리더십"] * 0.1 + self.inf_skills["지능"] * 0.1 + self.inf_skills["피지컬"] * 0.8,

            # 💼 경영 & 리더십 직군 (리더십 & 신뢰도 최우선, 예술 & 피지컬 낮음)
            "📢 CEO, 정치가, 경영자": self.inf_skills["매력"] * 0.3 + self.inf_skills["예술"] * 0.05 + self.inf_skills["신뢰도"] * 0.8 + self.inf_skills["리더십"] * 4.0 + self.inf_skills["지능"] * 4.8 + self.inf_skills["피지컬"] * 0.05,
            "📊 마케터, 광고기획자": self.inf_skills["매력"] * 1.5 + self.inf_skills["예술"] * 3.5 + self.inf_skills["신뢰도"] * 2.0 + self.inf_skills["리더십"] * 0.5 + self.inf_skills["지능"] * 2.0 + self.inf_skills["피지컬"] * 0.5,
            "🏛️ 외교관, 공무원, 행정가": self.inf_skills["매력"] * 0.15 + self.inf_skills["예술"] * 0.15 + self.inf_skills["신뢰도"] * 4.5 + self.inf_skills["리더십"] * 2.0 + self.inf_skills["지능"] * 3.0 + self.inf_skills["피지컬"] * 0.2,

            # 🏋️‍♂️ 스포츠 & 육체 직군 (피지컬 최우선, 지능 & 예술 낮음)
            "⚽ 운동선수, 트레이너": self.inf_skills["매력"] * 1.5 + self.inf_skills["예술"] * 0.1 + self.inf_skills["신뢰도"] * 0.3 + self.inf_skills["리더십"] * 1.0 + self.inf_skills["지능"] * 0.1 + self.inf_skills["피지컬"] * 7.0,
            "🚔 경찰, 군인, 소방관": self.inf_skills["매력"] * 0.1 + self.inf_skills["예술"] * 0.1 + self.inf_skills["신뢰도"] * 2.0 + self.inf_skills["리더십"] * 1.1 + self.inf_skills["지능"] * 1.2 + self.inf_skills["피지컬"] * 5.5,
            "🚀 파일럿, 레이서": self.inf_skills["매력"] * 1.0 + self.inf_skills["예술"] * 1.0 + self.inf_skills["신뢰도"] * 1.7 + self.inf_skills["리더십"] * 1.5 + self.inf_skills["지능"] * 0.8 + self.inf_skills["피지컬"] * 4.0,

            # 🧠 학문 & 기술 직군 (지능 최우선, 피지컬 & 예술 낮음)
            "🔬 과학자, 교수, 연구원": self.inf_skills["매력"] * 0.15 + self.inf_skills["예술"] * 0.05 + self.inf_skills["신뢰도"] * 1.5 + self.inf_skills["리더십"] * 1.4 + self.inf_skills["지능"] * 6.0 + self.inf_skills["피지컬"] * 0.4,
            "💻 프로그래머, 데이터 과학자": self.inf_skills["매력"] * 0.3 + self.inf_skills["예술"] * 1.2 + self.inf_skills["신뢰도"] * 1.0 + self.inf_skills["리더십"] * 0.3 + self.inf_skills["지능"] * 7.0 + self.inf_skills["피지컬"] * 0.2,
            "⚖️ 변호사, 판사": self.inf_skills["매력"] * 0.7 + self.inf_skills["예술"] * 0.2 + self.inf_skills["신뢰도"] * 4.0 + self.inf_skills["리더십"] * 1.0 + self.inf_skills["지능"] * 4.0 + self.inf_skills["피지컬"] * 0.1,

            # 🌍 서비스 & 커뮤니케이션 직군 (매력 & 신뢰도 최우선, 피지컬 낮음)
            "🎙️ 기자, 아나운서, 방송인": self.inf_skills["매력"] * 3.5 + self.inf_skills["예술"] * 0.5 + self.inf_skills["신뢰도"] * 3.5 + self.inf_skills["리더십"] * 0.5 + self.inf_skills["지능"] * 1.5 + self.inf_skills["피지컬"] * 0.5,
            "🛫 호텔리어, 승무원, 바텐더": self.inf_skills["매력"] * 6.0 + self.inf_skills["예술"] * 0.6 + self.inf_skills["신뢰도"] * 1.5 + self.inf_skills["리더십"] * 0.5 + self.inf_skills["지능"] * 0.4 + self.inf_skills["피지컬"] * 1.0,
        }

        self.animal = {
            # 🦁 리더십 & 피지컬이 강한 동물
            "🐅 호랑이": self.inf_skills["매력"] * 0.8 + self.inf_skills["예술"] * 0.4 + self.inf_skills["신뢰도"] * 1.2 + self.inf_skills["리더십"] * 4.0 + self.inf_skills["지능"] * 0.5 + self.inf_skills["피지컬"] * 3.1,
            "🦁 사자": self.inf_skills["매력"] * 1.5 + self.inf_skills["예술"] * 0.3 + self.inf_skills["신뢰도"] * 2.0 + self.inf_skills["리더십"] * 4.5 + self.inf_skills["지능"] * 0.3 + self.inf_skills["피지컬"] * 1.4,
            "🐺 늑대": self.inf_skills["매력"] * 1.2 + self.inf_skills["예술"] * 0.4 + self.inf_skills["신뢰도"] * 2.5 + self.inf_skills["리더십"] * 3.5 + self.inf_skills["지능"] * 1.0 + self.inf_skills["피지컬"] * 1.4,

            # 🦉 지능이 높은 동물 (인기 있는 동물로 변경)
            "🦉 올빼미": self.inf_skills["매력"] * 0.5 + self.inf_skills["예술"] * 0.3 + self.inf_skills["신뢰도"] * 1.5 + self.inf_skills["리더십"] * 1.0 + self.inf_skills["지능"] * 5.5 + self.inf_skills["피지컬"] * 1.2,
            "🐬 돌고래": self.inf_skills["매력"] * 1.0 + self.inf_skills["예술"] * 1.5 + self.inf_skills["신뢰도"] * 1.0 + self.inf_skills["리더십"] * 1.0 + self.inf_skills["지능"] * 4.5 + self.inf_skills["피지컬"] * 1.0,
            "🐱 고양이": self.inf_skills["매력"] * 3.5 + self.inf_skills["예술"] * 1.0 + self.inf_skills["신뢰도"] * 1.0 + self.inf_skills["리더십"] * 0.5 + self.inf_skills["지능"] * 3.0 + self.inf_skills["피지컬"] * 1.0,

            # 🦜 매력과 예술성이 높은 동물
            "🦚 공작새": self.inf_skills["매력"] * 5.0 + self.inf_skills["예술"] * 4.5 + self.inf_skills["신뢰도"] * 0.2 + self.inf_skills["리더십"] * 0.1 + self.inf_skills["지능"] * 0.1 + self.inf_skills["피지컬"] * 0.1,
            "🦜 앵무새": self.inf_skills["매력"] * 4.5 + self.inf_skills["예술"] * 3.5 + self.inf_skills["신뢰도"] * 1.0 + self.inf_skills["리더십"] * 0.5 + self.inf_skills["지능"] * 0.5 + self.inf_skills["피지컬"] * 0.0,
            "🦋 나비": self.inf_skills["매력"] * 6.0 + self.inf_skills["예술"] * 3.0 + self.inf_skills["신뢰도"] * 0.3 + self.inf_skills["리더십"] * 0.2 + self.inf_skills["지능"] * 0.3 + self.inf_skills["피지컬"] * 0.2,

            # 🐕 신뢰도가 높은 동물
            "🐶 강아지": self.inf_skills["매력"] * 2.5 + self.inf_skills["예술"] * 0.5 + self.inf_skills["신뢰도"] * 4.0 + self.inf_skills["리더십"] * 1.0 + self.inf_skills["지능"] * 1.5 + self.inf_skills["피지컬"] * 0.5,
            "🐘 코끼리": self.inf_skills["매력"] * 0.5 + self.inf_skills["예술"] * 0.2 + self.inf_skills["신뢰도"] * 2.5 + self.inf_skills["리더십"] * 1.5 + self.inf_skills["지능"] * 1.8 + self.inf_skills["피지컬"] * 3.5,
            "🐴 말": self.inf_skills["매력"] * 1.5 + self.inf_skills["예술"] * 0.5 + self.inf_skills["신뢰도"] * 4.5 + self.inf_skills["리더십"] * 2.0 + self.inf_skills["지능"] * 1.0 + self.inf_skills["피지컬"] * 0.5,

            # 🦅 피지컬이 뛰어난 동물
            "🦅 독수리": self.inf_skills["매력"] * 1.0 + self.inf_skills["예술"] * 0.5 + self.inf_skills["신뢰도"] * 2.0 + self.inf_skills["리더십"] * 2.5 + self.inf_skills["지능"] * 0.8 + self.inf_skills["피지컬"] * 3.2,
            "🐻 곰": self.inf_skills["매력"] * 1.2 + self.inf_skills["예술"] * 0.5 + self.inf_skills["신뢰도"] * 2.0 + self.inf_skills["리더십"] * 1.5 + self.inf_skills["지능"] * 1.8 + self.inf_skills["피지컬"] * 3.0,
            "🐢 거북이": self.inf_skills["매력"] * 1.0 + self.inf_skills["예술"] * 0.2 + self.inf_skills["신뢰도"] * 4.5 + self.inf_skills["리더십"] * 1.5 + self.inf_skills["지능"] * 1.5 + self.inf_skills["피지컬"] * 1.3,

            # 🌍 균형 잡힌 동물 (귀엽고 인기 많은 동물 포함)
            "🐼 판다": self.inf_skills["매력"] * 3.5 + self.inf_skills["예술"] * 1.5 + self.inf_skills["신뢰도"] * 2.0 + self.inf_skills["리더십"] * 1.0 + self.inf_skills["지능"] * 1.0 + self.inf_skills["피지컬"] * 1.0,
            "🦊 여우": self.inf_skills["매력"] * 4.5 + self.inf_skills["예술"] * 2.0 + self.inf_skills["신뢰도"] * 0.0 + self.inf_skills["리더십"] * 1.0 + self.inf_skills["지능"] * 2.5 + self.inf_skills["피지컬"] * 0.5,
            "🐿️ 다람쥐": self.inf_skills["매력"] * 3.0 + self.inf_skills["예술"] * 2.5 + self.inf_skills["신뢰도"] * 1.0 + self.inf_skills["리더십"] * 0.5 + self.inf_skills["지능"] * 2.5 + self.inf_skills["피지컬"] * 0.5,
        }

    def infer_careers(self):
        self.calc_values()
        sorted_careers = sorted(self.careers.items(), key=lambda x: x[1], reverse=True)
        sorted_animals = sorted(self.animal.items(), key=lambda x: x[1], reverse=True)
        careers_scores = [career[1]/10 for career in sorted_careers]
        animals_scores = [animals[1]/10 for animals in sorted_animals]
        careers = []
        animals = []

        for i in range(3) :
            careers.append(sorted_careers[i][0])
            animals.append(sorted_animals[i][0])

        return careers, animals, careers_scores, animals_scores, self.result_info, self.careers_info, self.animals_info

