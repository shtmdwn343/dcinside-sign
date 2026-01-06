from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox

import pyperclip
import time

def generate_password(length):
    import string, secrets
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

options = Options()
options.binary_location = r'C:\Programs\Tor Browser\Browser\firefox.exe'
options.add_argument(r'-profile C:\Programs\Tor Browser\Browser\TorBrowser\Data\Browser\profile.default')

while True:
    log = open('log.txt', 'a+')

    # Tor 접속
    driver = Firefox(options=options)
    driver.get('https://msign.dcinside.com/join/info_form')

    # 페이지 접속
    driver.get('https://msign.dcinside.com/join/info_form')

    # 비밀번호 입력
    password_input = driver.find_element(By.NAME, 'password')
    safe_level = driver.find_element(By.CSS_SELECTOR, '.stage')

    while True:
        password = generate_password(20)
        pyperclip.copy(password)
        password_input.send_keys(Keys.CONTROL + 'v')
        time.sleep(0.2)
        if 'three' in safe_level.get_attribute('class'):
            break
        password_input.clear()
        time.sleep(0.2)

    # 비밀번호 재확인
    repeat_pw_input = driver.find_element(By.NAME, 'repeatPw')
    repeat_pw_input.send_keys(Keys.CONTROL + 'v')

    # 고정닉 선택
    is_unique_select = Select(driver.find_element(By.NAME, 'is_unique'))
    is_unique_select.select_by_index(1)

    # 식별 코드 확인
    user_code = driver.find_element(By.NAME, 'user_code').get_attribute('value')
    pyperclip.copy(user_code)

    # 닉네임 입력
    nickname_input = driver.find_element(By.ID, 'nickname')
    nickname_input.send_keys(Keys.CONTROL + 'v')

    # 캡차 코드 입력
    code_confirm_input = driver.find_element(By.NAME, 'code_confirm')
    code_confirm_input.click()

    # 다음 클릭
    wait = WebDriverWait(driver, 3600)
    while True:
        try:
            label = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'label.chklbl')))
            label.click()

            button = driver.find_element(By.CSS_SELECTOR, 'button.btn-line.btn-line-inblue')
            button.click()

            security_code = wait.until(EC.presence_of_element_located((By.ID, 'securityCode'))).text.split(': ')[1]
            log.write(user_code + ' ' * (16 - len(user_code)) + password + '\t' + security_code + '\n')
            break
        except UnexpectedAlertPresentException as e:
            if e.alert_text == '더 이상 가입하실 수 없습니다.':
                break

    log.close()
    driver.quit()