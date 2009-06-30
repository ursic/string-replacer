<?xml version="1.0"?>

<rdf:RDF
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns="http://purl.org/rss/1.0/">

  <channel id="channel" rdf:about="http://example.com/example.xml">
    <title>pytme example</title>
    <link>http://example.com/example.xml</link>
    <description>
      ##DESC##
    </description>
    <items>
      <rdf:Seq>
	##RESOURCES_START##
        <rdf:li resource="##RESOURCE##" />
	##RESOURCES_END##
      </rdf:Seq>
    </items>
  </channel>

  ##ITEMS_START##
  <item rdf:about="##ABOUT##">
    <title>##TITLE##</title>
    <link>##LINK##</link>
    ##AUTHORS_START##
    <author>##AUTHOR##</author>
    ##AUTHORS_END##
    <description>##ITEM_DESC##</description>
  </item>
  ##ITEMS_END##

</rdf:RDF>
