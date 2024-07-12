# FetchXML-query-builder
A Simple Query Builder to Create FetchXML Queries in Python 3.

### Documentation for XMLQueryBuilder 

#### Overview 
The `XMLQueryBuilder` class allows you to build FetchXML queries using a Pandas-like syntax. This tool is useful for generating complex FetchXML queries programmatically.
#### Installation 
 
1. **Clone the repository:** 

```bash
git clone https://github.com/hariravichandran/FetchXML-query-builder.git
cd FetchXML-query-builder
```
 
2. **Install the package:** 

```bash
pip install .
```
 
3. **Install dependencies:** 

```bash
pip install -r requirements.txt
```

#### Usage 
Here's an example of how to use the `XMLQueryBuilder`:

```python
from xml_query_builder import XMLQueryBuilder

def main():
    # Create a query
    query = (XMLQueryBuilder("account")
             .select("name", "accountid")
             .link_entity("contact", alias="c", from_field="contactid", to_field="primarycontactid")
             .add_filter("name", "eq", "Contoso")
             .add_filter("statecode", "eq", 0)
             .add_order("name", descending=True)
             .add_aggregate("revenue", "total_revenue", "sum")
             .add_group_by("industry")
             .to_string(pretty=True))

    print(query)

if __name__ == "__main__":
    main()
```

### Methods 
Each method in the `XMLQueryBuilder` class has been designed to closely resemble functions in Pandas and SQL. 
- **`__init__(root_entity)`** : Initialize the XMLQueryBuilder with the root entity. 
  - **Args** : `root_entity (str)`: The name of the root entity.
 
  - **Example** :

```python
query = XMLQueryBuilder("account")
```
 
- **`select(*attributes)`** : Select attributes to include in the query. 
  - **Args** : `*attributes (str)`: Attributes to select. Use 'ALL' to select all attributes.
 
  - **Similar to** : 
    - Pandas: `df[['col1', 'col2']]`
 
    - SQL: `SELECT col1, col2 FROM table`
 
  - **Example** :

```python
query = XMLQueryBuilder("account").select("name", "accountid")
```
 
- **`link_entity(name, alias=None, from_field=None, to_field=None, link_type=None)`** : Link related entities. 
  - **Args** : 
    - `name (str)`: The name of the entity to link.
 
    - `alias (str, optional)`: The alias for the linked entity.
 
    - `from_field (str, optional)`: The field to join from.
 
    - `to_field (str, optional)`: The field to join to.
 
    - `link_type (str, optional)`: The type of join (inner or outer).
 
  - **Similar to** : 
    - Pandas: `df.merge(other_df, left_on='col1', right_on='col2')`
 
    - SQL: `JOIN other_table ON table.col1 = other_table.col2`
 
  - **Example** :

```python
query = XMLQueryBuilder("account").link_entity("contact", alias="c", from_field="contactid", to_field="primarycontactid")
```
 
- **`add_filter(attribute, operator, value)`** : Add filter conditions to the query. 
  - **Args** : 
    - `attribute (str)`: The attribute to filter on.
 
    - `operator (str)`: The operator for the condition (e.g., eq, gt, lt).
 
    - `value (str)`: The value to filter by.
 
  - **Similar to** : 
    - Pandas: `df[df['col'] == value]`
 
    - SQL: `WHERE col = value`
 
  - **Example** :

```python
query = XMLQueryBuilder("account").add_filter("name", "eq", "Contoso")
```
 
- **`add_order(attribute, descending=False)`** : Add sorting to the query. 
  - **Args** : 
    - `attribute (str)`: The attribute to sort by.
 
    - `descending (bool, optional)`: Whether to sort in descending order.
 
  - **Similar to** : 
    - Pandas: `df.sort_values(by='col', ascending=False)`
 
    - SQL: `ORDER BY col DESC`
 
  - **Example** :

```python
query = XMLQueryBuilder("account").add_order("name", descending=True)
```
 
- **`add_aggregate(attribute, alias, aggregate_type)`** : Add aggregate functions to the query. 
  - **Args** : 
    - `attribute (str)`: The attribute to aggregate.
 
    - `alias (str)`: The alias for the aggregated value.
 
    - `aggregate_type (str)`: The type of aggregation (e.g., sum, avg, count).
 
  - **Similar to** : 
    - Pandas: `df.groupby('col').agg({'col': 'sum'})`
 
    - SQL: `SELECT SUM(col) AS alias FROM table GROUP BY col`
 
  - **Example** :

```python
query = XMLQueryBuilder("account").add_aggregate("revenue", "total_revenue", "sum")
```
 
- **`add_group_by(*attributes)`** : Add group by clauses to the query. 
  - **Args** : `*attributes (str)`: Attributes to group by.
 
  - **Similar to** : 
    - Pandas: `df.groupby(['col1', 'col2'])`
 
    - SQL: `GROUP BY col1, col2`
 
  - **Example** :

```python
query = XMLQueryBuilder("account").add_group_by("industry")
```
 
- **`add_fetch_xml(fetch_xml_string)`** : Add an existing FetchXML string to the query builder. 
  - **Args** : `fetch_xml_string (str)`: The FetchXML string.
 
  - **Example** :

```python
fetch_xml_string = '''
<fetch>
  <entity name="account">
    <attribute name="name" />
    <attribute name="accountid" />
  </entity>
</fetch>
'''
query = XMLQueryBuilder("account").add_fetch_xml(fetch_xml_string)
```
 
