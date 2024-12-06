import time, os, subprocess, uuid, traceback
from datetime import datetime


def call_copyq(*args):
    copyq = os.environ["COPYQ"]
    return subprocess.Popen([copyq] + list(args), stdout=subprocess.PIPE).communicate()[0]

def get_doc_path():
    user_home_directory = os.path.expanduser('~')
    return os.path.join(user_home_directory, "Documents")

def get_log_path():
    return os.path.join(get_doc_path(), r'copyq-logs.txt')

def log(s):
    # 获取当前时间
    now = datetime.now()
    time_str = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
    with open(get_log_path(), 'a') as f:
        f.write(time_str+': '+str(s)+'\n')

def get_copyq_data():
    log("store: before call copyq")
    try:
        item1 = call_copyq('read', '0')
        item1 = item1.decode('utf-8')
        tags = call_copyq('read', 'application/x-copyq-tags', '0')
        notes = call_copyq('read', 'application/x-copyq-item-notes', '0')
        notes = notes.decode('utf-8')
        # log(notes)
        tags = tags.decode('utf-8')

        data = {"uuid": str(uuid.uuid4()), "content": item1, "timestamp": time.time(), "last_updated": time.time()}

        if notes != "":
            data["notes"] = notes
        if tags != "":
            data["tags"] = tags.split(',')

        return data
    except Exception as e:
        log(traceback.format_stack())
        return None

def pop_up(s):
    copyq = os.environ["COPYQ"]
    subprocess.call([copyq, "popup", s])
