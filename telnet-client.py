import telnetlib
import time

USER = 'freek'
PWD = '123'

HOST = '192.168.86.27'

if __name__ == '__main__':
    with telnetlib.Telnet(HOST) as tn:
        tn.read_until(b"login: ")
        tn.write(USER.encode('ascii') + b'\n')
        tn.read_until(b"password: ")
        tn.write(PWD.encode('ascii') + b'\n')

        while True:
            tn.write(b'test\n')
            time.sleep(3)
