#!/bin/bash

wget https://raw.githubusercontent.com/gnmiller/scraps/master/.bashrc --no-check-certificate
wget https://raw.githubusercontent.com/gnmiller/scraps/master/.vimrc --no-check-certificate
echo "source .bashrc" >> .profile

mkdir ~/.ssh/ -m g-rwx,o-rwx
touch ~/.ssh/authorized_keys
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDISWo3i9IJBBpnBD+j+svaUk0oDyd/b0gMOdzRWk+A71UiQkEAwrNnGzX7HYuQ7PUejjuYdUHSRaIJpvo0F/Mxv1jFA9TPNcKlS07ngEwM7qHyXPBtE4WDFd3lUpOxfEaPg4YBfrOcy40DcXwUMX0I3am1Z4OsXU7s3OK5bju1IAU8Xdkxk1oKjhHWMMHsUgvDqM/4yixRvD/X7/R1u6aFVnnxbhUygVHEhWNI5xpMN4gMVAq40I7y3kN4kPEMYiwjyGTX2h32Vn+uJtfKFsSrB4meHVxdJLUdWjXuB+ipeaNkKD8EUW3Z6ZFepzZ4fKadDUij7f9aprbNMYc76i9x greg.miller@gtbgremilles60a.tdi.corp.jwt.com" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