- **`to_string(pretty=False)`** : Convert the query to a FetchXML string. 
  - **Args** : 
    - `pretty (bool, optional)`: Whether to pretty-print the XML string.
 
  - **Returns** : `str`: The FetchXML string.
 
  - **Example** :

```python
query_string = XMLQueryBuilder("account").select("name", "accountid").to_string(pretty=True)
```
 
- **`from_fetch_xml(fetch_xml_string)`** : Create an XMLQueryBuilder instance from a FetchXML string. 
  - **Args** : `fetch_xml_string (str)`: The FetchXML string.
 
  - **Returns** : `XMLQueryBuilder`: An instance of XMLQueryBuilder.
 
  - **Example** :

```python
fetch_xml_string = '''
<fetch>
  <entity name="account">
    <attribute name="name" />
    <attribute name="accountid" />
  </entity>
</fetch>
'''
query_builder = XMLQueryBuilder.from_fetch_xml(fetch_xml_string)
```

### Building a Python Package 
 
1. **Create the directory structure:** 

```arduino
xmlquerybuilder/
├── xml_query_builder.py
├── requirements.txt
├── setup.py
├── README.md
├── LICENSE
└── xmlquerybuilder/
    ├── __init__.py
    └── xml_query_builder.py
```
 
2. **Create `setup.py`:** 

```python
from setuptools import setup, find_packages

setup(
    name="xmlquerybuilder",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'xmlquerybuilder=xmlquerybuilder.xml_query_builder:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to build FetchXML queries using a Pandas-like syntax.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/xmlquerybuilder",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
```
 
3. **Create `requirements.txt`:** 

```bash
# Add any dependencies here
xml.etree.ElementTree
xml.dom.minidom
```
 
4. **Create `README.md`:** 

```markdown
# XMLQueryBuilder

XMLQueryBuilder is a tool to build FetchXML queries using a Pandas-like syntax.

## Installation

Clone the repository and install the package:

```bash
git clone https://github.com/hariravichandran/FetchXML-query-builder.git
cd FetchXML-query-builder
pip install .
```

## Usage 

```python
from xml_query_builder import XMLQueryBuilder

def main():
    query = (XMLQueryBuilder("account")
             .select("name", "accountid")
             .link_entity("contact", alias="c", from_field="contactid", to_field="primarycontactid")
             .add_filter("name", "eq", "Contoso")
             .add_filter("statecode", "eq", 0)
             .add_order("name", descending=True)
             .add_aggregate("revenue", "total_revenue", "sum")
             .add_group_by("industry")
             .to_string(pretty=True))

    print(query)

if __name__ == "__main__":
    main()
```
 
7. **Build the package:** 

```bash
python setup.py sdist bdist_wheel
```

### Running the Example 

After installing the package, you can run the example by creating a Python script and executing it:

```python
from xml_query_builder import XMLQueryBuilder

def main():
    # Example usage
    query = (XMLQueryBuilder("account")
             .select("name", "accountid")
             .link_entity("contact", alias="c", from_field="contactid", to_field="primarycontactid")
             .add_filter("name", "eq", "Contoso")
             .add_filter("statecode", "eq", 0)
             .add_order("name", descending=True)
             .add_aggregate("revenue", "total_revenue", "sum")
             .add_group_by("industry")
             .to_string(pretty=True))

    print(query)

if __name__ == "__main__":
    main()
```

Run the script:


```bash
python your_script.py
```


### Creating a Virtual Environment 
You can create a virtual environment using `venv` or `conda`. Here are the instructions for both methods:Using `venv` 
1. **Create a virtual environment:** 

```bash
python3.10 -m venv venv
```
 
2. **Activate the virtual environment:**  
  - On Windows:

```bash
.\venv\Scripts\activate
```
 
  - On macOS/Linux:

```bash
source venv/bin/activate
```
 
3. **Install the package and dependencies:** 

```bash
pip install .
pip install -r requirements.txt
```
Using `conda` 
1. **Create a conda environment:** 

```bash
conda create -n xmlquerybuilder python=3.10
```
 
2. **Activate the conda environment:** 

```bash
conda activate xmlquerybuilder
```
 
3. **Install the package and dependencies:** 

```bash
pip install .
pip install -r requirements.txt
```

### Running the Example 

After setting up your environment, you can run the example:
 
1. **Create a Python script (`example.py`):** 

```python
from xmlquerybuilder.xml_query_builder import XMLQueryBuilder

def main():
    # Example usage
    query = (XMLQueryBuilder("account")
             .select("name", "accountid")
             .link_entity("contact", alias="c", from_field="contactid", to_field="primarycontactid")
             .add_filter("name", "eq", "Contoso")
             .add_filter("statecode", "eq", 0)
             .add_order("name", descending=True)
             .add_aggregate("revenue", "total_revenue", "sum")
             .add_group_by("industry")
             .to_string(pretty=True))

    print(query)

if __name__ == "__main__":
    main()
```
 
2. **Run the script:** 

```bash
python example.py
```

### Building the Package 

To build the package with these dependencies included:
 
1. **Ensure your directory structure is correct:** 

```arduino
xmlquerybuilder/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
└── xmlquerybuilder/
    ├── __init__.py
    └── xml_query_builder.py
```
 
2. **Run the setup script to build the package:** 

```bash
python setup.py sdist bdist_wheel
```
This command will create a `dist` directory containing the packaged distribution files (`tar.gz` and `.whl` files).
 
3. **Install the built package:** 

```bash
pip install dist/xmlquerybuilder-0.1.tar.gz
```
Replace `xmlquerybuilder-0.1.tar.gz` with the actual filename generated by `setup.py`.

