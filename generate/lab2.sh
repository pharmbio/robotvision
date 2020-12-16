#!/bin/bash

array=('a'  '0' '01' '012' '0123' '01234' '012345' '0123456' '01234567' '012345678' '0123456789' 'datamatrix')

for i in "${array[@]}"
do
    treepoem --type code93 --output "results3/${i}.png" $i
    treepoem --type code93ext --output "results3/${i}ext.png" $i
done