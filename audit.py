"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix 
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "nashville.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Circle", ""]

# UPDATE THIS VARIABLE
mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd":"Road",
            "Ave":"Avenue"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m.group() in mapping.keys():
        if m not in expected:
            name = re.sub(m.group(), mapping[m.group()], name)

    return name


def test():
    st_types = audit(OSMFILE)
    # assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
            if name == "Powder Springs Rd":
                assert better_name == "Powder Springs Road"


if __name__ == '__main__':
    test()

# In this function the city names are being cleaned up along with making it capitalised to make the city names consistent

def clean_c(city):
    if ',' in city:
        city = city.split(',')[0]
    elif '-' in city:
        city = city.split('-')[1]
    return(city.title())

cities = {}

for _, element in ET.iterparse(OSMFILE, events=("start",)):

    if element.tag == 'way' or element.tag == 'node':
        for tag in element.iter('tag'):
            if tag.attrib['k'] == 'addr:city':
                if ',' in tag.attrib['v'] or '-' in tag.attrib['v']:
                    bad_city = tag.attrib['v']
                    clean_city = clean_c(bad_city)
                    if bad_city not in cities:
                        cities[bad_city] = clean_city

pprint.pprint (cities)