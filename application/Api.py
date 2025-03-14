import time
import requests
from PyQt5.QtCore import QThread, pyqtSignal
import random

class ApiThread(QThread):
    finished_signal = pyqtSignal(dict)  # 완료 신호 (응답 데이터 전달)

    def run(self):
        try:
            api_response = None
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