#!/bin/bash

sed -e 's/[[:punct:]]/ &/g' test.txt > test2.txt