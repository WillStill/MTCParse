<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:math="http://www.w3.org/2005/xpath-functions/math" exclude-result-prefixes="xs math"
    version="3.0" xpath-default-namespace="urn:mtconnect.org:MTConnectStreams:2.0"
    xmlns:m="urn:mtconnect.org:MTConnectStreams:2.0"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="urn:mtconnect.org:MTConnectStreams:2.0 http://schemas.mtconnect.org/schemas/MTConnectStreams_2.0.xsd"
    xmlns="urn:mtconnect.org:MTConnectStreams:2.0">

    <xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/>
    <xsl:variable name="dataColl" as="document-node()+" select="collection('data/?select=*.xml')"/>
    <xsl:variable name="sequenceNumbList" as="xs:string+" select="$dataColl//*/@sequence => sort()"/>
    <xsl:template match="/">

        <!-- Processes for each file -->
        <xsl:for-each select="$dataColl">
            <xsl:variable name="currentMachineFile" as="document-node()" select="current()"/>
            
            <!-- Create Document -->
            <xsl:result-document
                href="{$currentMachineFile//*:DeviceStream[not(@name='Agent')]/@name}.xml"
                method="xml" indent="yes">
                
                <!-- Order the Suquence Numbers from any element with them -->
                <xsl:variable name="sequenceNumbList" as="xs:string+"
                    select="current()//*/@sequence => sort()"/>
                
                <!-- Create Root Element With Device Name -->
                <xsl:element name="{//*:DeviceStream[not(@name='Agent')]/@uuid}">
                    
                    <!-- For each Data Item -->
                    <xsl:for-each select="$sequenceNumbList">
                        
                        <!-- Get element and parents based on Sequence Number -->
                        <xsl:variable name="currentEle" as="element()"
                            select="$currentMachineFile//*[@sequence = current()]"/>
                        <xsl:variable name="parentEles" as="element()*"
                            select="$currentEle/ancestor::*[ancestor::*:Streams]"/>
                        
                        <!-- Create Element labeled Data Item -->
                        <xsl:element name="{$currentEle/name()}">
                            
                            <!-- Create Attributes from Attributes on Data Item -->
                            <xsl:for-each select="$currentEle/@*">
                                <xsl:attribute name="{current()/name()}">
                                    <xsl:value-of select="current()"/>
                                    
                                </xsl:attribute>
                            </xsl:for-each>
                            
                            <!-- Create Attributes from Attributes on Parent Nodes -->
                            <xsl:for-each select="$parentEles">
                                <xsl:if test="current()/@*">
                                    <xsl:attribute name="{current()/name()}">
                                        <xsl:for-each select="current()/@*">
                                            <xsl:variable name="value" as="xs:string"
                                                select="current() ! string()"/>
                                            <xsl:value-of select="concat($value, '/')"/>
                                            
                                        </xsl:for-each>
                                    </xsl:attribute>
                                </xsl:if>
                            </xsl:for-each>
                            
                            <!-- Apply Data Item data onto Element -->
                            <xsl:apply-templates select="$currentEle"/>
                            
                        </xsl:element>
                    </xsl:for-each>
                </xsl:element>
            </xsl:result-document>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
