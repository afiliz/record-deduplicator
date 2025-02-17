import json
import argparse
from datetime import datetime
from dataclasses import asdict, dataclass

@dataclass
class FieldChange:
	field: str
	old_value: str
	new_value: str

@dataclass
class RecordChange:
	old_record: dict
	new_record: dict
	field_changes: list

class DedupeHandler():
	def __init__(self, file_name=None):
		self.file_name = file_name
		self.json_data = json.load(open(file_name))
		self.records = self.json_data['leads']
		self.dupe_name = file_name.split('.')[0]

	def compare_fields(self, source, output):
		differences = []

		for field in source:
			if source[field] != output[field]:
				differences.append(FieldChange(field, source[field], output[field]))

		return differences

	# Use dedupe key ('_id' or 'email') to check for duplicates
	def dedupe_field(self, records, dedupe_key):
		unique_records = {}
		change_logs = []

		# Use dict to check against for duplicates
		for record in records:
			record_key = record[dedupe_key]

			if record_key not in unique_records:
				unique_records[record_key] = record
				change_logs.append(RecordChange(record, record, []))
			else:
				# Replace if new record is more recent, or if there is a date match, replace with new record
				current_record_date = datetime.fromisoformat(unique_records[record_key]['entryDate'])
				compare_record_date = datetime.fromisoformat(record['entryDate'])

				if current_record_date <= compare_record_date:
					change_logs.append(RecordChange(unique_records[record_key], record, self.compare_fields(unique_records[record_key], record)))
					unique_records[record_key] = record
					

		return [list(unique_records.values()), [asdict(log) for log in change_logs]]
	
	def dedupe_records(self):
		deduped_ids = self.dedupe_field(self.records, '_id')
		deduped_data = self.dedupe_field(deduped_ids[0], 'email')

		dedupe_logs = {'id_deduplication': deduped_ids[1], 'email_deduplication': deduped_data[1]}

		print(f'De-duped records in provided file. Writing results to {self.dupe_name}_deduped_result.json...')
		deduped_result = {'leads': deduped_data[0]}
		with open(self.dupe_name + '_deduped_result.json', 'w') as f:
			json.dump(deduped_result, f, indent=4)
		print(f'Writing de-duplication logs to {self.dupe_name}_deduped_log.json...')
		with open(self.dupe_name + '_deduped_log.json', 'w') as f:
			json.dump(dedupe_logs, f, indent=4)

		return deduped_data

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument("file_path", help="Path of JSON file to deduplicate")
	args = parser.parse_args()

	dedupe_handler = DedupeHandler(file_name=args.file_path)
	dedupe_handler.dedupe_records()