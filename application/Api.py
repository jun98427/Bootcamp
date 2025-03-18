from PyQt5.QtCore import QThread, pyqtSignal
import os
import openai


class ApiThread(QThread):
    finished_signal = pyqtSignal(dict)  # 완료 신호 (응답 데이터 전달)

    def run(self):
        try:
            print("check")
            query = '매력이 80점, 신뢰도가 60점, 리더십이 70점, 지능이 75점, 피지컬이 85점, 예술이 55점인 한국 연예인을 한명만 한 단어로 추천해줘'
            key = os.getenv("OPENAI_API_KEY")
            client = openai.OpenAI(api_key=key)
            print(key)
            api_response = None
            resp = client.chat.completions.create(
                model='gpt-4o',  # 'gpt4o-mini' 대신 'gpt-4-turbo' 사용 추천
                messages=[{'role': 'user', 'content': query}]
            )
            print("tmp")
            print(resp.choices[0].message.content)
            # time.sleep(1)  # 테스트용 딜레이
            # response = requests.get("http://127.0.0.1:8000/")  # 예제 API
            # data = {
            # "매력": random.randint(50,100),
            # "신뢰도": random.randint(50,100),
            # "리더십": random.randint(50,100),            
            # "지능": random.randint(50,100),
            # "피지컬": random.randint(50,100), 
            # "예술": random.randint(50,100),
            # }
            # print(data)

            self.finished_signal.emit(api_response)  # 결과 전달
        except Exception as e:
            self.finished_signal.emit({"error": str(e)})  # 에러 발생 시