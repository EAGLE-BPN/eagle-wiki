<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
<xsl:template match="/">
<wikitems>
    <xsl:for-each select="//p">
<xsl:variable name="iteminwiki">
    <xsl:sequence select="document(concat('http://www.eagle-network.eu/wiki/index.php/Special:EntityData/', substring-after(@title,':'),'.xml'))"/>
    <!--   http://www.eagle-network.eu/wiki/index.php/Special:EntityData/Q2372.xml -->
</xsl:variable>   
        <xsl:variable name="ctsurn">
            <xsl:variable name="ids">
<xsl:choose>
    <xsl:when test="$iteminwiki//property[@id='p37']">
        <xsl:text>EDB</xsl:text><xsl:value-of select="$iteminwiki//property[@id='p37']//datavalue/@value"/>
    </xsl:when>
    <xsl:otherwise>
        <xsl:choose>
            <xsl:when test="$iteminwiki//property[@id='p24']">
                <!--EDH-->
        <xsl:value-of select="$iteminwiki//property[@id='p24']//datavalue/@value"/>
    </xsl:when>
    <xsl:otherwise>
<xsl:choose>
    <xsl:when test="$iteminwiki//property[@id='p38']">
        <xsl:text>EDR</xsl:text><xsl:value-of select="$iteminwiki//property[@id='p38']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p22']">
        <xsl:text>HE</xsl:text><xsl:value-of select="$iteminwiki//property[@id='p22']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p33']">
        <xsl:text>petrae</xsl:text><xsl:value-of select="$iteminwiki//property[@id='p33']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p34']">
        <xsl:text>UEL</xsl:text><xsl:value-of select="$iteminwiki//property[@id='p34']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p35']">
        <xsl:text>DAI</xsl:text><xsl:value-of select="$iteminwiki//property[@id='p35']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p47']"> 
        <!--Last Statues of Antiquity-->
        <xsl:value-of select="$iteminwiki//property[@id='p47']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p40']"> 
        <!--BSR - IRT -->
        <xsl:value-of select="$iteminwiki//property[@id='p40']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p50']"> 
        <!--insAph -->
        <xsl:value-of select="$iteminwiki//property[@id='p50']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p48']"> 
        <!--ELTE-->
        <xsl:value-of select="$iteminwiki//property[@id='p48']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p51']"> 
        <xsl:text>AIO</xsl:text><xsl:value-of select="$iteminwiki//property[@id='p51']//datavalue/@value"/>
    </xsl:when>
    <xsl:when test="$iteminwiki//property[@id='p56']"> 
        <!--PHI-->
        <xsl:value-of select="$iteminwiki//property[@id='p56']//datavalue/@value"/>
    </xsl:when>
</xsl:choose>
    </xsl:otherwise></xsl:choose></xsl:otherwise>
