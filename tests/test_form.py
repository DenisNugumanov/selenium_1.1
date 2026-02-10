import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def driver():
    # Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


    # 1. Тест успешного входа
def test_successful_login(driver):

    # Открываем страницу формы авторизации
    driver.get("https://the-internet.herokuapp.com/login")

    # Заполняем текстовое поле
    text_input = driver.find_element(By.ID, "username") # Находим ID
    text_input.clear() # Очищаем поле
    text_input.send_keys("tomsmith") # Вводим данные для успешной авторизации

    # Заполняем поле пароля
    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys("SuperSecretPassword!") # Вводим данные для успешной авторизации

    # Находим кнопку отправки формы для входа
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    # Кликаем на кнопку входа
    login_button.click()

    # Проверяем успешную авторизацию
    # После успешного входа появляется flash-сообщение и кнопка logout
    flash_message = driver.find_element(By.ID, "flash")
    logout_button = driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius")

    # Ассерты для проверки успешной авторизации
    assert "You logged into a secure area!" in flash_message.text
    assert logout_button.is_displayed()
    assert "/secure" in driver.current_url



    # 2. Тест неудачного входа
def test_unsuccessful_login(driver):
    # Открываем страницу формы авторизации
    driver.get("https://the-internet.herokuapp.com/login")

    # Заполняем текстовое поле
    text_input = driver.find_element(By.ID, "username")  # Находим ID
    text_input.clear()  # Очищаем поле
    text_input.send_keys("Denis")  # Вводим неверные данные для авторизации

    # Заполняем поле пароля
    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys("HGFhgh3434")  # Вводим неверные данные для авторизации

    # Находим кнопку отправки формы для входа
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    # Кликаем на кнопку входа
    login_button.click()

    # Проверяем сообщение об ошибке
    flash_message = driver.find_element(By.ID, "flash")

    # Ассерты для проверки неудачной авторизации
    assert "Your username is invalid!" in flash_message.text
    assert "/login" in driver.current_url  # Остаемся на странице логина


    driver.quit()