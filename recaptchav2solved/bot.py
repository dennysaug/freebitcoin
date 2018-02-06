import requests
import time

class RecaptchaV2Solved:
    #key = key 2captcha
    def __init__(self, key):
        self.key = key
        self.request = 'http://2captcha.com/in.php'
        self.response = 'http://2captcha.com/res.php'

    def solve(self, googlekey, site):

        payload = {'key' : self.key, 'method' : 'userrecaptcha', 'googlekey' : googlekey, 'pageurl' : site}
        req = requests.get(self.request, params=payload)
        req = req.content.split('|')

        if req[0] == 'OK':
            idRequest = req[1]
            payload = {'key' : self.key, 'action' : 'get', 'id': idRequest}
            wait = True
            while wait:
                time.sleep(15)
                res = requests.get(self.response, params=payload)
                res = res.content.split('|')
                if res[0] == 'OK':
                    wait = False
                    return res[1]
                else:
                    print '[*] Waiting Solve Captcha'

        return False