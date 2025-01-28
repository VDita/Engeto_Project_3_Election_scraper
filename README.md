# Engeto_Project_3_Election_scraper
Třetí projekt pro Engeto Academy

# Popis projektu
Tento projekt slouží k získávání volebních dat z roku 2017. Odkaz výsledků voleb [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ). 

# Instalace knihoven
Knihovny použité v kódu jsou uloženy v souboru `requirements.txt`. Pro instalaci je doporučeno vytvořit nové virtuální prostředí
a s nainstalovaným manažerem spustit následovně:

```bash
$ pip3 --version                      # Ověří verzi manažeru
$ pip3 install -r requirements.txt    # Nainstaluje knihovny
```

# Spuštění projektu
Pro spuštění `projekt_3.py` jsou potřeba dva argumenty:

`python projekt_3.py <link_district> <final_file>`

Poté budou výsledky staženy do souboru `csv`.

# Ukázka projektu
Výsledky hlasování pro okres Mělník:
1. argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106`
2. argument: `vysledky_melnik.csv`

Spuštění programu:

```bash
python projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106" "vysledky_melnik.csv"
```

Průběh stahování:

```
STAHUJI DATA Z VYBRANÉHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106 
UKLÁDÁM DATA DO SOUBORU: vysledky_melnik.csv 
UKONČUJI projekt_3.py
```

Částečný výstup:
| Kód obce | Název obce    | Voliči v seznamu | Vydané obálky | Platné hlasy | Občanská demokratická strana |
|----------|---------------|------------------|---------------|--------------|-----------------------------|
| 534714   | Býkev         | 341              | 212           | 210          | 14                          |
| 534722   | Byšice        | 1 061            | 630           | 626          | 96                          |
| 534731   | Cítov         | 923              | 575           | 569          | 52                          |
| 598291   | Čakovičky     | 461              | 321           | 320          | 64                          |


