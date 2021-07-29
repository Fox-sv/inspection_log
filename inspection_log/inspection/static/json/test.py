import json, datetime

with open('images_name.json', 'r') as f:
	dict_ = json.load(f)

# print(json.dumps(dict_, indent=4))

# list_ = ['as', 'bs', 'qs']
# list_.remove('as')
# print(list_)


a = datetime.datetime.today()
print(len(a))