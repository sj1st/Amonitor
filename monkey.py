import socket
import threading

class Monkey:
    def __init__(self, url):
        self.lock = threading.Lock()
        self.url = url
        self.s = None
        urllist = url.split(':')
        port = int(urllist[-1])
        host = urllist[-2][2:]
        for res in socket.getaddrinfo(host, port,
                socket.AF_UNSPEC,
                socket.SOCK_STREAM,
                flags=socket.NI_NUMERICSERV):
            af, socktype, proto, canonname, sa = res
            try:
                s = socket.socket(af, socktype, proto)
            except OSError as msg:
                s = None
                continue
            try:
                s.connect(sa)
            except OSError as msg:
                s.close()
                s = None
                continue

        if s is None:
            print('could not open monkey url:', url)
            raise OSError
        else:
            s.settimeout(1)
        self.s = s

    def sendEvent(self, cmd):
        with self.lock:
            ret = 'FAILED'
            try:
                self.s.sendall(bytes(cmd + '\n', 'utf-8'))
                data = self.s.recv(1024)
                ret = data.decode('utf-8')[0:-1]
            except:
                pass
            finally:
                return ret

    def touchDown(self, x, y):
        ret = self.sendEvent('touch down {} {}'.format(x, y))
        if ret != 'OK':
            print('touch down', x, y, ret)

    def touchUp(self, x, y):
        ret = self.sendEvent('touch up {} {}'.format(x, y))
        if ret != 'OK':
            print('touch up', x, y, ret)

    def touchMove(self, x, y):
        ret = self.sendEvent('touch move {} {}'.format(x, y))
        if ret != 'OK':
            print('touch move', x, y, ret)

    def touch(self, x, y):
        ret = self.sendEvent('tap {} {}'.format(x, y))
        if ret != 'OK':
            print('touch', x, y, ret)

    def rotate(self, degree):
        ret = self.sendEvent('rotate {} true'.format(degree))
        if ret != 'OK':
            print('rotate', degree, ret)

    def scroll(self, dx, dy):
        ret = self.sendEvent('trackball {} {}'.format(dx, dy))
        if ret != 'OK':
            print('scroll', dx, dy, ret)

    def press(self, keyname):
        ret = self.sendEvent('press {}'.format(keyname))
        if ret != 'OK':
            print('press', keyname, ret)

    def keyDown(self, keyname):
        ret = self.sendEvent('key down {}'.format(keyname))
        if ret != 'OK':
            print('key down', keyname, ret)

    def keyUp(self, keyname):
        ret = self.sendEvent('key up {}'.format(keyname))
        if ret != 'OK':
            print('key up', keyname, ret)

    def type(self, string):
        ret = self.sendEvent('type {}'.format(string))
        if ret != 'OK':
            print('type', string, ret)

    def quit(self):
        ret = self.sendEvent('quit')
        if ret != 'OK':
            print('quit', ret)

    def getvar(self, var):
        ret = self.sendEvent('getvar {}'.format(var))
        if ret[0:3] == 'OK:':
            return ret[3:]
        return ret
