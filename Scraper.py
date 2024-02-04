from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver


class Scraper:
    def __init__(self, moves):
        self.options = webdriver.FirefoxOptions()
        self.driver = webdriver.Firefox(options=self.options)
        self.visible = EC.visibility_of_element_located
        self.presense = EC.presence_of_element_located
        self.wait = WebDriverWait(driver=self.driver, timeout=10)
        self.wait2 = WebDriverWait(driver=self.driver, timeout=45)
        self.wait3 = WebDriverWait(driver=self.driver, timeout=300)
        self.moves = moves
        self.cnt = 1

    def resizeWindow(self):
        self.driver.maximize_window()
        self.screen_width = self.driver.execute_script(
            "return window.screen.availWidth;")
        self.screen_height = self.driver.execute_script(
            "return window.screen.availHeight;")

        self.left_half_width = self.screen_width // 2 + 1
        self.driver.set_window_rect(
            0, 0, self.left_half_width, self.screen_height)

    def login(self):
        self.driver.get("https://www.chess.com/login")
        self.wait.until(self.visible((By.ID, "login")))
        usernameInput = self.driver.find_element(By.ID, "username")
        passwordInput = self.driver.find_element(By.ID, "password")
        # don't worry these creds won't work :)
        usernameInput.send_keys("cdzx29@gmail.com")
        passwordInput.send_keys("Testpass123")
        loginButton = self.driver.find_element(By.ID, "login")
        loginButton.click()

    def scrollToTop(self):
        self.driver.execute_script("window.scrollTo(0, 0);")

    def startGameSession(self):
        # TODO: change this
        self.driver.get('https://www.chess.com/play/online/new')

    def setTimeControls(self):
        baseTime = eval(input("Enter basetime: "))
        increment = eval(input("Enter increment: "))
        self.wait.until(self.visible(
            (By.CLASS_NAME, "selector-button-button")))
        button = self.driver.find_element(
            By.CLASS_NAME, "selector-button-button")
        button.click()

        selector = ""
        if (increment == 0):
            selector = f'time-selector-category-{baseTime}'
        else:
            selector = f'time-selector-category-{baseTime}|{increment}'

        self.wait.until(
            self.visible((By.XPATH, f'//button[@data-cy="{selector}"]')))
        timecontrol = self.driver.find_element(
            By.XPATH, f'//button[@data-cy="{selector}"]')
        timecontrol.click()

    def startGame(self):
        self.wait.until(self.visible(
            (By.XPATH, '//button[@data-cy="new-game-index-play"]')))
        playButton = self.driver.find_element(
            By.XPATH, '//button[@data-cy="new-game-index-play"]')
        playButton.click()
        # self.resizeWindow()
        self.scrollToTop()

    def waitForGameStart(self):
        print("waiting")
        self.scrollToTop()
        self.wait3.until(self.visible((By.CLASS_NAME, "eco-opening-name")))
        print("wait ended")

    def readMoves(self, color):
        # white odd moves
        # black even moves
        print(f"Waiting for move {self.cnt}...")
        self.wait3.until(
            self.visible((By.XPATH, f'//div[@data-ply="{self.cnt}"]')))
        move = self.driver.find_element(
            By.XPATH, f'//div[@data-ply="{self.cnt}"]')
        mv = move.text
        try:
            moveSymbol = move.find_element(
                By.CSS_SELECTOR, ".icon-font-chess").get_attribute("data-figurine")
            mv = str(moveSymbol) + mv
        except:
            pass

        if ((color == "white" and self.cnt % 2 == 0) or (color == "black" and self.cnt % 2 == 1)):
            print("Opponent Plays: ", mv)
        self.moves.append(mv)
        self.cnt = self.cnt + 1
        return True
