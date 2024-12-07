import unittest
from visualization_lib.visualizer import Visualizer

class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = Visualizer(title="Test Visualization")

    def test_line_plot(self):
        x = [1, 2, 3, 4]
        y = [10, 20, 30, 40]
        try:
            self.visualizer.line_plot(x, y)
        except Exception as e:
            self.fail(f"line_plot raised an exception: {e}")

    def test_bar_plot(self):
        x = ["A", "B", "C", "D"]
        y = [5, 15, 25, 35]
        try:
            self.visualizer.bar_plot(x, y)
        except Exception as e:
            self.fail(f"bar_plot raised an exception: {e}")

    def test_scatter_plot(self):
        x = [1, 2, 3, 4]
        y = [10, 20, 30, 40]
        try:
            self.visualizer.scatter_plot(x, y)
        except Exception as e:
            self.fail(f"scatter_plot raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
