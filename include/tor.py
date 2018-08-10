import os
import time
import socks
import socket
import subprocess

class TorManager(object):

    def __init__(self):
        self.dev_null = open(os.devnull, 'w')

    def install_tor(self):
        subprocess.call(['clear'])
        print '{0}[{1}-{0}]{2} Installing Tor, Please Wait {3}...{2}'.format(self.y, self.r, self.n, self.g);time.sleep(3)
        cmd = ['apt-get', 'install', 'tor', '-y']
        subprocess.Popen(cmd, stdout=self.dev_null, stderr=self.dev_null).wait()

    def restart_tor(self):
        cmd = ['service', 'tor', 'restart']
        subprocess.Popen(cmd, stdout=self.dev_null, stderr=self.dev_null).wait()
        time.sleep(.5)

    def stop_tor(self):
        cmd = cmd = ['service','tor','stop']
        subprocess.Popen(cmd,stdout=self.devnull,stderr=self.devnull).wait()

    def update_ip(self):
        self.restart_tor()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050, True)
        socket.socket = socks.socksocket