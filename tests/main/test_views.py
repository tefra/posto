from tests.utils import ViewTestCase


class ViewTests(ViewTestCase):
    def test_home(self):
        expected = {"code": 200, "description": "I am posto: 1.0.0", "status": "OK"}
        response = self.client.get("/")
        self.assertEqual(expected, response.json)

    def test_http_errors(self):
        expected = {
            "code": 404,
            "description": "The requested URL was not found on the server. If you entered "
            "the URL manually please check your spelling and try again.",
            "status": "Not Found",
        }
        response = self.client.get("/unknown/")
        self.assertEqual(expected, response.json)

    def test_unhandled_errors(self):
        secret = self.client.application.config["GITLAB_SECRET"]
        response = self.client.post(
            "/webhook/",
            content_type="application/json",
            data="{}",
            headers={"X-Gitlab-Token": secret},
        )
        expected = {
            "code": 500,
            "description": "Something's broken, something's broken, it's your fault!",
            "status": "Internal Server Error",
        }
        self.assertEqual(expected, response.json)
