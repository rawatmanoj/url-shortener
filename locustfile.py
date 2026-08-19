from locust import HttpUser, task, between, constant


class URLShortenerUser(HttpUser):
    wait_time = constant(0)

    @task
    def redirect(self):
        # self.client.get("/abc123",allow_redirects=False)
        self.client.get("/slow")
        # self.client.get("/cpu")