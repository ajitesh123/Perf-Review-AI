import yaml
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient

def load_config():
    with open('backend/config.yaml', 'r') as file:
        return yaml.safe_load(file)

CONFIG = load_config()

kinde_configuration = Configuration(host=CONFIG['kinde']['domain'])

kinde_api_client_params = {
    "configuration": kinde_configuration,
    "domain": CONFIG['kinde']['domain'],
    "client_id": CONFIG['kinde']['client_id'],
    "client_secret": CONFIG['kinde']['client_secret'],
    "grant_type": GrantType.AUTHORIZATION_CODE,
    "callback_url": CONFIG['kinde']['callback_url']
}

kinde_client = KindeApiClient(**kinde_api_client_params)