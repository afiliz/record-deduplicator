## Record De-Duplicator
This program takes in a JSON file containing account records and de-duplicates them based on record ID and email. After running the program, no record will have the same ID or email.

Files to be de-duplicated should be in the same format as leads.json in the /examples folder. Example output of the program is provided as well in /examples.

## Usage
    python3 deduplicator.py [filepath]

ex: python3 deduplicator.py examples/leads.json

The program will produce 2 files:
- [filename]_deduped_log.json: Log containing each step taken to de-duplicate the given file, including the source record, output record, and field changes.
- [filename]_deduped_result.json: De-duplicated JSON record file. 

