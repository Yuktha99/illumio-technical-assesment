from collections import defaultdict
import csv

"""
Write a program that can parse a file containing flow log data and maps each row to a tag based on a lookup table. 
The lookup table is defined as a csv file, and it has 3 columns, dstport,protocol,tag.   
The dstport and protocol combination decide what tag can be applied.   

Sample flow logs (default logs, version 2 only). 
2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK 
2 123456789012 eni-4d3c2b1a 192.168.1.100 203.0.113.101 23 49154 6 15 12000 1620140761 1620140821 REJECT OK 

For e.g.  the lookup table file can be something like: 
dstport,protocol,tag 
25,tcp,sv_P1 
68,udp,sv_P2 

The program should generate an output file containing the following:
 
Count of matches for each tag, sample o/p shown below 
Tag Counts:
Tag,Count 
sv_P2,1 

Count of matches for each port/protocol combination 
Port/Protocol Combination Counts: 
Port,Protocol,Count 
22,tcp,1 
23,tcp,1 


Requirement details 

Input file as well as the file containing tag mappings are plain text (ascii) files  
The flow log file size can be up to 10 MB 
The lookup file can have up to 10000 mappings 
The tags can map to more than one port, protocol combinations.  for e.g. sv_P1 and sv_P2 in the sample above. 
The matches should be case insensitive 
"""


class FlowLogParser:
    def __init__(self, flow_logs_file_name, lookup_table_file_name):
        # input files
        self.flow_logs_file_name = flow_logs_file_name
        self.lookup_table_file_name = lookup_table_file_name
        self.lookup_table = {}

        # output data
        self.tag_counts = defaultdict(int)
        self.port_protocol_counts = defaultdict(int)
        self.untagged_count = 0

    @staticmethod
    def get_protocol(protocol_number):
        if protocol_number == '6':
            return 'tcp'
        if protocol_number == '17':
            return 'udp'
        return 'icmp'

    """
    Function to load the contents of the lookup file into a dict/map
    """
    def load_lookup_table(self):
        with open(self.lookup_table_file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                port = row['dstport']
                protocol = row['protocol'].lower()
                tag = row['tag']

                # store data into a dict
                self.lookup_table[(port, protocol)] = tag
        # print(self.lookup_table)

    """
    Function to parse the flow logs 
    and update the tag_counts and port_protocol_counts 
    """
    def parse_flow_logs(self):
        with open(self.flow_logs_file_name, 'r') as file:
            for line in file:
                parts = line.split()

                # skip the log if it is not version 2 or invalid log
                if len(parts) < 14 or parts[0] != '2':
                    continue

                # retrieve the necessary data
                dstport = parts[5]
                protocol = FlowLogParser.get_protocol(parts[7])
                key = (dstport, protocol)

                # update the tag_counts and port_protocol_counts
                tag = self.lookup_table.get(key, 'Untagged')
                if tag == 'Untagged':
                    self.untagged_count += 1
                else:
                    self.tag_counts[tag] += 1

                self.port_protocol_counts[key] += 1

    """
    Function to write output to the output files
    """
    def write_output(self):
        print("tag counts==>")
        with open('tag_counts.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tag', 'Count'])
            for tag, count in self.tag_counts.items():
                print(tag,count)
                writer.writerow([tag, count])
            writer.writerow(['Untagged', self.untagged_count])
        
        print("port protocol counts==>",self.port_protocol_counts)
        with open('port_protocol_counts.csv','w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Port','Protocol','Count'])
            for (port, protocol), count in self.port_protocol_counts.items():
                print(port,protocol,count)
                writer.writerow([port,protocol,count])
    
    """
    Driver code 
    """
    def run(self):
        self.load_lookup_table()
        self.parse_flow_logs()
        self.write_output()
        print("Processing complete. Output is written to the files - tag_counts.csv, port_protocol_counts.csv")
        

if __name__=='__main__':
    flow_logs_file_name = input("Enter the flow logs file(.txt):")
    lookup_table_file_name = input("Enter the lookup table file(.CSV):")
    
    parser = FlowLogParser(flow_logs_file_name,lookup_table_file_name)
    parser.run()
    