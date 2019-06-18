A useful python tool for managing file duplicates.

You are required to generate an input file similar to: ../test/input.txt

The input file lists a set of files and their MD5 checksums.

Our tool will discover duplicates and name clashes, and provide output 
files to resolve these.

To consider the theory, refer to 'Diagram1.png'.

Three locations each contain some files. There are 3 cases our tool takes into consideration:

(1) : Identical file contents (based on hash/checksum + filesize), but different filenames.
(2) : Identical file names, but different file contents.
(3) : Identical files, both in name and file contents.


WORKFLOWS (choose your workflow from below):

Based on an input list of files....

Workflow 1: Remove redundant files in situ
------------------------------------------
You want to eliminate redundant copies of equivalent files (based on content), and just maintain 
a single copy: it doesn't matter which copy, just keep at least one of them.
In this case generate a list of "duplicates" that you can pass to 'rm', and eliminate the redundant
copies in situ. The output file 'workflow1.txt' is provided for this purpose.

Workflow 2: Amalgamate in a single destination
----------------------------------------------
In this workflow, you want to copy all the files to a single destination/directory. You do not
want redundant copies of the same file. You want to be careful of different files with the same name: 
these have to be identified and renamed in the destination (you don't care which of the clashing ones
get renamed). The output file 'workflow2.txt' is provided for this purpose.



