import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options() 
options.add_argument('--headless')  # 啟動 Headless 無頭
options.add_argument('--disable-gpu') # 關閉GPU 避免某些系統或是網頁出錯
options.add_argument("window-size=1400,800")

ID = "id"
PW = "password"
WAIT_TIME = 3

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://app.pers.ncku.edu.tw/ncov/index.php?c=auth")

# Login
element = driver.find_element(By.CSS_SELECTOR, "#user_id")
element.send_keys(ID)
element = driver.find_element(By.CSS_SELECTOR, "#passwd")
element.send_keys(PW)
element = driver.find_element(By.CSS_SELECTOR, "#submit_by_acpw")
element.click()
print("Login OK")

# If pop-up exists, cancel it
try:
    element = driver.find_element(By.CSS_SELECTOR, "#arch_grid > div.modal.fade.form.in > form > div > div > div.modal-footer > button.btn.btn-default.cancel_button")
    element.click()
except NoSuchElementException:
    pass

time.sleep(WAIT_TIME)
element = driver.find_element(By.CSS_SELECTOR, "#grid_tool_add > i")
ActionChains(driver).move_to_element(element).click().perform()
driver.save_screenshot("screenshot.png")
print("Show Form OK")

time.sleep(WAIT_TIME)
element = driver.find_element(By.CSS_SELECTOR, "#fs_upd_N")
element.click()
element = driver.find_element(By.CSS_SELECTOR, "#other_upd_N")
element.click()
element = driver.find_element(By.CSS_SELECTOR, "#hastyfp_notice_N")
element.click()
element = driver.find_element(By.CSS_SELECTOR, "#taketest_N")
element.click()
element = driver.find_element(By.CSS_SELECTOR, "#arch_grid > div.modal.fade.form.in > form > div > div > div.modal-footer > button.btn.btn-primary.save_button")
element.click()
print("Submit OK")

time.sleep(WAIT_TIME)
element = driver.find_element(By.CSS_SELECTOR, "#show_light > div.modal-dialog.modal-md > div > div.modal-footer2 > button")
element.click()
print("Close OK")

time.sleep(WAIT_TIME)
driver.save_screenshot("screenshot.png")
driver.close()
