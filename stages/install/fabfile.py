#
# Copyright (c) 2015 Midokura SARL, All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from kusudama.config import Config

from fabric.api import env,parallel,roles,run
from fabric.colors import yellow
from fabric.utils import puts

metadata = Config(os.environ["CONFIGFILE"])

@parallel
@roles('all_servers')
def install():
    puts(yellow("installing packages and configuring server [%s]" % env.host_string))

    #
    # prepare the box
    #
    run("""
DOMAIN="%s"
HOST="%s"

echo 'nameserver 8.8.8.8' > /etc/resolv.conf

yes | dpkg --configure -a
apt-get update 1>/dev/null
DEBIAN_FRONTEND=noninteractive apt-get -y -u dist-upgrade 1>/dev/null

for PKG in puppet htop vim screen atop tcpdump nload make git dstat bridge-utils openjdk-7-jre-headless iperf iperf3 traceroute mosh python minicom strace; do
    dpkg -l "${PKG}" | grep "ii  ${PKG}" || \
        DEBIAN_FRONTEND=noninteractive apt-get -q --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install -- "${PKG}" || true
done

echo "${HOST}" > /etc/hostname

hostname "${HOST}"

cat >/etc/hosts<<EOF
127.0.0.1 localhost.localdomain localhost
127.0.0.1 $(hostname).${DOMAIN} $(hostname)

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts
EOF

exit 0

""" % (metadata.config["domain"], env.host_string))

