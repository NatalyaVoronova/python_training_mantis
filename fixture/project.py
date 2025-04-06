import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    project_cache = None

    def open_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_page.php"):
            wd.find_element_by_link_text("Manage").click()
            wd.find_element_by_link_text("Manage Projects").click()

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            # group_list = []
            self.project_cache = []
            wait = WebDriverWait(self.app.wd, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//table[@class='width100' and @cellspacing=1]")))
            projects = wd.find_elements_by_xpath("//table[3]/tbody/tr")[2:]
            for each in projects:
                project = each.find_elements_by_css_selector("td")
                address = project[0].find_element_by_tag_name("a").get_attribute("href")
                project_id_str = re.search("id=.*", address).group(0)
                project_id = project_id_str[3:len(project_id_str)]
                project_name = project[0].text
                project_description = project[4].text
                self.project_cache.append(Project(project_id=project_id, project_name=project_name, description=project_description))
            return list(self.project_cache)  # group_list

    def count_projects(self):
        wd = self.app.wd
        self.open_projects_page()
        try:
            l = len(wd.find_elements_by_xpath("//table[3]/tbody/tr")) - 2
        except:
            l = 0
        return l

    def add_project(self, project):
        wd = self.app.wd
        self.open_projects_page()
        wd.find_element_by_css_selector('[value="Create New Project"]').click()
        self.fill_form(project)
        wd.find_element_by_css_selector('[value="Add Project"]').click()
        self.project_cache = None

    def fill_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.project_name)
        self.change_field_value('description', project.description)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def delete_project(self, project):
        wd = self.app.wd
        self.open_projects_page()
        project_link = wd.find_element_by_xpath(f"//a[contains(@href, 'id={project.project_id}')]")
        project_link.click()
        wd.implicitly_wait(2)
        wd.find_element_by_css_selector("input.button[value='Delete Project']").click()
        wd.implicitly_wait(2)
        wd.find_element_by_css_selector("input.button[value='Delete Project']").click()
        self.project_cache = None
