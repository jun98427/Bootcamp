import time
import requests
from PyQt5.QtCore import QThread, pyqtSignal


class ApiThread(QThread):
    finished_signal = pyqtSignal(dict)  # 완료 신호 (응답 데이터 전달)

    def run(self):
        try:
            time.sleep(5)  # 테스트용 딜레이
            response = requests.get("http://127.0.0.1:8000/")  # 예제 API
            data = response.json()
            print(data)

            self.finished_signal.emit(data)  # 결과 전달
        except Exception as e:
            self.finished_signal.emit({"error": str(e)})  # 에러 발생 시