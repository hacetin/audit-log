import random
from datetime import datetime

from locust import HttpUser, task, constant


class AuditLogUser(HttpUser):
    wait_time = constant(0)

    host = "http://example.com"

    auth = ("admin", "password")
    event_types = ["test_event1", "test_event2", "test_event3"]
    str_values = ["test_str_value1", "test_str_value2", "test_str_value2"]
    now = datetime.now()
    time_format = "%Y%m%dT%H%M%S.%fZ"
    datetimes = [
        now.strftime(time_format),
        datetime.fromtimestamp(now.timestamp() + 10).strftime(time_format),
        datetime.fromtimestamp(now.timestamp() + 100).strftime(time_format),
        datetime.fromtimestamp(now.timestamp() + 1000).strftime(time_format),
    ]

    @task(10)
    def test_write(self):
        self.client.post(
            "/write",
            json={
                "event_type": random.choice(self.event_types),
                "event_fields": {
                    "test_str_field": random.choice(self.str_values),
                    "test_int_field": random.randint(1, 1000),
                },
            },
            auth=self.auth,
        )

    @task
    def test_search_without_time_stop(self):
        self.client.get(
            "/search",
            json={
                "event_type": random.choice(self.event_types),
                "time_start": random.choice(self.datetimes),
                "query_params": {
                    "test_str_field": random.choice(self.str_values),
                    "test_int_field": random.randint(1, 1000),
                },
            },
            auth=self.auth,
        )

    @task
    def test_search_with_time_stop(self):
        three_sec_ago = datetime.fromtimestamp(datetime.now().timestamp() - 3000).strftime(self.time_format)
        self.client.get(
            "/search",
            json={
                "event_type": random.choice(self.event_types),
                "time_start": random.choice(self.datetimes),
                "time_stop": random.choice([self.datetimes[-1], three_sec_ago]),
                "query_params": {
                    "test_str_field": random.choice(self.str_values),
                    "test_int_field": random.randint(1, 1000),
                },
            },
            auth=self.auth,
        )


def on_start(self):
    self.client.post("/login", {"username": "foo", "password": "bar"})
