import json
from datetime import datetime
from dataclasses import dataclass

@dataclass
class FieldChange:
	field: str
	old_value: str
	new_value: str


class DedupeHandler():
	def __init__(self, file_name=None):
		self.file_name = file_name
		self.json_data = json.load(open(file_name))
		self.records = self.json_data['leads']

	def dedupe_field(self, records, dedupe_key):
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
	
	def dedupe_records(self):
		deduped_ids = self.dedupe_field(self.records, '_id')
		deduped_data = self.dedupe_field(deduped_ids, 'email')

		print("Deduped records in provided file. Writing results to deduped_leads.json...")
		deduped_result = {'leads': deduped_data}
		with open('deduped_leads.json', 'w') as f:
			json.dump(deduped_result, f, indent=4)

		return deduped_data

if __name__ == '__main__':
	dedupe_handler = DedupeHandler(file_name='leads.json')
	dedupe_handler.dedupe_records()