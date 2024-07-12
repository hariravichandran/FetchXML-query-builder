from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="xmlquerybuilder",
    version="0.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'xmlquerybuilder=xmlquerybuilder.xml_query_builder:main',
        ],
    },
    author="Hari Ravichandran",
    author_email="hari@live.com",
    description="A tool to build FetchXML queries using a Pandas-like syntax.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hariravichandran/FetchXML-query-builder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)