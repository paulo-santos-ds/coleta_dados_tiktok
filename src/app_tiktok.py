import os
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configurações
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')

# Cria as pastas se não existirem
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

# Configurações do WebDriver
CHROME_DRIVER_PATH = os.path.join(CONFIG_DIR, 'chromedriver')
TIKTOK_SEARCH_URL = "https://www.tiktok.com/search?q="

# Função para esperar um tempo aleatório
def random_sleep(min_time=2, max_time=5):
    time.sleep(random.uniform(min_time, max_time))

# Função para inicializar o WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
    return driver

# Função para coletar dados dos vídeos
def scrape_tiktok_videos(driver, search_query, max_videos=50):
    driver.get(TIKTOK_SEARCH_URL + search_query)
    videos_data = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(videos_data) < max_videos:
        try:
            # Espera até que os vídeos sejam carregados
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.video-item"))
            )
            videos = driver.find_elements(By.CSS_SELECTOR, "div.video-item")

            for video in videos:
                try:
                    title = video.find_element(By.CSS_SELECTOR, "strong.video-title").text
                    likes = video.find_element(By.CSS_SELECTOR, "span.likes-count").text
                    comments = video.find_element(By.CSS_SELECTOR, "span.comments-count").text
                    link = video.find_element(By.CSS_SELECTOR, "a.video-link").get_attribute("href")
                    videos_data.append({
                        "title": title,
                        "likes": likes,
                        "comments": comments,
                        "link": link
                    })
                except NoSuchElementException:
                    continue

                if len(videos_data) >= max_videos:
                    break

            # Rola a página para carregar mais vídeos
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            random_sleep(3, 5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        except TimeoutException:
            print("Timeout ao carregar vídeos.")
            break

    return videos_data

# Função principal
def main():
    search_query = "python programming"  # Exemplo de query de pesquisa
    driver = init_driver()
    try:
        videos_data = scrape_tiktok_videos(driver, search_query)
        df = pd.DataFrame(videos_data)
        output_file = os.path.join(DATA_DIR, f"tiktok_videos_{search_query.replace(' ', '_')}.csv")
        df.to_csv(output_file, index=False)
        print(f"Dados salvos em {output_file}")
    except Exception as e:
        print(f"Erro durante a execução: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()