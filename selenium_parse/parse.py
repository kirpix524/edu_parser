import time
import csv
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# 1. Настраиваем опции Chrome: отключаем уведомления
chrome_options = Options()
chrome_options.add_argument("--disable-notifications")

# 2. Инициализируем браузер с этими опциями
driver = webdriver.Chrome(options=chrome_options)

# URL категории "Свет" на сайте divan.ru
url = "https://www.divan.ru/category/svet"

# Открываем страницу
driver.get(url)

# Ждём, чтобы страница прогрузилась (можно увеличить время при медленном интернете)
time.sleep(3)

# Ищем все карточки товара по селектору div._Ud0k
cards = driver.find_elements(By.CSS_SELECTOR, "div._Ud0k")

# Список для хранения результатов
parsed_data = []

for card in cards:
    try:
        # Название товара
        name_elem = card.find_element(By.CSS_SELECTOR, "span[itemprop='name']")
        name = name_elem.text.strip()
    except:
        name = None

    try:
        # Цена товара (строка вида "4990")
        price_elem = card.find_element(By.CSS_SELECTOR, "span.KIkOH[data-testid='price']")
        price = price_elem.text.strip()
    except:
        price = None

    try:
        # Получаем относительную ссылку из <a class="ProductName">
        link_elem = card.find_element(By.CSS_SELECTOR, "a.ProductName")
        href = link_elem.get_attribute("href")
        # Если href относительный (не начинается с http), склеиваем с базовым URL
        if href and not href.startswith("http"):
            detail_url = urljoin(url, href)
        else:
            detail_url = href
    except:
        detail_url = None

    # Добавляем запись в общий список
    parsed_data.append([name, price, detail_url])

# Закрываем браузер
driver.quit()

# Сохраняем результаты в CSV
with open("divan_lamps.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    # Заголовки столбцов
    writer.writerow(["Название", "Цена", "Ссылка"])
    # Записываем все строки
    writer.writerows(parsed_data)

print("Сбор данных завершён. Результаты сохранены в divan_lamps.csv")