#!/usr/bin/env bash

if [ ! -d "fo_bundle" ]
then
    mkdir "fo_bundle"
fi

if [ ! -f "fo_bundle/https%3A%2F%2Fedugain.org%2F" ]
then
    create_jwks.py > fo_bundle/https%3A%2F%2Fedugain.org%2F
fi

if [ ! -f "fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F" ]
then
    create_jwks.py > fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F
fi

if [ ! -d "public" ]
then
    mkdir "public"
fi
if [ ! -d "public/fo_bundle" ]
then
    mkdir "public/fo_bundle"
fi

if [ ! -f "public/fo_bundle/https%3A%2F%2Fedugain.org%2F" ]
then
    ./public_jwks.py fo_bundle/https%3A%2F%2Fedugain.org%2F > public/fo_bundle/https%3A%2F%2Fedugain.org%2F
fi

if [ ! -f "public/fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F" ]
then
    ./public_jwks.py fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F > public/fo_bundle/https%3A%2F%2Fswamid.sunet.se%2F
fi

