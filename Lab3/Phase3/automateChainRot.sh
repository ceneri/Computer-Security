#!/bin/bash

echo working...
counter=0
for filename in dataProcessedPhase4/user*Output/decriptedMessage/*; do
	python decipherChainRot.py $counter $filename
	counter=$((counter+1)) 
done
grep jgcastel  cipherResultsChainRot/* >AAAourChainRotMessages
grep ceneri  cipherResultsChainRot/* >>AAAourChainRotMessages
echo done