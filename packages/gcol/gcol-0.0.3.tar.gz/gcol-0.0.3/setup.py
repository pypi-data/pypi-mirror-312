from setuptools import setup, find_packages

setup(
    name='gcol',
    version='0.0.3',
    author='Rhyd Lewis',
    author_email='lewisr9@cardiff.ac.uk',
    url="https://github.com/Rhyd-Lewis/GCol",
    description='A Python Library for Graph Coloring',
    readme = "readme.md",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires='>=3.7',
    install_requires='networkx>=3.0'
)

