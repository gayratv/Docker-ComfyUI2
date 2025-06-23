#!/bin/bash

source vast-env-run-fill-env.sh
ssh -p $VAST_SSH "root@$VAST_PUBLIC_IPADDR" -i ~/.ssh/mvps/ud_rsa
