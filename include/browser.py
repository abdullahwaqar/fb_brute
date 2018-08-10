import json
import random
import requests
import cookielib
import mechanize

class Browser(object):

    def __init__(self):
        self.br = None

    def create_browser(self):
        br = mechanize.Browser()
        br.set_handle_equiv(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_cookiejar(cookielib.LWPCookieJar())
        br.addheaders=[('User-agent',self.useragent())]
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
        self.br = br

    def delete_browser(self):
        self.br.close()
        del self.br

    def getIp(self):
        try:
          return json.loads(requests.get('https://api.ipify.org/?format=json').text)['ip']
        except KeyboardInterrupt:self.kill()
        except:
            pass

    def exists(self, name):
        pass

    def login(self, username, password):
        if any([not self.alive, self.isFound]):
            return

        try:
            self.display(password)
            self.br.open(self.url)
            self.br.select_form(nr=0)
            self.br.form['email'] = username
            self.br.form['pass'] = password
            return self.br.submit().read()
        except KeyboardInterrupt:
                self.kill()
        except:
            return