from setuptools import setup, find_packages

setup(
    name="dstructslib",  # New name without underscores or dashes
    version="1.0.2",       # Start fresh or increment version if necessary
    install_requires=[],   # Add dependencies if any
    description="Data Structures Collections: BST and Linked Lists.",
    long_description=open("README.md").read(),
    packages=find_packages(),
    long_description_content_type="text/markdown",
    author='Bhuyan Md Anowarul Kairm',                # Replace with your name
    author_email='anowarulkarim8@gmail.com', # Replace with your email
    url='https://github.com/anowarulkarim/dstructlib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

