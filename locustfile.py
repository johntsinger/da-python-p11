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
        """Response will be 400 when there are no more places available
        in this competition, so we consider 400 to be a success.
        """
        with self.client.post(
            '/purchasePlaces',
            {
                'competition': self.competition['name'],
                'club': self.club['name'],
                'places': 1
            },
            catch_response=True
        ) as response:
            if response.status_code == 400:
                response.success()

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
