import json
import requests

testo_indicizzato = (
"[0:Hamilcar,] [1:Hannibalis] [2:filius,] [3:cognomine] [4:Barca,] [5:Karthaginiensis,] [6:primo] [7:Poenico] [8:bello,] [9:sed] "
    "[10:temporibus] [11:extremis,] [12:admodum] [13:adulescentulus] [14:in] [15:Siciliā] [16:praeesse] [17:coepit] [18:exercitui.] "
    "[19:Cum] [20:ante] [21:eius] [22:adventum] [23:et] [24:mari] [25:et] [26:terrā] [27:male] [28:res] [29:gererentur] "
    "[30:Karthaginiensium,] [31:ipse] [32:ubi] [33:adfuit,] [34:numquam] [35:hosti] [36:cessit] [37:neque] [38:locum] [39:nocendi] "
    "[40:dedit,] [41:saepeque] [42:e] [43:contrario] [44:occasione] [45:datā] [46:lacessivit] [47:semperque] [48:superior] [49:discessit.] "
    "[50:Quo] [51:facto,] [52:cum] [53:paene] [54:omnia] [55:in] [56:Siciliā] [57:Poeni] [58:amisissent,] [59:ille] [60:Erycem] "
    "[61:sic] [62:defendit,] [63:ut] [64:bellum] [65:eo] [66:loco] [67:gestum] [68:non] [69:videretur.] [70:Interim] "
    "[71:Karthaginienses] [72:classe] [73:apud] [74:insulas] [75:Aegatis] [76:a] [77:C.] [78:Lutatio,] [79:consule] [80:Romanorum,] "
    "[81:superati] [82:statuerunt] [83:belli] [84:facere] [85:finem] [86:eamque] [87:rem] [88:arbitrio] [89:permiserunt] [90:Hamilcaris.] "
    "[91:Ille] [92:etsi] [93:flagrabat] [94:bellandi] [95:cupiditate,] [96:tamen] [97:paci] [98:serviundum] [99:putavit,] [100:quod] "
    "[101:patriam] [102:exhaustam] [103:sumptibus] [104:diutius] [105:calamitates] [106:belli,] [107:ferre] [108:non] [109:posse] "
    "[110:intellegebat,] [111:sed] [112:ita] [113:ut] [114:statim] [115:mente] [116:agitaret,] [117:si] [118:paulum] [119:modo] "
    "[120:res] [121:essent] [122:refectae,] [123:bellum] [124:renovare] [125:Romanosque] [126:armis] [127:persequi,] [128:donicum] "
    "[129:aut] [130:virtute] [131:vicissent] [132:aut] [133:victi] [134:manus] [135:dedissent.] [136:Hoc] [137:consilio] [138:pacem] "
    "[139:conciliavit,] [140:in] [141:quo] [142:tanta] [143:fuit] [144:ferocia,] [145:cum] [146:Catulus] [147:negaret] [148:bellum] "
    "[149:compositurum,] [150:nisi] [151:ille] [152:cum] [153:suis,] [154:qui] [155:Erycem] [156:tenuerant,] [157:armis] [158:relictis] "
    "[159:Siciliā] [160:decederent,] [161:ut] [162:succumbente] [163:patriā] [164:ipse] [165:periturum] [166:se] [167:potius] "
    "[168:dixerit,] [169:quam] [170:cum] [171:tanto] [172:flagitio] [173:domum] [174:rediret:] [175:non] [176:enim] [177:suae] "
    "[178:esse] [179:virtutis] [180:arma] [181:a] [182:patriā] [183:accepta] [184:adversus] [185:hostis] [186:adversariis] [187:tradere.] "
    "[188:Huius] [189:pertinaciae] [190:cessit] [191:Catulus.] [192:At] [193:ille] [194:ut] [195:Karthaginem] [196:venit,] [197:multo] "
    "[198:aliter] [199:ac] [200:sperarat] [201:rem] [202:publicam] [203:se] [204:habentem] [205:cognovit.] [206:Namque] [207:diuturnitate] "
    "[208:externi] [209:mali] [210:tantum] [211:exarsit] [212:intestinum] [213:bellum,] [214:ut] [215:numquam] [216:pari] [217:periculo] "
    "[218:fuerit] [219:Karthago] [220:nisi] [221:cum] [222:deleta] [223:est.] [224:Primo] [225:mercennarii] [226:milites,] [227:quibus] "
    "[228:usi] [229:adversus] [230:Romanos] [231:fuerant,] [232:desciverunt,] [233:quorum] [234:numerus] [235:erat] [236:viginti] "
    "[237:milium.] [238:Hi] [239:totam] [240:abalienarunt] [241:Africam,] [242:ipsam] [243:Karthaginem] [244:oppugnarunt.] [245:Quibus] "
    "[246:malis] [247:adeo] [248:sunt] [249:Poeni] [250:perterriti,] [251:ut] [252:etiam] [253:auxilia] [254:ab] [255:Romanis] "
    "[256:petierint] [257:eaque] [258:impetrarint.] [259:Sed] [260:extremo,] [261:cum] [262:prope] [263:iam] [264:ad] [265:desperationem] "
    "[266:pervenissent,] [267:Hamilcarem] [268:imperatorem] [269:fecerunt.] [270:Is] [271:non] [272:solum] [273:hostis] [274:a] "
    "[275:muris] [276:Karthaginis] [277:removit,] [278:cum] [279:amplius] [280:centum] [281:milia] [282:facta] [283:essent] "
    "[284:armatorum,] [285:sed] [286:etiam] [287:eo] [288:compulit,] [289:ut] [290:locorum] [291:angustiis] [292:clausi] [293:plures] "
    "[294:fame] [295:quam] [296:ferro] [297:interirent.] [298:Omnia] [299:oppida] [300:abalienata,] [301:in] [302:his] [303:Uticam] "
    "[304:atque] [305:Hipponem,] [306:valentissima] [307:totius] [308:Africae,] [309:restituit] [310:patriae.] [311:Neque] [312:eo] "
    "[313:fuit] [314:contentus,] [315:sed] [316:etiam] [317:finis] [318:imperii] [319:propagavit,] [320:totā] [321:Africā] [322:tantum] "
    "[323:otium] [324:reddidit,] [325:ut] [326:nullum] [327:in] [328:eā] [329:bellum] [330:videretur] [331:multis] [332:annis] "
    "[333:fuisse.] [334:Rebus] [335:his] [336:ex] [337:sententiā] [338:peractis] [339:fidenti] [340:animo] [341:atque] [342:infesto] "
    "[343:Romanis,] [344:quo] [345:facilius] [346:causam] [347:bellandi] [348:reperiret,] [349:effecit] [350:ut] [351:imperator] "
    "[352:cum] [353:exercitu] [354:in] [355:Hispaniam] [356:mitteretur,] [357:eoque] [358:secum] [359:duxit] [360:filium] "
    "[361:Hannibalem] [362:annorum] [363:novem.] [364:Erat] [365:praeterea] [366:cum] [367:eo] [368:adulescens] [369:illustris,] "
    "[370:formosus,] [371:Hasdrubal,] [372:quem] [373:nonnulli] [374:diligi] [375:turpius,] [376:quam] [377:par] [378:erat,] "
    "[379:ab] [380:Hamilcare] [381:loquebantur:] [382:non] [383:enim] [384:maledici] [385:tanto] [386:viro] [387:deesse] [388:poterant.] "
    "[389:Quo] [390:factum] [391:est,] [392:ut] [393:a] [394:praefecto] [395:morum] [396:Hasdrubal] [397:cum] [398:eo] [399:vetaretur] "
    "[400:esse.] [401:Huic] [402:ille] [403:filiam] [404:suam] [405:in] [406:matrimonium] [407:dedit,] [408:quod] [409:moribus] "
    "[410:eorum] [411:non] [412:poterat] [413:interdici] [414:socero] [415:genero.] [416:De] [417:hoc] [418:ideo] [419:mentionem] "
    "[420:fecimus,] [421:quod] [422:Hamilcare] [423:occiso] [424:ille] [425:exercitui] [426:praefuit] [427:resque] [428:magnas] "
    "[429:gessit] [430:et] [431:princeps] [432:largitione] [433:vetustos] [434:pervertit] [435:mores] [436:Karthaginiensium] "
    "[437:eiusdemque] [438:post] [439:mortem] [440:Hannibal] [441:ab] [442:exercitu] [443:accepit] [444:imperium.] [445:At] "
    "[446:Hamilcar,] [447:posteaquam] [448:mare] [449:transiit] [450:in] [451:Hispaniamque] [452:venit,] [453:magnas] [454:res] "
    "[455:secundā] [456:gessit] [457:fortunā:] [458:maximas] [459:bellicosissimasque] [460:gentes] [461:subegit,] [462:equis,] "
    "[463:armis,] [464:viris,] [465:pecuniā] [466:totam] [467:locupletavit] [468:Africam.] [469:Hic] [470:cum] [471:in] [472:Italiam] "
    "[473:bellum] [474:inferre] [475:meditaretur,] [476:nono] [477:anno] [478:postquam] [479:in] [480:Hispaniam] [481:venerat,] "
    "[482:in] [483:proelio] [484:pugnans] [485:adversus] [486:Vettones] [487:occisus] [488:est.] [489:Huius] [490:perpetuum] "
    "[491:odium] [492:erga] [493:Romanos] [494:maxime] [495:concitasse] [496:videtur] [497:secundum] [498:bellum] [499:Poenicum.] "
    "[500:Namque] [501:Hannibal,] [502:filius] [503:eius,] [504:assiduis] [505:patris] [506:obtestationibus] [507:eo] [508:est] "
    "[509:perductus,] [510:ut] [511:interire] [512:quam] [513:Romanos] [514:non] [515:experiri] [516:mallet.]"
)


