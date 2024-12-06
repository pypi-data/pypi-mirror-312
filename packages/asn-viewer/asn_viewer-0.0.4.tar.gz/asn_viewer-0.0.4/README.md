ASN files viewer tool

* Parses ASN.1 specification
* Decodes BER encoded ASN.1 files including multiple ASN Objects in one file
* Can search file content

Use as a standalone application:

```
python -m asn_viewer [-h] [-c CONFIG] [-d DEFINITION] [-o OUTPUT] [-n OBJECT_NAME] [-f [FILES ...]] [-s [SEARCH ...]]

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config filename
  -d DEFINITION, --definition DEFINITION
                        Schema Definition file
  -o OUTPUT, --output OUTPUT
                        Output filename
  -n OBJECT_NAME, --object-name OBJECT_NAME
                        ASN Object Name
  -f [FILES ...], --files [FILES ...]
                        Filenames to decode
  -s [SEARCH ...], --search [SEARCH ...]
                        Search filter

```
    
