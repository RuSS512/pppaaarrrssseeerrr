import requests
from bs4 import BeautifulSoup
import csv
import time

START_ID = 1
END_ID = 2800

# Задержка между запросами, чтобы не спамить
DELAY_SECONDS = 1.5

def parse_owner_from_html(html: str) -> str:
    """
    Ищет в HTML фрагмент вида:
      <a href="https://t.me/XXXX"><i class="tgme_gift_owner_photo ..."></i></a>
    Возвращает ссылку (например "https://t.me/dricxsa") или пустую строку.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Ищем тег <i class="tgme_gift_owner_photo...">
    i_tag = soup.find("i", class_="tgme_gift_owner_photo")
    if not i_tag:
        return ""
    
    # Родительским элементом для <i> должен быть <a href="...">
    parent_a = i_tag.parent
    if parent_a and parent_a.name == "a" and parent_a.has_attr("href"):
        return parent_a["href"]
    
    return ""

def main():
    owners = {}
    
    for token_id in range(START_ID, END_ID + 1):
        url = f"https://t.me/nft/PlushPepe-{token_id}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                owner_link = parse_owner_from_html(resp.text)
                owners[token_id] = owner_link
                print(f"#{token_id}: {owner_link}")
            else:
                # Страница не 200 (часто 404 или 302)
                owners[token_id] = ""
                print(f"#{token_id}: status {resp.status_code}")
        except requests.RequestException as e:
            print(f"Ошибка запроса для {url}: {e}")
            owners[token_id] = ""
        
        time.sleep(DELAY_SECONDS)
    
    # Сохраняем результат в CSV
    with open("owners.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["PlushPepeID", "OwnerLink"])
        for token_id in range(START_ID, END_ID + 1):
            writer.writerow([token_id, owners.get(token_id, "")])

    print("Готово! Результаты сохранены в owners.csv")

if __name__ == "__main__":
    main()
