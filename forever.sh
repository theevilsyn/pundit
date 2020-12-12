#!/bin/bash

while :
do
	echo Starting now `date` >> /home/pundit/pundit/status.log
	python3 /home/pundit/pundit/start.py
done
