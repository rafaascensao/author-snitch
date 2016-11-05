#!/bin/bash

#This script normalizes the a given text as asked in the LN course.
if [ -z "$1" ] 
	then
		echo "Input file not provided"
		exit
fi 
sed -e 's/\([[:punct:]]\)\([[:punct:]]\)/\1 \2/g' -e 's/[[:punct:]] / &/g' -e 's/ [[:punct:]]/& /g' -e 's/^[[:punct:]]/& /g' -e 's/[[:punct:]]$/ &/g' -e 's/  / /g' "$1" 
