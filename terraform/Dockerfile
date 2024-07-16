# AWS Lambda Python 3.9 런타임 이미지 사용
FROM public.ecr.aws/lambda/python:3.10

# Lambda 함수 소스 코드 복사
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Lambda 함수 핸들러 설정
CMD ["lambda_function.lambda_handler"]
