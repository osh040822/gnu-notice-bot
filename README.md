# 학과 공지 텔레그램 알리미 (gnu-notice-bot)

경상국립대학교 컴퓨터과학과 공지사항 게시판에 새 글이 올라오면 텔레그램으로 알려주는 봇입니다.
GitHub Actions로 30분마다 실행되며, 별도 서버 없이 운영 중입니다.

## 동작 방식
1. GitHub Actions가 30분마다 `crawler.py`를 실행합니다.
2. requests로 게시판 HTML을 가져와 BeautifulSoup으로 글 번호(data-id)와 제목을 뽑습니다.
3. 상단 고정 공지 때문에 첫 줄이 최신 글이 아닐 수 있어, 글 번호의 최댓값을 최신 글로 판단합니다.
4. `last_id.txt`에 저장된 번호와 다르면 텔레그램으로 보내고 번호를 갱신합니다.

## 기술
Python 3.12 · requests · BeautifulSoup4 · python-telegram-bot · GitHub Actions

## 설정
저장소 Settings → Secrets and variables → Actions에 아래 두 값을 등록합니다.
- `BOT_TOKEN`: 텔레그램 봇 토큰
- `CHAT_ID`: 알림을 받을 채팅 ID

## 한계와 개선 계획
- 30분 사이에 공지가 여러 개 올라오면 가장 최신 1건만 알림이 갑니다. 마지막으로 알린 번호보다 큰 글을 모두 보내도록 고칠 계획입니다.
- GitHub Actions의 예약 실행은 지연될 수 있습니다.

## 소개 페이지
https://sites.google.com/view/seunghyun-oh/projects/공지-알리미
