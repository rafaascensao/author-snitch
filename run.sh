#!/bin/bash

rm -rf target/
mkdir target/

find ./corpora/treino -name "*.txt" -type f -exec echo {} \; > aux.txt 
sed -e 's/\.\///g' aux.txt > target/filenames.txt
rm aux.txt
authors=()
i=0
while IFS='' read -r line || [[ -n "$line" ]]; do 
    folder=`dirname "$line"`
    file=`basename "$line"`
    author=`basename "$folder"` 
    mkdir -p target/"$folder"
    ./normalize.sh "$line" > target/"$folder"\/normalized-"$file"
    bool=0
    if [[ ! " ${authors[@]} " =~ " ${author} " ]]; then
       bool=1
    fi
    if [ "$bool" -eq 1 ]; then
	authors["$i"]="$author"
	((i++))
	echo $i
    fi	 
done < target/filenames.txt
echo "${authors[@]}"
for a in "${authors[@]}"; do
	echo "$a"
	cd target/
	cat corpora/treino/"$a"/* > "$a".txt
	python ../ngrams.py -d "$a".txt
	cd ..
done
