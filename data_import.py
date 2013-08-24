import json
from collections import defaultdict
import csv
import sys
import chardet
import codecs


def __csvfile(datafile):
    """ Detect file encoding and open appropriately """
    filehandle = open(datafile)
    diagnose = chardet.detect(filehandle.read())
    charset = diagnose['encoding']
    try:
        csvfile = codecs.open(datafile, 'r', charset)
    except IOError:
        error('Could not open specified csv file, %s, or it does not exist' % datafile, 0)
    else:
        return list(charset_csv_reader(csv_data=csvfile, 
                                            charset=charset))

def charset_csv_reader(csv_data, dialect=csv.excel, charset='utf-8', **kwargs):
    csv_reader = csv.reader(charset_encoder(csv_data, charset), 
                            dialect=dialect, **kwargs)
    csv_reader.next()
    for row in csv_reader:
        yield [unicode(cell, charset) for cell in row]

def charset_encoder(csv_data, charset='utf-8'):
    for line in csv_data:
        yield line.encode(charset)

def handle(*args):
    csvfilename = args[0]
    csvfile = __csvfile(csvfilename)

    d = defaultdict(list)
    d['name'] = "LokSabha"
    for row in csvfile:
        state = row[0].strip()
        child = next((x for x in d['children'] if x['name'] == state), None)
        if child is None:
            d['children'].append({
                'name': state,
                'children': [{
                        'name': row[1].strip()
                    }]
                })
        else:
            child['children'].append({'name': row[1].strip()})

    print json.dumps([d])
if __name__ == "__main__": handle(*sys.argv[1:])