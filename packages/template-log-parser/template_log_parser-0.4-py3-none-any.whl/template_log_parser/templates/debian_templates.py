# Base templates for Debian Type OS log analysis

# Events with bracketed id numbers
# These identifiers occur first, so running them first reduces chance of false matches to other events
anacron = "{time} {server_name} anacron[{id}]: {message}"
apt_systemd_daily = "{time} {server_name} apt.systemd.daily[{id}]: {message}"
avahi_daemon = "{time} {server_name} avahi-daemon[{id}]: {message}"
blkdeactivate = "{time} {server_name} blkdeactivate[{id}]: {message}"
chpasswd = "{time} {server_name} chpasswd[{id}]: {message}"
chronyd = "{time} {server_name} chronyd[{id}]: {message}"
collectd = "{time} {server_name} collectd[{id}]: {message}"
containerd = "{time} {server_name} containerd[{id}]: {message}"
cpufrequtils = "{time} {server_name} cpufrequtils[{id}]: {message}"
cron = "{time} {server_name} CRON[{id}]: {message}"
cron_lower = "{time} {server_name} cron[{id}]: {message}"
crontab = "{time} {server_name} crontab[{id}]: {message}"
dbus_daemon = "{time} {server_name} dbus-daemon[{id}]: {message}"
dbus_send = "{time} {server_name} dbus-send[{id}]: {message}"
desktop = "{time} {server_name} {prefix}.desktop[{id}]: {message}"
dhclient = "{time} {server_name} dhclient[{id}]:{message}"
dietpi_preboot = "{time} {server_name} DietPi-PreBoot[{id}]:{message}"
dockerd = "{time} {server_name} dockerd[{id}]: {message}"
dropbear = "{time} {server_name} dropbear[{id}]: {message}"
fake_hwclock = "{time} {server_name} fake-hwclock[{id}]: {message}"
fstrim = "{time} {server_name} fstrim[{id}]: {message}"
gnome_shell = "{time} {server_name} gnome-shell[{id}]: {message}"
groupadd = "{time} {server_name} groupadd[{id}]: {message}"
gvfsd_network = "{time} {server_name} gvfsd-network[{id}]: {message}"
ifup = "{time} {server_name} ifup[{id}]:{message}"
kernel = "{time} {server_name} kernel: [{id}]{message}"
loadcpufreq = "{time} {server_name} loadcpufreq[{id}]: {message}"
logrotate = "{time} {server_name} logrotate[{id}]: {message}"
monit = "{time} {server_name} monit[{id}]: {message}"
network_manager = "{time} {server_name} NetworkManager[{id}]: {message}"
postfix = "{time} {server_name} postfix[{id}]: {message}"
postfix_process = "{time} {server_name} postfix/{process}[{id}]: {message}"
quotarpc_process = "{time} {server_name} quotarpc.{process}[{id}]: {message}"
rpc_process = "{time} {server_name} rpc.{process}[{id}]: {message}"
rrdcached = "{time} {server_name} rrdcached[{id}]: {message}"
rsyncd = "{time} {server_name} rsyncd[{id}]: {message}"
rtkit_deamon = "{time} {server_name} rtkit-daemon[{id}]: {message}"
run_parts = "{time} {server_name} run-parts[{id}]: {message}"
samba_process = "{time} {server_name} samba-{process}[{id}]: {message}"
smbd = "{time} {server_name} smbd[{id}]: {message}"
sm_notify = "{time} {server_name} sm-notify[{id}]: {message}"
sshd = "{time} {server_name} sshd[{id}]: {message}"
systemd = "{time} {server_name} systemd[{id}]: {message}"
systemd_process = "{time} {server_name} systemd-{process}[{id}]: {message}"
useradd = "{time} {server_name} useradd[{id}]: {message}"
usermod = "{time} {server_name} usermod[{id}]: {message}"
wpa_supplicant = "{time} {server_name} wpa_supplicant[{id}]: {message}"
wsdd = "{time} {server_name} wsdd[{id}]: {message}"

