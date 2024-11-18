import mlflow
import numpy as np


def prediction_test(model_path: str):
    feat_vecs = [np.random.rand(1, (i + 1) * 10, 6, 192).astype(np.float32) for i in range(0, 8)]
    model = mlflow.pyfunc.load_model(model_path)

    for i, feat_vec in enumerate(feat_vecs):
        try:
            result = model.predict({"feature_vector": feat_vec})
            print(f"Prediction of shape (1, {(i+1) * 10}, 6, 192) succeeded, length: {len(result)}")
        except Exception:
            print(f"Prediction of shape (1, {(i+1) * 10}, 6, 192) failed")


def main():
    model_path0 = "s3://sleep-models-test/classifier/highball/v0.1.0/mlflow"
    model_path1 = "s3://sleep-models-test/classifier/highball/v0.2.0/mlflow"
    model_path2 = "s3://sleep-models-test/classifier/highball/v0.3.0/mlflow"

    # test for highbal v0.1.0
    prediction_test(model_path0)

    # test for highbal v0.2.0
    prediction_test(model_path1)

    # test for highbal v0.3.0
    prediction_test(model_path2)


main()
