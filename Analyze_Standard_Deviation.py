#파일 read 함수 만들어서 타임 스테프 로드하기 및 Passing 함수 만들기 

import os
import sys
import json
from pathlib import Path 
import numpy as np
from datetime import datetime

class LogAnalysis:
    def __init__(self):
        self.content = None
        self.result =  None
        
        self.base_path = Path("/root/project")
        self.app_path = self.base_path / "app"
        self.file_path = self.app_path / "logs.json"
        
        #result_path 
        self.result_path = self.app_path / "Analyze_result"
        
        #Parsing Dict
        self.ip_dict = {}

    def openfile(self):
        try:
            if os.path.isfile(self.file_path) and os.path.exists(self.file_path):
                print(f"{self.file_path} 파일이 존재합니다.")
                with open(self.file_path, "r", encoding = "utf-8") as f:
                    self.content = f.read()
                    
            else:
                print(f"{self.file_path} 파일이 존재하지 않습니다.")
                sys.exit(1)
        except Exception as e:
            print(f'ERROR: {e}')

    def parsing(self):
        try:
            if not self.content:
                print("파일이 비어있습니다.")
                sys.exit(1)
            lines  = self.content.split('\n')

            for line in lines:
                if not line.strip():
                    continue
                log_data = json.loads(line)
                ip = log_data.get("ip")
                timestamp = log_data.get("timestamp")
                username = log_data.get("username")

                #아이피를 대상으로 타임 스태프를 딕셔너리에 저장
                if ip and timestamp:
                    if ip not in self.ip_dict:
                        self.ip_dict[ip] = {
                            "username": username,
                            "timestamps": []
                        }
                        print(f"새로운 접속 아이피 감지: {ip} (사용자명 : {username})")

                    #이미 존재하는 IP에 타임 스탬프 추가
                    self.ip_dict[ip]["timestamps"].append(timestamp)

            print(f"파싱이 완료되었습니다. {len(self.ip_dict)}개의 고유한 IP가 감지되었습니다.")
                
        except Exception as e:
            print(f'Parsing ERROR: {e}')
    
    def show_parsing_result(self):
        print("\n" + "="*30)
        print("IP별 접속 기록 요약")
        print("="*30)
        #dict Key = ip, Value = {"username": username, "timestamps": [timestamp1, timestamp2, ...]} 
        for ip, data in self.ip_dict.items():
            print(f"IP: {ip} - 사용자명: {data['username']}\n 접속 횟수: {len(data['timestamps'])} - 타임스탬프 (10개): {data['timestamps'][:10]}")
        print("="*30)

    def intevals(self, timestamps):
        if len(timestamps) < 2:
            return []
        intervals = []

        for i in range(1, len(timestamps)):
            current_time = timestamps[i]
            previous_time = timestamps[i-1]
            diff = current_time - previous_time
            intervals.append(diff)

        return intervals    

    def get_std(self, intervals):
        if not intervals:
            return 0.0
        
        std_value = np.std(intervals)  
        return std_value  
        
    def save_result(self):
        try:
            result_list = []

            for ip, data in self.ip_dict.items():
                username = data["username"]
                timestamps = data["timestamps"]
                intervals = self.intevals(timestamps)
                std_value = self.get_std(intervals)
            
                res_obj = {
                    "ip": ip,
                    "username": username,
                    "connection_count": len(timestamps),
                    "std_deviation": std_value,
                    "status" : "allow"
                }
                result_list.append(res_obj)
            self.save_file_path = self.file_path / "analysis_result.json"
            with open(self.save_file_path, "w", encoding="utf-8") as f:
                json.dump(result_list, f, ensure_ascii=False, indent=4)
            print(f"분석 결과가 '{self.save_file_path}' 파일로 저장되었습니다. {len(result_list)}개의 IP 분석 결과가 포함되어 있습니다.")

        except Exception as e:
            print(f"결과 저장 오류: {e}")

if __name__ == "__main__":
    analysis = LogAnalysis()
    analysis.openfile() 
    analysis.parsing()  
    analysis.show_parsing_result() 
    analysis.save_result()