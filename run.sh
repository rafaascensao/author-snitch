#!/bin/bash

rm -rf target/
mkdir target/

find ./corpora/treino -name "*.txt" -type f -exec echo {} \; > aux.txt 
sed -e 's/\.\///g' aux.txt > target/filenames.txt
rm aux.txt

while IFS='' read -r line || [[ -n "$line" ]]; do 
    folder=`dirname "$line"`
    file=`basename "$line"` 
    mkdir -p target/"$folder"
    ./normalize.sh "$line" > target/"$folder"\/normalized-"$file"
done < target/filenames.txt
