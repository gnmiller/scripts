#!/bin/bash
#blacklist IP specified in the firewall ; uses firewall-cmd
sudo firewall-cmd --permanent --add-rich-rule="rule family='ipv4' source address='$1' reject"
echo "don't forget to reload the firewall now"
