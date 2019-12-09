import json as js

output = {}
for i in range(3):
    with open('data_{}.json'.format(i),'r') as f:
        data = js.load(f)

    for k,v in data.items():
        output[k] = v


with open('data.json','w') as f:
    js.dump(output,f,indent=4)
