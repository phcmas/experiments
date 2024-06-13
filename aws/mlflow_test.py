import mlflow
from config import load_settings, logger

settings = load_settings()


def load_ai_model(model_path: str):
    try:
        ai_model = mlflow.pyfunc.load_model(model_path)
    except Exception as exc:
        logger.exception(exc)
        raise

    return ai_model


def main():
    logger.info("sqs message sended")
    model_path0 = "s3://sleep-models-test/feature_extractor/highball/v0.1.0/mlflow"
    model_path1 = "/home/oem/asleep/ai-model/feature_extractor/highball/v0.1.0/mlflow"

    model0 = load_ai_model(model_path0)
    model1 = load_ai_model(model_path1)

    print(model0)
    print(model1)


main()
