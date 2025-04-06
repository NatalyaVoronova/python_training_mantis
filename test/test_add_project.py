import random
import string
from model.project import Project


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for _ in range(random.randrange(maxlen))])


def test_add_project(app):
    # app.session.login("administrator", "root")
    old_list = app.project.get_project_list()
    project = Project(project_name=random_string("name", 10), description=random_string("description", 10))
    app.project.add_project(project)
    new_list = app.project.get_project_list()
    old_list.append(project)
    assert len(old_list) == len(new_list)
    assert sorted(new_list, key=Project.id_or_max) == sorted(old_list, key=Project.id_or_max)


def test_add_project_soap(app):
    old_projects_list = app.soap.get_project_list_soap()
    project_new = Project(project_name=random_string("name", 10), description=random_string("description", 10))
    app.project.add_project(project_new)
    new_projects_list = app.soap.get_project_list_soap()
    old_projects_list.append(project_new)
    assert sorted(old_projects_list, key=Project.id_or_max) == sorted(new_projects_list, key=Project.id_or_max)
