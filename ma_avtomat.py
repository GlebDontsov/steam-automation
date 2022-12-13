import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from steampy.guard import generate_one_time_code


def get_guard():
    with open(f"data/ma_files/{user}.maFile", "r") as file1:
        shared_secret = json.loads(file1.read())
        share = shared_secret["shared_secret"]
    one_time_authentication_code = generate_one_time_code(share)
    return one_time_authentication_code


def sign_in(driver):
    driver.find_element(By.NAME, "username").send_keys(user)
    driver.find_element(By.NAME, "password").send_keys(password)
    try:
        driver.find_element(By.CLASS_NAME, "btn_blue_steamui").click()
    except Exception:
        pass


def Steam_Authenticator(driver):
    driver.find_element(By.CLASS_NAME, "twofactorauthcode_entry_input").send_keys(get_guard())
    driver.find_element(By.XPATH, "//div[@class='auth_button leftbtn' and @type='submit']").click()


def click_me(driver):
    time.sleep(4)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element(By.XPATH, "//button[@class='DialogButton _DialogLayout Secondary Focusable']").click()


def go_find(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element(By.XPATH,
                        "//div[@class='salequestdisplay_questCtn_14UQz']/a").click()


def js(driver):
    driver.execute_script("""/* eslint-env browser */
    /* global g_sessionID jQuery */

    /* Thanks to Sqbika#0657 for the initial script */

    (async() => {
        let delay = (ms) => new Promise((res) => setTimeout(res, ms));
        await jQuery.post("/saleaction/ajaxopendoor", {
            "sessionid":      g_sessionID,
            "authwgtoken":    jQuery("#application_config").data("userinfo").authwgtoken,
            "door_index":     0,
            "clan_accountid": 41316928,
        });
        for (let link of [
            "/category/arcade_rhythm/?snr=1_614_615_clorthaxquest_1601",
            "/category/strategy_cities_settlements/?snr=1_614_615_clorthaxquest_1601",
            "/category/sports/?snr=1_614_615_clorthaxquest_1601",
            "/category/simulation/?snr=1_614_615_clorthaxquest_1601",
            "/category/multiplayer_coop/?snr=1_614_615_clorthaxquest_1601",
            "/category/casual/?snr=1_614_615_clorthaxquest_1601",
            "/category/rpg/?snr=1_614_615_clorthaxquest_1601",
            "/category/horror/?snr=1_614_615_clorthaxquest_1601",
            "/vr/?snr=1_614_615_clorthaxquest_1601",
            "/category/strategy/?snr=1_614_615_clorthaxquest_1601",
        ]) {
            try {
                let html = await jQuery.get(link);
                await jQuery.post("/saleaction/ajaxopendoor", {
                    "sessionid":      g_sessionID,
                    "authwgtoken":    jQuery("#application_config", html).data("userinfo").authwgtoken,
                    "door_index":     jQuery("#application_config", html).data("capsuleinsert").payload,
                    "clan_accountid": 41316928,
                    "datarecord":     jQuery("#application_config", html).data("capsuleinsert").datarecord,
                });
                console.log("You got a new badge!");
            } catch (e) {
                console.error("Failed to obtain badge!", e);
            } finally {
                await delay(1500);
            }
        }
    })();""")
    time.sleep(40)


def refresh(driver):
    driver.back()
    driver.refresh()


def save(driver):
    driver.find_element(By.XPATH, "//div[@class='profilemodifier_Preview_2GvFU']/img").click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element(By.XPATH, "//button[@class='DialogButton _DialogLayout Primary Focusable']").click()
    driver.quit()


def browser():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        executable_path='../gh/Data/chromedriver.exe',
        options=options
    )
    driver.implicitly_wait(5)
    driver.get(
        url="https://store.steampowered.com/login/?redir=sale%2"
            "Fclorthax_quest&redir_ssl=1&snr=1_614_615_clorthaxquest_global-header")
    return driver


def main():
    driver = browser()
    sign_in(driver)
    Steam_Authenticator(driver)
    click_me(driver)
    go_find(driver)
    js(driver)
    refresh(driver)
    click_me(driver)
    go_find(driver)
    save(driver)


with open("data/ma_accounts.txt", "r") as file:
    accounts = file.readlines()

for i, item in enumerate(accounts):
    user = item.split(":")[0]
    password = item.split(":")[1]
    try:
        main()
    except Exception:
        continue

