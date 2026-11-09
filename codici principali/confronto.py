import json
from deepdiff import DeepDiff
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score


# devo prima appiattire? i file json in modo da permettere l'analisi comparativa. ottengo così coppie di chiavi più semplici
def flatten_json(data, prefix=""):
  items = {}  # dizionario di queste coppie più semplici
  if isinstance(data, dict):
    for k, v in data.items():
      full_key = (
          f"{prefix}.{k}" if prefix else str(k)
      )  # creo la chiave più semplice unendone due con un punto
      items.update(flatten_json(v, full_key))
  elif isinstance(data, list):
    for i, v in enumerate(data):
      full_key = f"{prefix}[{i}]"
      items.update(flatten_json(v, full_key))
  else:
    items[prefix] = data
  return items


# leggo il file di riferimento principale (Ground Truth)
with open("gLETT.json", "r", encoding="utf-8") as f1:
  file1_data = json.load(f1)

# appiattisco il file di riferimento una sola volta
flat_ref = flatten_json(file1_data)
ref_items = set(
    flat_ref.items()
)  # ogni elemento del riferimento adesso è una tupla (insiemi)

# elenco dei file predetti da confrontare con il riferimento
confronti = ["outputLETT1.json", "outputLETT2.json", "outputLETT3.json", "outputLETT4.json", "outputLETT5.json", "outputLETT6.json",]

# dizionario generale per raccogliere tutti i report
report_totale = {}

# ciclo su ciascun file per calcolare le metriche singolarmente
for nome_file in confronti:
  with open(nome_file, "r", encoding="utf-8") as f2:
    file2_data = json.load(f2)

  # inizio l'analisi comparativa
  diff = DeepDiff(file1_data, file2_data, ignore_order=True)

  flat_pred = flatten_json(file2_data)
  pred_items = set(flat_pred.items())

  # calcolo le differenze nei due file (insiemi) json
  tp = len(ref_items & pred_items)
  fp = len(pred_items - ref_items)
  fn = len(ref_items - pred_items)

  precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
  recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
  f1 = (
      (2 * precision * recall) / (precision + recall)
      if (precision + recall) > 0
      else 0.0
  )

  # oppure in alternativa trasformo in vettori i file in modo da usare scikitlearn:
  all_items = list(ref_items | pred_items)
  y_true = [1 if item in ref_items else 0 for item in all_items]
  y_pred = [1 if item in pred_items else 0 for item in all_items]

  # precision = precision_score(y_true, y_pred, zero_division=0)
  # recall = recall_score(y_true, y_pred, zero_division=0)
  # f1 = f1_score(y_true, y_pred, zero_division=0)

  # output a schermo per ogni file
  print("=" * 40)
  print(f"Confronto: gLETT.json VS {nome_file}")
  print(f"Counts:    TP={tp}, FP={fp}, FN={fn}")
  print(f"Precision: {precision:.4f}")
  print(f"Recall:    {recall:.4f}")
  print(f"F1 Score:  {f1:.4f}")

  # salvo i risultati di questo file nel dizionario
  report_totale[nome_file] = {
      "metrics": {
          "precision": round(precision, 4),
          "recall": round(recall, 4),
          "f1_score": round(f1, 4),
          "counts": {"tp": tp, "fp": fp, "fn": fn},
      },
      "differences": json.loads(diff.to_json()),
  }

# scrivo un nuovo documento con tutti i report e le differenze trovate
with open("diff_MODERNO.json", "w", encoding="utf-8") as diff_file:
  json.dump(report_totale, diff_file, indent=4, ensure_ascii=False)

print("\nReport completo salvato con successo in 'diffMODERNO.json'")