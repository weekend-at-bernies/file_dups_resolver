#!/bin/bash
rm Driver.py workflow1.txt workflow2.txt ignored.txt summary.txt
cp ../Driver.py .
python Driver.py -o -i input.txt -d "/path/to/"
DIFF=$(diff summary.txt summary.txt.good)
if [ "$DIFF" != "" ]
then
  echo ""
  echo "FAILED TEST"
  echo ""
else
  echo ""
  echo "PASSED TEST"
  echo ""
fi
