import requests



def request_nlu(text, project_dir, port):
    url = 'http://localhost:' + port + '/parse'
    print(url)
    data = {
        "q": text,
        "project": project_dir,
        "model": "nlu"
    }
    try:
        response = requests.post(url, json=data)
    except Exception as e:
        print(e)
        return None
    
    return response.json()


if __name__ == '__main__':
    print(request_nlu('Li Fu', 'name_server', '5061'))