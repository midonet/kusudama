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
from fabric.colors import yellow,green,red
from fabric.utils import puts

metadata = Config(os.environ["CONFIGFILE"])

def install_juju():
    run("""

if [[ ! -f "/etc/apt/sources.list.d/juju-stable-trusty.list" ]]; then
    yes | add-apt-repository ppa:juju/stable
    apt-get update
fi

dpkg -l juju-core | grep 'ii  juju-core' || apt-get -y -u install juju-core

""")

def configure_environment():
    run("""

mkdir -pv /root/.juju

cat >/root/.juju/environments.yaml <<EOF
#
# autogenerated by a script. if you touch this you have been warned.
#
default: kusudama

environments:
    kusudama:
        type: manual

        bootstrap-host: %s
        bootstrap-user: root

        # storage-listen-ip:
        # storage-port: 8040

        enable-os-refresh-update: true
        enable-os-upgrade: true

EOF

""" % metadata.servers[env.host_string]["ip"])

def bootstrap_environment():
    run("""

test -f /root/.juju/environments/kusudama.jenv || juju bootstrap -v

juju status | grep -A1 units | grep 'juju-gui' || juju deploy juju-gui --to 0

exit 0

""")

def add_machines():
    for server in sorted(metadata.servers):
        if not server == env.host_string:
            puts(green("adding node %s to juju environment" % server))

            run("""
IP="%s"

juju status | grep "${IP}" || juju add-machine "ssh:root@${IP}"

exit 0

""" % metadata.servers[server]["ip"])

@parallel
@roles('bootstrap')
def bootstrap():
    puts(yellow("using server [%s] for juju bootstrapping" % env.host_string))

    install_juju()

    configure_environment()

    bootstrap_environment()

    add_machines()