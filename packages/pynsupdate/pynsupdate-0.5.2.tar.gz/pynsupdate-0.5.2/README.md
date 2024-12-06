# pynsupdate

A python wrapper to Dynamically update DNS using nsupdate

# Installation

# Usage

# Automated updates

You can find on how to configure the service to run automatically
in this section.

## Service (SystemD)

Add the following to `/etc/systemd/system/nsupdate.service`

### Virtual environment

```
[Unit]
Description=Runs pynsupdate
After=network.target
Wants=pynsupdate.timer

[Service]
Type=oneshot
User=fooservice
WorkingDirectory={{ venv_home }}
ExecStart={{ venv_home }}/bin/fooservic

[Install]
WantedBy=multi-user.target
```

### System install 

```
[Unit]
Description=Runs Logs system statistics to the systemd journal
Wants=myMonitor.timer

[Service]
Type=oneshot
ExecStart=/usr/bin/free

[Install]
WantedBy=multi-user.target
```


## Timer

# This timer unit is for testing
# By David Both
# Licensed under GPL V2
#

[Unit]
Description=Logs some system statistics to the systemd journal
Requires=myMonitor.service

[Timer]
Unit=myMonitor.service
OnCalendar=*-*-* *:*:00

[Install]
WantedBy=timers.target
