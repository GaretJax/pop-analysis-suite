<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	xmlns:xs="http://www.w3.org/2001/XMLSchema"
	xmlns:func="http://gridgroup.eia-fr.ch/popc"
	xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl"
	xmlns:exsl="http://exslt.org/common"
	xmlns:set="http://exslt.org/sets"
	xmlns:math="http://exslt.org/math"
	exclude-result-prefixes="xs xd"
	extension-element-prefixes="func set math exsl"
	version="1.0">

	<xd:doc scope="stylesheet">
		<xd:desc>
			<xd:p><xd:b>Created on:</xd:b> Dec 28, 2010</xd:p>
			<xd:p><xd:b>Author:</xd:b> Jonathan Stoppani</xd:p>
			<xd:p/>
		</xd:desc>
	</xd:doc>

	<xsl:output
		method="html"
		encoding="UTF-8"
		indent="yes"
		omit-xml-declaration="yes"
		doctype-public="XSLT-compat"/>
		
	<xsl:variable name="nodecount" select="count(//port)" />

	<xsl:template match="/">
		<html>
			<head>
				<meta charset="utf-8" />
				
				<title>Report</title>
				
				<link rel="stylesheet" href="styles/master.css" type="text/css" charset="utf-8" />
				<link rel="stylesheet" href="styles/pygments/pastie.css" type="text/css" charset="utf-8" />
				
				<script type="text/javascript" src="scripts/libs/jquery-1.5.js"></script>
				<script type="text/javascript" src="scripts/plugins.js"></script>
				<script type="text/javascript" src="scripts/master.js"></script>
			</head>
			
			<body>
				<header>
					<h1>POP Analysis suite <sup>v0.1</sup></h1>
				</header>
				
				<xsl:call-template name="navigation" />
				
				<section id="diagram">
					<table class="transactions">
						<xsl:apply-templates />
					</table>
				</section>
			</body>
		</html>
	</xsl:template>
	
	<xsl:template name="navigation">
		<nav>
			<ul>
				<li><a href="#summary">Summary</a></li>
				<li class="active"><a href="#diagram">Diagram</a></li>
				<li><a href="#log">Measure log</a></li>
				<li><a href="#code">Code</a></li>
			</ul>
			<ul>
				<li><xsl:comment> - </xsl:comment></li>
				<li class="frame-filter-bar">
					<div class="flags-filter">
						<strong>Show:</strong>
						<ol class="bubbles">
							<li class="active"><a href="#">all</a></li>
							<li><a href="#">hide ACK-only</a></li>
							<li><a href="#">smart SYN/FIN</a></li>
							<li><a href="#">PSH only</a></li>
						</ol>
					</div>
					<div class="conversation-filter">
						<strong>Conversations:</strong>
						<div>
							<button>All conversations</button>
							<ol>
								<xsl:for-each select="set:distinct(//packet/@conversation)">
									<xsl:sort data-type="number" />
									<li>
										<input type="checkbox" checked="checked" name="conv">
											<xsl:attribute name="value">
												<xsl:value-of select="concat('conversation-', .)"/>
											</xsl:attribute>
											<xsl:attribute name="id">
												<xsl:value-of select="concat('filter-conv-', .)"/>
											</xsl:attribute>
										</input>
										<label>
											<xsl:attribute name="for">
												<xsl:value-of select="concat('filter-conv-', .)"/>
											</xsl:attribute>
											<xsl:value-of select="concat('Conversation ', .)" />
										</label>
									</li>
								</xsl:for-each>
							</ol>
						</div>
					</div>
					<div class="bindstatus-filter">
						<strong>BindStatus:</strong>
						<ol class="bubbles">
							<li class="active"><a href="#">normal</a></li>
							<li><a href="#">smart</a></li>
							<li><a href="#">hide</a></li>
						</ol>
					</div>
					<div class="details-switch">
						<strong>Details:</strong>
						<ol class="bubbles">
							<li class="active"><a href="#">hide all</a></li>
							<li><a href="#">show all</a></li>
						</ol>
					</div>
				</li>
				<li><xsl:comment> - </xsl:comment></li>
				<li><xsl:comment> - </xsl:comment></li>
			</ul>
		</nav>
	</xsl:template>
	
	<xsl:template match="/measure/actors">
		<thead>
			<tr>
				<th><span><xsl:comment> - </xsl:comment></span></th>
				<xsl:for-each select="node">
					<th class="node">
						<xsl:attribute name="colspan">
							<xsl:value-of select="count(port)"/>
						</xsl:attribute>
						<span><xsl:value-of select="@addr"/></span>
					</th>
				</xsl:for-each>
				<td></td>
			</tr>
			<tr>
				<th></th>
				<xsl:for-each select="node/port">
					<th class="port">
						<span><xsl:value-of select="concat(':', @port)"/></span>
					</th>
				</xsl:for-each>
				<td></td>
			</tr>
		</thead>
	</xsl:template>
	
	<xsl:template match="/measure/transactions">
		<tbody>
			<tr class="placeholder">
				<td><span><xsl:comment> - </xsl:comment></span></td>
				<xsl:for-each select="//port">
					<td><span><xsl:comment> - </xsl:comment></span></td>
				</xsl:for-each>
				<td><span><xsl:comment> - </xsl:comment></span></td>
			</tr>
			
			<xsl:for-each select="packet">
				<tr>
					<xsl:variable name="from" select="from"/>
					<xsl:variable name="to" select="to"/>
					
					<xsl:variable name="offsets">
						<before><xsl:value-of select="count(//node[@addr=$from/@addr]/port[@port=$from/@port]/preceding::port)"/></before>
						<before><xsl:value-of select="count(//node[@addr=$to/@addr]/port[@port=$to/@port]/preceding::port)"/></before>
						<after><xsl:value-of select="count(//node[@addr=$from/@addr]/port[@port=$from/@port]/following::port)"/></after>
						<after><xsl:value-of select="count(//node[@addr=$to/@addr]/port[@port=$to/@port]/following::port)"/></after>
					</xsl:variable>
					
					<xsl:variable name="before" select="math:min(exsl:node-set($offsets)/before)" />
					<xsl:variable name="after" select="math:min(exsl:node-set($offsets)/after)" />
					<xsl:variable name="width" select="$nodecount - $before - $after" />
					
					<xsl:attribute name="class">
						<xsl:variable name="conversation" select="@conversation"/>

						<xsl:value-of select="concat('conversation-', $conversation)"/>

						<xsl:choose>
							<xsl:when test="@ack=1 and @fin=0 and @syn=0 and (@psh=0 or count(payload) = 0)"> ack-only</xsl:when>
							<xsl:when test="@syn=1 and @ack=0"> syn1</xsl:when>
							<xsl:when test="@syn=1 and @ack=1"> syn2</xsl:when>
							<xsl:when test="@fin=1 and not(preceding-sibling::packet[@conversation=$conversation and @fin=1])"> fin1</xsl:when>
							<xsl:when test="@fin=1 and preceding-sibling::packet[@conversation=$conversation and @fin=1]"> fin2</xsl:when>
						</xsl:choose>
						
						<xsl:choose>
							<xsl:when test="exsl:node-set($offsets)/before[1] &lt; exsl:node-set($offsets)/before[2]"> ltr</xsl:when>
							<xsl:otherwise> rtl</xsl:otherwise>
						</xsl:choose>
						
						<xsl:if test="decoded/request[@classid=0]/method[@id=0]"> bindstatus-request</xsl:if>
						<xsl:if test="decoded/response[@classid=0]/method[@id=0]"> bindstatus-response</xsl:if>
						
						<xsl:if test="not(decoded)"> no-payload</xsl:if>
					</xsl:attribute>
					
					<th>
						<span><xsl:value-of select="@conversation"/></span>
					</th>
					
					<xsl:if test="$before &gt; 0">
						<td class="before">
							<xsl:attribute name="colspan">
								<xsl:value-of select="$before"/>
							</xsl:attribute>
						</td>
					</xsl:if>
					
					<td class="transaction">
						<xsl:attribute name="colspan">
							<xsl:value-of select="$width"/>
						</xsl:attribute>
						<span><xsl:comment> - </xsl:comment></span>
					</td>
					
					<xsl:if test="$after &gt; 0">
						<td class="after">
							<xsl:attribute name="colspan">
								<xsl:value-of select="$after"/>
							</xsl:attribute>
						</td>
					</xsl:if>
					
					<td class="details">
						<ul class="bubbles flags">
							<xsl:if test="@syn=1"><li class="syn" title="SYN flag set">SYN</li></xsl:if>
							<xsl:if test="@fin=1"><li class="fin" title="FIN flag set">FIN</li></xsl:if>
							<xsl:if test="@psh=1"><li class="psh" title="PSH flag set">PSH</li></xsl:if>
							<xsl:if test="@ack=1"><li class="ack" title="ACK flag set">ACK</li></xsl:if>
						</ul>
						<xsl:if test="decoded">
							<ul class="bubbles type">
								<xsl:if test="decoded/request"><li class="req" title="Request">→</li></xsl:if>
								<xsl:if test="decoded/response"><li class="res" title="Response">←</li></xsl:if>
								<xsl:if test="decoded/exception"><li class="exc" title="Exception">×</li></xsl:if>
							</ul>
						</xsl:if>
						<xsl:if test="decoded/request">
							<ul class="bubbles semantics">
								<xsl:if test="decoded/request/semantics/@seq = 1"><li class="seq" title="Sequential">SEQ</li></xsl:if>
								<xsl:if test="decoded/request/semantics/@conc = 1"><li class="conc" title="Concurrent">CONC</li></xsl:if>
								<xsl:if test="decoded/request/semantics/@mutex = 1"><li class="mutex" title="Mutex">MTX</li></xsl:if>
								
								<xsl:if test="decoded/request/semantics/@sync = 1"><li class="sync" title="Synchronous">SYNC</li></xsl:if>
								<xsl:if test="decoded/request/semantics/@async = 1"><li class="async" title="Asynchronous">ASYNC</li></xsl:if>
								
								<xsl:if test="decoded/request/semantics/@construct = 1"><li class="construct" title="Constructor">CONSTRUCT</li></xsl:if>
							</ul>
						</xsl:if>
						
						<xsl:if test="decoded">
							<code><xsl:value-of select="decoded//short" /></code>
							<div class="details">
								<!-- Highlighted code -->
								<xsl:copy-of select="decoded//highlighted/*" />
								
								<!-- Encoded payload -->
								<div class="payload"><xsl:copy-of select="func:format_stream(payload/text())"/></div>
								
								<!-- Actors -->
								<p class="actors">
									<span>From:</span> <strong><xsl:value-of select="concat(from/@addr, ':', from/@port)"/></strong>
									<span>To:</span> <strong><xsl:value-of select="concat(to/@addr, ':', to/@port)"/></strong>
								</p>
							</div>
						</xsl:if>
					</td>
				</tr>
			</xsl:for-each>
		</tbody>
	</xsl:template>
</xsl:stylesheet>



