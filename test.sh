#!/bin/sh

ssh -i ~/router root@192.168.1.1 -- killall python3
# Stop current running master if any
ssh -i ~/router root@192.168.1.1 -- /etc/init.d/turtetris-slave restart

# Remove old one
ssh -i ~/router root@192.168.1.1 -- rm -rf turtetris_master
# Deploy
scp -i ~/router -r turtetris_master root@192.168.1.1:
# Run
ssh -i ~/router root@192.168.1.1 -- python3 -m turtetris_master
