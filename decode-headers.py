#!/usr/bin/env python3

import os
import syslog
import argparse
import pickle
import Milter
from email.header import decode_header
from pprint import pprint


class DecodeHeaders(Milter.Base):

    def __init__(self):  # A new instance with each new connection.
        self.id = Milter.uniqueID()  # Integer incremented with each call.
        self.message_id = "unknown"
        self.headers_to_decode = pickle.loads(os.environ["HEADERS-TO-DECODE-PICKLE"])
        syslog.syslog(syslog.LOG_DEBUG, "[%s] DecodeHeaders.__init__: will decode headers: %s" % (self.id, repr(self.headers_to_decode)))

    def connect(self, IPname, family, hostaddr):
        syslog.syslog(syslog.LOG_DEBUG, "[%s] DecodeHeaders.connect: %s, %s, %s" % (self.id, repr(IPname), repr(family), repr(hostaddr)))
        self.headers = list()
        return Milter.CONTINUE

    def header(self, name, hval):
        syslog.syslog(syslog.LOG_DEBUG, "[%s] DecodeHeaders.header: %s, %s" % (self.id, repr(name), repr(hval)))

        if name == "Message-Id":
            self.message_id = hval

        if name in self.headers_to_decode:
            x = decode_header(hval)
            if x[0][1]:
                try:
                    new_header = "X-Decoded-%s" % (name)
                    syslog.syslog(syslog.LOG_DEBUG, "[%s] DecodeHeaders.header: will add header: %s" % (self.id, repr(new_header)))
                    self.headers.append((new_header, x[0][0].decode(x[0][1])))
                    new_header = "X-Decoded-%s-Encoding" % (name)
                    syslog.syslog(syslog.LOG_DEBUG, "[%s] DecodeHeaders.header: will add header: %s" % (self.id, repr(new_header)))
                    self.headers.append((new_header, x[0][1]))
                except Exception as e:
                    syslog.syslog(syslog.LOG_ERR, '[%s] error with message_id %s: %s' % (self.id, self.message_id, e))

        return Milter.CONTINUE

    def eom(self):
        syslog.syslog(syslog.LOG_DEBUG, "[%s] DecodeHeaders.eom: called" % (self.id))
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
    parser.add_argument('--header', type=str, action='append', help=help_header, default=['From', 'Subject'])
    help_socketspec = "Specifies the socket that should be established by the filter to receive connections from "
    help_socketspec += "Postfix in order to provide service. socketspec is in one of two forms: local:path which "
    help_socketspec += "creates a UNIX domain socket at the specified path, or inet:port[@host] or inet6:port[@host] "
    help_socketspec += "which creates a TCP socket on the specified port using the requested protocol family. "
    help_socketspec += "Default: 'inet:8899@0.0.0.0'."
    parser.add_argument('--socketspec', type=str, help=help_socketspec, default="inet:8899:0.0.0.0")
    help_timeout = "Sets the number of seconds libmilter will wait for an MTA communication (read or write) before "
    help_timeout += "timing out. Default: 600"
    parser.add_argument('--timeout', type=int, help=help_timeout, default=600)
    args = parser.parse_args()

    syslog.syslog(syslog.LOG_INFO, "starting")
    syslog.syslog(syslog.LOG_DEBUG, "command line arguments: %s" % (repr(args)))

    # Set environment variable for what to decode
    headers_to_decode = list(set(args.header))
    os.environ["HEADERS-TO-DECODE-PICKLE"] = pickle.dumps(headers_to_decode)

    # Start milter
    Milter.factory = DecodeHeaders
    Milter.set_flags(Milter.ADDHDRS)
    syslog.syslog(syslog.LOG_DEBUG, "running milter")
    Milter.runmilter("decodeheaders", args.socketspec, args.timeout)

    # Finished
    syslog.syslog("shutdown")


if __name__ == "__main__":
    main()
