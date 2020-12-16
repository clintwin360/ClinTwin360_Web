from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class TestLogin(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.vars = {}


    def tearDown(self):
        # self.driver.close()
        pass

    def test_adminOptions(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.NAME, "remember").click()
        self.driver.find_element(By.ID, "login_button").click()
        elements = self.driver.find_elements(By.ID, "navbarDropdown")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "Manage Clinical Trials")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "spnsr-btn")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "navbarDropdown").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Create New Sponsor")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "View Sponsors")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "View Criteria Requests")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "View Access Requests")
        assert len(elements) > 0
        self.driver.find_element(By.LINK_TEXT, "Manage Clinical Trials").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Create New Clinical Trial")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "View Clinical Trials")
        assert len(elements) > 0
        self.driver.find_element(By.CSS_SELECTOR, "main").click()
        try:
            self.driver.find_element(By.ID, "logout_link").click()
        except NoSuchElementException:
            pass
        self.driver.close()
        self.driver.quit()


    def test_sponsorOptions(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element(By.ID, "id_username").send_keys("amsterdam")
        self.driver.find_element(By.ID, "id_password").send_keys("redlight")
        self.driver.find_element(By.NAME, "remember").click()
        self.driver.find_element(By.ID, "login_button").click()
        elements = self.driver.find_elements(By.ID, "navbarDropdown")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "navbarDropdown").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "Create New Clinical Trial")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "View Clinical Trials")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "dashboard-trial-cards").click()
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".card-footer")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".col-lg-6:nth-child(2) > .trial-cards")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "dropdownMenuLink").click()
        elements = self.driver.find_elements(By.ID, "start-trial-link")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "criteria-trial-link")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "update-trial-link")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "delete-trial-link")
        assert len(elements) > 0
        self.driver.find_element(By.CSS_SELECTOR, ".col-lg-6:nth-child(2) > #selected-trial-header").click()
        try:
            self.driver.find_element(By.ID, "logout_link").click()
        except NoSuchElementException:
            pass
        self.driver.close()
        self.driver.quit()

    def test_createSponsor(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.NAME, "remember").click()
        self.driver.find_element(By.ID, "login_button").click()
        self.driver.find_element(By.ID, "spnsr-btn").click()
        self.driver.find_element(By.ID, "id_organization").click()
        self.driver.find_element(By.ID, "id_organization").send_keys("Test_org")
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys("Tes_loc")
        self.driver.find_element(By.ID, "id_contactPerson").click()
        self.driver.find_element(By.ID, "id_contactPerson").send_keys("Test_contact")
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys("test@test.com")
        self.driver.find_element(By.ID, "id_phone").send_keys("+17817817812")
        self.driver.find_element(By.ID, "id_notes").click()
        self.driver.find_element(By.ID, "id_notes").send_keys("No Comments")
        self.driver.find_element(By.ID, "create_button").click()
        try:
            self.driver.find_element(By.ID, "logout_link").click()
        except NoSuchElementException:
            pass
        self.driver.close()
        self.driver.quit()

    def test_testcontactform(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element(By.ID, "contact_us").click()
        self.driver.find_element(By.ID, "id_organization").click()
        self.driver.find_element(By.ID, "id_organization").send_keys("Test_Org")
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys("Test_org_location")
        self.driver.find_element(By.ID, "id_first_name").click()
        self.driver.find_element(By.ID, "id_first_name").send_keys("Test")
        self.driver.find_element(By.ID, "id_last_name").click()
        self.driver.find_element(By.ID, "id_last_name").send_keys("Last")
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys("test@test.org")
        self.driver.find_element(By.ID, "id_phone").click()
        self.driver.find_element(By.ID, "id_phone").send_keys("+17817817811")
        self.driver.find_element(By.ID, "id_comment").click()
        self.driver.find_element(By.ID, "id_comment").send_keys("Test_Comments")
        self.driver.find_element(By.ID, "create_button").click()

    def test_testaddtrial(self):
        self.driver.get("http://127.0.0.1:8000/sponsor/accounts/login/")
        self.driver.find_element(By.ID, "id_username").send_keys("amsterdam")
        self.driver.find_element(By.ID, "id_password").send_keys("redlight")
        self.driver.find_element(By.NAME, "remember").click()
        self.driver.find_element(By.ID, "login_button").click()
        self.driver.find_element(By.ID, "navbarDropdown").click()
        self.driver.find_element(By.LINK_TEXT, "Create New Clinical Trial").click()
        self.driver.find_element(By.ID, "id_custom_id").click()
        self.driver.find_element(By.ID, "id_custom_id").send_keys("Test_trial")
        self.driver.find_element(By.ID, "id_title").send_keys("Test_title")
        elements = self.driver.find_elements(By.ID, "id_is_virtual")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "id_url").click()
        self.driver.find_element(By.ID, "id_url").send_keys("https://google.com")
        self.driver.find_element(By.CSS_SELECTOR, "#div_id_recruitmentStartDate .glyphicon").click()
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > .day:nth-child(3)").click()
        self.driver.find_element(By.CSS_SELECTOR, "#div_id_recruitmentEndDate .input-group-text").click()
        self.driver.find_element(By.CSS_SELECTOR, ".today").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").send_keys("500")
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys("Test_location")
        self.driver.find_element(By.ID, "id_objective").click()
        self.driver.find_element(By.ID, "id_objective").send_keys("Test_Objective")
        self.driver.find_element(By.ID, "create_button").click()
        self.driver.find_element(By.ID, "criteria-lookup").click()
        self.driver.find_element(By.ID, "ui-id-2").click()
        self.driver.find_element(By.ID, "criteria-lookup").send_keys("tobacco")
        self.driver.find_element(By.ID, "add_btn").click()
        element = self.driver.find_element(By.ID, "add_btn")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.ID, "select2-criteria-value-container").click()
        self.driver.find_element(By.ID, "select2-criteria-value-container").click()
        self.driver.find_element(By.ID, "criteria-submit-button").click()
        self.driver.find_element(By.LINK_TEXT, "Exclusion Criteria").click()
        self.driver.find_element(By.ID, "criteria-lookup").click()
        self.driver.find_element(By.ID, "ui-id-2").click()
        self.driver.find_element(By.ID, "criteria-lookup").click()
        self.driver.find_element(By.ID, "criteria-lookup").send_keys("pregnant")
        self.driver.find_element(By.ID, "add_btn").click()
        element = self.driver.find_element(By.ID, "add_btn")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.ID, "select2-criteria-value-container").click()
        self.driver.find_element(By.ID, "criteria-submit-button").click()
        self.driver.find_element(By.LINK_TEXT, "Review Criteria").click()
        self.driver.find_element(By.LINK_TEXT, "Continue").click()
        self.driver.find_element(By.ID, "greeting").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

    def test_teststartendtrial(self):
        self.driver.get("http://127.0.0.1:8000/sponsor/")
        self.driver.find_element(By.ID, "id_password").send_keys("qftQk4hEQS6DhtM")
        self.driver.find_element(By.ID, "id_username").send_keys("amsterdam")
        self.driver.find_element(By.ID, "id_password").send_keys("redlight")
        self.driver.find_element(By.NAME, "remember").click()
        self.driver.find_element(By.ID, "login_button").click()
        self.driver.find_element(By.CSS_SELECTOR, "#trial-card-7 .card-title").click()
        self.driver.find_element(By.ID, "dropdownMenuLink").click()
        self.driver.find_element(By.ID, "start-trial-link").click()
        element = self.driver.find_element(By.ID, "start-trial-link")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()
        self.driver.find_element(By.ID, "dropdownMenuLink").click()
        self.driver.find_element(By.ID, "end-trial-link").click()
        self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()
        self.driver.find_element(By.ID, "dropdownMenuLink").click()
        self.driver.find_element(By.ID, "delete-trial-link").click()
        self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()
        self.driver.find_element(By.CSS_SELECTOR, ".swal2-confirm").click()
        self.driver.find_element(By.ID, "greeting").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

    def test_aboutus(self):
        self.driver.get("http://127.0.0.1:8000/sponsor/accounts/login/")
        self.driver.find_element(By.ID, "contact_us").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "info@clintwin.com")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.ID, "contact_us")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "navbarDropdown").click()
        elements = self.driver.find_elements(By.LINK_TEXT, "About Us")
        assert len(elements) > 0
        elements = self.driver.find_elements(By.LINK_TEXT, "How Does It Works")
        assert len(elements) > 0
        self.driver.find_element(By.LINK_TEXT, "About Us").click()
        self.driver.find_element(By.ID, "navbarDropdown").click()
        self.driver.find_element(By.LINK_TEXT, "How Does It Works").click()

    def test_addsponsoraccount(self):
        self.driver.get("http://127.0.0.1:8000/sponsor/viewsponsors")
        self.driver.find_element(By.ID, "id_password").send_keys("qftQk4hEQS6DhtM")
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.NAME, "remember").click()
        self.driver.find_element(By.ID, "login_button").click()
        self.driver.find_element(By.LINK_TEXT, "View").click()
        self.driver.find_element(By.LINK_TEXT, "Add Account").click()
        self.driver.find_element(By.ID, "id_username").click()
        self.driver.find_element(By.ID, "id_username").send_keys("test_username")
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys("test@test.com")
        self.driver.find_element(By.ID, "id_first_name").send_keys("Name")
        self.driver.find_element(By.ID, "id_last_name").send_keys("Last_name")
        self.driver.find_element(By.ID, "create_button").click()
        self.driver.find_element(By.ID, "greeting").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

    def test_editsponsor(self):
        self.driver.get("http://127.0.0.1:8000/sponsor/viewsponsors")
        self.driver.find_element(By.ID, "id_password").send_keys("qftQk4hEQS6DhtM")
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        self.driver.find_element(By.LINK_TEXT, "Edit").click()
        self.driver.find_element(By.CSS_SELECTOR, "main > .container-fluid").click()
        self.driver.find_element(By.ID, "id_phone").send_keys("+17817817811")
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys("Amsterdam_test")
        self.driver.find_element(By.ID, "id_notes").click()
        self.driver.find_element(By.ID, "id_notes").send_keys("Test Koningsdag")
        self.driver.find_element(By.ID, "edit_button").click()
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(8)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(8)").text == "Phone: +17817817811"
        self.driver.find_element(By.LINK_TEXT, "Return to Dashboard").click()
        self.driver.find_element(By.ID, "greeting").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

    def test_accessRequest(self):
        self.driver.get("http://127.0.0.1:8000/sponsor/viewsponsors")
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        self.driver.find_element(By.ID, "navbarDropdown").click()
        self.driver.find_element(By.LINK_TEXT, "View Access Requests").click()
        self.driver.find_element(By.LINK_TEXT, "Close Request").click()
        self.driver.find_element(By.ID, "contact-list-title").click()
        assert self.driver.find_element(By.ID, "contact-list-title").text == "Sponsor Access Request Dashboard"
        self.driver.find_element(By.ID, "greeting").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()

    def test_forgotPassword(self):
        self.driver.get("http://127.0.0.1:8000/sponsor/accounts/login/")
        self.driver.find_element(By.LINK_TEXT, "Forgot password?").click()
        self.driver.find_element(By.ID, "id_email").click()
        self.driver.find_element(By.ID, "id_email").send_keys("test@test.com")
        self.driver.find_element(By.CSS_SELECTOR, ".reset_btn").click()
        self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(1)").click()
        assert self.driver.find_element(By.LINK_TEXT, "We\'ve emailed you the link for resetting your password. In case the email does not arrive in a few minutes, please check your spam folder.").text == "We\\\'ve emailed you the link for resetting your password. In case the email does not arrive in a few minutes, please check your spam folder."

    def test_testadmincreatesponsor(self):
        self.driver.get("http://127.0.0.1:8000/sponsor/viewsponsors")
        self.driver.find_element(By.ID, "id_password").send_keys("qftQk4hEQS6DhtM")
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.NAME, "remember").click()
        self.driver.find_element(By.ID, "login_button").click()
        self.driver.find_element(By.LINK_TEXT, "Manage Clinical Trials").click()
        self.driver.find_element(By.LINK_TEXT, "Create New Clinical Trial").click()
        self.driver.find_element(By.ID, "id_custom_id").click()
        self.driver.find_element(By.ID, "id_custom_id").send_keys("Test_admin_trial")
        self.driver.find_element(By.ID, "id_sponsor").click()
        dropdown = self.driver.find_element(By.ID, "id_sponsor")
        dropdown.find_element(By.XPATH, "//option[. = '1,Academisch Medisch Centrum - Universiteit van Amsterdam (AMC-UvA)']").click()
        self.driver.find_element(By.ID, "id_title").click()
        self.driver.find_element(By.ID, "id_title").send_keys("Test_admin_trial")
        elements = self.driver.find_elements(By.ID, "id_is_virtual")
        assert len(elements) > 0
        self.driver.find_element(By.ID, "id_url").click()
        self.driver.find_element(By.ID, "id_url").send_keys("https://google.com")
        self.driver.find_element(By.CSS_SELECTOR, "#div_id_recruitmentStartDate .glyphicon").click()
        self.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(2) > .day:nth-child(3)").click()
        self.driver.find_element(By.CSS_SELECTOR, "#div_id_recruitmentEndDate .glyphicon").click()
        self.driver.find_element(By.CSS_SELECTOR, ".today").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").click()
        self.driver.find_element(By.ID, "id_enrollmentTarget").send_keys("501")
        self.driver.find_element(By.ID, "id_location").click()
        self.driver.find_element(By.ID, "id_location").send_keys("Test_admin_location")
        self.driver.find_element(By.ID, "id_objective").click()
        self.driver.find_element(By.ID, "id_objective").send_keys("Test Objective")
        self.driver.find_element(By.ID, "create_button").click()
        self.driver.find_element(By.ID, "add_btn").click()
        self.driver.find_element(By.ID, "criteria-lookup").click()
        self.driver.find_element(By.ID, "ui-id-3").click()
        self.driver.find_element(By.ID, "criteria-lookup").send_keys("pregnant")
        self.driver.find_element(By.ID, "add_btn").click()
        element = self.driver.find_element(By.ID, "add_btn")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.ID, "select2-criteria-value-container").click()
        self.driver.find_element(By.ID, "criteria-submit-button").click()
        self.driver.find_element(By.LINK_TEXT, "Exclusion Criteria").click()
        self.driver.find_element(By.ID, "criteria-lookup").click()
        self.driver.find_element(By.ID, "ui-id-6").click()
        self.driver.find_element(By.ID, "criteria-lookup").send_keys("last doctor vist")
        self.driver.find_element(By.ID, "add_btn").click()
        element = self.driver.find_element(By.ID, "add_btn")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions = ActionChains(self.driver)
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.ID, "select2-criteria-value-container").click()
        self.driver.find_element(By.ID, "criteria-submit-button").click()
        self.driver.find_element(By.LINK_TEXT, "Review Criteria").click()
        self.driver.find_element(By.LINK_TEXT, "Continue").click()
        self.driver.find_element(By.ID, "greeting").click()
        self.driver.find_element(By.LINK_TEXT, "Logout").click()