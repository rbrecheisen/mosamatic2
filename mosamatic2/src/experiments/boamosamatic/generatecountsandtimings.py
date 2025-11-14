import utils

file_mapping = utils.load_dictionary('filemapping.json')
time_per_scan = 30/42.0
counts = {}
for l3_file_path, _ in file_mapping.items():
    hospital_name = utils.get_parent_name(l3_file_path)
    if hospital_name not in counts.keys():
        counts[hospital_name] = [0, 0]
    counts[hospital_name][0] += 1
    counts[hospital_name][1] += time_per_scan
utils.save_dictionary(counts, 'countsandtimings.json')