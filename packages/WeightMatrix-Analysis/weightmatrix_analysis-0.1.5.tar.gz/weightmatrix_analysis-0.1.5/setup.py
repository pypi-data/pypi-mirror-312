from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='WeightMatrix_Analysis',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'WeightMatrix = WeightMatrix.main:WeightMatrix',
            'left_null_space = WeightMatrix_Analysis.main:left_null_space',
            'right_null_space = WeightMatrix_Analysis.main:right_null_space'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)