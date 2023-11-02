from locust import HttpUser, task, constant
import server


class UserTask(HttpUser):
    abstract = True
    wait_time = constant(0.1)

    @task
    def index(self):
        self.client.get('/')

    @task
    def show_summary(self):
        self.client.post(
            '/showSummary',
            {'email': self.club['email']}
        )

    @task
    def book(self):
        self.client.get(
            f"/book/{self.competition['name']}/{self.club['name']}"
        )

    @task
    def purchase_places(self):
        self.client.post(
            '/purchasePlaces',
            {
                'competition': self.competition['name'],
                'club': self.club['name'],
                'places': 1
            }
        )

    @task
    def logout(self):
        self.client.get('/logout')

    @task
    def clubs_points(self):
        self.client.get('/clubsPoints')


class TestUser1(UserTask):
    def on_start(self):
        self.competition = server.competitions[0]
        self.club = server.clubs[0]


class TestUser2(UserTask):
    def on_start(self):
        self.competition = server.competitions[0]
        self.club = server.clubs[1]


class TestUser3(UserTask):
    def on_start(self):
        self.competition = server.competitions[0]
        self.club = server.clubs[2]
