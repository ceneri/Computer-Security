#!/bin/bash
#S1 should be the name of the folder 

echo working...
counter=0
for filename in dataProcessedPhase4/user*Output/decriptedMessage/*; do
	python decipherAffine.py $counter $filename
	counter=$((counter+1)) 
done
grep jgcastel  cipherResultsAffine/* >AAAourAffineMessages
grep ceneri  cipherResultsAffine/* >>AAAourAffineMessages
echo done