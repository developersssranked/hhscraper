from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains as AC
from pathlib import Path
import pathlib
user_login = str(input("Введите номер телефона"))
user_password = str(input("Введите пароль"))
user_find = str(input("Введите поисковой запрос"))
city = str(input("Введите город"))
time_dict = {"0": "За все время", "1": "За месяц",
             "2": "За неделю", "3": "За последние три дня", "4": "За сутки"}
print(time_dict)
choise = int(input(
    "Введите цифру, которой присвоенно значение нужного вам временного промежутка"))
path = Path(pathlib.Path.cwd(), 'data.csv')
with open(path, "a", newline="", encoding='cp1251') as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(("Название", "Номер телефона", "Почта", "Фио"))

options = webdriver.ChromeOptions()

# Пропишите здесь свой юзер агент. в формате "user-agent="

options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options, service=Service(
    ChromeDriverManager().install()))
driver.get(url='https://hh.ru')
try:
    print("Пытаюсь выполнить вход в аккаунт...")
    login_button = driver.find_element(By.CSS_SELECTOR, "[data-qa='login']")
    login_button.click()
    login_by_password = driver.find_element(
        By.CSS_SELECTOR, '[data-qa="expand-login-by-password"]')
    login_by_password.click()
    sleep(2)
    email = driver.find_element(
        By.CSS_SELECTOR, '[data-qa="login-input-username"]')
    email.click()
    email.send_keys(user_login)
    sleep(2)
    password = driver.find_element(
        By.CSS_SELECTOR, '[data-qa="login-input-password"]')
    password.click()
    password.send_keys(user_password)
    sleep(2)
    confirm_button = driver.find_element(
        By.CSS_SELECTOR, '[data-qa="account-login-submit"]')
    confirm_button.click()
    print("Вход прошел успешно")
    sleep(10)
    find = driver.find_element(By.ID, "a11y-search-input")
    find.click()
    find.send_keys(user_find)
    confirm = driver.find_element(By.CSS_SELECTOR, '[data-qa="search-button"]')
    sleep(2)
    print("Поиск прошел успешно")
    confirm.click()
    sleep(3)
    city_button = driver.find_element(
        By.CSS_SELECTOR, '[data-qa="mainmenu_areaSwitcher"]')
    city_button.click()

    sleep(5)
    city_input = driver.find_element(By.ID, "area-search-input")
    city_input.click()
    city_input.send_keys(city)
    sleep(2)
    city_confirm = driver.find_element(
        By.CLASS_NAME, "area-switcher-autocomplete-item")
    city_confirm.click()
    print("Город установлен успешно")
    sleep(10)
    time_button = driver.find_elements(
        By.CSS_SELECTOR, '[data-qa="bloko-custom-select-select"]')[1]
    time_button.click()
    sleep(1)
    buton = driver.find_elements(
        By.CLASS_NAME, "bloko-select-dropdown-option")[choise]
    buton.click()
    print("Временные категории установлены успешно, начинаю парсинг")
    while True:
        ads = driver.find_elements(By.CLASS_NAME, "vacancy-serp-item__layout")
        for ad in ads:
            sleep(1)
            title = ad.find_element(By.CLASS_NAME, "serp-item__title").text
            try:
                contact_button = ad.find_element(
                    By.CSS_SELECTOR, '[data-qa="vacancy-serp__vacancy_contacts"]')
                contact_button.click()
                sleep(2)
                try:
                    phone_number = driver.find_element(
                        By.CLASS_NAME, "vacancy-contacts-call-tracking__phone-number").text
                except:
                    phone_number = "Не указан номер телефона"
                try:
                    name = driver.find_element(
                        By.CSS_SELECTOR, '[data-qa="vacancy-contacts__fio"]').text
                except:
                    name = "Не указано имя"
                try:
                    mail = driver.find_element(
                        By.CSS_SELECTOR, '[data-qa="vacancy-contacts__email"]').text
                except:
                    mail = "Не указана почта"
                # print(
                    # f"Название: {title}, номер телефона: {phone_number}, фио:  #{name}, Почта: {mail} ")
                path = Path(pathlib.Path.cwd(), 'data.csv')

                with open(path, "a", newline="", encoding='cp1251') as file:
                    writer = csv.writer(file, delimiter=";")
                    writer.writerow((title, phone_number, mail, name))

            except Exception as ex:

                print("Контакты не оставлены")
        try:
            next_page = driver.find_element(
                By.CSS_SELECTOR, '[data-qa="pager-next"]')
            next_page.click()
            print("Начинаю парсинг следующей страницы")
        except:
            break
            print(f"Парсинг завершен, файл сохранен в {str(path)}")
except Exception as ex:
    print("Перезапустите парсер")
finally:
    driver.close()
    driver.quit()
