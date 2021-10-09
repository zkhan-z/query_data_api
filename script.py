port requests
import json





def fetch_json():
    h = {'Content-Type': 'application/json'}
    body = {
        "start": "add time",
        "filter": {
            "add filter": "add filter"
        }
    }
    ss = "["+requests.post('add api uri',headers=h,json=body).content.decode('utf-8').replace('}}','}},')[:-1] + "]"
    data = json.loads(ss.replace('}},]','}}]'))

    with open('data.json','w') as f:
        json.dump(data , f)

    return data

def process(data):
    names = list(set([x['name'] for x in data if "env" in x['name']]))
    output = {}
    for name in names:
        print(f"Scanning for {name}...")
        print("--"*14)
        values = [float(x['value']) for x in data if x['name']==name]
        avg = round(sum(values)/len(values),2)
        minVal = min(values)
        maxVal = max(values)
        minNode = list([[x['meta']['node'],x['timestamp']] for x in data if x['name']==name and x['value']==minVal])[0]
        maxNode = list([[x['meta']['node'],x['timestamp']] for x in data if x['name']==name and x['value']==maxVal])[0]
        if not output.get(name):
            output[name] = {}
        output[name]['minVal'] = minVal
        output[name]['maxVal'] = maxVal

        output[name]['minVal_node'] = minNode[0]
        output[name]['maxVal_node'] = maxNode[0]
        output[name]['minVal_timestamp'] = minNode[1]
        output[name]['maxVal_timestamp'] = maxNode[1]
        output[name]['average'] = avg
    return output

data = fetch_json()
output = (process(data))

with open('output.json','w') as f:
    json.dump(output, f)
