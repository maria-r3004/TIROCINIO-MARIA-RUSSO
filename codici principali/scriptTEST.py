import json
import requests


testo_indicizzato = (
    "[0:E] [1:veramente,] [2:considerando] [3:che] [4:questi] [5:nostri] [6:climi] [7:sijno] [8:sotto] "
    "[9:l'amparo] [10:del] [11:Re] [12:Cattolico] [13:nostro] [14:Signore,] [15:che] [16:è] "
    "[17:quel] [18:Sole] [19:che] [20:mai] [21:tramonta,] [22:e] [23:che] [24:sopra] [25:di] "
    "[26:essi,] [27:con] [28:riflesso] [29:Lume,] [30:qual] [31:Luna] [32:giamai] [33:calante,] "
    "[34:risplenda] [35:l'Heroe] [36:di] [37:nobil] [38:Prosapia] [39:che] [40:pro] [41:tempore] "
    "[42:ne] [43:tiene] [44:le] [45:sue] [46:parti,] [47:e] [48:gl'Amplissimi] [49:Senatori] "
    "[50:quali] [51:Stelle] [52:fisse,] [53:e] [54:gl'altri] [55:Spettabili] [56:Magistrati] "
    "[57:qual'erranti] [58:Pianeti] [59:spandino] [60:la] [61:luce] [62:per] [63:ogni] [64:doue,] "
    "[65:venendo] [66:così] [67:a] [68:formare] [69:un] [70:nobilissimo] [71:Cielo,] [72:altra] "
    "[73:causale] [74:trouar] [75:non] [76:si] [77:può] [78:del] [79:vederlo] [80:tramutato] "
    "[81:in] [82:inferno] [83:d'atti] [84:tenebrosi,] [85:malvaggità] [86:e] [87:sevitie] [88:che] "
    "[89:dagl'huomini] [90:temerarij] [91:si] [92:vanno] [93:moltiplicando,] [94:se] [95:non] "
    "[96:se] [97:arte] [98:e] [99:fattura] [100:diabolica,] [101:attesoché] [102:l'humana] "
    "[103:malitia] [104:per] [105:sé] [106:sola] [107:bastar] [108:non] [109:dourebbe] [110:a] "
    "[111:resistere] [112:a] [113:tanti] [114:Heroi,] [115:che] [116:con] [117:occhij] "
    "[118:d'Argo] [119:e] [120:braccj] [121:di] [122:Briareo,] [123:si] [124:vanno] "
    "[125:trafficando] [126:per] [127:li] [128:pubblici] [129:emolumenti.]"
)

