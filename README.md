# csv2json-fixture
This script can be used to convert CSV data to [Django fixtures](https://docs.djangoproject.com/en/stable/howto/initial-data/) JSON format.

## Usage
```
python3 csv2json.py file.csv app.Model
python3 manage.py loaddata file.json
```

## License
This is Korean port of [maur1th's code](https://github.com/maur1th/csv2json-fixture) licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)

This is a Python 3 port of [Brian Gershon's code](https://djangosnippets.org/snippets/1680/) licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0)

## Many-to-many
M:N 관계를 형성하기 위해, 미리 csv file값(row value)에 공백으로 데이터를 구분한 String값을 저장함. (ex `"1 2 3 4 5"`)

csv2json.py가 실행되면 for문을 순회하며 각 row값을 split() 함수로 분리하여 map()을 통해 int형으로 변환.

리스트 형태로 reference를 지정하고, json 파일로 변환을 시도하면 원하는 관계형 정보로 저장됨.

- M:N 관계를 미리 파악하여, 해당 데이터를 String 형태로 준비. 
  - 이렇게 했던 이유는 csv 파일을 자동화 코드로 조작하여 만들었기 때문에, 재가공할 필요가 있었음.
- 데이터가 비어있거나, 순회 범위 혹은 column 값을 잘 확인해야함.
```python
# row 의 형태 : "1 3 4 5 6"
active_field = list(map(int, row[i].split()))
# list reference
fields[header_row[i]] = active_field
```