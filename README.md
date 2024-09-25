# illumio-technical-assesment

Technical assesment for Illumio Software Engineer

## A program that can parse a file containing flow log data and maps each row to a tag based on a lookup table

The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag.\
The dstport and protocol combination decide what tag can be applied.\
\
Sample flow logs (default logs, version 2 only).\
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK\
2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK\

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
sv_P2,1\
\
Count of matches for each port/protocol combination\
Port/Protocol Combination Counts:\
Port,Protocol,Count\
22,tcp,1\
23,tcp,1\

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

