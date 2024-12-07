
`visualization_lib` is a Python library that helps with automatic data cleaning and visualization. It provides functions to clean missing data, encode categorical variables, and visualize the relationships between features and the target variable.

## Installation

To install the package, use `pip`:

```bash
pip install visualization_lib
```
## Usage
import pandas as pd
from visualization_lib.visualizer import DataVisualizerAndCleaner

# Load your dataset
df = pd.read_csv('your_data.csv')

# Initialize the visualizer
visualizer = DataVisualizerAndCleaner(df, target_column='n_enrolled')

# Clean and visualize the data
visualizer.visualize_and_clean()
