Generating an 'input.txt' to throw at Driver.py:

STEP 1:
-------
What's the directory you'll be recursively searching under?
Let's suppose it's: /your/location

STEP 2:
-------
What file types are you interested in? 
Let's suppose: .txt
However, if you are not sure, you can do something like the following to enumerate all the different types
of file extensions lurking under a directory, in order of frequency (most frequently encountered
at the start):

$ find "/your/location" -type f | sed -e 's/.*\.//' | sed -e 's/.*\///' | sort | uniq -c | sort -rn
   6533 jpg
   5751 png
   5040 pdf
    ... etc.

NOTE: the frequency count cannot be assumed to be accurate/correct. 

Reference: https://stackoverflow.com/questions/1842254/how-can-i-find-all-of-the-distinct-file-extensions-in-a-folder-hierarchy

STEP 3:
-------
OK assuming we are still after .txt files, next step is to determine
how many files you EXPECT to capture:

$ find "/your/location" -iname "*.txt" | wc -l
1076

STEP 4:
-------
'xargs' will not like to process over files with the following character anywhere in the path: '
Find out if there are any files like this:

$ find /your/location -iname "*.txt" | grep "'"
<output any offending files>

STEP 5:
-------
Manually process any offending files caught in STEP 4 (eg. rename them).

What if there are TOO MANY to manually patch? Proceed and se the SECOND command in 
STEP 6 instead.

FIXME: what if there are A LOT of them?
You have to have a way of splitting offending files into:
(1) files with ' in a subdirectory leading up to file
(2) files with ' in the actual file
(3) both (1)+(2)

STEP 6:
-------
Generate 'input.txt':

(1)
$ find "/your/location" -iname "*.txt" | xargs -I{} md5sum {} > input.txt

(2) Here we replace single quote with slash AND single quote, before passing input to xargs (this
is essentially automating STEP 5): 
$ find "/your/location" -iname "*.txt" | sed 's/'"'"'/\\'"'"'/g' | xargs -I{} md5sum {} > input.txt

See below "Known errors", if any errors are thrown.

STEP 7:
-------
Verify 'input.txt' file count:

$ cat input.txt | wc -l 
1076                           <--- yes, same as expected.


Now you are ready to pass 'input.txt' to Driver.py!


-------------

Known errors:

(1) xargs: unmatched single quote; by default quotes are special to xargs unless you use the -0 option

What does this mean?
Let's suppose there are 10 files. This means one of the files has this character in it: '

You can work out which are the offending files like this:

$ find /your/location -iname "*.txt" | grep "'"
/your/location/syx/Dexed_cart_1.0/Rec'Up/Missing.txt              <--- there is a ' in this file

So 'xargs' will get to this file, throw the error, and NOT continue (ie. if it's was the 3rd file, xargs
would've gotten up to the 3rd file, successfully processing 2 files before it, and NOT have continued).










