<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:func="http://gridgroup.eia-fr.ch/popc"
	xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
	exclude-result-prefixes="xs xd"
	extension-element-prefixes="func"
	version="1.0">

	<xd:doc scope="stylesheet">
		<xd:desc>
			<xd:p><xd:b>Created on:</xd:b> Dec 28, 2010</xd:p>
			<xd:p><xd:b>Author:</xd:b> Jonathan Stoppani</xd:p>
			<xd:p/>
		</xd:desc>
	</xd:doc>

	<xsl:output
		method="xml"
		encoding="UTF-8"
		indent="yes"/>

	<xsl:template match="@* | node()">
		<xsl:copy>
			<xsl:apply-templates select="@* | node()"/>
		</xsl:copy>
	</xsl:template>

	<xsl:template match="//packet[payload]">
		<xsl:copy>
			<xsl:apply-templates select="@* | node()"/>
			<decoded><xsl:copy-of select="func:decode(payload/text())" /></decoded>
		</xsl:copy>
	</xsl:template>
</xsl:stylesheet>