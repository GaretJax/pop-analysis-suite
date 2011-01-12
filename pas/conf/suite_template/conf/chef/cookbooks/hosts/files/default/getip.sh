#!/bin/bash

ifconfig $1 | grep -E -o 'inet addr:[0-9.]{7,15}' | awk -F ':' '{print $2}'