</xsl:choose>
            </xsl:variable>
            <xsl:choose>
                <xsl:when test="$iteminwiki//property[@id='p3']">
            <xsl:value-of select="concat('urn:cts:tm:', $iteminwiki//property[@id='p3']//datavalue/@value, '.eagle:', $ids)"/>
        </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="concat('urn:cts:eagle:', $ids)"/> <!--this is just to test, it should never actually happen but the problem remains for multiple tm..-->
            </xsl:otherwise>
            </xsl:choose></xsl:variable>
        <xsl:variable name="englishtranslations">
            <xsl:sequence select="$iteminwiki//property[@id='p11']"/>
        </xsl:variable>
        <xsl:variable name="germantranslations">
            <xsl:sequence select="$iteminwiki//property[@id='p12']"/>
        </xsl:variable>
        <xsl:variable name="italiantranslations">
            <xsl:sequence select="$iteminwiki//property[@id='p13']"/>
        </xsl:variable>
        <xsl:variable name="spanishtranslations">
            <xsl:sequence select="$iteminwiki//property[@id='p14']"/>
        </xsl:variable>
        <xsl:variable name="frenchtranslations">
            <xsl:sequence select="$iteminwiki//property[@id='p15']"/>
        </xsl:variable>
        <xsl:variable name="hungariantranslations">
            <xsl:sequence select="$iteminwiki//property[@id='p19']"/>
        </xsl:variable>
        <xsl:variable name="croatiantranslations">
            <xsl:sequence select="$iteminwiki//property[@id='p57']"/>
        </xsl:variable>
        
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
        <teiHeader>
            <fileDesc>
                <titleStmt>
                    <title xml:lang="en"><xsl:value-of select="$iteminwiki//description[@language='en']/@value"/></title>
                    <title xml:lang="de"><xsl:value-of select="$iteminwiki//description[@language='de']/@value"/></title>
                    <title xml:lang="it"><xsl:value-of select="$iteminwiki//description[@language='it']/@value"/></title>
                    <title xml:lang="es"><xsl:value-of select="$iteminwiki//description[@language='es']/@value"/></title>
                    <title xml:lang="fr"><xsl:value-of select="$iteminwiki//description[@language='fr']/@value"/></title>
                     <xsl:if test="$iteminwiki//property[@id='p11']">
                                <xsl:for-each select="$englishtranslations">
                                    <editor role="translator" lang="en">
                                    <xsl:choose>
                                        <xsl:when test="$iteminwiki//property[@id='p11']//property[@id='p21']">
                                            <xsl:value-of select="$iteminwiki//property[@id='p11']//property[@id='p21']//datavalue/@value"/>
                                        </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>unknown</xsl:text>
                                    </xsl:otherwise>
                                    </xsl:choose>
                                </editor>
                                </xsl:for-each>
                            </xsl:if>
                            <xsl:if test="$iteminwiki//property[@id='p12']">
                                <xsl:for-each select="$germantranslations">
                                    <editor role="translator" lang="de">
                                        <xsl:choose>
                                            <xsl:when test="$iteminwiki//property[@id='p12']//property[@id='p21']">
                                                <xsl:value-of select="$iteminwiki//property[@id='p12']//property[@id='p21']//datavalue/@value"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:text>unknown</xsl:text>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </editor>
                                </xsl:for-each>
                            </xsl:if>
                    <xsl:if test="$iteminwiki//property[@id='p13']">
                        <xsl:for-each select="$italiantranslations">
                            <editor role="translator" lang="it">
                                <xsl:choose>
                                    <xsl:when test="$iteminwiki//property[@id='p13']//property[@id='p21']">
                                        <xsl:value-of select="$iteminwiki//property[@id='p13']//property[@id='p21']//datavalue/@value"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>unknown</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </editor>
                        </xsl:for-each>
                    </xsl:if>
                    <xsl:if test="$iteminwiki//property[@id='p14']">
                        <xsl:for-each select="$spanishtranslations">
                            <editor role="translator" lang="es">
                                <xsl:choose>
                                    <xsl:when test="$iteminwiki//property[@id='p14']//property[@id='p21']">
                                        <xsl:value-of select="$iteminwiki//property[@id='p14']//property[@id='p21']//datavalue/@value"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>unknown</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </editor>
                        </xsl:for-each>
                    </xsl:if>
                    <xsl:if test="$iteminwiki//property[@id='p15']">
                        <xsl:for-each select="$frenchtranslations">
                            <editor role="translator" lang="fr">
                                <xsl:choose>
                                    <xsl:when test="$iteminwiki//property[@id='p15']//property[@id='p21']">
                                        <xsl:value-of select="$iteminwiki//property[@id='p15']//property[@id='p21']//datavalue/@value"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>unknown</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </editor>
                        </xsl:for-each>
                    </xsl:if>
                    <xsl:if test="$iteminwiki//property[@id='p19']">
                            <xsl:for-each select="$hungariantranslations">
                                <editor role="translator" lang="hu">
                                    <xsl:choose>
                                        <xsl:when test="$iteminwiki//property[@id='p19']//property[@id='p21']">
                                            <xsl:value-of select="$iteminwiki//property[@id='p19']//property[@id='p21']//datavalue/@value"/>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <xsl:text>unknown</xsl:text>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </editor>
                            </xsl:for-each>
                    </xsl:if>
                    <xsl:if test="$iteminwiki//property[@id='p57']">
                        <xsl:for-each select="$croatiantranslations">
                            <editor role="translator" lang="hr">
                                <xsl:choose>
                                    <xsl:when test="$iteminwiki//property[@id='p19']//property[@id='p21']">
                                        <xsl:value-of select="$iteminwiki//property[@id='p19']//property[@id='p21']//datavalue/@value"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:text>unknown</xsl:text>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </editor>
                        </xsl:for-each>
                    </xsl:if>
                </titleStmt>
                <publicationStmt>
                    <authority>Europeana Network of Ancient Greek and Latin Epigraphy</authority>
                    <idno type="urn:cts">
                        <xsl:value-of select="$ctsurn"/></idno>
                    <availability>
                        <p>
                            <ref type="license" target="http://creativecommons.org/licenses/by-sa/3.0/"/>