CHUNK_SIZE = 50
parole = testo_indicizzato.split()
chunks = [" ".join(parole[i : i + CHUNK_SIZE]) for i in range(0, len(parole), CHUNK_SIZE)]

print(f"Testo suddiviso in {len(chunks)} chunk(s) da {CHUNK_SIZE} parole ciascuno.")

tutte_le_entita = []


for idx, chunk in enumerate(chunks, start=1):
    print(f"\n--- ANALISI CHUNK {idx}/{len(chunks)} ---")
    print(f"TESTO CHUNK:\n{chunk}\n")

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
\"\"\"{chunk}\"\"\"
"""

    response = requests.post(
        "http://172.24.172.59:11434/api/chat",
        json={
            "model": "llava:13b",
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "format": "json",
            "stream": False,
        },
        timeout=900,
    )

    print("STATUS:", response.status_code)
    print("RISPOSTA SERVER:", response.text)
    print("URL:", response.url)
    print("MODELLO:", response.request.body[:500] if response.request.body else None)

    response.raise_for_status()

    raw_json_string = response.json()["message"]["content"]
    parsed_data = json.loads(raw_json_string)

    # Raccolta e unione delle entità
    entita_chunk = parsed_data.get("entita", []) if isinstance(parsed_data, dict) else parsed_data
    for entita in entita_chunk:
        if entita not in tutte_le_entita:
            tutte_le_entita.append(entita)


risultato_unificato = {"entita": tutte_le_entita}

output_filename = "outputLATINOPREINDICIllava.json"
with open(output_filename, "w", encoding="utf-8") as out_file:
    json.dump(risultato_unificato, out_file, indent=4, ensure_ascii=False)

print(f"\nInferenza completata con successo ({len(tutte_le_entita)} entità estratte), file salvato in '{output_filename}'")