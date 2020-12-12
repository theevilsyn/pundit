#!/bin/bash


error() {
  printf '\E[31m'; echo "$@"; printf '\E[0m'
}

if [[ $EUID -ne 0 ]]; then
    error "Please run this script as root!!"
    exit 1
fi

mysql -u root -e "CREATE DATABASE pundit"
mysql -u root pundit < $1