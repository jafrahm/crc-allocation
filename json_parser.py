import json
from pprint import pprint 

def parse_file(filename):
 
    json_data=open(filename)
    data = json.load(json_data)

    for x in data:
        tmp = x["owner"]["username"]
	tmp = tmp + "," + x["name"]
        tmp = tmp + "," + str(round(x["used"]))
        tmp = tmp + "," + str(round(x["credit"]))
        tmp = tmp + "," + str(round(x["balance"]))
        for u in x["members"]:
            tmp = tmp + "," + u["username"]
        print tmp
  
    json_data.close()

if __name__ == '__main__':      
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file", help="file to parse")
    
    (options, args) = parser.parse_args()
    
    if options.file:
        parse_file(options.file)
    
