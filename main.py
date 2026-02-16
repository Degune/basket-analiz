from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# =========================
# ANALİZ MOTORU
# =========================

class BasketAnaliz:
    def __init__(self):
        self.ev_dna = None
        self.dep_dna = None
        self.toplam_dna = None
        self.dna_hiz = None

    def baslat(self, ev, dep):
        self.ev_dna = ev
        self.dep_dna = dep
        self.toplam_dna = ev + dep
        self.dna_hiz = self.toplam_dna / 40

    def q1_on_adil(self):
        return round(self.dna_hiz * 10, 2)

    def q1_5dk(self, skor):
        tempo = skor / 5
        proj = tempo * 10
        return round(proj, 2)

    def reset(self):
        self.__init__()


analiz = BasketAnaliz()

# =========================
# MODELLER
# =========================

class BaslatModel(BaseModel):
    ev_dna: float
    dep_dna: float

class SkorModel(BaseModel):
    skor: float


# =========================
# ENDPOINTLER
# =========================

@app.post("/start")
def start(data: BaslatModel):
    analiz.baslat(data.ev_dna, data.dep_dna)
    return {
        "toplam_dna": analiz.toplam_dna,
        "dna_hiz": analiz.dna_hiz
    }

@app.get("/q1/on")
def q1_on():
    return {
        "adil_barem": analiz.q1_on_adil()
    }

@app.post("/q1/5dk")
def q1_5dk(data: SkorModel):
    return {
        "projeksiyon": analiz.q1_5dk(data.skor)
    }

@app.post("/reset")
def reset():
    analiz.reset()
    return {"mesaj": "Analiz sıfırlandı"}
