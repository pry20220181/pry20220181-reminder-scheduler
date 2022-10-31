import json

def get_app_settings():
    with open('appsettings.json') as f:
        data = json.load(f)
        return data

if __name__ == '__main__':
    app_settings = get_app_settings()
    print(app_settings['RestApi']['BaseUrl'])