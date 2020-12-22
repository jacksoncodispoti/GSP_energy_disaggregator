#!/bin/bash
#Regenerate entire dataset from scratch

echo "Deleting CSV files"
for h in {1..6}; do
	rm house_$h/*.csv
	python create.py $h
done

echo "Regenerating dataset"
for h in {1..6}; do
	python create.py $h
done
