import setuptools 

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bidplotter',
    version='0.6',
    packages=["bidplotter"],  # Finds all packages
    install_requires=['matplotlib'],
    description='A library for predicting auction prices and visualizing bidding progress.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Priya Shanmugam',
    author_email='priyashan112002@example.com',
    url='https://github.com/Priya-1110/bidplotter',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
