import random
import string
from model.project import Project


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def test_delete_project(app):
    # app.session.login("administrator", "root")
    if app.project.count_projects() == 0:
        project = Project(project_name=random_string("name", 10), description=random_string("description", 10))
        app.project.add_project(project)
    old_list = app.project.get_project_list()
    project = random.choice(old_list)
    app.project.delete_project(project)
    new_list = app.project.get_project_list()
    old_list.remove(project)
    assert sorted(new_list, key=Project.id_or_max) == sorted(old_list, key=Project.id_or_max)
