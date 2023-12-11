import os, json, datetime

BASE_DIR = os.path.dirname(__file__)
SAVE_FILE = BASE_DIR + '/data/bbs.json'

def load_data():
    if not os.path.exists(SAVE_FILE):
        return []
    with open(SAVE_FILE, 'r') as fin:
        return json.load(fin)

def save_data(data_list):
    with open(SAVE_FILE, 'w') as fout:
        json.dump(data_list, fout, ensure_ascii=False, indent=2)

def save_data_append(user, text):
    now = datetime.datetime.now()
    strtime = f'{now:%Y/%m/%d %H:%M}'
    data = {'name': user, 'text': text, 'date':strtime}
    data_list = load_data()
    data_list.insert(0, data) # 最新の投稿を先頭に挿入
    save_data(data_list)
