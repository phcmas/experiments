from fastapi import FastAPI


app = FastAPI(
    title="webhook",
    description="Document Of Asleep Data API",
    contact={"name": "Liam", "email": "liam@asleep.ai"},
    docs_url="/_docs",
    root_path=None,
)


@app.post("/inference-complete", tags=["webhook"])
def receive_inference_complete(request: dict):
    file_path = "webhook.log"

    with open(file_path, "a") as f:
        f.write(str(request) + "\n")

    return {"message": "success"}


@app.post("/session-complete", tags=["webhook"])
def receive_session_complete(request: dict):
    file_path = "webhook.log"

    with open(file_path, "a") as f:
        f.write(str(request) + "\n")

    return {"message": "success"}
