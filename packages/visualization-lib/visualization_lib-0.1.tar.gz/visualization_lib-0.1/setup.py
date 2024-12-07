from setuptools import setup, find_packages

setup(
    name='visualization_lib',
    version='0.1',
    description='A library for data cleaning and visualization based on relationships in data.',
    author='Ammar Jamshed',
    author_email='ammarjamshed123@gmail.com',
    url='https://github.com/AmmarJamshed/visualization_lib',  # Replace with your repo URL
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn',
        'scipy',
        'pytest'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
