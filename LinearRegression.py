from statistics import mean
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


class LinearRegression:
    def __init__(self,dataset,parameters):
        plt.style.use("fivethirtyeight")
        plt.title("Click to add points")
        self.dataset = dataset
        ani = FuncAnimation(plt.gcf(), self.update, interval=100)

        plt.tight_layout()
        plt.show()

    def best_fit_line(self,xs, ys):
        m = (mean(xs) * mean(ys) - mean(xs * ys))
        m = m / (mean(xs) * mean(xs) - mean(xs * xs))
        b = mean(ys) - m * mean(xs)
        return m, b

    def get_xs_ys(self):
        xs = np.array([])
        ys = np.array([])
        for i in self.dataset:
            xs = np.append(xs, i[0])
            ys = np.append(ys, i[1])

        return xs, ys

    def update(self,i):
        [pt] = plt.ginput()
        pt = list(pt)
        plt.figtext(.5, .9, "Linear Regression finds the best fit line for a set of points", fontsize=13, ha='center')
        self.dataset.append(pt)
        plt.cla()
        xs, ys = self.get_xs_ys()
        m, b = self.best_fit_line(xs, ys)
        plt.scatter(xs, ys)
        plt.plot(xs, [m * x + b for x in xs])


