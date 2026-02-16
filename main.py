from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# GLOBAL ANALİZ NESNESİ
analiz = None


# SENİN CLASS'IN (sadece gerekli kısmı koyduk)
class BasketbolAnalizor:

    def __init__(self):
        self.dna = None
        self.dna_hiz = None

    def dna_hesapla(self, ev_dna, dep_dna):

        self.dna = ev_dna + dep_dna
        self.dna_hiz = self.dna / 40

        return self.dna, self.dna_hiz


   def q1_on_adil(self):

    q1_katsayi = 1.05
    on_hiz = self.dna_hiz * q1_katsayi
    q1_on_barem = on_hiz * 10

    return q1_on_barem, esikler



# INPUT MODELLERİ

class StartInput(BaseModel):

    ev_dna: float
    dep_dna: float


# ENDPOINTS

@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/start")
def start(data: StartInput):

    global analiz

    analiz = BasketbolAnalizor()

    dna, hiz = analiz.dna_hesapla(
        data.ev_dna,
        data.dep_dna
    )

    return {
        "toplam_dna": dna,
        "dna_hiz": hiz
    }


@app.get("/q1/on")
def q1_on():

    global analiz

    if analiz is None:
        return {"error": "Önce /start çağır"}

    barem = analiz.q1_on_adil()

    return {
        "adil_barem": barem
    }

