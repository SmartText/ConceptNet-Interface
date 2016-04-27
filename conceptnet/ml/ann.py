def train(classes, y_samples, feature_dict, classes_dict):
    # Using dev version of slearn, 1.9
    from sklearn.neural_network import MLPClassifier

    clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(50, 25), random_state=1, verbose=True)
    clf.fit(y_samples, classes)

    return clf
