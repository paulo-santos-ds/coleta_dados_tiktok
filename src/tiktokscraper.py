import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Caminho para o ChromeDriver
chrome_driver_path = r"C:\Users\prasd\Downloads\chromedriver.exe"

try:
    # Configuração do WebDriver usando Service
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    # Acessa a página do TikTok
    driver.get("https://www.tiktok.com")
    logging.info(f"Título da página: {driver.title}")

except SessionNotCreatedException as e:
    logging.error(f"Erro de compatibilidade: {e}")
except WebDriverException as e:
    logging.error(f"Erro ao inicializar o WebDriver: {e}")
except Exception as e:
    logging.critical(f"Erro inesperado: {e}")
finally:
    if 'driver' in locals():
        driver.quit()
        logging.info("Navegador fechado.")