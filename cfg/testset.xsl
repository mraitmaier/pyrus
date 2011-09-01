<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
    <!--
        This is an XSLT template file. Fill in this area with the
        XSL elements which will transform your XML to XHTML.
    -->
    <html>
    <head>
    <title>Test Set '<xsl:value-of select="//TestSet/@name" />'</title>

    <style type="text/css">

body {
    font-family: FreeSans, Candara, Tahoma, Sans, Helvetica;
}
table { table-layout: auto; 
        empty-cells: show;
}
tr { border: 5 }
td { background: lightblue; }

.font12px { font-size: 12px; }
.tblborder { border: thin dotted; }
.tblheader { background-color: black; color: white; }
.lime { background-color: lime; }
.red  { background-color: red; }
.gold { background-color: gold; }

    </style>

    </head>
    <body>
    <h1>Test Set: "<xsl:value-of select="//TestSet/@name" />"</h1>
<!-- test set setup & cleanup -->
    <div>
    <table class="tblborder">
        <tr class="tblheader">
            <th style="width:10%" />
            <th style="width:70%">Action</th>
            <th style="width:20%">Arguments</th>
        </tr>
        <tr>
            <td>Setup</td>
            <td><xsl:value-of select="//TestSet/Setup/Action" /></td>
            <td><xsl:value-of select="//TestSet/Setup/Args" /></td>
        </tr>
        <tr>
            <td>Cleanup</td>
            <td><xsl:value-of select="//TestSet/Cleanup/Action" /></td>
            <td><xsl:value-of select="//TestSet/Cleanup/Args" /></td>
        </tr>
    </table>
    </div>
<!-- configuration part -->
    <xsl:for-each select="//Configuration">
    <div>
    <h3>Configuration: <xsl:value-of select="@name" /></h3> 

    <table class="tblborder">
        <tr class="tblheader">
            <th>Test Object</th>
            <th style="width:80%"><xsl:value-of select="TestObject/@name" /></th>
        </tr>
        <tr>
            <td>Type</td>
            <td><xsl:value-of select="TestObject/Type" /></td>
        </tr>
        <tr>
            <td>IP Address</td>
            <td><xsl:value-of select="TestObject/IP" /></td>
        </tr>
        <tr>
            <td>Description</td>
            <td><xsl:value-of select="TestObject/Description" /></td>
        </tr>
        <tr>
            <td>Additional Arguments</td>
            <td><xsl:value-of select="TestObject/Args" /></td>
        </tr>
    </table>
    <p />
    <div>
    <table class="tblborder">
        <tr class="tblheader">
            <th style="width:10%" />
            <th style="width:70%">Action</th>
            <th style="width:20%">Arguments</th>
        </tr>
        <tr>
            <td>Setup</td>
            <td><xsl:value-of select="Setup/Action/Script" /></td>
            <td><xsl:value-of select="Setup/Action/Args" /></td>
        </tr>
        <tr>
            <td>Cleanup</td>
            <td><xsl:value-of select="Cleanup/Action/Script" /></td>
            <td><xsl:value-of select="Cleanup/Action/Args" /></td>
        </tr>
    </table>
    </div>

    <p />
<!-- test case part -->
    <table class="tblborder" >
        <tr class="tblheader">
            <th>Test Cases</th>
            <th>Test Steps</th>
            <th>Action</th>
            <th>Arguments</th>
            <th>Expected Status</th>
        </tr>

        <xsl:for-each select="TestCase">
        <tr>
            <td><xsl:value-of select="@name" /> </td>
            <td /><td /><td /><td />
        </tr>
        <tr>
            <td />
            <td>Setup</td>
            <td><xsl:value-of select="Setup/Action/Script" /></td>
            <td><xsl:value-of select="Setup/Action/Args" /></td>
            <td><xsl:value-of select="@expected" /></td>
        </tr>

        <xsl:for-each select="TestStep">
        <tr>
            <td />
            <td><xsl:value-of select="@name" /></td>
            <td><xsl:value-of select="Script" /></td>
            <td><xsl:value-of select="Args" /></td>
            <td><xsl:value-of select="@expected" /></td>
        </tr>
        </xsl:for-each> <!-- for-each teststep -->

        <tr>
            <td />
            <td>Cleanup</td>
            <td><xsl:value-of select="Cleanup/Action/Script" /></td>
            <td><xsl:value-of select="Cleanup/Action/Args" /></td>
            <td><xsl:value-of select="@expected" /></td>
        </tr>

         
        </xsl:for-each> <!-- for-each testcase -->
    </table>
    </div>
    </xsl:for-each> <!-- for-each configuration -->

    </body>
    </html>
</xsl:template>

</xsl:stylesheet> 
