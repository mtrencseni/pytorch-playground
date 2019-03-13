import os
import csv
import subprocess
import time
import rxe
from collections import defaultdict

def execute(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, _ = p.communicate()
    return out.strip()

def get_post_ids(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_reader.next()
        return [row[0] for row in csv_reader]

def get_post(post_id):
    path = "cache/%s.json" % post_id
    if not os.path.isfile(path):
        print('Downloading post data into cache...')
        url = """https://hn.algolia.com/api/v1/items/%s""" % post_id
        contents = execute("""curl -s %s > %s""" % (url, path))
        time.sleep(1)
    with open(path, 'r') as f:
        return f.read()
    
def get_commenters(post_id):
    post = get_post(post_id)
    r = rxe.one('"author":"').one_or_more(rxe.set_except(['"'])).one('"')
    return set([fragment[10:-1] for fragment in r.findall(post)])

post_ids = get_post_ids('top_10k_posts.csv')
user_comments = defaultdict(lambda: [])
for post_id in post_ids:
    print('Getting comments for post %s' % post_id)
    for user_id in get_commenters(post_id):
        user_comments[user_id].append(post_id)
with open("post_comments_10k.csv", "w") as f:
    num_prolific = 0
    for user_id in user_comments:
        if len(user_comments[user_id]) >= 3 and len(user_comments[user_id]) <= 50:
            num_prolific += 1
            for post_id in user_comments[user_id]:
                f.write('%s,%s\n' % (post_id, user_id))
    print('Qualifying commenters = %d' % num_prolific)