<!--                         this would be fine in most cases. there are some which are University of Oxford and some others which are CC0. the IPR statement is specified for each translation   -->
                        </p>
                    </availability>
                </publicationStmt>
                <sourceDesc>
                    <p/>
                </sourceDesc>
            </fileDesc>
            <profileDesc>
                <langUsage>
                    <language ident="en"/>
                    <language ident="grc"/>
                    <language ident="la"/>
                    <language ident="fr"/>
                    <language ident="de"/>
                    <language ident="grc-Latn"/>
                    <language ident="la-Grek"/>
                    <language ident="cop"/>
                </langUsage>
            </profileDesc>
            <revisionDesc>
                <change when="2014-05-14T"
                    who="http://http://data.perseus.org/sosol/users/Bridget%20Almas">Eagle mediawiki - perseids epidoc</change>
            </revisionDesc>
        </teiHeader>
        <text xml:lang="eng">
            <body>
                <xsl:if test="$iteminwiki//property[@id='p11']">
                    <xsl:for-each select="$englishtranslations">
                        <div xml:lang="eng" type="translation" xml:space="preserve" n="{$ctsurn}">
                                    <xsl:value-of select="$iteminwiki//property[@id='p11']//mainsnak/datavalue/@value"/>
                            </div>
                    </xsl:for-each>
                </xsl:if>
                <xsl:if test="$iteminwiki//property[@id='p12']">
                    <xsl:for-each select="$germantranslations">
                        <div xml:lang="de" type="translation" xml:space="preserve" n="{$ctsurn}">
                                    <xsl:value-of select="$iteminwiki//property[@id='p12']//mainsnak/datavalue/@value"/>
                            </div>
                    </xsl:for-each>
                </xsl:if>
                
                <xsl:if test="$iteminwiki//property[@id='p13']">
                    <xsl:for-each select="$italiantranslations">
                        <div xml:lang="it" type="translation" xml:space="preserve" n="{$ctsurn}">
                                    <xsl:value-of select="$iteminwiki//property[@id='p13']//mainsnak/datavalue/@value"/>
                            </div>
                    </xsl:for-each>
                </xsl:if>
                <xsl:if test="$iteminwiki//property[@id='p14']">
                    <xsl:for-each select="$spanishtranslations">
                        <div xml:lang="es" type="translation" xml:space="preserve" n="{$ctsurn}">
                                    <xsl:value-of select="$iteminwiki//property[@id='p14']//mainsnak/datavalue/@value"/>
                            </div>
                    </xsl:for-each>
                </xsl:if>
                
                <xsl:if test="$iteminwiki//property[@id='p15']">
                    <xsl:for-each select="$germantranslations">
                        <div xml:lang="de" type="translation" xml:space="preserve" n="{$ctsurn}">
                                    <xsl:value-of select="$iteminwiki//property[@id='p15']//mainsnak/datavalue/@value"/>
                            </div>
                    </xsl:for-each>
                </xsl:if>
                <xsl:if test="$iteminwiki//property[@id='p19']">
                    <xsl:for-each select="$hungariantranslations">
                        <div xml:lang="hu" type="translation" xml:space="preserve" n="{$ctsurn}">
                                    <xsl:value-of select="$iteminwiki//property[@id='p19']//mainsnak/datavalue/@value"/>
                            </div>
                    </xsl:for-each>
                </xsl:if>
                <xsl:if test="$iteminwiki//property[@id='p57']">
                    <xsl:for-each select="$croatiantranslations">
                        <div xml:lang="hr" type="translation" xml:space="preserve" n="{$ctsurn}">
                                    <xsl:value-of select="$iteminwiki//property[@id='p57']//mainsnak/datavalue/@value"/>
                            </div>
                    </xsl:for-each>
                </xsl:if>
            </body>
        </text>
    </TEI>
</xsl:for-each>
</wikitems>
</xsl:template>
</xsl:stylesheet>