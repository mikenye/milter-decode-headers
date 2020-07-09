#!/usr/bin/env python

import sys
import syslog
import Milter
from email.header import decode_header

class DecodeHeaders(Milter.Base):

    def __init__(self):  # A new instance with each new connection.

        self.id = Milter.uniqueID()  # Integer incremented with each call.
        self.message_id = "unknown"

    def connect(self, IPname, family, hostaddr):

        syslog.syslog("[%s] connect from %s at %s" % (self.id, IPname, hostaddr))
        self.headers = list()
        
        return Milter.CONTINUE

    def header(self, name, hval):

        if name == "Message-Id":
            self.message_id = hval

        if name in ('From', 'Subject'):
            x = decode_header(hval)
            if x[0][1]:
                try:
                    syslog.syslog("[%s] decoding header %s" % (self.id, name))
                    new_header = "X-Decoded-%s" % (name)
                    self.headers.append((new_header, x[0][0].decode(x[0][1])))
                    new_header = "X-Decoded-%s-Encoding" % (name)
                    self.headers.append((new_header, x[0][1]))
                except Exception as e:
                    syslog.syslog('[%s] error with message_id %s: %s' % (self.id, self.message_id, e))

        return Milter.CONTINUE

    def eom(self):
        for x in self.headers:
            try:
                self.addheader(x[0], x[1])
            except Exception as e:
                    syslog.syslog('[%s] error with message_id %s: %s' % (self.id, self.message_id, e))
        
        return Milter.ACCEPT

def main():

    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)

    # todo: use argparse
    # todo: better logging to stdout
    socketname = "inet:8899@127.0.0.1"
    timeout = 600

    Milter.factory = DecodeHeaders
    #Milter.set_flags(Milter.ADDHDRS)

    syslog.syslog("decodeheaders startup")
    Milter.runmilter("decodeheaders",socketname,timeout)
    syslog.syslog("shutdown")

if __name__ == "__main__":
  main()