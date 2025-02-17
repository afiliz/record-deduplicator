import json
from datetime import datetime

def dedupe_records(records, dedupe_key):
	unique_entries = {}

	for record in records:
		record_key = record[dedupe_key]

		if record_key not in unique_entries:
			unique_entries[record_key] = record
		else:
			current_record_date = datetime.fromisoformat(unique_entries[record_key]['entryDate'])
			compare_record_date = datetime.fromisoformat(record['entryDate'])

			if current_record_date <= compare_record_date:
				unique_entries[record_key] = record

	return list(unique_entries.values())

with open('leads.json', 'r') as f:
	records = json.load(f)['leads']

deduped_ids = dedupe_records(records, 'email')
deduped_data = dedupe_records(deduped_ids, '_id')

deduped_result = {'leads': deduped_data}

with open('deduped_leads.json', 'w') as f:
	json.dump(deduped_result, f, indent=4)