#!/usr/bin/with-contenv bash
# shellcheck shell=bash

# Set up timezone
if [ -z "${TZ}" ]; then
  echo "WARNING: TZ environment variable not set"
else
  ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" >/etc/timezone
fi

# log dirs & permissions
mkdir -p /var/log/syslogd
chown nobody:nogroup /var/log/syslogd
mkdir -r /var/log/opendkim
chown nobody:nogroup /var/log/syslogd