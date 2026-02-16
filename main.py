from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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

    # ÖRNEK hesap (senin matematik buraya gelecek)
    if oran1 > oran2:
        sonuc = "VALUE BET"
    else:
        sonuc = "DEĞİL"

    return {
        "sonuc": sonuc,
        "oran1": oran1,
        "oran2": oran2
    }
