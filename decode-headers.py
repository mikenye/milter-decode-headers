#!/usr/bin/env python

import sys
import syslog
import Milter
from email.header import decode_header

class DecodeHeaders(Milter.Base):

    def __init__(self):  # A new instance with each new connection.
        self.id = Milter.uniqueID()  # Integer incremented with each call.

    def connect(self, IPname, family, hostaddr):
        syslog.syslog("connect from %s at %s" % (IPname, hostaddr))
        self.headers = list()
        return Milter.CONTINUE

    def header(self, name, hval):

        if name in ('From', 'Subject'):
            x = decode_header(hval)
            if x[0][1]:
                try:
                    syslog.syslog("decoding header %s" % (name))
                    new_header = "X-Decoded-%s" % (name)
                    self.headers.append((new_header, x[0][0].decode(x[0][1])))
                    new_header = "X-Decoded-%s-Encoding" % (name)
                    self.headers.append((new_header, x[0][1]))
                except Exception as e:
                    syslog.syslog('Error: %s' % (e))

        return Milter.CONTINUE

    def eom(self):
        for x in self.headers:
            try:
                self.addheader(x[0], x[1])
            except Exception as e:
                    syslog.syslog('Error: %s' % (e))
        
        return Milter.ACCEPT

def main():
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