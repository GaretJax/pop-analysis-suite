<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema" exclude-result-prefixes="xs xd"
	xmlns:set="http://exslt.org/sets"
	xmlns:exsl="http://exslt.org/common"
	extension-element-prefixes="set exsl"
	xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" version="1.0">

	<xd:doc scope="stylesheet">
		<xd:desc>
			<xd:p><xd:b>Created on:</xd:b> Oct 20, 2010</xd:p>
			<xd:p><xd:b>Author:</xd:b> Jonathan Stoppani</xd:p>
			<xd:p/>
		</xd:desc>
	</xd:doc>

	<xsl:output method="xml" encoding="UTF-8" indent="yes"/>

	<xsl:key name="ip" match="//field[@name='ip.src' or @name='ip.dst']" use="@value"/>
	
	<xsl:template match="/">
		<measure>
			<actors>
				<xsl:variable name="addresses" select="//field[@name='ip.src' or @name='ip.dst']"/>

				<xsl:for-each select="$addresses[generate-id() = generate-id(key('ip', @value)[1])]">
					<node>
						<xsl:variable name="ip" select="@value"/>
						
						<xsl:attribute name="addr">
							<xsl:value-of select="@show" />
						</xsl:attribute>

						<xsl:variable name="from"
							select="//packet[proto[@name='ip']/field[@name='ip.src']/@value=$ip]"/>
						
						<xsl:variable name="to"
							select="//packet[proto[@name='ip']/field[@name='ip.dst']/@value=$ip]"/>

						<xsl:variable name="ports">
							<xsl:for-each select="$from/proto[@name='tcp']/field[@name='tcp.srcport']|$to/proto[@name='tcp']/field[@name='tcp.dstport']">
								<port>
									<xsl:value-of select="@show" />
								</port>
							</xsl:for-each>
						</xsl:variable>
						
						<xsl:for-each select="set:distinct(exsl:node-set($ports)/port)">
							<xsl:sort data-type="number" />
							<port>
								<xsl:attribute name="port">
									<xsl:value-of select="." />
								</xsl:attribute>
							</port>
						</xsl:for-each>
					</node>
				</xsl:for-each>
			</actors>

			<transactions>
				<xsl:apply-templates/>
			</transactions>
		</measure>
	</xsl:template>

	<xsl:template match="/pdml/packet">
		<packet>
			<xsl:attribute name="conversation">
				<xsl:value-of
					select="proto[@name='tcp']/field[@name='tcp.stream']/@show"/>
			</xsl:attribute>
			<xsl:attribute name="timestamp">
				<xsl:value-of
					select="proto[@name='geninfo']/field[@name='timestamp']/@value"/>
			</xsl:attribute>
			<xsl:attribute name="psh">
				<xsl:value-of
					select="proto[@name='tcp']//field[@name='tcp.flags.push']/@value"/>
			</xsl:attribute>
			<xsl:attribute name="syn">
				<xsl:value-of
					select="proto[@name='tcp']//field[@name='tcp.flags.syn']/@value"/>
			</xsl:attribute>
			<xsl:attribute name="fin">
				<xsl:value-of
					select="proto[@name='tcp']//field[@name='tcp.flags.fin']/@value"/>
			</xsl:attribute>
			<xsl:attribute name="ack">
				<xsl:value-of
					select="proto[@name='tcp']//field[@name='tcp.flags.ack']/@value"/>
			</xsl:attribute>

			<from>
				<xsl:attribute name="addr">
					<xsl:value-of select="proto[@name='ip']/field[@name='ip.src']/@show"
					/>
				</xsl:attribute>
				<xsl:attribute name="port">
					<xsl:value-of
						select="proto[@name='tcp']/field[@name='tcp.srcport']/@show"/>
				</xsl:attribute>
			</from>
			<to>
				<xsl:attribute name="addr">
					<xsl:value-of select="proto[@name='ip']/field[@name='ip.dst']/@show"
					/>
				</xsl:attribute>
				<xsl:attribute name="port">
					<xsl:value-of
						select="proto[@name='tcp']/field[@name='tcp.dstport']/@show"/>
				</xsl:attribute>
			</to>
			
			<!--
				The tcp.pdu.size field is used when tshark decodes the payload as another protocol,
				while the fake-field-wrapper protocol is inserted when no protocol is recognized.
			-->
			<xsl:apply-templates select="proto[@name='fake-field-wrapper']/field[@name='data']|proto[@name='tcp']/field[@name='tcp.pdu.size']"/>
		</packet>
	</xsl:template>

	<xsl:template match="proto[@name='fake-field-wrapper']/field[@name='data']|proto[@name='tcp']/field[@name='tcp.pdu.size']">
		<payload>
			<xsl:value-of select="@value"/>
		</payload>
	</xsl:template>
</xsl:stylesheet>
