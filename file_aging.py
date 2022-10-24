# Script requires 1 positional sys argument of numeric value for days since last accessed. Output is a CSV file with filenames, last accessed date, and file size in the same directory that the script was ran in. Also displays a total file count and total file size

# Example command to run script:  python file_aging.py 60  
# Will output a CSV with files in current directory and all sub-directories that have not been accessed in 60 days.

import os
import sys
import time
import csv

older_than = int(sys.argv[1])
older_than_in_secs = older_than * 86400
dir = "./"
files_to_review = []

def scan_dir(dir):
    count = 0
    size = 0
    for file in os.listdir(dir):
        if os.path.isdir(file):
            count1, size1 = scan_dir(file)
            count += count1
            size += size1
        elif os.path.isfile(file):
            last_accessed = os.path.getatime(file)
            if last_accessed > older_than_in_secs:
                file_size = os.path.getsize(file)
                file_size_in_mb = file_size / (1024 * 1024)
                files_to_review.append([file, time.ctime(last_accessed), f"{file_size_in_mb} MBs"])
                count += 1
                size += file_size_in_mb
    return count, size

total_count, total_size = scan_dir(dir)

with open (f"files_not_touched_in_{older_than}_days.csv", "w", newline="") as f:
    writer = csv.writer(f, dialect="excel")
    writer.writerow(["Filename", "Last Accessed", "Size (MB)"])
    writer.writerows(files_to_review)
    writer.writerow([f"Total Files to review: {total_count}",f"Total Size of Files to review: {total_size} MBs"])
