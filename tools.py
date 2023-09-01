import os
import yaml

def load_config():
    path = os.path.dirname(os.path.realpath(__file__)) + "/config.yaml"
    #print(path)
    with open(path, "r", encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config
def get_useragent():
    return "Skland/1.0.1 (com.hypergryph.skland; build:100001014; Android 30; ) Okhttp/4.11.0"
