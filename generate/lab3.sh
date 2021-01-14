#!/bin/bash

# array=('ean8' 'code128')
array=('4302755' '3939255' '1144312' '8943906' '6145235')

for i in "${array[@]}" 
do
	treepoem --type ean8 --output "${i}.png" $i width=6
done