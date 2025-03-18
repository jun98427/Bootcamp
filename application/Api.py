from PyQt5.QtCore import QObject, QThread, pyqtSignal
import os
import openai
import json

# def encode_image():
#     image_path = '/home/willtek/Bootcamp/application/captured_frame.jpg'
#     with open(image_path, 'rb') as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

class ApiThread(QThread):
    finished_signal = pyqtSignal(dict)  # 완료 신호 (응답 데이터 전달)

    def __init__(self, celebrity) -> None:
        super().__init__()
        self.celebrity = celebrity

    def run(self):
        try:
            print("api : ", self.celebrity)            
            key = os.getenv("OPENAI_API_KEY")
            client = openai.OpenAI(api_key=key)
            
            text = '{} 가수면 대표곡을 배우면 대표작을 알려줘. json 형식으로 key 값은 제목과 년도로 보내줘'.format(self.celebrity)
            print("text ", text)
            # encoded_image = encode_image()

            resp = client.chat.completions.create(
                model='gpt-4o',  # 'gpt4o-mini' 대신 'gpt-4-turbo' 사용 추천
                messages=[
                    {
                        'role': 'user', 
                        'content': [
                            {
                                "type" : "text",
                                "text" : text
                            },
                        ],
                    }
                ],
            )
            print(resp.choices[0].message.content)

            # response_text = resp["choices"][0]["message"]["content"]
            # # res = json.loads(resp['choices'][0].message.content)
            # print('-----------------------')
            # print(response_text)

            self.finished_signal.emit({"content": resp.choices[0].message.content})
            # self.finished_signal.emit({"content": "hi"})
        except Exception as e:
            self.finished_signal.emit({"error": str(e)})  # 에러 발생 시