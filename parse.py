import json

with open('apidata.txt') as f:
    the_api_data = f.read()
print(f'the api data is {the_api_data}')
#convert cached and stringified api data back to json for parsing
json_object = json.loads(the_api_data)

print(json_object)
#output
#<class 'dict'>

#access first_name in dictionary
# print(json_object["first_name"])
