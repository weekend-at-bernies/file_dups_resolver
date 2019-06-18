#!/usr/bin/env python

import os
import sys
import optparse

outfiles = [["ignored.txt", []], ["summary.txt", []], ["workflow1.txt", []], ["workflow2.txt", []]]
	
if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", help="input file (required)", dest="inputfile", metavar="<filename>")
    parser.add_option("-d", help="destination", dest="destination", default="/tmp/workflow2/", metavar="<destination>")
    parser.add_option("-o", "--overwrite", action="store_true", dest="overwrite", default=False, help="output overwrite switch")
    (opts, args) = parser.parse_args()

if opts.inputfile is None:
    print "Error: input file not provided\n"
    parser.print_help()
    exit(-1)


for outfile in outfiles:
    if os.path.exists(outfile[0]) and not opts.overwrite:
        print "Error: file exists: %s\n"%(outfile[0])
        exit(-1)


if not os.path.exists(opts.inputfile):
    print "Error: input file %s does not exist\n"%(opts.inputfile)
    exit(-1)


lines = []
with open(opts.inputfile, "r") as f:
    for line in f:
        lines.append(line.strip())
f.close()



# FIXME: do the md5 calc here - NO! get user to do this... md5 calcs are EXPENSIVE computationally
# enforce user to do this 

# Input files we ignored
ignored_list = outfiles[0][1]

# Unique input file subset (with name clashes indicated):
summary_list = outfiles[1][1]

# List of redundant files to remove in-situ:
workflow1_list = outfiles[2][1]

# Copy-to-destination file list:
workflow2_list = outfiles[3][1]


# 'd1' is dictionary where the (unique) lookup keys are file hashes/checksums.
# Hence it maintains only UNIQUE files.
d1 = {}
# We expect each line to be of format:  <HASH> <FILE>
# Comments are lines starting with '#'
for line in lines:
    if line.startswith('#'):
        continue

    f_hash = line.split()[0]
    f_path = line[len(f_hash):].strip()   

    try:
        f_size = os.path.getsize(f_path)

        # 'd1' has the hash already?
        if f_hash in d1.keys(): 
            # Yes: duplicate file possibly detected (need confirmation).
      
            prior = d1[f_hash]
            prior_f_path = prior[0]
            prior_f_size = prior[1]

            # Confirm by looking at file sizes.
            if f_size == prior_f_size:
                # Confirmed. 
                workflow1_list.append(f_path)
            else:
                # We have encountered 2 different files with the SAME hash.
                # Same hash, different file size. 
                # Not impossible, but STATISTICALLY rare! 
                #print "wow... same hash value, different file sizes... a rare hash collision!"
                # We append "_1" to the hash and add it to 'd1' : FIXME - not good! 
                d1["%s_1"%(f_hash)] = [f_path, f_size]   
                print "WARNING: fix me case 1"         

        else: 
            # No.
            d1[f_hash] = [f_path, f_size]



    except OSError:
        print "WARNING: file could not be found: %s"%(line)
        ignored_list.append(f_path)
        continue


destination = opts.destination
if not destination.endswith('/'):
    destination = "%s/"%(destination)

# 'd2' is dictionary where the (unique) lookup keys are base filenames (sourced from 'd1').
# Hence it maintains only UNIQUE base filenames.
# The lookup value returned is the number of occurrences of that base filename in 'd1'.
d2 = {}
for f_hash in d1:
 
    # Go through every file in 'd1' and get its base filename:   
    # Eg. 'locs/loc1/loc2_foo3.txt' => 'loc2_foo3.txt'
    f_path = d1[f_hash][0]
    f_basename = os.path.basename(f_path)

    # FIX ME FUTURE WORK: do a whole slew of things here like enforce "sane" base filenames, with non-crazy characters, etc.
    
    new_f_basename = f_basename

    # Does the base filename exist already?
    if f_basename in d2.keys():
        # Yes: name clash.
        f_basename_count = d2[f_basename][0]


        d2[f_basename][0] = f_basename_count + 1

        new_f_basename = "%d_%s"%((f_basename_count + 1), f_basename)     

        if new_f_basename in d2.keys():
            # Unlikely event that the new filename is also in use:
            new_f_basename = "%s_%s"%(f_hash, f_basename)
            # FIXME : 
            print "WARNING: fix me case 2"
        

    else:
        # No.
        d2[f_basename] = [1, 0]

    workflow2_list.append("cp \"%s\" \"%s%s\""%(f_path, destination, new_f_basename))



clash_group_index = 1
for f_basename in d2.keys():
    f_basename_count = d2[f_basename][0]
    if f_basename_count > 1:
        d2[f_basename][1] = clash_group_index
        clash_group_index += 1


clash_count = 0
for f_hash in d1:
    f_path = d1[f_hash][0]
    f_basename = os.path.basename(f_path)
    clash_group_index = d2[f_basename][1]

    s = "%s %s"%(f_hash, f_path)

    if clash_group_index > 0:
        clash_count += 1
        s += " ("
        for i in range(clash_group_index):
            s += "*"
        s += ")"
        
    summary_list.append(s)


for outfile in outfiles:
    f = open(outfile[0], "w")
    for line in outfile[1]:
        f.write("%s\n"%(line))
    f.close()


print "Input file count: %d"%(len(lines))
print "Ignored: %d"%(len(ignored_list))
print "Unique: %d"%(len(summary_list))
print "Redundant: %d"%(len(workflow1_list))
print "Base filename clashes: %d"%(clash_count)
    



 
