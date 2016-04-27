def train(classes, y_samples, feature_dict, classes_dict):
    # Using dev version of slearn, 1.9
    from sklearn.neural_network import MLPClassifier

    clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(50, 25), random_state=1, verbose=True)
    clf.fit(y_samples, classes)

    return clf

def test(classes, y_samples, clf):
    correct = 0
    incorrect = 0

    for class_int,y_sample in zip(classes, y_samples):
        pred = clf.predict([y_sample])
        if pred[0] == class_int:
            correct += 1
        else:
            incorrect += 1
    print(correct*100/(correct+incorrect))
