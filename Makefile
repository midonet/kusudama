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

#
# set this if you want to see debugging info
#
# DEBUG = xoxo

PREREQUISITES = preflight sshconfig sshkey

ALLTARGETS = $(PREREQUISITES) install auth bootstrap

all: $(ALLTARGETS)

include include/kusudama.mk

#
# prepare the machines and install the puppet modules
#
install: $(PREREQUISITES)
	$(RUNSTAGE)

#
# uploads the ssh key to the bootstrap host and adds it to authorized_keys everywhere
#
auth: $(PREREQUISITES)
	SSHPUBKEY=$(SSHPUBKEY) SSHPRIVKEY=$(SSHPRIVKEY) $(RUNSTAGE)

#
# prepare the juju bootstrap node
#
bootstrap: $(PREREQUISITES)
	$(RUNSTAGE)

clean:
	rm -rf ./$(shell basename $(TMPDIR))

