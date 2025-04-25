#!/bin/bash

./vast-wait.sh
source vast-env-run.sh
echo "http://$VAST_PUBLIC_IPADDR:$VAST_COMFY"
cmd.exe /c start chrome "http://$VAST_PUBLIC_IPADDR:$VAST_COMFY"
ssh -p $VAST_SSH "root@$VAST_PUBLIC_IPADDR" -i ~/.ssh/mvps/ud_rsa