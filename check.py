import time
import json
from loguru import logger
from argparse import ArgumentParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

WAIT_TIME = 3

OPTIONS = Options()
OPTIONS.add_argument('--headless')  # 啟動 Headless 無頭
OPTIONS.add_argument('--disable-gpu')  # 關閉GPU 避免某些系統或是網頁出錯
OPTIONS.add_argument("window-size=1400,800")


def get_credentials(json_path):
    with open(json_path) as f:
        obj = json.load(f)
    return obj.get("id"), obj.get("password")


def checkin(no, password):
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=OPTIONS
    )
    driver.get("https://app.pers.ncku.edu.tw/ncov/index.php?c=auth")

    # Login
    driver.find_element(By.CSS_SELECTOR, "#user_id").send_keys(no)
    driver.find_element(By.CSS_SELECTOR, "#passwd").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "#submit_by_acpw").click()
    logger.info("Login OK")

    # If pop-up exists, cancel it
    try:
        driver.find_element(
            By.CSS_SELECTOR,
            "#arch_grid > div.modal.fade.form.in > form > div > div > div.modal-footer > button.btn.btn-default.cancel_button",
        ).click()
    except NoSuchElementException:
        pass

    time.sleep(WAIT_TIME)
    element = driver.find_element(By.CSS_SELECTOR, "#grid_tool_add > i")
    ActionChains(driver).move_to_element(element).click().perform()
    driver.save_screenshot("screenshot.png")
    logger.info("Show Form OK")

    time.sleep(WAIT_TIME)
    driver.find_element(By.CSS_SELECTOR, "#fs_upd_N").click()
    driver.find_element(By.CSS_SELECTOR, "#other_upd_N").click()
    driver.find_element(By.CSS_SELECTOR, "#hastyfp_notice_N").click()
    element = driver.find_element(By.CSS_SELECTOR, "#taketest_N").click()
    element = driver.find_element(
        By.CSS_SELECTOR,
        "#arch_grid > div.modal.fade.form.in > form > div > div > div.modal-footer > button.btn.btn-primary.save_button",
    ).click()
    logger.info("Submit OK")

    time.sleep(WAIT_TIME)
    driver.find_element(
        By.CSS_SELECTOR,
        "#show_light > div.modal-dialog.modal-md > div > div.modal-footer2 > button",
    ).click()
    logger.info("Close OK")

    time.sleep(WAIT_TIME)
    driver.save_screenshot("screenshot.png")
    driver.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", help="credential path")
    args = parser.parse_args()
    no, password = get_credentials(args.path)
    checkin(no, password)
