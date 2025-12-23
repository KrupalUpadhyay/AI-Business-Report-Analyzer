from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pypdf import PdfReader

from app.llm import analyze_business_report, answer_question
from app.state import DOCUMENT_CONTEXT

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    global DOCUMENT_CONTEXT

    reader = PdfReader(file.file)
    text = ""

    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()

    DOCUMENT_CONTEXT = text

    analysis = analyze_business_report(text)
    return analysis


@app.post("/ask")
async def ask(question: str):
    if not DOCUMENT_CONTEXT:
        return {"answer": "Please upload a report first."}

    answer = answer_question(DOCUMENT_CONTEXT, question)
    return {"answer": answer}
