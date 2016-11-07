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
    echo "Normalizing $file"
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

echo "Finish normalizing authors texts files"
echo "AUTHORS : ${authors[@]}"
for a in "${authors[@]}"; do
	echo "Filling information of author $a. Please wait..."
	cd target/
	cat corpora/treino/"$a"/* > "$a".txt
	python ../ngrams.py -d "$a".txt
	cd ..
	echo "Finished filling information of author $a."
done

echo "Finish filling information"

find ./corpora/teste -name "*.txt" -type f -exec echo {} \; > aux.txt 
sed -e 's/\.\///g' aux.txt > target/filetests.txt
rm aux.txt

echo "#######################################"
echo "TESTS"
while IFS='' read -r line || [[ -n "$line" ]]; do 
    folder=`dirname "$line"`
    file=`basename "$line"`
    nwords=`basename "$folder"` 
    ./normalize.sh "$line" > target/"$nwords"-normalized-"$file"
    echo "Testing "$nwords"-"$file" with method unigrams"
    python ngrams.py -t target/"$nwords"-normalized-"$file" uni
    echo "Testing "$nwords"-"$file" with method bigrams"
    python ngrams.py -t target/"$nwords"-normalized-"$file" bi
    echo "Testing "$nwords"-"$file" with method medium of phrases"
    python ngrams.py -t target/"$nwords"-normalized-"$file" medium	
done < target/filetests.txt
echo "The End"

