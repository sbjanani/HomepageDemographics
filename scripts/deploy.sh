#!/bin/sh

read -p ".site Username:" USERNAME

TARGET_SERVER=qtmhgate08.atl.careerbuilder.com

scp -r {python/,oozie/,scripts/} $USERNAME@$TARGET_SERVER:~/Homepage-Demographics/

ssh -o pubKeyAuthentication=no $USERNAME@$TARGET_SERVER < scripts/deploy_server.sh