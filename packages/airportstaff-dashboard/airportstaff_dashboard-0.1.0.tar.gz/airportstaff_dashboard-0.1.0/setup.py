from setuptools import setup, find_packages

setup(
    name="airportstaff_dashboard",
    version="0.1.0",
    author="Benny Geddam",
    author_email="geddambenny55@gmail.com",
    description="Simple library for listing/managing airport staff dashboards",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Comrade-Glitch-cloud/airportstaff_daashboard-Library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
