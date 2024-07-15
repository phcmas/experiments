FROM python:3.10

# 필요한 패키지 설치
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./config ./config
COPY ./debug ./debug

# 엔트리 포인트 설정
CMD ["python", "debug/convert_logits.py"]