prompt = f"""
You are an expert Named Entity Recognition (NER) extractor specializing in high-recall, exhaustive textual analysis.

Analyze the provided text and extract all relevant entities belonging to the following categories:

CATEGORIES TO EXTRACT:
- PERSONA: First and/or last names of real, historical, or fictional people (e.g., "Dessy", "Dante").
- DATA: Specific temporal references, years, centuries, dates.
- RUOLO: ANY professional title, office, occupation, or functional societal role. IMPORTANT:
  * Include humble, rural, and informal trades (e.g., "pastora", "venditore ambulante", "contadino").
  * Include plural occupational groups (e.g., "intellettuali", "medici", "politici").
  * Include literary and communicative roles (e.g., "Narratore", "oratore").
  * Include institutional/governmental titles (e.g., "maestra", "ministro", "presidente").
- LUOGO: Specific geographic toponyms, countries, regions, cities, islands (e.g., "Sardegna", "Roma").
  * STRICT NEGATIVE RULE: EXCLUDE demonyms/nationality adjectives (e.g., "sardo", "italiano", "francese" are NOT locations).


TOKENIZATION AND INDEXING RULES:
1. The text is provided pre-numbered as [index:word].

3. If an entity is made of multiple words (e.g., "venditore ambulante"), use the index of the first word for "indice_parola_inizio" and the index of the last word for "indice_parola_fine".
4. In "testo", strip all external punctuation (commas, colons, brackets, ellipses).
5. Output MUST be ONLY a valid JSON object matching the schema.

---

EXAMPLE 1 (Medieval Vernacular - Honorifics, Personifications, False Friends):
Indexed input text:
[0:Messer] [1:Guido,] [2:quel] [3:dolce] [4:latino] [5:d'Amor] [6:giunse] [7:a] [8:Firenze.]

Output:
{{
    "entita": [
        {{"testo": "Messer", "etichetta": "RUOLO", "indice_parola_inizio": 0, "indice_parola_fine": 0}},
        {{"testo": "Guido", "etichetta": "PERSONA", "indice_parola_inizio": 1, "indice_parola_fine": 1}},
        {{"testo": "Amor", "etichetta": "PERSONA", "indice_parola_inizio": 5, "indice_parola_fine": 5}},
        {{"testo": "Firenze", "etichetta": "LUOGO", "indice_parola_inizio": 8, "indice_parola_fine": 8}}
    ]
}}
(Note: "latino" means song/language in this context, so it is strictly excluded from LUOGO).

---

EXAMPLE 2 (Poetic Formulas - Seasonal Time, Honorific Titles, Negative Landscape Terms):
Indexed input text:
[0:In] [1:sul] [2:tempo] [3:di] [4:primavera,] [5:vostr'altezza] [6:discese] [7:per] [8:la] [9:rivera.]

Output:
{{
    "entita": [
        {{"testo": "primavera", "etichetta": "DATA", "indice_parola_inizio": 4, "indice_parola_fine": 4}},
        {{"testo": "vostr'altezza", "etichetta": "RUOLO", "indice_parola_inizio": 5, "indice_parola_fine": 5}}
    ]
}}
(Note: "rivera" and "tempo" are common landscape/abstract terms, excluded from LUOGO and DATA).

---

EXAMPLE 3 (Literary Titles and Demonyms):
Indexed input text:
[0:La] [1:gentil] [2:Madonna] [3:Bice] [4:partì] [5:da] [6:Bologna] [7:nel] [8:mese] [9:di] [10:giugno.]

Output:
{{
    "entita": [
        {{"testo": "Madonna", "etichetta": "RUOLO", "indice_parola_inizio": 2, "indice_parola_fine": 2}},
        {{"testo": "Bice", "etichetta": "PERSONA", "indice_parola_inizio": 3, "indice_parola_fine": 3}},
        {{"testo": "Bologna", "etichetta": "LUOGO", "indice_parola_inizio": 6, "indice_parola_fine": 6}},
        {{"testo": "giugno", "etichetta": "DATA", "indice_parola_inizio": 10, "indice_parola_fine": 10}}
    ]
}}

---

Indexed input text to analyze:
\"\"\"{testo_indicizzato}\"\"\"
"""

url = "http://172.24.172.59:11434/api/chat"

payload = {
    "model": "Almawave/Velvet:14b",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "format": "json",
    "stream": False,
    "options": {
        "num_ctx": 4096,
        "num_predict": 1024,
        "temperature": 0.3
    }
}

session = requests.Session()
session.trust_env = False
 
response = session.post(
    url,
    json=payload,
    timeout=(10, 600)
) 

print("STATUS:", response.status_code)
print("RISPOSTA SERVER:", response.text)
print("URL:", response.url)
print("MODELLO:", response.request.body[:500] if response.request.body else None)
 
response.raise_for_status()


raw_json_string = response.json()["message"]["content"]
parsed_data = json.loads(raw_json_string)

output_filename = "outputCLASSvelvet.json"
with open(output_filename, "w", encoding="utf-8") as out_file:
    json.dump(parsed_data, out_file, indent=4, ensure_ascii=False)

print(f"Inferenza completata con successo, file salvato in '{output_filename}'")