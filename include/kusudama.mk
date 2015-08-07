
#
# works on ubuntu. live with it.
#

TMPDIR = $(PWD)/tmp

ifeq "$(CONFIGFILE)" ""
CONFIGFILE = $(PWD)/conf/servers.yaml
endif

STAGES = stages

INCLUDE = include

REQUIREMENTS = $(INCLUDE)/requirements.txt

PP = PYTHONPATH="$(PWD)/lib"

CC = CONFIGFILE="$(CONFIGFILE)"

DD = DEBUG="$(DEBUG)"

TT = TMPDIR="$(TMPDIR)"

SSHCONFIG = $(TMPDIR)/.ssh/config

SSHPRIVKEY = $(TMPDIR)/.ssh/id_rsa

SSHPUBKEY = $(SSHPRIVKEY).pub

FABSSH = --ssh-config-path=$(SSHCONFIG) --disable-known-hosts

FABFILE = --fabfile $(STAGES)/$(@)/fabfile.py

FAB = $(DD) $(PP) $(CC) $(TT) fab $(FABSSH) $(FABFILE) $(@)

RUNSTAGE = $(FAB)

preflight: pipinstalled pipdeps $(TMPDIR)

$(TMPDIR):
	mkdir -pv $(TMPDIR)

pipinstalled:
	which pip || sudo apt-get -y install python-pip
	dpkg -l | grep ^ii | grep python-dev || sudo apt-get -y install python-dev
	dpkg -l | grep ^ii | grep python-yaml || sudo apt-get -y install python-yaml
	dpkg -l | grep ^ii | grep python-netaddr || sudo apt-get -y install python-netaddr

pipdeps:
	pip list | grep -i Fabric || sudo pip install --upgrade -r "$(REQUIREMENTS)"

sshkey:
	mkdir -pv $(shell dirname $(SSHCONFIG))
	test -f $(shell dirname $(SSHCONFIG))/id_rsa || ssh-keygen -t rsa -f $(shell dirname $(SSHCONFIG))/id_rsa -N ''

#
# this creates a local tmp/.ssh/config file for fabric to use
# it also creates a local tmp/servers.txt for parallel-ssh (pssh) to use
#
# do not change this unless you know what you are doing.
#
sshconfig: preflight
	mkdir -pv $(shell dirname $(SSHCONFIG))
	touch $(SSHCONFIG)
	SSHCONFIG=$(SSHCONFIG) $(RUNSTAGE)

