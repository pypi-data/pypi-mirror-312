from setuptools import setup, find_packages

setup(
    name="algocraft",  # Name of your package
    version="0.2.2",  # Package version
    description="A collection of classic algorithms in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Leander",  # Your name
    author_email="your.email@example.com",  # Your email
    packages=find_packages(),  # Automatically find all the Python modules in your project
    install_requires=[
        # List any dependencies here, e.g.,
        # 'numpy', 'scipy', etc. Leave it empty if there are none.
        'numpy','heapq','math',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",  # Change if necessary
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version required
)
