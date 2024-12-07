from customerService.env import url

class Auth:
    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.host = self.get_host()
        self.app_secret = app_secret

    def get_host(self):
        """Obtain the corresponding domain name that the customer needs to use based on the app_key

        :return: host
        """
        return url
        # return 'http://127.0.0.1:33300'
