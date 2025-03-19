from PyQt5.QtCore import QThread, pyqtSignal
import os
import openai
import json

# def encode_image():
#     image_path = '/home/willtek/Bootcamp/application/captured_frame.jpg'
#     with open(image_path, 'rb') as image_file:
#         return base64.b64encode(image_file.read()).decode('utf-8')

class ApiThread(QThread):
    finished_signal = pyqtSignal(dict)  # 완료 신호 (응답 데이터 전달)

    def __init__(self, skill, career, animal, celebrity) -> None:
        super().__init__()
        self.celebrity = celebrity
        self.careers = career
        self.animals = animal
        self.skills = skill

    def run(self):
        try:
            # print("api : ", self.celebrity)
            key = os.getenv("OPENAI_API_KEY")
            client = openai.OpenAI(api_key=key)
            # text = '{} 가수면 대표곡을 배우면 대표작을 알려줘. json 형식으로 key 값은 제목과 년도로 보내줘'.format(self.celebrity)
            # text = '{} 가수면 대표곡을 배우면 대표작을 알려줘. 대표작 명 , 출시 시기 순서로 총 3작품씩 알려줘 '.format(self.celebrity)

            text1 = """배우나 가수의 이름을 주면 그 사람의 대표작 3개와 해당 연도를 아래 형식으로 답하시오.
            특히, 작품명은 반드시 큰따옴표(" ")로 감싸고, 꺾쇠 괄호(<>)등 다른 처리를 사용하지 마시오.
            또한, 응답을 HTML에서 줄바꿈이 정상적으로 표시될 수 있도록 각 줄 끝에 <br> 태그를 추가하시오.

            1. "작품명" (년도)<br>
            2. "작품명" (년도)<br>
            3. "작품명" (년도)<br>

            이름: {}""".format(self.celebrity)

            

            text2 = """ 너는 사람의 특성을 분석하여 적합한 직업을 추천하는 전문가이다.  
                다음 능력치 정보를 바탕으로 이 사람이 추천 직업이 어울리는 이유를 설명해줘.  
                분석할 때 **능력치나 직업명을 직접 언급하지 말고**, 마치 사람을 평가하는 것처럼 작성해줘. 
                불필요한 부가 설명 없이 2문장으로 답하도록. 답변시 '이 사람은' 으로 시작하는것이 아닌 '당신은' 으로 시작하고 어미는 습니다. 입니다. 등의 말투로 사용해줘
                능력치 : {}, 추천 직업 : {}""".format(self.skills, self.careers)
                        
            text3 = """ 너는 사람의 특성을 분석하여 어울리는 동물을 추천하는 전문가이다.  
                다음 능력치 정보를 바탕으로 이 사람이 해당 동물이 어울리는 이유를 설명해줘.  
                분석할 때 **능력치나 동물명을 직접 언급하지 말고**, 마치 사람을 평가하는 것처럼 작성해줘. 
                불필요한 부가 설명 없이 2문장으로 답하도록. 답변시 '이 사람은' 으로 시작하는것이 아닌 '당신은' 으로 시작하고 어미는 습니다. 입니다. 등의 말투로 사용해줘
                능력치 : {}, 닮은 동물 : {}""".format(self.skills, self.animals)

            # text = """배우나 가수의 이름을 주면 그 사람의 대표작 3개와 해당 연도를 아래 형식으로 답하시오.  
            #     다른 부가 설명 없이 오직 아래 형식으로만 답변하시오.

            #     1. "<작품명>" (<년도>)
            #     2. "<작품명>" (<년도>)
            #     3. "<작품명>" (<년도>)

            #     이름: {}""".format(self.celebrity)
            # print("text ", text)
            # encoded_image = encode_image()

            resp = client.chat.completions.create(
                model='gpt-4o',  # 'gpt4o-mini' 대신 'gpt-4-turbo' 사용 추천
                messages=[
                    {
                        'role': 'user', 
                        'content': [
                            {
                                "type" : "text",
                                "text" : text1
                            },
                        ],
                    }
                ],
                # response_format = "json",
            )
            # print(resp.choices[0].message.content)

            resp2 = client.chat.completions.create(
                model='gpt-4o',  # 'gpt4o-mini' 대신 'gpt-4-turbo' 사용 추천
                messages=[
                    {
                        'role': 'user', 
                        'content': [
                            {
                                "type" : "text",
                                "text" : text2
                            },
                        ],
                    }
                ],
            )
            # print(resp2.choices[0].message.content)

            resp3 = client.chat.completions.create(
                model='gpt-4o',  # 'gpt4o-mini' 대신 'gpt-4-turbo' 사용 추천
                messages=[
                    {
                        'role': 'user', 
                        'content': [
                            {
                                "type" : "text",
                                "text" : text3
                            },
                        ],
                    }
                ],
            )
            # print(resp3.choices[0].message.content)

            # response_text = resp["choices"][0]["message"]["content"]
            # # res = json.loads(resp['choices'][0].message.content)
            # print('-----------------------')
            # print(response_text)

            self.finished_signal.emit({"content": resp.choices[0].message.content, "content2": resp2.choices[0].message.content, "content3": resp3.choices[0].message.content})
            # self.finished_signal.emit({"content": "hi"})
        except Exception as e:
            self.finished_signal.emit({"error": str(e)})  # 에러 발생 시