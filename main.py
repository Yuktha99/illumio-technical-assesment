from collections import defaultdict
import csv
import os

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

    """
    Function to get protocol name from the number from flow logs 
    """
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
        if not os.path.exists(self.lookup_table_file_name):
            raise FileNotFoundError(f'Lookup Table File {self.lookup_table_file_name} not found.')
        try:
            with open(self.lookup_table_file_name, 'r') as file:
                reader = csv.DictReader(file)
                expected_headers = ['dstport','protocol','tag']
                if not all(header in reader.fieldnames for header in expected_headers):
                    raise KeyError("lookup table CSV file is missing one/more required headers:",expected_headers)
                for row in reader:
                    port = row['dstport']
                    protocol = row['protocol'].lower().strip()
                    tag = row['tag'].strip()
                    
                    # skip invalid data
                    if not port or not protocol or not tag:
                        raise ValueError("Invalid lookup table entry", row)

                    # store data into a dict
                    self.lookup_table[(port, protocol)] = tag
        except Exception as e:
            print("Error reading lookup table:",e)

    """
    Function to parse the flow logs 
    and update the tag_counts and port_protocol_counts 
    """
    def parse_flow_logs(self):
        if not os.path.exists(self.flow_logs_file_name):
            raise FileNotFoundError(f'Flow logs File {self.flow_logs_file_name} not found.')
        try:
            with open(self.flow_logs_file_name, 'r') as file:
                for line in file:
                    parts = line.split()

                    # skip the log if it is not version 2 or invalid log
                    if len(parts) < 14 or parts[0] != '2':
                        print("skipping invalid log entry:",{line.strip()})
                        continue

                    # retrieve the necessary data
                    dstport = parts[6] # dst port is at index 6
                    protocol = FlowLogParser.get_protocol(parts[7]) # protocol number is at index 7
                    key = (dstport, protocol)

                    # update the tag_counts and port_protocol_counts
                    tag = self.lookup_table.get(key, 'Untagged')
                    if tag == 'Untagged':
                        self.untagged_count += 1
                    else:
                        self.tag_counts[tag] += 1

                    self.port_protocol_counts[key] += 1
        except Exception as e:
            print("Error parsing flowlogs file:",e)

    """
    Function to write output to the output files
    """
    def write_output(self):
        with open('tag_counts.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Tag', 'Count'])
            for tag, count in self.tag_counts.items():
                writer.writerow([tag, count])
            writer.writerow(['Untagged', self.untagged_count])
        
        with open('port_protocol_counts.csv','w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Port','Protocol','Count'])
            for (port, protocol), count in self.port_protocol_counts.items():
                writer.writerow([port,protocol,count])
    
    """
    Driver code 
    """
    def run(self):
        try: 
            self.load_lookup_table()
            self.parse_flow_logs()
            self.write_output()
            print("Processing complete. Output is written to the files - tag_counts.csv, port_protocol_counts.csv")
        except Exception as e:
            print("Error during processing:",e)
        

if __name__=='__main__':
    flow_logs_file_name = input("Enter the flow logs file(.txt):")
    lookup_table_file_name = input("Enter the lookup table file(.CSV):")
    
    parser = FlowLogParser(flow_logs_file_name,lookup_table_file_name)
    parser.run()
    