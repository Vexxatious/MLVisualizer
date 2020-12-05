import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from collections import Counter


class KNN:
    def __init__(self, dataset, parameters):
        self.k = parameters[0]
        plt.style.use('fivethirtyeight')
        plt.title("Click to add new points")
        self.dataset = dataset
        [[plt.scatter(ii[0], ii[1], s=100, color=i) for ii in dataset[i]] for i in dataset]
        ani = FuncAnimation(plt.gcf(), self.update, interval=500)

        plt.tight_layout()
        plt.show()

    def k_nearest(self, dataset, predict, k):
        distances = []
        for group in dataset:
            for features in dataset[group]:
                distance = np.linalg.norm(np.array(features) - np.array(predict))
                distances.append([distance, [group, features]])
        votes = [i[1][0] for i in sorted(distances)[:k]]

        for i in sorted(distances)[1:k + 1]:
            xs = [i[1][1][0], predict[0]]
            ys = [i[1][1][1], predict[1]]
            plt.plot(xs, ys)

        vote_result = Counter(votes).most_common(1)[0][0]

        return vote_result

    def update(self, i):
        [pt] = plt.ginput()
        plt.figtext(.5, .9, "KNN finds the closest k neighbors to classify a point", fontsize=13, ha='center')
        pt = np.asarray(pt)
        plt.cla()
        self.dataset[self.k_nearest(self.dataset, pt, self.k)].append(pt)
        [[plt.scatter(ii[0], ii[1], s=100, color=i) for ii in self.dataset[i]] for i in self.dataset]

