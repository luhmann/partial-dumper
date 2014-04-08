#!/bin/bash
keyPrefix='content:v1:de:de:live:'
filename='keys.txt'
filelines=`cat $filename`

echo $filelines

mkdir -p keys

for line in $filelines ; do
    output=${line//\//_}
    redis-cli GET "$keyPrefix$line" > "keys/$output.json"
done

tar cvzf redis-dump.tar.gz keys