from PyQt5.QtCore import QObject, QThread, pyqtSignal
import os
import openai
import base64

def encode_image():
    image_path = '/home/willtek/Bootcamp/application/captured_frame.jpg'
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

class ApiThread(QThread):
    finished_signal = pyqtSignal(dict)  # 완료 신호 (응답 데이터 전달)

    def __init__(self, skills) -> None:
        super().__init__()
        self.skills = skills

    def run(self):
        try:            
            # key = os.getenv("OPENAI_API_KEY")
            # client = openai.OpenAI(api_key=key)
            
            # text = '모든 능력치는 100점 만점 기준이야. 매력이 80점, 신뢰도가 60점, 리더십이 70점, 지능이 75점, 피지컬이 85점, 예술이 55점이고 이 사진 속 인물의 특징을 설명해줘'
            # encoded_image = encode_image()

            # api_response = None
            # resp = client.chat.completions.create(
            #     model='gpt-4o',  # 'gpt4o-mini' 대신 'gpt-4-turbo' 사용 추천
            #     messages=[
            #         {
            #             'role': 'user', 
            #             'content': [
            #                 {
            #                     "type" : "text",
            #                     "text" : text
            #                 },
            #                 # {
            #                 #     "type" : "image_url",
            #                 #     "image_url" : {
            #                 #     "url": f"data:image/jpeg;base64,{encoded_image}",
            #                 #     },
            #                 # },

            #             ],
            #         }
            #     ],
            # )
            # print(resp.choices[0].message.content)
            
            # self.finished_signal.emit({"content": resp.choices[0].message.content})
            print("hi")
            self.finished_signal.emit({"content": 'hi'})
        except Exception as e:
            self.finished_signal.emit({"error": str(e)})  # 에러 발생 시