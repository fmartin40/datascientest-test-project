import asyncio
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
from pprint import pprint
import re
from typing import List
from  nodriver import * 
from selectorlib import Extractor

# extractor = Extractor.from_yaml_file('rules_indeed.yaml')
extractor = Extractor.from_yaml_file('rules_indeed_js.yaml')


@dataclass
class JobUrl:
    company: str
    job_name: str
    url: str 
    processed: bool = False

    def __post_init__(self):
        self.url = f"https://fr.indeed.com/{self.url}"

def scrape_page(html_content: str):
    match = re.search(r'window\._initialData\s*=\s*({.*?});', html_content, re.DOTALL)
    if match:
        raw_js_object = match.group(1)  # Récupérer l'objet JS brut
        
        # 2️⃣ Convertir en JSON valide
        # - Ajouter des guillemets autour des clés
        json_compatible_str = re.sub(r'(\w+):', r'"\1":', raw_js_object)

        # 3️⃣ Charger en tant qu'objet Python
        try:
            data = json.loads(json_compatible_str)
            print("✅ Données converties en dictionnaire Python :", data)
            return data
        except json.JSONDecodeError as e:
            print("❌ Erreur lors de la conversion en JSON:", e)

    else:
        print("❌ Données non trouvées dans le HTML")
    


async def open_browser():
    browser = await start(
        headless=False,
        lang="fr-FR"   # this could set iso-language-code in navigator, not recommended to change
    )
    page = await browser.get('https://fr.indeed.com/jobs?q=data+engineer')
    html = await page.get_content()
    await browser.wait(5)
    await page.close()
    return html
    


if __name__ == '__main__':
    ROOT_DIR = Path(__file__).parent.parent.parent
    EXTRACT_FOLDER = os.path.join(ROOT_DIR, "doc")
    
    html = asyncio.run(open_browser())
    json_data = scrape_page(html)
    print(json)
    # with open(f"{EXTRACT_FOLDER}/indeed.json", "w", encoding="utf-8") as json_file:
    #         json.dump(json_data, json_file, indent=4, ensure_ascii=False) 

    with open(f"{EXTRACT_FOLDER}/indeed.html", "w", encoding="utf-8") as html_file:
            html_file.write(html) 
    
