import requests
import json
import time

TOKEN = 'whos-2d1a91b4-c7e1-41b7-8768-21840fe56ef2'

def features():
    try:
        url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/features?limit=10000'   
        resp = requests.get(url)
        data = json.loads(resp.text)
        with open('features.json', 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(str(e))
            
def get_foi_id():
    with open('feature_informations.json', 'r') as f:
        data_feat = f.read()
        parsed_data_feat = json.loads(data_feat)
        results = parsed_data_feat['results']
        with open('observations_resp.json', 'r') as g:
            data_obs = g.read()
            parsed_data_obs = json.loads(data_obs)
            members = parsed_data_obs['member']
            for feature in results:
                for member in members:
                    if feature['id'] == member['featureOfInterest']['href'] and feature['parameter'][0]['value'] == 'Argentina':
                        id = feature['id']
                        begin = member['phenomenonTime']['begin']
                        end = member['phenomenonTime']['end']
                        ob_id = member['id']
                        print('\n' + id + '\n', begin, '|', end + '\n', ob_id +'\n')
                        try:
                            # url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/observations?observationIdentifier={id}&beginPosition={begin}&endPosition={end}&includeData=true&useCache=true&offset=1&limit=1000'
                            # url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/observations?feature={ob_id}&beginPosition={begin}&endPosition={end}&includeData=true&useCache=true&offset=1&limit=1000'
                            url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/observations?observationIdentifier={id}&beginPosition={begin}&endPosition={end}&includeData=true&useCache=true&offset=1&limit=1000'
                            resp = requests.get(url)
                            if "No timeseries matched" in resp.text:
                                time.sleep(1)
                                continue
                            else:
                                data = json.loads(resp.text)
                                with open(f'{ob_id}.json', 'w') as f:
                                    json.dump(data, f)
                                time.sleep(1)
                        except Exception as e:
                            print('bad resp', str(e))
                            continue
                        
##########################################

def get_ids_timestamps():
    try:
        # url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/observations?limit=10&useCache=true'
        url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/observations'   
        resp = requests.get(url)
        data = json.loads(resp.text)
        return data
    except Exception as e:
        print(str(e))                        

def get_metadata_with_ob_id(observation_identifier):
    try:
        url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/observations?observationIdentifier={observation_identifier}'   
        resp = requests.get(url)
        data = json.loads(resp.text)
        # with open(f'{observation_identifier}_metadata.json', 'w') as f:
        #     json.dump(data, f)
        members = data['member']
        metadata_for_id = []
        for member in members:
            metadata = member['result']['metadata']
            default_point_metadata = member['result']['defaultPointMetadata']
            metadata_for_id.append(metadata)
            metadata_for_id.append(default_point_metadata)
        return metadata_for_id
    except Exception as e:
        print(str(e))

def get_data_with_id(observation_id):
    try:
        url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/observations?observationIdentifier{observation_id}&includeData=true&limit=2'   
        resp = requests.get(url)
        data = json.loads(resp.text)
        # with open(f'get_data_id_{observation_id}.json', 'w') as f:
        #     json.dump(data, f)    
        print(data)
        return data
    except Exception as e:
        print(str(e))    

def get_data_with_id_and_timerange(observation_id, begin_position, end_position):
    try: 
        url = f'https://whos.geodab.eu/gs-service/services/essi/token/{TOKEN}/view/whos-emodnet/om-api/observations?observationIdentifier{observation_id}&beginPosition={begin_position}&endPosition={end_position}&includeData=true&limit=1' 
        resp = requests.get(url)
        data = json.loads(resp.text)
        # with open(f'get_data_id_timerange_{observation_id}_usecache.json', 'w') as f:
        #     json.dump(data, f)    
        print(data)
        return data
    except Exception as e:
        print(str(e))

# print(get_metadata_with_ob_id('1853D77030E9D16A907D794578C0CA8DD85E9A58'))
# print(get_ids_timestamps())
# get_data_with_id('1853D77030E9D16A907D794578C0CA8DD85E9A58')
# get_data_with_id_and_timerange('1853D77030E9D16A907D794578C0CA8DD85E9A58','2024-01-28T19:00:00Z','2024-01-30T00:00:00Z')

features()