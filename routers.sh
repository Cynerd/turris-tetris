#!/bin/sh

#ROUTERS="1 159 190 156 104 199 136 173 245 172"
ROUTERS="1 159 189 156 104 199 135 171 244 172"

I=0

for R in $ROUTERS; do
	echo "=== Runnining on 192.168.1.$R ==="
	ssh -i ~/router root@192.168.1.$R -- $@
	#scp -i ~/router user.lua root@192.168.1.$R:/etc/updater/user.lua
	#ssh -i ~/router root@192.168.1.$R -- uci set turtetris.line=$I
	#ssh -i ~/router root@192.168.1.$R -- /etc/init.d/turtetris-slave restart
	#I=$(expr $I + 1)
done

#ssh-copy-id -i ~/router root@192.168.1.$R
