import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import csv

def binarize_image(image, threshold):
    m, n = image.shape
    result = np.zeros((m, n)).astype('uint8')
    for i in range(m):
        for j in range(n):
            if image[i, j] >= threshold:
                result[i, j] = 255
    return result


if __name__ == '__main__':
    # Setup
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    # Load image 
    img_gray = Image.open('nba_half_court.png').convert("L") # as gray scale
    
    plt.figure(figsize=(7, 7))
    plt.imshow(img_gray)
    
    img_court = binarize_image(np.array(img_gray), 200)
    img_bw = Image.fromarray(np.uint8(img_court))

    plt.figure(figsize=(7, 7))
    plt.imshow(img_bw)
    
    # Load data
    data = []
    with open('Stephen_2017.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            row = []
            for cell in line:
                row.append(float(cell))
            data.append(row)

    # Preprocess data
    data_ = np.array(data)
    # Change the coordinate to fit the image
    X = np.column_stack((data_[:, 1], -data_[:, 0]))
    y = data_[:, 2].astype(np.integer)


    # Machine Learning - Classification
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    import matplotlib.pyplot as plt
    from mlxtend.plotting import plot_decision_regions

    from sklearn.tree import DecisionTreeClassifier
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.ensemble import VotingClassifier

    # Training classifiers
    clf_dtree = DecisionTreeClassifier(max_depth = 4)
    clf_kNN = KNeighborsClassifier(n_neighbors = 10)
    clf_svm = SVC(kernel='rbf', gamma=0.7, C=1.0)
    voting_clf = VotingClassifier(estimators=[('dt', clf_dtree), ('knn', clf_kNN),
                                        ('svc', clf_svm)],
                            voting='soft', weights=[2, 1, 2])

    clf_dtree.fit(X, y)
    clf_kNN.fit(X, y)
    clf_svm.fit(X, y)
    voting_clf.fit(X, y)
    
    
    plt.figure(figsize=(7, 7))
    
    plot_decision_regions(X = X, y = y, clf = clf_svm, legend = 2)
    

    '''
    import product
    # Plotting decision regions
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))

    f, axarr = plt.subplots(2, 2, sharex='col', sharey='row', figsize=(10, 8))

    for idx, clf, tt in zip(product([0, 1], [0, 1]),
                            [clf1, clf2, clf3, eclf],
                            ['Decision Tree (depth=4)', 'KNN (k=7)',
                             'Kernel SVM', 'Soft Voting']):

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        axarr[idx[0], idx[1]].contourf(xx, yy, Z, alpha=0.4)
        axarr[idx[0], idx[1]].scatter(X[:, 0], X[:, 1], c=y,
                                      s=20, edgecolor='k')
        axarr[idx[0], idx[1]].set_title(tt)

    plt.show()
    '''