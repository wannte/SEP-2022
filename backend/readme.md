# 실행방법

cd backend/apps/src
sql/database.py 에서 import config 부분을 alembic에 맞게 변경
alembic upgrade head
sql/database.py 원상복귀 (이러한 문제는 alembic과 uvicorn의 실행위치가 달라서 생기는 문제입니다.)
cd ../.. (SEP-2022/backend 위치)
uvicorn apps.src.main:app --reload
