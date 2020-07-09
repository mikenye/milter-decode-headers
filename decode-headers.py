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
            syslog.syslog("decoding header %s" % (name))
            x = decode_header('hval')
            syslog.syslog("header decoded")
            new_header = "X-Decoded-%s" % (name)
            syslog.syslog("decoded header created")
            syslog.syslog(repr(x))
            self.addheader(new_header, x[0][0])
            syslog.syslog("decoded header written")
            new_header = "X-Decoded-%s-Encoding" % (name)
            syslog.syslog("decoded encoded header created")
            self.addheader(new_header, x[0][1])
            syslog.syslog("decoded encoded header written")

        return Milter.CONTINUE

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