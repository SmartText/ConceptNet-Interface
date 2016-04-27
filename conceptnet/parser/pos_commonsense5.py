from re import sub,compile
pattern = compile(b'[\[\]]')

def get_template(str):
    return sub(pattern, b' ', str)

def get_pos(relation_pos_server):
    import requests,json

    relation,pos_server = relation_pos_server
    template,obj = relation
    r = requests.post(pos_server, data=template.encode(), stream=True)

    deps = []

    from nltk.tree import Tree
    for resp in r.content.split(b'\n'):
        if not resp:
            continue
        data = json.loads(resp.decode())
        dep = Tree.fromstring(data['tree'])
        deps.append(dep)
    obj['pos'] = deps
    return template,obj

from multiprocessing import Pool
p = Pool(100)

def process_relations(conf, path, file, output_dir):
    output_file = "%s/%s.pkl" % (output_dir, file)
    try:
        open(output_file, "rb")
        print("file %s.pkl already exists" % file)
        return
    except IOError:
        pass

    import pickle
    relations = pickle.load(open(path, "rb"))

    pos_server = conf['pos_server']
    objs = p.map(get_pos, [(relation, pos_server) for relation in relations])

    pickle.dump(objs, open(output_file, "wb"))

def parse_files(conf):
    import os

    try:
        path_generator = os.walk("%s/%s" % (conf['output_dir'], "extracted_relations"))
    except IOError as e:
        return (1, "Output dir cannot be read %s" % str(e))

    dir = "%s/%s" % (conf['output_dir'], "pos_tags")
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    for root,dirs,files in path_generator:
        for file in files:
            path = "%s/%s" % (root, file)
            print(path)
            process_relations(conf, path, file, dir)

