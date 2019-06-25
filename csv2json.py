# csv2json.py
#
# Copyright 2009 Brian Gershon -- briang at webcollective.coop
# Copyright 2016 Thomas Maurin -- http://github.com/maur1th/
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

import csv
import codecs
import json
import os
import re
import sys


# Options
ENCODING = 'utf-8'
CSV_DELIMITER = ','

# Check arguments
try:
    script, input_name, model_name = sys.argv
except ValueError:
    print('\nRun via:\n\n%s input_name model_name' % sys.argv[0])
    print('\ne.g. %s airport.csv app_airport.Airport' % sys.argv[0])
    print('\nNote: input_name should be a path relative to where this script is.')
    sys.exit()

# Compute file paths and names
in_file = os.path.dirname(__file__) + input_name
if len(re.findall('\.csv$', input_name)) != 0:
    output_name = re.sub('\.csv$', '.json', input_name)
else:
    output_name += '.json'
out_file = os.path.dirname(__file__) + output_name

# Convert
print('Converting %s from CSV to JSON as %s' % (in_file, out_file))
with codecs.open(in_file, 'r', encoding=ENCODING) as f:
    reader = csv.reader(f, delimiter=CSV_DELIMITER)

    header_row = []
    entries = []

    for row in reader:
        if not header_row:
            header_row = row
            continue

        pk = row[0]
        model = model_name
        fields = {}
        print(row)
        for i in range(1, len(row)):
            # 8, 9 ,10 => M:N relationship
            if 7 < i < 11:
                # row 의 형태 : "1 3 4 5 6"
                active_field = list(map(int, row[i].split()))
                # list reference
                fields[header_row[i]] = active_field
            else:
                active_field = row[i] if row[i] != '' else '0'
                # convert numeric strings into actual numbers by converting to either
                # int or float
                if active_field.isdigit():
                    try:
                        new_number = int(active_field)
                    except ValueError:
                        new_number = float(active_field)
                    fields[header_row[i]] = new_number
                else:
                    fields[header_row[i]] = active_field.strip()

        row_dict = {}
        row_dict['pk'] = int(pk)
        row_dict['model'] = model_name
        row_dict['fields'] = fields
        entries.append(row_dict)

f.close()

with open(out_file, 'w', encoding=ENCODING) as fo:
    fo.write('%s' % json.dumps(entries, indent=4, ensure_ascii=False))
fo.close()


# Usage

## Create .json file
### python csv2json.py genre.csv movies.genre

## Data Seeding
### python manage.py loaddata actor.json