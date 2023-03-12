from sklearn.linear_model import LinearRegression
import numpy as np
import cubic_interpolation


class Interpolator:
    def __init__(self):
        self.regression = LinearRegression()

    def linear_regression(self, data):

        years = data[:, 0]
        self.regression.fit(years[:, np.newaxis], data[:, 1])
        return self.regression.predict(years[:, np.newaxis])

    def linear_regression_predict(self, year):
        return self.regression.predict(np.array([[year]]))

    def cubic_inter_predict(self, data):
        years = data[:, 0]
        spline = cubic_interpolation.build_spline(years, data[:, 1], len(years))
        interpolated = []
        for year in years:
            interpolated.append(cubic_interpolation.interpolate(spline, year))
        return np.array(interpolated)

    def pearsonr(x, y):
        # Assume len(x) == len(y)
        n = len(x)
        sum_x = float(sum(x))
        sum_y = float(sum(y))
        sum_x_sq = sum(xi * xi for xi in x)
        sum_y_sq = sum(yi * yi for yi in y)
        psum = sum(xi * yi for xi, yi in zip(x, y))
        num = psum - (sum_x * sum_y / n)
        den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
        if den == 0: return 0
        return num / den
