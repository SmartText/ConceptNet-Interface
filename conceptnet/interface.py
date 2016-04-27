#!/usr/bin/python3

def print_help(e_str=None):
    from sys import exit
    if e_str:
        print("ERROR: %s" % e_str)
    print("\t-h: This menu")
    print("\t--conceptnet_dir: Conceptnet extracted csv files")
    exit(1)

def test_text(conf, text):
    from utilities import pos
    return pos.compute_pos(conf, text)

if __name__ == "__main__":
    from sys import argv
    from getopt import getopt, GetoptError

    conf = {
        'mode': 'None',
        'conceptnet_dir'    : None,
        'output_dir'        : None,
        'pos_server'        : None,
        'assimilator_server': None,
    }

    try:
        opts,args = getopt(argv[1:], "h", ["conceptnet_dir=", "output_dir=", "mode=", "pos_server=", "save_mode=", "test="])
    except GetoptError as e:
        print_help(str(e))

    for arg,opt in opts:
        if arg == '-h':
            print_help()
        else:
            arg = arg[2:]
            conf[arg] = opt

    mode = conf['mode']
    if mode == "extract":
        from parser import parse_commonsense5
        parse_commonsense5.parse_files(conf)
    elif mode == "pos":
        from parser import pos_commonsense5
        pos_commonsense5.parse_files(conf)
    elif mode == "train":
        from parser import samples_commonsense5
        # Get training samples
        samples = samples_commonsense5.get_samples(conf, 150000)

        # A feature dictionary to keep the variables contant
        feature_dict = {}
        classes_dict = {}

        from ml import feature, ann
        features,classes = feature.get_features(conf, samples, feature_dict, classes_dict)
        clf = ann.train(classes, features, feature_dict, classes_dict)

        # Get testing samples
        test_samples = samples_commonsense5.get_samples(conf, 5000)
        features,classes = feature.get_features(conf, samples, feature_dict, classes_dict)
        ann.test(classes, features, clf)
        
        features,classes = feature.get_features(conf, samples, feature_dict, classes_dict)

        if conf['test']:
            pos_tags = test_text(conf, conf['test'])
            feature = feature.get_feature(pos_tags, feature_dict)
            predict = clf.predict([feature])
            class_str = [class_str for class_str,class_int in classes_dict.items() if class_int==predict[0]]
            print(class_str)
