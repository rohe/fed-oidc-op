#!/usr/bin/env bash

if [ ! -d "fo_bundle" ]
then
    mkdir "fo_bundle"
fi

if [ ! -f "fo_bundle/https%3A%2F%2Fedugain.org%2F.json" ]
then
    create_jwks.py > fo_bundle/https%3A%2F%2Fedugain.org%2F
fi

if [ ! -f "fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F.json" ]
then
    create_jwks.py > fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F
fi

if [ ! -d "sms" ]
then
    mkdir "sms"
fi

if [ ! -d "sms/discovery" ]
then
    mkdir "sms/discovery"
fi

./provider_info.py conf

packer.py -j fo_bundle/https%3A%2F%2Fedugain.org%2F -i https://edugain.org/ -r provider_info.json > sms/discovery/https%3A%2F%2Fedugain.org%2F
packer.py -j fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F -i https://swamid.sunet.se/ -r provider_info.json > sms/discovery/https%3A%2F%2Fswamid.sunet.se%2F