import asyncio
import os
from bs4 import BeautifulSoup
import requests
import telegram

# --- 설정 값 ---
BOT_TOKEN = '8855923871:AAEcIDMjHWSxmB5HyB2BVVJe4uQA3ocUokA'
CHAT_ID = '7658817457'
ID_FILE = 'last_id.txt'
URL = 'https://www.gnu.ac.kr/cse/na/ntt/selectNttList.do?mi=17093&bbsId=4753'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
# -------------

bot = telegram.Bot(token=BOT_TOKEN)

async def send_telegram_msg(title, link):
    message = f'📢 새로운 공지사항 등록!\n\n제목: {title}\n링크: {link}'
    await bot.send_message(chat_id=CHAT_ID, text=message)

def run_crawler():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code != 200:
        print(f'페이지 접속 실패: {response.status_code}')
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select('table tbody tr')

    all_data = []

    # 모든 글을 돌며 ID와 제목을 수집
    for row in rows:
        title_tag = row.select_one('a')
        if title_tag and title_tag.get('data-id'):
            ntt_id = title_tag.get('data-id')
            title = title_tag.get_text(strip=True)
            all_data.append({'id': int(ntt_id), 'title': title})

    if not all_data:
        return

    # ID가 가장 큰 것(진짜 최신 글) 찾기
    latest_item = max(all_data, key=lambda x: x['id'])
    latest_id = str(latest_item['id'])
    latest_title = latest_item['title']
    latest_link = f'https://www.gnu.ac.kr/cse/na/ntt/selectNttInfo.do?mi=17093&bbsId=4753&nttSn={latest_id}'

    # 파일에서 기존 ID 불러오기
    if os.path.exists(ID_FILE):
        with open(ID_FILE, 'r', encoding='utf-8') as f:
            saved_id = f.read().strip()
    else:
        saved_id = '0'

    # 비교 후 알림 발송
    if latest_id != saved_id:
        asyncio.run(send_telegram_msg(latest_title, latest_link))
        print(f'새 공지 발견! 알림 발송: {latest_title}')
        
        # 새 ID 저장
        with open(ID_FILE, 'w', encoding='utf-8') as f:
            f.write(latest_id)
    else:
        print('새로운 공지가 없습니다.')

if __name__ == "__main__":
    run_crawler()