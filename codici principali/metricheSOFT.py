import json
import os
import re


def normalizza_testo(testo: str) -> str:
    """Rimuove residui di indici numerici (es. '[0:Roma]'), spaziature superflue
    e punteggiatura esterna per garantire un confronto puramente testuale.
    """
    if not isinstance(testo, str):
        return ""
    t = testo.strip()

    t = re.sub(r"^\[?\d+:\s*", "", t)
    t = re.sub(r"\]$", "", t)

    t = t.strip(".,:;!?\"'»«()[]")
    return t.lower()


def analizza_predizioni(gold_list, pred_list):
    """Confronta la lista di riferimento con quella predetta in modo puramente testuale.
    Implementa una Soft Evaluation conteggiando nei True Positives (TP) sia i match esatti
    sia i match parziali (sovrapposizione di testo con stessa etichetta).
    """

    gold_rimanenti = list(gold_list)
    pred_rimanenti = list(pred_list)

    tp_entita = []          # Match esatti (testo identico + etichetta identica)
    tp_parziali = []        # Match parziali (sottostringa/sovrapposizione + etichetta identica)
    etichette_errate = []

    # 1. Match Esatti (stesso testo e stessa etichetta)
    i_pred = 0
    while i_pred < len(pred_rimanenti):
        p = pred_rimanenti[i_pred]
        p_txt = normalizza_testo(p.get("testo", ""))
        p_lbl = str(p.get("etichetta", "")).strip().upper()

        match_idx = -1
        for i_gold, g in enumerate(gold_rimanenti):
            g_txt = normalizza_testo(g.get("testo", ""))
            g_lbl = str(g.get("etichetta", "")).strip().upper()

            if p_txt == g_txt and p_lbl == g_lbl:
                match_idx = i_gold
                break

        if match_idx != -1:
            tp_entita.append(
                {"testo": p.get("testo"), "etichetta": p_lbl}
            )
            pred_rimanenti.pop(i_pred)
            gold_rimanenti.pop(match_idx)
        else:
            i_pred += 1

    # 1-bis. Match Parziali (testo parziale/sottostringa con stessa etichetta) -> Inclusi in TP (Soft Matrix)
    i_pred = 0
    while i_pred < len(pred_rimanenti):
        p = pred_rimanenti[i_pred]
        p_txt = normalizza_testo(p.get("testo", ""))
        p_lbl = str(p.get("etichetta", "")).strip().upper()

        match_idx = -1
        for i_gold, g in enumerate(gold_rimanenti):
            g_txt = normalizza_testo(g.get("testo", ""))
            g_lbl = str(g.get("etichetta", "")).strip().upper()

            # Condizione Soft: una stringa è contenuta nell'altra e l'etichetta coincide
            if p_txt and g_txt and (p_txt in g_txt or g_txt in p_txt) and p_lbl == g_lbl:
                match_idx = i_gold
                break

        if match_idx != -1:
            tp_parziali.append(
                {
                    "testo_predetto": p.get("testo"),
                    "testo_corretto": gold_rimanenti[match_idx].get("testo"),
                    "etichetta": p_lbl,
                }
            )
            pred_rimanenti.pop(i_pred)
            gold_rimanenti.pop(match_idx)
        else:
            i_pred += 1

    # 2. Identificazione degli scambi di etichetta (stesso testo, etichetta diversa)
    i_pred = 0
    while i_pred < len(pred_rimanenti):
        p = pred_rimanenti[i_pred]
        p_txt = normalizza_testo(p.get("testo", ""))
        p_lbl = str(p.get("etichetta", "")).strip().upper()

        match_idx = -1
        for i_gold, g in enumerate(gold_rimanenti):
            g_txt = normalizza_testo(g.get("testo", ""))
            if p_txt == g_txt:
                match_idx = i_gold
                break

        if match_idx != -1:
            g_lbl = str(gold_rimanenti[match_idx].get("etichetta", "")).strip().upper()
            etichette_errate.append(
                {
                    "testo": p.get("testo"),
                    "etichetta_predetta": p_lbl,
                    "etichetta_corretta": g_lbl,
                }
            )
            pred_rimanenti.pop(i_pred)
            gold_rimanenti.pop(match_idx)
        else:
            i_pred += 1

    # 3. Gli elementi residui corrispondono a:
    # - pred_rimanenti: entità inventate / non presenti nel Golden (Falsi Positivi Puri)
    # - gold_rimanenti: entità non estratte dal modello (Falsi Negativi Puri)
    trovate_erronee = [
        {"testo": p.get("testo"), "etichetta_predetta": p.get("etichetta")}
        for p in pred_rimanenti
    ]
    non_trovate = [
        {"testo": g.get("testo"), "etichetta_corretta": g.get("etichetta")}
        for g in gold_rimanenti
    ]

    # Calcolo metriche con Soft Evaluation:
    # I True Positives includono sia i match esatti sia i match parziali
    tp = len(tp_entita) + len(tp_parziali)
    fp = len(trovate_erronee) + len(etichette_errate)
    fn = len(non_trovate) + len(etichette_errate)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        (2 * precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    return {
        "metrics": {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "counts": {
                "tp": tp,
                "tp_esatti": len(tp_entita),
                "tp_parziali": len(tp_parziali),
                "fp": fp,
                "fn": fn,
                "totale_gold": len(gold_list),
                "totale_pred": len(pred_list),
            },
        },
        "diagnostica": {
            "etichette_errate": etichette_errate,
            "non_trovate": non_trovate,
            "trovate_erroneamente": trovate_erronee,
            "corrette_esatte": tp_entita,
            "corrette_parziali": tp_parziali,
        },
    }


def main():
    file_riferimento = "goldLATINOPREINDICIZZATO.json"
    if not os.path.exists(file_riferimento):
        print(f"Errore: File di riferimento '{file_riferimento}' non trovato.")
        return

    with open(file_riferimento, "r", encoding="utf-8") as f_ref:
        ref_raw = json.load(f_ref)
        gold_data = (
            ref_raw.get("entita", []) if isinstance(ref_raw, dict) else ref_raw
        )

    confronti = [
        "outputLATINOPREINDICIgemma.json",
        "outputLATINOPREINDICIqwen.json",
                
        "outputLATINOPREINDICIllama.json",
    ]

    report_totale = {}

    for nome_file in confronti:
        if not os.path.exists(nome_file):
            continue

        with open(nome_file, "r", encoding="utf-8") as f_pred:
            pred_raw = json.load(f_pred)
            pred_data = (
                pred_raw.get("entita", [])
                if isinstance(pred_raw, dict)
                else pred_raw
            )

        risultato = analizza_predizioni(gold_data, pred_data)
        report_totale[nome_file] = risultato

        metrics = risultato["metrics"]
        diag = risultato["diagnostica"]

        # Output sintetico e chiaro a terminale
        print("=" * 65)
        print(f"Confronto: {file_riferimento} VS {nome_file}")
        print("=" * 65)
        print(
            f"Counts:    TP={metrics['counts']['tp']} (Esatti: {metrics['counts']['tp_esatti']}, Parziali: {metrics['counts']['tp_parziali']}), "
            f"FP={metrics['counts']['fp']}, FN={metrics['counts']['fn']}"
        )
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1_score']:.4f}\n")

        print(f"1. ENTITÀ CON ETICHETTA ERRATA ({len(diag['etichette_errate'])}):")
        if diag["etichette_errate"]:
            for item in diag["etichette_errate"]:
                print(
                    f"   - \"{item['testo']}\": Predetta=[{item['etichetta_predetta']}] -> Corretta=[{item['etichetta_corretta']}]"
                )
        else:
            print("   (Nessuna)")

        print(f"\n2. ENTITÀ NON TROVATE / MANCANTI ({len(diag['non_trovate'])}):")
        if diag["non_trovate"]:
            for item in diag["non_trovate"]:
                print(
                    f"   - \"{item['testo']}\" [{item['etichetta_corretta']}]"
                )
        else:
            print("   (Nessuna)")

        print(f"\n3. ENTITÀ TROVATE ERRONEE / EXTRA ({len(diag['trovate_erroneamente'])}):")
        if diag["trovate_erroneamente"]:
            for item in diag["trovate_erroneamente"]:
                print(
                    f"   - \"{item['testo']}\" [{item['etichetta_predetta']}]"
                )
        else:
            print("   (Nessuna)")

        print(f"\n4. MATCH PARZIALI ACCETTATI COME TP ({len(diag['corrette_parziali'])}):")
        if diag["corrette_parziali"]:
            for item in diag["corrette_parziali"]:
                print(
                    f"   - Predetto: \"{item['testo_predetto']}\" <-> Corretto: \"{item['testo_corretto']}\" [{item['etichetta']}]"
                )
        else:
            print("   (Nessuno)")

        print()

    output_report = "diff_LATINOPREINDINDICIZZATOSOFT.json"
    with open(output_report, "w", encoding="utf-8") as out_f:
        json.dump(report_totale, out_f, indent=4, ensure_ascii=False)

    print("=" * 65)
    print(f"Report diagnostico completo salvato in '{output_report}'")
    print("=" * 65)


if __name__ == "__main__":
    main()