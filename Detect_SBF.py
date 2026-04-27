import json 
import os
from pathlib import Path

class SBFDetector:
    def __init__(self):
        self.base_path = Path("/root/project")
        self.app_path = self.base_path / "app"
        self.file_path = self.app_path / "analysis_result.json"

        self.data = []
    
    def load_logs(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
                print(f"{self.file_path} 파일이 성공적으로 로드되었습니다.")
            else:
                print(f"{self.file_path} 파일이 존재하지 않습니다.")
        except Exception as e:
            print(f"파일 로드 중 에러 발생: {e}")
    
    def detect_bots(self):
        block_count = 0
        suspicious_count = 0
        if not self.data:
            print("분석할 데이터가 없음")
            return []
        
        for res in self.data:
            std = res.get("std_deviation")
            count = res.get("connection_count")

            #최소 카운트 횟수 지정은 마음대로..
            if count >= 50 and std is not None and std < 2.0:
                res["status"] = "block"
                print(f"IP : {res['ip']} 차단됨 (std: {std:.2f})")
                block_count += 1
            elif count >= 50 and std is not None and 2.1< std < 22:
                res["status"] = "suspicious"
                print(f"IP : {res['ip']} 의심됨 (std: {std:.2f})")
                suspicious_count += 1
        
        print(f"탐지 완료 : 차단된 IP : {block_count}, 의심되는 IP : {suspicious_count}")

    def save_results(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            print(f"분석 결과가 {self.file_path}에 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 중 에러 발생: {e}")

if __name__ == "__main__":
    detector = SBFDetector()
    detector.load_logs()        # 1. 로그 로드
    detector.detect_bots()      # 2. 봇 탐지 (기본 2.0 기준)
    detector.save_results()