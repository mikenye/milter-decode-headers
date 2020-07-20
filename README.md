# mikenye/milter-decode-headers

A very basic [milter](https://en.wikipedia.org/wiki/Milter), that will decode MIME encoded message headers.

It is primarily designed to work with (and is tested on) [Postfix](http://www.postfix.org), although it should work with any MTA that supports the use of milters.

When used with Postfix, it allows the mail administrator to use [`milter_header_checks`](http://www.postfix.org/postconf.5.html#milter_header_checks), as encoded headers cannot reliably/easily be checked with normal [`header_checks`](http://www.postfix.org/postconf.5.html#header_checks).

This milter can be run standalone (requires python3 + [pymilter](https://pypi.org/project/pymilter/)), or can be run [as a docker container](https://hub.docker.com/r/mikenye/milter-decode-headers). See below.

## Operation

This milter will only decode MIME encoded headers. By default, only the `From` and `Subject` headers are decoded, however this can be configured at run time (see below).

For headers to decode, two additional headers will be added to the message:

* `X-Decoded-HEADER`: containing the decoded header; and
* `X-Decoded-HEADER-Encoding`: containing the encoding of the original header

(where `HEADER` is the name of the header being decoded).

For example, for a message with the following subject header:

* `Subject: =?UTF-8?B?VGhpcyBpcyBhIHV0Zi04IGJhc2U2NCBlbmNvZGVkIHN1YmplY3Q?=`

...two new headers will be added to the message:

* `X-Decoded-Subject: This is a utf-8 base64 encoded subject`
* `X-Decoded-Subject-Encoding: utf-8`

## Deploying with Docker

### Up and Running

Example `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  decode_headers:
    image: mikenye/milter-decode-headers:latest
    container_name: decode_headers
    restart: always
    logging:
      driver: "json-file"
      options:
        max-file: "10"
        max-size: "1m"
    ports:
      - "8899:8899"
    environment:
      DECODE_HEADERS: "Subject"
      TZ: "Australia/Perth"
```

Once the container is up and running, you can add `inet:<docker_host>:8899` to your Postfix's `smtpd_milters` configuration parameter.

### Container Environment Variables

| Environment Variable | Details |
|-----|-----|
| `DECODE_HEADERS`  | Optional. Headers to decode (if encoded). Comma separated list (no spaces). Case sensitive. Default: `From,Subject`. |
| `MILTER_TIMEOUT`  | Optional. Sets the number of seconds libmilter will wait for an MTA communication (read or write) before timing out. Default: `600`. |
| `SYSLOG_PRIORITY` | Optional. Log only messages more urgent than `SYSLOG_PRIORITY`. `1` = Alert, `2` = Critical, `3` = Error, `4` = Warning, `5` = Notice, `6` = Info (the default), `7` = Debug. |
| `TZ`              | Recommended. Set the timezone for the container. Default is `UTC`. |

## Deploying Standalone

### Prepare the host

Examples below assume a Debian-like OS.

#### Checkout project ####

```shell
git clone https://github.com/mikenye/milter-decode-headers.git /tmp/milter-decode-headers
```

#### Install `python` & other prerequisites ####

```shell
apt-get install gcc libmilter-dev libmilter1.0.1 libpython3.7-dev python3 python3-pip python3-setuptools python3-wheel
```
```shell
pip3 install -r /tmp/milter-decode-headers/requirements.txt
```

#### Install `decode-headers.py` ####

```shell
cp /tmp/milter-decode-headers/decode-headers.py /usr/local/bin/
chmod a+x /usr/local/bin/decode-headers.py
```

#### Configure service scripts ####

Configure your service script to start the milter.

```text
usage: decode-headers.py [-h] [--header HEADER] [--socketspec SOCKETSPEC]
                         [--timeout TIMEOUT]

Decode MIME encoded email headers

optional arguments:
  -h, --help            show this help message and exit
  --header HEADER       Case sensitive. Default: 'From' and 'Subject'.
  --socketspec SOCKETSPEC
                        Specifies the socket that should be established by the
                        filter to receive connections from Postfix in order to
                        provide service. socketspec is in one of two forms:
                        local:path which creates a UNIX domain socket at the
                        specified path, or inet:port[@host] or
                        inet6:port[@host] which creates a TCP socket on the
                        specified port using the requested protocol family.
                        Default: 'inet:8899@0.0.0.0'.
  --timeout TIMEOUT     Sets the number of seconds libmilter will wait for an
                        MTA communication (read or write) before timing out.
                        Default: 600
```

## Logging

* Logging is via Syslog, to the `mail` facility.
* An `info` message is logged for each header that is decoded.
* There is also a significant amount of `debug` messages logged, for troubleshooting, so it's recommended to have your syslog configured to drop these messages during normal operation.

## Getting help

Please feel free to [open an issue on the project's GitHub](https://github.com/mikenye/milter-decode-headers/issues).

I also have a [Discord channel](https://discord.gg/k8qUEEG), feel free to [join](https://discord.gg/k8qUEEG) and converse.
