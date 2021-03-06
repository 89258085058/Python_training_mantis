from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("manage_proj_page.php")):
            wd.get(self.app.base_url + "manage_proj_page.php")

    def create(self, project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element_by_css_selector('input[value="Create New Project"]').click()
        self.fill_project_form(project)
        wd.find_element_by_css_selector('input[value="Add Project"]').click()


    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    project_cache = None

    def get_project_list(self):
        wd = self.app.wd
        self.open_project_page()
        self.project_cache = []
        for element in wd.find_elements_by_xpath("//td/a[contains(@href,'manage_proj_edit_page.php?project_id=')]"):
            text = element.text
            id = element.get_attribute("href").replace(self.app.base_url + "manage_proj_edit_page.php?project_id=", '')
            self.project_cache.append(Project(name=text, id = id))
        return list(self.project_cache)

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_project_page()
        self.select_project_by_id(id)
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()
        wd.find_element_by_css_selector('input[value="Delete Project"]').click()


    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.get(self.app.base_url + "manage_proj_edit_page.php?project_id="+id)