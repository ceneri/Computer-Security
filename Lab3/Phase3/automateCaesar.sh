#!/bin/bash

echo working...
counter=0
for filename in dataProcessedPhase4/user*Output/decriptedMessage/*; do
	python decipherCaesar.py $counter $filename
	counter=$((counter+1)) 
done
grep jgcastel  cipherResultsCaesar/* >AAAourCaesarMessages
grep ceneri  cipherResultsCaesar/* >>AAAourCaesarMessages
echo done