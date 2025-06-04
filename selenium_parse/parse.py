import time
import csv
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Отключаем уведомления (если необходимо)
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.divan.ru/category/svet")

# Ждём, чтобы первоначальные карточки загрузились
time.sleep(3)

# Функция для получения текущего количества карточек на странице
def get_card_count():
    return len(driver.find_elements(By.CSS_SELECTOR, "div._Ud0k"))

parsed_data = []
prev_count = get_card_count()

# Цикл: скроллим до контейнера пагинации (div.ui-jDl24) и ждём подгрузки новых карточек
while True:
    try:
        # Находим контейнер с номерами страниц
        pagination = driver.find_element(By.CSS_SELECTOR, "div.ui-jDl24")

        # Скроллим к контейнеру пагинации
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pagination)
        # Даем немного времени, чтобы новые товары подгрузились
        time.sleep(2)

        # Считаем, сколько карточек стало после прокрутки
        new_count = get_card_count()

        if new_count > prev_count:
            # Появились новые карточки — обновляем счётчик и повторяем
            prev_count = new_count
            continue
        else:
            # Количество не изменилось — все страницы подгружены
            break

    except Exception as e:
        # Если контейнер пагинации не найден или другое исключение — выходим
        print("Пагинация недоступна или всё подгружено:", e)
        break

# Собираем все карточки после завершения подгрузки
cards = driver.find_elements(By.CSS_SELECTOR, "div._Ud0k")
for card in cards:
    try:
        name = card.find_element(By.CSS_SELECTOR, "span[itemprop='name']").text.strip()
    except:
        name = ""
    try:
        price = card.find_element(By.CSS_SELECTOR, "span.KIkOH[data-testid='price']").text.strip()
    except:
        price = ""
    try:
        href = card.find_element(By.CSS_SELECTOR, "a.ProductName").get_attribute("href")
        detail_url = href if href.startswith("http") else urljoin(driver.current_url, href)
    except:
        detail_url = ""
    parsed_data.append([name, price, detail_url])

driver.quit()

# Записываем результат в CSV
with open("divan_lamps_all_pages.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["name", "price", "detail_url"])
    writer.writerows(parsed_data)

print(f"Готово! Всего записано товаров: {len(parsed_data)}. Файл: divan_lamps_all_pages.csv")
