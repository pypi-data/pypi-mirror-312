# coding="utf-8"

# create log object
import logging
import datetime

if 1:
    logger = logging.getLogger("ezconfig_client1")

    def my_error_log(*args):
        msg = " ".join(
            [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            + [str(x) for x in args]
        )
        logger.error(msg)


try:
    from ezconfig_client import loader
except Exception as e:
    # print(f"ezconfig_client not found, error: {e}")
    # python log
    my_error_log(f"ezconfig_client not found, error: {e}")


class Query(object):
    def __init__(self, env, app_id, secret, url):
        self.env = env
        self.app_id = app_id
        self.secret = secret
        self.url = url

    def get_config(self):
        res = loader.get_latest_config_by_params(
            self.env, self.app_id, self.secret, self.url
        )
        return res
