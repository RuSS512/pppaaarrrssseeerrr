import requests
from bs4 import BeautifulSoup
import csv
import time

# Изменяем диапазон (теперь от 1 до 500)
START_ID = 1
END_ID = 500

# Задержка между запросами, чтобы не «досить» сервер. 
# При желании уменьшайте, но осторожно, иначе могут быть блокировки от t.me.
DELAY_SECONDS = 1.5

def parse_owner_from_html(html: str) -> str:
    """
    Ищет в HTML фрагмент вида:
      <a href="https://t.me/XXX"><i class="tgme_gift_owner_photo ..."></i></a>
    Возвращает строку "https://t.me/XXX" или пустую строку, если не нашёл.
    """
    soup = BeautifulSoup(html, 'html.parser')
    # Ищем тег <i> с классом "tgme_gift_owner_photo"
    i_tag = soup.find("i", class_="tgme_gift_owner_photo")
    if not i_tag:
        return ""
    
    # Проверяем, что родитель этого i_tag — <a href="...">
    parent_a = i_tag.parent
    if parent_a and parent_a.name == "a" and parent_a.has_attr("href"):
        return parent_a["href"]
    
    return ""

def main():
    print("=== Начало работы скрипта по парсингу PlushPepe (1..500) ===")

    owners = {}
    total_found = 0  # Счётчик, сколько реально нашли владельцев

    for token_id in range(START_ID, END_ID + 1):
        url = f"https://t.me/nft/PlushPepe-{token_id}"
        print(f"\n[INFO] Обрабатываем PlushPepe #{token_id} → {url}")
        
        try:
            resp = requests.get(url, timeout=10)
            status_code = resp.status_code
            
            if status_code == 200:
                owner_link = parse_owner_from_html(resp.text)
                if owner_link:
                    owners[token_id] = owner_link
                    print(f"[FOUND] Найдена ссылка на владельца: {owner_link}")
                    total_found += 1
                else:
                    owners[token_id] = ""
                    print("[EMPTY] Владелец не обнаружен в HTML")
            else:
                owners[token_id] = ""
                print(f"[WARN] Страница вернула статус {status_code}, владелец не извлечён")
        
        except requests.RequestException as e:
            owners[token_id] = ""
            print(f"[ERROR] Ошибка при запросе {url}: {e}")
        
        # Пауза между запросами
        time.sleep(DELAY_SECONDS)

    # Выводим итоги парсинга
    print("\n=== Итоги парсинга ===")
    print(f" - Всего обработано ссылок: {END_ID - START_ID + 1}")
    print(f" - Найдено владельцев: {total_found}")

    # Сохраняем результат в CSV
    csv_filename = "owners.csv"
    with open(csv_filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["PlushPepeID", "OwnerLink"])
        for token_id in range(START_ID, END_ID + 1):
            owner_link = owners.get(token_id, "")
            writer.writerow([token_id, owner_link])
    
    print(f"=== Скрипт завершён! Результаты сохранены в файле: {csv_filename} ===")

if __name__ == "__main__":
    main()
