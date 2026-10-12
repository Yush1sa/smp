from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
from decimal import Decimal
from generator_ts.models import Project, ProjectStage, StageTask


# Create your tests here.
class ProjectViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.manager = User.objects.create_user(
            username='manager_test',
            password='password123'
        )

        self.customer = User.objects.create_user(
            username='customer_test',
            password='password123'
        )

    def test_get_list(self):

        project = baker.make('generator_ts.project')

        r = self.client.get('/api/projects/')
        data = r.json()
        print(data)

        assert project.title == data[0]['title']
        assert project.dbeg.isoformat() == data[0]['dbeg']
        assert project.dend.isoformat() == data[0]['dend']

    def test_create_project(self):
            r = self.client.post('/api/projects/', data={
                "title": "Test project",
                "dbeg": "2026-10-07",
                "dend": "2026-10-08",
                "structure_code": 123,
                "kosgu": 456,
                "kps": 789,
                "summ_application": 1000,
                "funding_article": "article",
                "reflect_method": "method",
                "manager": self.manager.id,
                "customer": self.customer.id,
            })

            new_project_id = r.json()['id']

            projects = Project.objects.all()
            assert len(projects) == 1

            new_project = Project.objects.filter(pk=new_project_id).first()
            assert new_project.title == "Test project"
            assert new_project.dbeg.isoformat() == "2026-10-07"
            assert new_project.dend.isoformat() == "2026-10-08"
            assert new_project.customer == self.customer

    def test_delete_project(self):
        projects = baker.make('generator_ts.project', 10)
        r = self.client.get('/api/projects/')
        data = r.json()
        assert len(data) == 10

        project_id_to_delete = projects[3].id
        self.client.delete(f'/api/projects/{project_id_to_delete}/')

        r=self.client.get('/api/projects/')
        data = r.json()
        assert len(data) == 9

        assert project_id_to_delete not in [i['id'] for i in data]

    def test_update_project(self):
        projects = baker.make('generator_ts.project', 10)
        project: Project = projects[3]

        r = self.client.get(f'/api/projects/{project.id}/')
        data = r.json()
        print(data)
        assert data['title'] == project.title

        r = self.client.patch(f'/api/projects/{project.id}/', {
            'title': 'New title',
        })

        assert r.status_code == 200

        r = self.client.get(f'/api/projects/{project.id}/')
        data = r.json()
        assert data['title'] == "New title"

        project.refresh_from_db()
        assert data['title'] == project.title


class ProjectStageViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_get_list(self):
        project = baker.make('generator_ts.project')

        stage = baker.make('generator_ts.ProjectStage', project=project)

        r = self.client.get('/api/stages/')
        data = r.json()

        assert stage.title == data[0]['title']
        assert stage.executor_deadline.isoformat() == data[0]['executor_deadline']
        assert stage.customer_deadline.isoformat() == data[0]['customer_deadline']
        assert stage.result == data[0]['result']
        assert stage.material_result == data[0]['material_result']
        assert stage.project_id == data[0]['project']

    def test_create_stage(self):
        project = baker.make('generator_ts.project')

        r = self.client.post('/api/stages/', {
            "stage_number": 1,
            "title": "Test stage",
            "executor_deadline": "2026-10-07",
            "customer_deadline": "2026-10-08",
            "result": "test result",
            "material_result": "link gitlab",
            "project": project.id,
        })

        new_stage_id = r.json()['id']

        stages = ProjectStage.objects.all()
        assert len(stages) == 1

        new_stage = ProjectStage.objects.filter(id=new_stage_id).first()
        assert new_stage.title == "Test stage"
        assert new_stage.stage_number == 1
        assert new_stage.material_result == "link gitlab"
        assert new_stage.project == project

    def test_delete_stage(self):
        stages = baker.make('generator_ts.ProjectStage', 10)
        r = self.client.get('/api/stages/')
        data = r.json()
        assert len(data) == 10

        stage_id_to_delete = stages[3].id
        self.client.delete(f'/api/stages/{stage_id_to_delete}/')

        r = self.client.get('/api/stages/')
        data = r.json()
        assert len(data) == 9

        assert stage_id_to_delete not in [i['id'] for i in data]

    def test_update_stage(self):
        stages = baker.make('generator_ts.ProjectStage', 10)
        stage: ProjectStage = stages[2]

        r = self.client.get(f'/api/stages/{stage.id}/')
        data = r.json()
        print(data)
        assert data['title'] == stage.title

        r = self.client.patch(f'/api/stages/{stage.id}/',{
            'title': 'New title'
        })

        assert r.status_code == 200

        r = self.client.get(f'/api/stages/{stage.id}/')
        data = r.json()
        assert data['title'] == "New title"

        stage.refresh_from_db()
        assert stage.title == "New title"

class StageTaskViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.executor = User.objects.create_user(
            username='executor_test',
            password='password123'
        )

    def test_get_list(self):
        stage = baker.make('generator_ts.ProjectStage')
        task = baker.make(
            'generator_ts.StageTask',
            stage=stage,
            executor=self.executor,
        )

        r = self.client.get('/api/tasks/')
        data = r.json()
        print(data)

        assert task.task_number == data[0]['task_number']
        assert Decimal(data[0]['cost']) == task.cost
        assert task.description == data[0]['description']
        assert task.stage_id == data[0]['stage']
        assert task.executor_id == data[0]['executor']

    def test_create_task(self):
        stage = baker.make('generator_ts.ProjectStage')

        r = self.client.post('/api/tasks/', {
            "stage": stage.id,
            "task_number": 1,
            "executor": self.executor.id,
            "cost": "1234.56",
            "description": "Test task",
        })

        assert r.status_code == 201, r.json()

        new_task_id = r.json()['id']

        tasks = StageTask.objects.all()
        assert len(tasks) == 1

        new_task = StageTask.objects.filter(pk=new_task_id).first()
        assert new_task.task_number == 1
        assert new_task.cost == Decimal("1234.56")
        assert new_task.description == "Test task"
        assert new_task.stage == stage
        assert new_task.executor == self.executor

    def test_delete_task(self):
        tasks = baker.make('generator_ts.StageTask', 10)
        r = self.client.get('/api/tasks/')
        data = r.json()
        assert len(data) == 10

        task_id_to_delete = tasks[3].id
        self.client.delete(f'/api/tasks/{task_id_to_delete}/')

        r = self.client.get('/api/tasks/')
        data = r.json()
        assert len(data) == 9

        assert task_id_to_delete not in [i['id'] for i in data]

    def test_update_task(self):
        tasks = baker.make('generator_ts.StageTask', 10)
        task: StageTask = tasks[2]

        r = self.client.get(f'/api/tasks/{task.id}/')
        data = r.json()
        assert data['description'] == task.description

        r = self.client.patch(
            f'/api/tasks/{task.id}/',
            {'description': 'New description'},
            format='json',
        )
        assert r.status_code == 200

        r = self.client.get(f'/api/tasks/{task.id}/')
        data = r.json()
        assert data['description'] == "New description"

        task.refresh_from_db()
        assert task.description == "New description"