# Other events
php = "{time} {server_name} php{version}-{process}: {message}"
rsyslogd = "{time} {server_name} rsyslogd: {message}"
rsync_sync = "{time} {server_name} rsync-{id} {message}"
runuser = "{time} {server_name} runuser: {message}"
sudo = "{time} {server_name} sudo: {message}"

# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings (ie: disconnected from SSID, connected to) will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific


debian_events_with_bracketed_id_dict = {
    "anacron[": [anacron, 4, "anacron"],
    "apt.systemd.daily": [apt_systemd_daily, 4, "apt_systemd_daily"],
    "avahi-daemon": [avahi_daemon, 4, "avahi_daemon"],
    "blkdeactivate": [blkdeactivate, 4, "blkdeactivate"],
    "chpasswd": [chpasswd, 4, "chpasswd"],
    "chronyd": [chronyd, 4, "chronyd"],
    "collectd": [collectd, 4, "collectd"],
    "containerd": [containerd, 4, "containerd"],
    "cpufrequtils": [cpufrequtils, 4, "cpufrequtils"],
    "cron": [cron_lower, 4, "cron"],
    "CRON": [cron, 4, "cron"],
    "crontab": [crontab, 4, "crontab"],
    "dbus-daemon": [dbus_daemon, 4, "dbus_daemon"],
    "dbus-send": [dbus_send, 4, "dbus_send"],
    ".desktop": [desktop, 5, "desktop"],
    "dhclient": [dhclient, 4, "dhclient"],
    "DietPi-PreBoot": [dietpi_preboot, 4, "dietpi_preboot"],
    "dockerd": [dockerd, 4, "dockerd"],
    "dropbear": [dropbear, 4, "dropbear"],
    "fake-hwclock": [fake_hwclock, 4, "fake_hwclock"],
    "fstrim": [fstrim, 4, "fstrim"],
    "gnome-shell": [gnome_shell, 4, "gnome_shell"],
    "groupadd": [groupadd, 4, "groupadd"],
    "gvfsd-network": [gvfsd_network, 4, "gvfsd_network"],
    "ifup": [ifup, 4, "ifup"],
    "kernel": [kernel, 4, "kernel"],
    "loadcpufreq": [loadcpufreq, 4, "loadcpufreq"],
    "logrotate": [logrotate, 4, "logrotate"],
    "monit": [monit, 4, "monit"],
    "NetworkManager": [network_manager, 4, "network_manager"],
    "postfix[": [postfix, 4, "postfix"],
    "postfix/": [postfix_process, 5, "postfix_process"],
    "quotarpc": [quotarpc_process, 5, "quotarpc_process"],
    "rpc.": [rpc_process, 5, "rpc_process"],
    "rrdcached": [rrdcached, 4, "rrdcached"],
    "rsyncd": [rsyncd, 4, "rsyncd"],
    "rtkit-daemon": [rtkit_deamon, 4, "rtkit_daemon"],
    "run-parts": [run_parts, 4, "run_parts"],
    "samba-": [samba_process, 5, "samba_process"],
    "smbd": [smbd, 4, "smbd"],
    "sm-notify": [sm_notify, 4, "sm_notify"],
    "sshd": [sshd, 4, "sshd"],
    "systemd": [systemd, 4, "systemd"],
    "systemd-": [systemd_process, 5, "systemd_process"],
    "useradd": [useradd, 4, "useradd"],
    "usermod": [usermod, 4, "usermod"],
    "wpa_supplicant": [wpa_supplicant, 4, "wpa_supplicant"],
    "wsdd": [wsdd, 4, "wsdd"],
}

debian_other_events = {
    "php": [php, 5, "php"],
    "rsyslogd": [rsyslogd, 3, "rsyslogd"],
    "rsync": [rsync_sync, 4, "rsync_sync"],
    " runuser": [runuser, 3, "runuser"],
    "sudo": [sudo, 3, "sudo"],
}

debian_template_dict = {**debian_events_with_bracketed_id_dict, **debian_other_events}
