import openai
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing import Literal

from dotenv import load_dotenv

load_dotenv()

audio_file= open("./data/bestellung.mp3", "rb")
bestellung_transcript = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
print("*** Transkribierter Text ***:")
print()
print(bestellung_transcript.text)
print()

llm = ChatOpenAI(temperature=0, model="gpt-4o")

class OrderExtraction(BaseModel):
    sentiment: Literal["positiv", "neutral", "negativ"]
    name: str = Field(description="Name des Anrufers")
    geraet: str = Field(description="Herstellername und Gerätebezeichnung des Geräts")
    thema: Literal["Reklamation", "Reservierung", "Dank"] = Field(description="Grund des Anrufs")
    details: str = Field(description="Alle verfügbaren Details und Informationen zum Grund des Anrufs in ausführlicher Form")
    wunsch: str = Field(description="Reaktion und nächste Schritte, die sich der Anrufer wünscht")
    sprache: Literal["deutsch", "englisch", "französisch", "russisch"]

extraction_chain = llm.with_structured_output(OrderExtraction)
data_extraction_result = extraction_chain.invoke(bestellung_transcript.text)

print("*** Extrahierte Daten:")
print(json.dumps(data_extraction_result, indent=2, ensure_ascii=False, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o)))
print()

llm_email = ChatOpenAI(temperature=0.1, model="gpt-4o")

messages = [
    SystemMessage(
        content="Du bist ein freundlicher AI-Assistent in einem Elektronikfachmarkt. Du schreibst Antworten in der Wir-Form und verwendest in der Ansprache Sie. Beende Antworten mit Mit freundlichen Grüßen,\nIhr Elektronikfachmarkt Karlsruhe"
    ),
    HumanMessage(
        content="Schreibe eine Bestätigung zu folgender Reservierungsanfrage: " + " " + bestellung_transcript.text + " "+ str(data_extraction_result)
    ),
]

email_answer = llm_email.invoke(messages)
print()
print("*** Email-Antwort ***:")
print()
print(email_answer.content)
