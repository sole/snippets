#!/bin/bash

# Small utility to make sure your wireless connection is up and running
# Use this as a cron task or whatever you like
# Change PING_ADDRESS to your fav address (can be an IP too)

PING_ADDRESS=google.com

x=`ping -c1 $PING_ADDRESS 2>&1 | grep unknown`

if [ ! "$x" = "" ]; then
	echo "Wireless network is down, turning on and off again"

	dbus-send --system --type=method_call --dest=org.freedesktop.NetworkManager /org/freedesktop/NetworkManager org.freedesktop.DBus.Properties.Set string:org.freedesktop.NetworkManager string:WirelessEnabled variant:boolean:false

	dbus-send --system --type=method_call --dest=org.freedesktop.NetworkManager /org/freedesktop/NetworkManager org.freedesktop.DBus.Properties.Set string:org.freedesktop.NetworkManager string:WirelessEnabled variant:boolean:true
fi
