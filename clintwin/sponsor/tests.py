from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class TestLogin(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
        self.driver.get("https://clintwin.com/")
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("test@gmail.com")
        self.driver.find_element(By.ID, "id_password").send_keys("test")
        self.driver.find_element(By.NAME, "remember").click()
        self.driver.find_element(By.ID, "login_button").click()

    def tearDown(self):
        try:
            self.driver.find_element(By.ID, "logout_link").click()
        except NoSuchElementException:
            pass
        self.driver.close()
        self.driver.quit()

    def test_logout(self):
        self.driver.find_element(By.ID, "logout_link").click()
        elements = self.driver.find_elements(By.ID, "login_button")
        assert len(elements) > 0

    def test_checkSponsorSectionOptions(self):
        elements = self.driver.find_elements(By.ID, "navbarDropdown")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "navbarDropdown")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "navbarLogo")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "logout_link")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".card:nth-child(1)")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "trialdetails").click()
        elements = self.driver.find_elements(By.ID, "trialdetails")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "navbarDropdown").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Create New Clinical Trial")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "View Clinical Trials")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "View Clinical Trials2")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "Inclusion Criteria")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "Exclusion Criteria")
        assert len(elements) > 0

    def test_checkAddClinicalTrialForm(self):
        self.driver.find_element(By.ID, "navbarDropdown").click()
        self.driver.find_element(By.LINK_TEXT, "Create New Clinical Trial").click()
        self.driver.find_element(By.ID, "id_title").click()
        self.driver.find_element(By.ID, "id_title").send_keys("Test Trial")
        self.driver.find_element(By.ID, "id_url").send_keys("http://testtrial.com")
        self.driver.find_element(By.ID, "id_recruitmentStartDate").click()
        self.driver.find_element(By.ID, "id_recruitmentStartDate").send_keys("08/02/20")
        self.driver.find_element(By.ID, "id_recruitmentEndDate").send_keys("07/02/21")
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").send_keys("499")
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").send_keys("500")
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").send_keys("501")
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").send_keys("502")
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        element = self.driver.find_element(By.ID, "id_enrollmentTarget")
        self.driver.find_element(By.ID, "id_enrollmentTarget").send_keys("501")
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").send_keys("500")
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        element = self.driver.find_element(By.ID, "id_enrollmentTarget")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys("Boston")
        self.driver.find_element(By.ID, "id_objective").click()
        self.driver.find_element(By.ID, "id_objective").send_keys("Treat Cancer")
        self.driver.find_element(By.ID, "id_comments").click()
        self.driver.find_element(By.ID, "id_comments").send_keys("Test Trial")
        self.driver.find_element(By.ID, "id_followUp").click()
        self.driver.find_element(By.ID, "id_followUp").send_keys("Test Trial followup")
        element = self.driver.find_element(By.ID, "create_button")
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        actions.click(element)
        actions.perform()

    def test_adminOptions(self):
        elements = self.driver.find_elements(By.ID, "navbarDropdown")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "navbarDropdown").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Create New Sponsor")
        elements = self.driver.find_elements(By.LINK_TEXT, "View Sponsors")
        elements = self.driver.find_elements(By.LINK_TEXT, "View Sponsor Requests")
        self.driver.find_element(By.ID, "navbarDropdown").click()
        self.driver.find_element(By.LINK_TEXT, "Create New Sponsor").click()
        self.driver.find_element(By.ID, "id_organization").click()
        self.driver.find_element(By.ID, "id_organization").send_keys("ClintWin")
        self.driver.find_element(By.ID, "id_location").send_keys("Boston")
        self.driver.find_element(By.ID, "id_contactPerson").send_keys("Adaeze")
        self.driver.find_element(By.ID, "id_email").send_keys("test@rediffmail.com")
        self.driver.find_element(By.ID, "id_phone").send_keys("3333333333")
        self.driver.find_element(By.ID, "id_notes").send_keys("My comments")
        self.driver.find_element(By.ID, "create_button").click()
        self.driver.find_element(By.ID, "navbarDropdown").click()
        self.driver.find_element(By.LINK_TEXT, "View Sponsors").click()