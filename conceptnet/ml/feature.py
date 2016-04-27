# Since all samples are of different lengths, pad smaller strings with 0's
pad = 25

def get_feature(pos_tags, feature_dict):
    y_values = []
    append = y_values.append
    get = feature_dict.get
    for tag in pos_tags:
        try:
            append(feature_dict[tag])
        except KeyError:
            feature_dict[tag] = len(feature_dict)+1
            append(feature_dict[tag])

    features = []
    for i in range(5):
        feature = []
        for j in range(0, len(y_values)-i-1):
            feature.extend((y_values[j:j+i+1]))
        features.extend(feature)

    features = features + [0 for i in range(pad-len(features))]
    return features[:25]

def get_features(conf, samples, feature_dict, classes_dict):
    all_features = []
    all_classes  = []
    for template,obj in samples:
        pos_tags = []
        extend = pos_tags.extend
        [extend([word[1] for word in tree.pos()]) for tree in obj['pos']]

        features  = get_feature(pos_tags, feature_dict)
        class_rel = obj['rel']
        try:
            class_int = classes_dict[class_rel]
        except KeyError:
            class_int = len(classes_dict)+1
            classes_dict[class_rel] = class_int
        all_classes.append(class_int)
        all_features.append(features)
    return all_features, all_classes
