import xml.etree.ElementTree as ET
import xml.dom.minidom

class XMLQueryBuilder:
    def __init__(self, root_entity):
        """
        Initialize the XMLQueryBuilder with the root entity.

        Args:
            root_entity (str): The name of the root entity for the FetchXML query.

        Example:
            query = XMLQueryBuilder("account")
        """
        self.root_entity_name = root_entity
        self.root = ET.Element("fetch")
        self.entity = ET.SubElement(self.root, "entity", {"name": root_entity})
        self.select_attributes = []
        self.filters = []
        self.linked_entities = []
        self.orders = []
        self.aggregates = []

    def select(self, *attributes):
        """
        Select attributes to include in the query.

        Args:
            *attributes (str): Attributes to select. Use 'ALL' to select all attributes.

        Similar to:
            - Pandas: df[['col1', 'col2']]
            - SQL: SELECT col1, col2 FROM table

        Example:
            query = XMLQueryBuilder("account").select("name", "accountid")
        """
        if attributes == ('ALL',):
            ET.SubElement(self.entity, "all-attributes")
        else:
            for attr in attributes:
                ET.SubElement(self.entity, "attribute", {"name": attr})
                self.select_attributes.extend(attributes)
        return self

    def link_entity(self, name, alias=None, from_field=None, to_field=None, link_type=None):
        """
        Link related entities.

        Args:
            name (str): The name of the entity to link.
            alias (str, optional): The alias for the linked entity.
            from_field (str, optional): The field to join from.
            to_field (str, optional): The field to join to.
            link_type (str, optional): The type of join (inner or outer).

        Similar to:
            - Pandas: df.merge(other_df, left_on='col1', right_on='col2')
            - SQL: JOIN other_table ON table.col1 = other_table.col2

        Example:
            query = XMLQueryBuilder("account").link_entity("contact", alias="c", from_field="contactid", to_field="primarycontactid")
        """
        link = ET.SubElement(self.entity, "link-entity", {
            "name": name,
            "alias": alias if alias else name,
            "from": from_field if from_field else f"{name}id",
            "to": to_field if to_field else f"{name}id",
            "link-type": link_type if link_type else "inner"
        })
        self.linked_entities.append(link)
        return self

    def add_filter(self, attribute, operator, value):
        """
        Add filter conditions to the query.

        Args:
            attribute (str): The attribute to filter on.
            operator (str): The operator for the condition (e.g., eq, gt, lt).
            value (str): The value to filter by.

        Similar to:
            - Pandas: df[df['col'] == value]
            - SQL: WHERE col = value

        Example:
            query = XMLQueryBuilder("account").add_filter("name", "eq", "Contoso")
        """
        if not self.filters:
            self.filter_root = ET.SubElement(self.entity, "filter", {"type": "and"})
            self.filters.append(self.filter_root)
        ET.SubElement(self.filter_root, "condition", {
            "attribute": attribute,
            "operator": operator,
            "value": str(value)
        })
        return self

    def add_order(self, attribute, descending=False):
        """
        Add sorting to the query.

        Args:
            attribute (str): The attribute to sort by.
            descending (bool, optional): Whether to sort in descending order.

        Similar to:
            - Pandas: df.sort_values(by='col', ascending=False)
            - SQL: ORDER BY col DESC

        Example:
            query = XMLQueryBuilder("account").add_order("name", descending=True)
        """
        order = ET.SubElement(self.entity, "order", {
            "attribute": attribute,
            "descending": "true" if descending else "false"
        })
        self.orders.append(order)
        return self

    def add_aggregate(self, attribute, alias, aggregate_type):
        """
        Add aggregate functions to the query.

        Args:
            attribute (str): The attribute to aggregate.
            alias (str): The alias for the aggregated value.
            aggregate_type (str): The type of aggregation (e.g., sum, avg, count).

        Similar to:
            - Pandas: df.groupby('col').agg({'col': 'sum'})
            - SQL: SELECT SUM(col) AS alias FROM table GROUP BY col

        Example:
            query = XMLQueryBuilder("account").add_aggregate("revenue", "total_revenue", "sum")
        """
        aggregate = ET.SubElement(self.entity, "attribute", {
            "name": attribute,
            "alias": alias,
            "aggregate": aggregate_type
        })
        self.aggregates.append(aggregate)
        return self

    def add_group_by(self, *attributes):
        """
        Add group by clauses to the query.

        Args:
            *attributes (str): Attributes to group by.

        Similar to:
            - Pandas: df.groupby(['col1', 'col2'])
            - SQL: GROUP BY col1, col2

        Example:
            query = XMLQueryBuilder("account").add_group_by("industry")
        """
        for attr in attributes:
            ET.SubElement(self.entity, "attribute", {
                "name": attr,
                "groupby": "true"
            })
        return self

    def add_fetch_xml(self, fetch_xml_string):
        """
        Add an existing FetchXML string to the query builder.

        Args:
            fetch_xml_string (str): The FetchXML string.

        Example:
            fetch_xml_string = '''
            <fetch>
              <entity name="account">
                <attribute name="name" />
                <attribute name="accountid" />
              </entity>
            </fetch>
            '''
            query = XMLQueryBuilder("account").add_fetch_xml(fetch_xml_string)
        """
        fetch_xml_root = ET.fromstring(fetch_xml_string)
        self.root = fetch_xml_root
        self.entity = fetch_xml_root.find(".//entity")
        return self

    def to_string(self, pretty=False):
        """
        Convert the query to a FetchXML string.

        Args:
            pretty (bool, optional): Whether to pretty-print the XML string.

        Returns:
            str: The FetchXML string.

        Example:
            query_string = XMLQueryBuilder("account").select("name", "accountid").to_string(pretty=True)
        """
        xml_str = ET.tostring(self.root, encoding='unicode')
        if pretty:
            dom = xml.dom.minidom.parseString(xml_str)
            xml_str = dom.toprettyxml()
        return xml_str

    @classmethod
    def from_fetch_xml(cls, fetch_xml_string):
        """
        Create an XMLQueryBuilder instance from a FetchXML string.

        Args:
            fetch_xml_string (str): The FetchXML string.

        Returns:
            XMLQueryBuilder: An instance of XMLQueryBuilder.

        Example:
            fetch_xml_string = '''
            <fetch>
              <entity name="account">
                <attribute name="name" />
                <attribute name="accountid" />
              </entity>
            </fetch>
            '''
            query_builder = XMLQueryBuilder.from_fetch_xml(fetch_xml_string)
        """
        fetch_xml_root = ET.fromstring(fetch_xml_string)
        entity_name = fetch_xml_root.find(".//entity").attrib["name"]
        query_builder = cls(entity_name)
        query_builder.add_fetch_xml(fetch_xml_string)
        return query_builder


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

    # Converting from FetchXML string to XMLQueryBuilder
    fetch_xml_string = '''
    <fetch>
      <entity name="account">
        <attribute name="name" />
        <attribute name="accountid" />
        <filter type="and">
          <condition attribute="name" operator="eq" value="Contoso" />
          <condition attribute="statecode" operator="eq" value="0" />
        </filter>
        <link-entity name="contact" alias="c" from="contactid" to="primarycontactid" link-type="inner" />
        <order attribute="name" descending="true" />
        <attribute name="revenue" alias="total_revenue" aggregate="sum" />
        <attribute name="industry" groupby="true" />
      </entity>
    </fetch>
    '''

    query_builder = XMLQueryBuilder.from_fetch_xml(fetch_xml_string)
    print(query_builder.to_string(pretty=True))

if __name__ == "__main__":
    main()
