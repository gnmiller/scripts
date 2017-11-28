#!/bin/bash
#initalize a Linux account with my bashrc, vimrc and my stock standard public key
#ignores ssl checks on the remote servers additionally creates and chmod .ssh and authorized_keys as needed

cd ~/
mv ~/.bashrc ~/.bashrc.orig
wget https://raw.githubusercontent.com/gnmiller/scraps/master/.bashrc --no-check-certificate
wget https://raw.githubusercontent.com/gnmiller/scraps/master/.vimrc --no-check-certificate
echo "source .bashrc" >> .profile

mkdir ~/.ssh/ -m g-rwx,o-rwx
touch ~/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDISWo3i9IJBBpnBD+j+svaUk0oDyd/b0gMOdzRWk+A71UiQkEAwrNnGzX7HYuQ7PUejjuYdUHSRaIJpvo0F/Mxv1jFA9TPNcKlS07ngEwM7qHyXPBtE4WDFd3lUpOxfEaPg4YBfrOcy40DcXwUMX0I3am1Z4OsXU7s3OK5bju1IAU8Xdkxk1oKjhHWMMHsUgvDqM/4yixRvD/X7/R1u6aFVnnxbhUygVHEhWNI5xpMN4gMVAq40I7y3kN4kPEMYiwjyGTX2h32Vn+uJtfKFsSrB4meHVxdJLUdWjXuB+ipeaNkKD8EUW3Z6ZFepzZ4fKadDUij7f9aprbNMYc76i9x greg.miller@gtbgremilles60a.tdi.corp.jwt.com" >> ~/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoDthhhLKwnl1C7j0Vqs3vcj0bQ3pEimygk37bTdqqr2Q5ADwiK+JWEyHiQSADjfykhuhlKAjigiXLKuXqANDKwhBul9wfBfdBa1FdpU8LOSe6y7UtWEuYxX/dD7W3zE1vf2LLQ82Z/FJehgwoo2f8mfiOOncPa3v5GRx+dP9iHBUC7Sc631dnSrrTSSQnCjnBC7dYqDOnxc8MZ4C6xGYZeqZDepS8mQe511E8WW7f+euIiiAdihSG5usUc72f2K8h3jWg5uBw5G+S6D3WBOxGEK7E/bR+dc+nptHCOSSlM8DKnSdNy9XVEmyKVFHIxsQGbr9gb1IfKC/G7Yz5bv47 root@kalecgos" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
