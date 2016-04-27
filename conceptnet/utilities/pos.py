def compute_pos(conf, text):
    import requests,json

    pos_server = conf['pos_server']
    r = requests.post(pos_server, data=text.encode(), stream=True)

    deps = []

    from nltk.tree import Tree
    for resp in r.content.split(b'\n'):
        if not resp:
            continue
        data = json.loads(resp.decode())
        dep = Tree.fromstring(data['tree'])
        deps.append(dep)
    tags = []
    extend = tags.extend
    [extend([word[1] for word in dep.pos()]) for dep in deps]

    return tags
