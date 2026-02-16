from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS izni ekle (KRİTİK)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Veri(BaseModel):
    oran1: float
    oran2: float

@app.get("/")
def home():
    return {"status": "API çalışıyor"}

@app.post("/analyze")
def analyze(veri: Veri):

    oran1 = veri.oran1
    oran2 = veri.oran2

    if oran1 > oran2:
        sonuc = "VALUE BET"
    else:
        sonuc = "DEĞİL"

    return {"sonuc": sonuc}
