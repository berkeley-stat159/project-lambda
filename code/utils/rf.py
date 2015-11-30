from sklearn.ensemble import RandomForestClassifier
import numpy as np
# look at train_test_split() to see if that's an option

def rf_accuracy(X, y):
    model = RandomForestClassifier(n_estimators=1000,
                                   max_features=10,
                                   max_depth=10)
    index_array = np.arange(X.shape[0])
    np.random.shuffle(index_array)
    eighty = int(X.shape[0] * 0.8)
    train_index = index_array[:eighty]
    test_index = index_array[eighty:]
    train_X = X[train_index]
    train_y = np.empty_like(train_index)
    for num in range(len(train_index)):
        train_y[num] = y[train_index[num]]
    test_X = X[test_index]
    test_y = np.empty_like(test_index)
    for num in range(len(test_index)):
        test_y[num]=y[test_index[num]]
    model.fit(train_X, train_y)
    results = model.score(test_X, test_y)
    return results
