#!/usr/bin/env python3

import syslog
import argparse
import Milter
from email.header import decode_header
from pprint import pprint


class DecodeHeaders(Milter.Base):

    def __init__(self):  # A new instance with each new connection.
        self.id = Milter.uniqueID()  # Integer incremented with each call.
        self.message_id = "unknown"

    def connect(self, IPname, family, hostaddr):
        self.headers = list()
        return Milter.CONTINUE

    def header(self, name, hval):

        if name == "Message-Id":
            self.message_id = hval

        if name in ('From', 'Subject'):
            x = decode_header(hval)
            if x[0][1]:
                try:
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
                syslog.syslog("[%s] %s: wrote header '%s'" % (self.id, self.message_id, x[0]))
                self.addheader(x[0], x[1])
            except Exception as e:
                syslog.syslog('[%s] error with message_id %s: %s' % (self.id, self.message_id, e))

        return Milter.ACCEPT


def main():

    syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)

    # Set up argparse
    parser = argparse.ArgumentParser(description='Decode MIME encoded email headers')
    help_header = "Specify one or more headers that should be decoded (if MIME encoded). "
    help_header = "Case sensitive. Default: 'From' and 'Subject'."
    parser.add_argument('-h', '--header', type=str, action='append', nargs='+', help=help_header, default=['From', 'Subject'])
    help_socketspec = "Specifies the socket that should be established by the filter to receive connections from "
    help_socketspec += "Postfix in order to provide service. socketspec is in one of two forms: local:path which "
    help_socketspec += "creates a UNIX domain socket at the specified path, or inet:port[@host] or inet6:port[@host] "
    help_socketspec += "which creates a TCP socket on the specified port using the requested protocol family. "
    help_socketspec += "Default: 'inet:8899@0.0.0.0'."
    parser.add_argument('-p', '--socketspec', type=str, help=help_socketspec, default="inet:8899:0.0.0.0")
    help_timeout = "Sets the number of seconds libmilter will wait for an MTA communication (read or write) before "
    help_timeout += "timing out. Default: 600"
    parser.add_argument('-t', '--timeout', type=int, help=help_timeout, default=600)
    args = parser.parse_args()

    pprint(args)

    syslog.syslog(syslog.LOG_INFO, "Starting")
    syslog.syslog(syslog.LOG_DEBUG, "Command line arguments: %s" % (repr(args)))

    Milter.factory = DecodeHeaders
    Milter.set_flags(Milter.ADDHDRS)

    syslog.syslog(syslog.LOG_DEBUG, "")
    Milter.runmilter("decodeheaders", args.socketspec, args.timeout)
    syslog.syslog("shutdown")


if __name__ == "__main__":
    main()
