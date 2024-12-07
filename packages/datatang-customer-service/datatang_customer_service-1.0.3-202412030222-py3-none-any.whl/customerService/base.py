import hashlib
import time

from customerService.auth import Auth


class Base:
    def __init__(self, auth: Auth):
        self.app_key = auth.app_key
        self.app_secret = auth.app_secret
        self.host = auth.get_host()
        self.app_id = "66CC4C2C0F8E11EBB4777CD30ADBB1A4"

    def get_header(self, **kwargs: dict):
        nonce = self._create_nonce()
        return {
            "appKey": self.app_key,
            "appSecret": self.app_secret,
            "appId": self.app_id,
            "nonce": str(nonce),
            "sign": self._create_sign(nonce, **kwargs),
        }

    def _create_nonce(self):
        """13-digit UNIX timestamp, valid within 10 minutes, for example 1654842893791.

        :return: 13-digit UNIX timestamp
        """
        return int(time.time()) * 1000

    def _create_sign(self, nonce: int, **kwargs: dict):
        """Signature, signature calculation method: md5(param={param}&secert={secert}&nonce={nonce}),
        param is the result value of all parameters of the current request sorted and combined according to the key.

        :param nonce: 13-digit UNIX timestamp
        :param args: Parameters for each request
        :return: md5(param={param}&secert={secert}&nonce={nonce})
        """
        sorted_dict = dict(sorted(kwargs.items()))
        param = ""
        for k, v in sorted_dict.items():
            param = param + (k + "=" + str(v) + "&")
        sign = param + "appSecret=" + self.app_secret + "&nonce=" + str(nonce)
        return self._md5_hash(sign)

    def _md5_hash(self, string: str):
        """Create an MD5 encrypted object

        :param string: sign
        :return:
        """
        hash_object = hashlib.md5()

        # encode
        hash_object.update(string.encode("utf-8"))
        md5_hash = hash_object.hexdigest()
        return md5_hash
