# 薬玉
This project is the fourth installer written for Midonet by me.

The first one was an internal installer aimed to provide RHEL and Ubuntu support, mostly used to install testbeds in Midocloud Japan.

The second installer (https://github.com/midonet/orizuru) is used for demos. It will install Midonet and Openstack in Docker containers.

The third installer (https://github.com/midonet/senbazuru) can be used for building L4LB testbeds fast and easy, it is already using the puppet modules from Jaume.

This installer will use Fabric to launch Juju commands on servers to install Openstack and Midonet with the Juju Charms maintained by Toni.

