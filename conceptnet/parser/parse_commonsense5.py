from re import sub,compile
pattern = compile(b'[\[\]]')

def get_template(str):
    return sub(pattern, b' ', str)

def process_csv(path, data, languages=[b'en']):
    all_templates = []
    file = open(path, "rb")

    for i,line in enumerate(file.readlines()):
        line = line[:-1]
        record = line.split(b'\t')

        rel,src,dst = record[1:4]
        sample = record[-1]

        rel = rel.split(b'/')[2]

        lang = src.split(b'/')[2]
        if lang in languages and sample:
            template = get_template(sample)
            all_templates.append((rel.decode(), template.decode()))

    for rel,template in all_templates:
        try:
            data[template]['count'] += 1
        except KeyError:
            i += 1
            data[template] = {'count': 1, 'rel': rel, 'pos': None, 'template': template}

    return all_templates

def parse_files(conf):
    import os

    try:
        path_generator = os.walk(conf['conceptnet_dir'])
    except IOError as e:
        return (1, "Coneceptnet dir cannot be read %s" % str(e))

    data = {}
    for root,dirs,files in path_generator:
        for file in files:
            path = "%s/%s" % (root, file)
            if path.endswith('.csv'):
                print(path)
                process_csv(path, data)

    dir = "%s/%s" % (conf['output_dir'], "extracted_relations")
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    import pickle
    data = list(data.items())
    buckets = 50000
    for i in range(0, len(data), buckets):
        pickle.dump(data[i:i+buckets], open("%s/part_%d.pkl" % (dir, i/buckets), "wb"))

    return 0, ""
