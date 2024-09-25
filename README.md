# illumio-technical-assesment

Technical assesment for Illumio Software Engineer

## A program that can parse a file containing flow log data and maps each row to a tag based on a lookup table

The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag.\
The dstport and protocol combination decide what tag can be applied.\
\
Sample flow logs (default logs, version 2 only).\
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\
2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK

For e.g.  the lookup table file can be something like:\
dstport,protocol,tag\
25,tcp,sv_P1\
68,udp,sv_P2\
\
The program should generate an output file containing the following:\
\
Count of matches for each tag, sample o/p shown below\
Tag Counts:\
Tag,Count\
sv_P2,1
\
Count of matches for each port/protocol combination\
Port/Protocol Combination Counts:\
Port,Protocol,Count\
22,tcp,1\
23,tcp,1

### Requirement details

* Input file as well as the file containing tag mappings are plain text (ascii) files  
* The flow log file size can be up to 10 MB
* The lookup file can have up to 10000 mappings
* The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample above.
* The matches should be case insensitive

### Assumptions

* The flow log format is consistent (version 2 only).
* Protocols are mapped from their numeric codes (e.g., 6 for TCP, 17 for UDP, 1 for ICMP).
* The lookup table is case-insensitive for protocols.
* Logs without matching tags are categorized as “Untagged.”

### Notes

* Used a class based approach as it is easier to add more fucntions as and when required
* The output is written into two CSV files port_protocol_counts.csv and tag_counts.csv.
* The program takes the flow logs and lookup table filenames as the input.

### Instructions to run the code


#### Prerequisites

* Make sure you have Python 3.x installed on your system.
* No additional external libraries are required; the program uses standard Python libraries like csv and os.

#### Files needed

* Clone the git repository, and go to the project folder.
* Update the files lookup_table.csv - CSV file containing port, protocol and tag mappings, flow_logs.txt - text file having flow logs data in version 2

#### Run the program

* Run the python file main.py. `python3 main.py`
* Input the  flow logs and lookup table filenames.
* The output is written into two CSV files port_protocol_counts.csv and tag_counts.csv.

### Tests performed

#### Test case 1: Valid lookup table and flow logs provided

* A valid lookup_table.csv and flow_logs.txt file were provided.
* Result: The program successfully mapped ports and protocols to tags, generated the correct tag and port counts, and created the tag_counts.csv and port_protocol_counts.csv files.

#### Test Case 2: Lookup Table File not found:

* The lookup table file was missing.
* Result: The program raised a FileNotFoundError and printed the error message: Lookup table file 'lookup_table.csv' not found.

#### Test Case 3: Invalid Flow Log Format:

* A flow log entry was modified to have fewer columns or the wrong version (not version 2).
* Result: The program skipped invalid log entries and printed a warning for each invalid line, e.g., Skipping invalid log entry.

#### Test Case 4: Missing Header in CSV File:

* The lookup_table.csv was modified to have incorrect or missing headers (e.g., missing tag).
* Result: The program raised a KeyError and printed the message: lookup table CSV file is missing one/more required headers: ['dstport', 'protocol', 'tag'].

#### Test Case 6: Untagged Entries:

* The flow log contained entries that didn’t match any dstport/protocol combination in the lookup table.
* Result: Those entries were tagged as Untagged, and the Untagged count was correctly incremented.

#### Test Case 5: Invalid Data in Lookup Table:

* Some rows in the lookup_table.csv had missing or invalid data (e.g., empty dstport or tag).
* Result: The program skipped those rows and printed an error message: Invalid lookup table entry {...}.

### Analysis of the Code/Program:

#### Design Choices:

* Class-Based Design: The program is designed as a class (FlowLogParser), which organizes the functionality into distinct methods for loading the lookup table, parsing the flow logs, and writing output. This makes the code modular and reusable.
* Default Dictionaries: defaultdict is used to simplify the counting of tags and port/protocol combinations, reducing the need for explicit checks on whether a key exists.
* Error Handling: Comprehensive error handling has been added for file I/O operations, missing data, and incorrect formats, ensuring the program runs smoothly even in the face of common user errors.

#### Performance Considerations:

* The program is designed to handle lookup tables with up to 10,000 entries and flow logs up to 10 MB. By loading the lookup table into memory as a dictionary, it allows for fast lookups while parsing flow logs.
* Since the program does not use external libraries, its performance is sufficient for the task’s scale, but for extremely large datasets, you might consider optimizations (like parallel processing or using a database).

#### Limitations:

* Case Sensitivity: The protocol lookup is case-insensitive (tcp, udp), but other parts of the code (such as port numbers) expect exact matches. If port numbers or protocols are formatted inconsistently in input files, it could affect matching.
* Flow Log Format: The program is designed to handle AWS default log format (version 2). It does not support custom formats or other versions of flow logs.

#### Possible Enhancements:

* Configurable Version Files: Allow users to specify the flow log version and configure code accordingly to be compatible with all versions.
*  Logging: Add a logging mechanism to log errors, warnings, and information instead of printing to the console.
*  Unit Tests: Write unit tests for each method to ensure correct functionality with various edge cases.