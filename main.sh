#!/usr/bin/env bash

version="0.1"
echo -e "Bluedos v. $version\nDeveloped by @ceigh\n"

echo "Running ..."
#Scanning and get addresses from stdout in str format
hciData=`hcitool scan | awk 'NR>1 {print}'` || echo "Bluetooth error"
echo -e "hciData:\n$hciData" #Control

addresses=`echo $hciData | awk '{print $1}'`
echo -e "\naddresses:\n$addresses" #Control

#Counting addresses number
addressesNumber=`echo $addresses | wc -w`
if [ $addressesNumber -eq 0 ]; then
  echo "There's no devices around"
  exit 0
fi

#If 1 -> attack it, if >1 -> select which addr attack
if [ $addressesNumber -gt 1 ]; then
  names=`echo $hciData | awk '{print $2}'`
  echo "Found $addressesNumber devies, choose:"
  for counter in {1..$addressesNumber}; do
    echo "$counter)" `echo $addresses | awk -v NR=$counter 'NR==$NR'`
  done
else
  echo "ONE"
fi
