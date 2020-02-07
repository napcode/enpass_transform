import json
import sys
import csv
import argparse

class Entry:
    url = ''
    type = ''
    username = ''
    password = ''
    hostname = ''
    extra = ''
    name = ''
    grouping = ''

def write_csv(outputfile, entries):
    lfile = open(outputfile, 'w')
    fieldnames = ['url','type','username','password','hostname','extra','name','grouping']
    writer = csv.DictWriter(lfile, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    for row in entries:
        writer.writerow({
            'url': row.url,
            'type': row.type,
            'username': row.username,
            'password': row.password,
            'hostname': row.hostname,
            'extra': row.extra,
            'name': row.name,
            'grouping': row.grouping
            })


def parse_folder_dict(enpass_json):
    result = dict()
    for folder in enpass_json['folders']:
        result[folder['uuid']] =  folder['title']
    return result


def find_field(label, fields):
    for field in fields:
        if field['label'].lower() == label.lower():
            return field['value']
    return ""


def parse_items(enpass_json, folders, override_group):
    result = [];
    for item in enpass_json['items']:
        entry = Entry()
        if not 'fields' in item:
            # secure note
            entry.url = 'http://sn'
        else:
            entry.username = find_field('Username', item['fields'])
            entry.url = find_field('url', item['fields'])
            entry.password = find_field('password', item['fields'])
        entry.extra = item['note']
        if item['subtitle']:
            entry.name = item['title'] + " - " + item['subtitle']
        else:
            entry.name = item['title']
        if override_group:
            entry.grouping = override_group
        else:
            if 'folders' in item:
                entry.grouping = folders[item['folders'][0]]

        result.append(entry)

    return result


def main(argv):
    parser = argparse.ArgumentParser(description = 'Transforms an Enpass JSON export to LastPass CSV')
    parser.add_argument('-i', '--input', required = True, help = 'JSON exported from Enpass')
    parser.add_argument('-o', '--output', default = 'lastpass_import.csv', help = 'CSV to be imported into LastPass')
    parser.add_argument('-g', '--group', help = 'Optional group/folder name. Useful to import into a separate folder within LastPass. If not set, first folder that is referenced by the Enpass item will be used.')
    
    args = parser.parse_args(argv)

    enpass_json = json.load(open(args.input, 'r'))
    folders = parse_folder_dict(enpass_json)
    entries = parse_items(enpass_json, folders, args.group)
    write_csv(args.output, entries)
    print("Wrote " + args.output)
    print("# folders: {}".format(len(folders)))
    print("# input items: {}".format(len(enpass_json['items'])))
    print("# output items: {}".format(len(entries)))


if __name__ == "__main__":
    main(sys.argv[1:])
