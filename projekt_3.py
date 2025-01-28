"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Dita Velčevová
email: d.velcevova@gmail.com
discord: dita8703
"""

# argument 1 = https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106
# argument 2 = vysledky_melnik.csv

import requests
from bs4 import BeautifulSoup
import csv
import sys

def download_html(url: str, print_first: bool = False) -> BeautifulSoup:
    """Stáhne HTML obsah z URL a vrátí jej jako objekt BeautifulSoup pro parsování.

    Args:
        url (str): URL adresa stránky.
        print_first (bool, optional): Pokud je True, vypíše URL před stažením dat. Výchozí je False.

    Returns:
        BeautifulSoup: Parsovaný HTML obsah stránky.
    """
    if print_first:
        print(f"STAHUJI DATA Z VYBRANÉHO URL: {url}")
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def get_municipality_name(html: BeautifulSoup) -> list:
    """Extrahuje a vrátí seznam názvů obcí z HTML tabulky pomocí třídy 'overflow_name'"""
    return [municipality.get_text() for municipality in html.find_all("td", class_="overflow_name")]

def get_urls(html: BeautifulSoup) -> list:
    """Extrahuje a vrátí seznam URL odkazů na detailní stránky obcí z HTML tabulky volebních výsledků"""
    base_url = "https://www.volby.cz/pls/ps2017nss/"
    return [f"{base_url}{url.a['href']}" for url in html.find_all("td", class_='cislo') if url.a]

def get_municipality_code(html: BeautifulSoup) -> list:
    """Extrahuje a vrátí seznam kódů obcí z HTML tabulky"""
    return [code.text for code in html.find_all("td", class_="cislo")]

def get_political_parties(urls: list) -> list:
    """Extrahuje a vrátí seznam politických stran pro každou obec z jejich detailních stránek"""
    parties = []

    for url in urls:
        html = download_html(url)
        for party in html.find_all("td", class_="overflow_name"):
            party_name = party.text.strip()
            if party_name not in parties:
                parties.append(party_name)

    return parties

def get_voter_data(urls: list) -> tuple:
    """Extrahuje data o voličích, účasti a platných hlasech pro každou obec z jejich detailních stránek"""
    registered_voters, envelopes, valid_votes = [], [], []

    def extract_data(html: BeautifulSoup, header_id: str) -> list:
        """Získá data z HTML podle daného header_id (např. počet voličů, vydané obálky)"""
        return [cell.text.replace('\xa0', ' ') for cell in html.find_all("td", headers=header_id)]

    for url in urls:
        html = download_html(url)
        registered_voters.extend(extract_data(html, 'sa2'))
        envelopes.extend(extract_data(html, 'sa3'))
        valid_votes.extend(extract_data(html, 'sa6'))

    return registered_voters, envelopes, valid_votes

def get_vote_results(urls: list) -> list:
    """Stahuje a vrací výsledky voleb pro každou stranu z daných URL"""
    return [
        [votes.text.replace('\xa0', ' ') for votes in download_html(url).find_all("td", class_="cislo",
                                                                                  headers=["t1sa2 t1sb3", "t2sa2 t2sb3"])]
        for url in urls
    ]

def create_rows(municipality_code: list, municipality_name: list, url: list) -> list:
    """Vytváří seznam řádků pro CSV soubor obsahující kombinované informace o obcích, voličích a volebních výsledcích"""

    registered_voters, envelopes, valid_votes = get_voter_data(url)

    results = get_vote_results(url)

    # Zajištění, že všechny seznamy mají stejnou délku
    min_len = min(len(municipality_code), len(municipality_name), len(registered_voters), len(envelopes),
                  len(valid_votes), len(results))

    rows = []
    for i in range(min_len):
        row = [municipality_code[i], municipality_name[i], registered_voters[i], envelopes[i], valid_votes[i]]
        rows.append(row + results[i])

    return rows

def save_to_csv(file_name: str, header: list, rows: list):
    """Uloží seznam dat (řádků a hlavičky) do CSV souboru s názvem 'file_name'"""
    try:
        with open(file_name, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow(header)
            writer.writerows(rows)
        print(f"UKLÁDÁM DATA DO SOUBORU: {file_name}")
    except IOError as e:
        print(f"CHYBA PŘI UKLÁDÁNÍ SOUBORU, UKONČUJI {file_name}: {e}")
        sys.exit(1)

def main():
    """Hlavní funkce programu"""
    # Kontrola správnosti zadaných argumentů
        if len(sys.argv) != 3:
        print("CHYBNĚ ZADANÉ ARGUMENTY.\nARGUMENTY ZADEJ VE FORMÁTU: projekt_3.py <link_district> <final_file>"
        sys.exit(1)

    link_district, final_file = sys.argv[1], sys.argv[2]

    if not link_district.startswith("http://") and not link_district.startswith("https://"):
        print("CHYBA: První argument musí být platná URL adresa.")
        sys.exit(1)

    if not final_file.endswith(".csv"):
        print("CHYBA: Druhý argument musí být název souboru s příponou .csv.")
        sys.exit(1)

    html = download_html(odkaz, print_first=True)  # Pouze při prvním stažení URL

    municipality_name = get_municipality_name(html)
    url = get_urls(html)
    municipality_code = get_municipality_code(html)

    parties = get_political_parties(url)

    rows = create_rows(municipality_code, municipality_name, url)

    header = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"] + [party for sublist in parties for party in sublist]

    save_to_csv(vysledny_soubor, header, rows)

    print(F"UKONČUJI {sys.argv[0]}")

if __name__ == "__main__":
    main()

