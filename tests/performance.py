from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    def on_start(self):
        self.login()

    def on_stop(self):
        self.logout()

    def login(self):
        response = self.client.get("/accounts/login/")
        csrftoken = response.cookies['csrftoken']
        print(csrftoken)
        self.client.post("/accounts/login/",
                         {"username": "admin", "password": "admin"},
                         headers={"X-CSRFToken": csrftoken})

    def logout(self):
        self.client.get("/accounts/logout/")

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def scoreboard(self):
        self.client.get("/scoreboard/")

    @task(3)
    def challenges(self):
        self.client.get("/challenges/")

    @task(4)
    def challenge(self):
        self.client.get("/challenges/#7")

    @task(5)
    def profile(self):
        self.client.get("/accounts/profile/206")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 1500
