from suds.client import Client
from suds import WebFault  # выбрасывается исключение, если что-то пошло не так
from model.project import Project


class SoapHelper:

    def __init__(self, app):
        self.app = app

    def can_login(self, username, password):
        client = Client(self.app.base_url + 'api/soap/mantisconnect.php?wsdl')

        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list_soap(self):
        client = Client(self.app.base_url + '/api/soap/mantisconnect.php?wsdl')
        try:
            list_projects = client.service.mc_projects_get_user_accessible(self.app.config["webadmin"]["username"],
                                                                           self.app.config["webadmin"]["password"])
            projects = []
            for project in list_projects:
                projects.append(Project(project_id=project.id, project_name=project.name, description=project.description))
            return projects or []
        except WebFault:
            return False
