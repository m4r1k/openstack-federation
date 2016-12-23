#!/usr/bin/python

from __future__ import print_function
import argparse
from lxml import etree
import sys

args = None

namespaces = {
    'saml'  : 'urn:oasis:names:tc:SAML:2.0:assertion',
    'samlp' : 'urn:oasis:names:tc:SAML:2.0:protocol',
    'md'    : 'urn:oasis:names:tc:SAML:2.0:metadata',
    'ds'    : 'http://www.w3.org/2000/09/xmldsig#',
    'xenc'  : 'http://www.w3.org/2001/04/xmlenc#',
    'xs'    : 'http://www.w3.org/2001/XMLSchema',
}

#-------------------------------------------------------------------------------

def get_entity_id(doc):
    entity_descriptor = doc.xpath('//md:EntityDescriptor',
                                  namespaces=namespaces)

    # Locate the EntityDescriptor element, assure there is exactly one
    if not entity_descriptor:
        raise ValueError("could not locate the EntityDescriptor")

    if len(entity_descriptor) > 1:
        raise ValueError("multiple EntityDescriptor elements found (%d)"
                         % len(entity_descriptor))
        
    # Locate the entityID attributes in the EntityDescriptor element,
    # assure there is exactly one
    entity_id = entity_descriptor[0].xpath('@entityID')

    if not entity_id:
        raise ValueError("could not locate the entityID attribute")

    if len(entity_id) > 1:
        raise ValueError("multiple entityID attributes found (%d)"
                         % len(entity_id))
        
    # return the entityID
    return entity_id[0]

#-------------------------------------------------------------------------------

def main():
    global args

    # Get command line arguments
    parser = argparse.ArgumentParser(
        description='Extract info from SAML2 metadata')

    parser.add_argument('filename', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)

    args = parser.parse_args()

    # Parse the XML metadata file
    try:
        doc = etree.parse(args.filename)
    except Exception as e:
        print("ERROR cannot parse file %s: %s" %
              (args.filename.name, e), file=sys.stderr)
        return 1

        
    # Extract the entity ID
    try:
        entity_id = get_entity_id(doc)
    except Exception as e:
        print("ERROR %s, input file=%s" %
              (e, args.filename.name), file=sys.stderr)
        return 2

    print(entity_id)
    
    return 0

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main())
