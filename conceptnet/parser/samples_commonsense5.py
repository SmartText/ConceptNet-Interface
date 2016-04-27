def read_pickled_file(file):
    import pickle

    template_objs = pickle.load(open(file, "rb"))
    return template_objs

def get_samples(conf, count):
    # Load output directory to load parsed pos samples
    dir = "%s/%s" % (conf['output_dir'], "pos_tags")

    import os
    generator = os.walk(dir)

    samples = []

    for path,dirs,files in generator:
        from random import shuffle
        shuffle(files)

        for file in files:
            file = "%s/%s" % (path, file)
            _samples = read_pickled_file(file)
            samples.extend(_samples[:count-len(samples)])
            count -= len(samples)
            if count <= 0:
                return samples
    return samples
