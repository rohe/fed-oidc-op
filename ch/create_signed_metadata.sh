#!/usr/bin/env bash

if [ ! -d "sms" ]
then
    mkdir "sms"
fi

if [ ! -d "sms/discovery" ]
then
    mkdir "sms/discovery"
fi

./provider_info.py conf

# crude I know

packer.py -j fo_bundle/https%3A%2F%2Fedugain.org%2F -i https://edugain.org/ -r provider_info.json > sms/discovery/https%3A%2F%2Fedugain.org%2F
packer.py -j fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F -i https://swamid.sunet.se/ -r provider_info.json > sms/discovery/https%3A%2F%2Fswamid.sunet.se%2F