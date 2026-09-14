from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "Enterprise Knowledge Copilot API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/questions")
def ask_question(request: QuestionRequest):
    return {
        "question_received": request.question
    }