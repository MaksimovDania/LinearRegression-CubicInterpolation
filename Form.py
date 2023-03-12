import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
from Interpolator import Interpolator
from FileReader import FileReader
from StringWorker import StringWorker
from tkinter import messagebox
import tkinter.filedialog
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class Form:
    def __init__(self):
        self.fig, self.axs = plt.subplots()
        self.fig.subplots_adjust(bottom=0.2)

        # Axes for buttons/textBox
        DrawGrathAx = self.fig.add_axes([0.59, 0.05, 0.2, 0.05])
        PredictYearAx = self.fig.add_axes([0.8, 0.05, 0.19, 0.05])
        FileDialogAx = self.fig.add_axes([0.18, 0.1, 0.29, 0.05])

        GeographyTextAx = self.fig.add_axes([0.18, 0.05, 0.29, 0.05])
        ParameterTextAx = self.fig.add_axes([0.18, 0, 0.29, 0.05])
        PredictYearTextAx = self.fig.add_axes([0.8, 0, 0.19, 0.05])

        # Buttons/TextBox
        b_file_dialog = Button(FileDialogAx, 'FileDialog')
        b_draw_graph = Button(DrawGrathAx, 'DrawGrath')
        b_predict_year = Button(PredictYearAx, 'PredictYear')

        self.GeographyText = TextBox(GeographyTextAx, "Country / region", textalignment="center")
        self.ParameterText = TextBox(ParameterTextAx, "Parameter", textalignment="center")
        self.PredictYearText = TextBox(PredictYearTextAx, "", textalignment="center")

        # OnClickButtons
        b_draw_graph.on_clicked(self.draw_plot)
        b_predict_year.on_clicked(self.draw_point)
        b_file_dialog.on_clicked(self.file_dialog)

        plt.show()

    def file_dialog(self, event):
        self.filename = tkinter.filedialog.askopenfile(mode='r', type='csv')

    def draw_plot(self, event):
        try:
            strings = FileReader.read_file(self.filename)

            geography = self.GeographyText.text
            parameter = self.ParameterText.text

            array = StringWorker.two_dimensional_array(strings, geography, parameter)
            data = np.array(array)

            self.interpolator = Interpolator()

            pearson_coef = Interpolator.pearsonr(data[:, 0], data[:, 1])
            regression = self.interpolator.linear_regression(data)
            interpolation = self.interpolator.cubic_inter_predict(data)

            self.axs.clear()
            self.axs.set_title(f"Linear regression && Cubic Interpolation\n Pearson: {round(pearson_coef, 2)}")
            self.axs.scatter(data[:, 0], data[:, 1])
            self.axs.plot(data[:, 0], regression)
            self.axs.plot(data[:, 0], interpolation)
        except Exception as ex:
            messagebox.showinfo("Error", ex)

    def draw_point(self, event):
        try:
            year = int(self.PredictYearText.text)
            self.axs.scatter(year, self.interpolator.linear_regression_predict(year))
        except Exception as ex:
            messagebox.showinfo("Error", ex)


form = Form()
