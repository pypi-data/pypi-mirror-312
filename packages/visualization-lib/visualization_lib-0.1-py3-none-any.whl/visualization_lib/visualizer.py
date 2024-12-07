import matplotlib.pyplot as plt

class Visualizer:
    """
    A class for creating visualizations such as line plots, bar plots, and scatter plots.
    """

    def __init__(self, title="Visualization Library"):
        self.title = title

    def line_plot(self, x, y, xlabel="X-axis", ylabel="Y-axis", title=None):
        """
        Create a line plot.
        """
        plt.figure()
        plt.plot(x, y, marker="o")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title if title else self.title)
        plt.grid()
        plt.show()

    def bar_plot(self, x, y, xlabel="X-axis", ylabel="Y-axis", title=None):
        """
        Create a bar plot.
        """
        plt.figure()
        plt.bar(x, y)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title if title else self.title)
        plt.grid(axis="y")
        plt.show()

    def scatter_plot(self, x, y, xlabel="X-axis", ylabel="Y-axis", title=None):
        """
        Create a scatter plot.
        """
        plt.figure()
        plt.scatter(x, y, c="blue", alpha=0.7)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title if title else self.title)
        plt.grid()
        plt.show()
