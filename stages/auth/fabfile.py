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
def auth():

    f = open(os.environ["SSHPUBKEY"], 'r')

    run("""

mkdir -pv /root/.ssh

echo '%s' >> /root/.ssh/authorized_keys

""" % f.read())

    f.close()

    if env.host_string in metadata.roles["bootstrap"]:
        q = open(os.environ["SSHPRIVKEY"], 'r')

        run("""
mkdir -pv /root/.ssh

echo '%s' > /root/.ssh/id_rsa

chown -R root:root /root

chmod 0700 /root/.ssh

chmod 0600 /root/.ssh/id_rsa

""" % q.read())

        q.close()
