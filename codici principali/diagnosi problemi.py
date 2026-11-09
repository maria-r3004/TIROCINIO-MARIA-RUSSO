import json


def confronta_annotazioni(path_golden: str, path_predetto: str):
    with open(path_golden, "r", encoding="utf-8") as fg:
        golden = json.load(fg).get("entita", [])
    with open(path_predetto, "r", encoding="utf-8") as fp:
        predetto = json.load(fp).get("entita", [])

    print(f"Totale entità nel Golden:   {len(golden)}")
    print(f"Totale entità nel Predetto: {len(predetto)}\n")

    print("--- DETTAGLIO CONFRONTO ---")
    for i, g in enumerate(golden):
        print(f"\n[Golden #{i+1}]: '{g['testo']}' | {g['etichetta']} | indici: [{g['indice_parola_inizio']}, {g['indice_parola_fine']}]")
        
        # Cerca corrispondenze parziali di testo
        corrispondenze_testo = [p for p in predetto if g["testo"].lower() in p["testo"].lower() or p["testo"].lower() in g["testo"].lower()]
        
        if not corrispondenze_testo:
            print("  -> NESSUNA corrispondenza di testo trovata nel predetto (Falso Negativo).")
        else:
            for p in corrispondenze_testo:
                offset_inizio = p["indice_parola_inizio"] - g["indice_parola_inizio"]
                offset_fine = p["indice_parola_fine"] - g["indice_parola_fine"]
                print(f"  -> Trovato nel predetto: '{p['testo']}' | {p['etichetta']} | indici: [{p['indice_parola_inizio']}, {p['indice_parola_fine']}]")
                if offset_inizio == 0 and offset_fine == 0 and p["etichetta"] == g["etichetta"]:
                    print("     ESITO: MATCH ESATTO (True Positive)")
                else:
                    print(f"     ESITO: MISMATCH (Offset Inizio: {offset_inizio:+d}, Offset Fine: {offset_fine:+d}, Label Uguale: {p['etichetta'] == g['etichetta']})")

if __name__ == "__main__":
    # Sostituisci con i percorsi reali dei tuoi due file JSON
    confronta_annotazioni("goldenLETT1.json", "outputLETT2.json")