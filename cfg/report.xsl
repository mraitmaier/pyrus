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
    <title>Test Report for <xsl:value-of select="//TestSet/@name" /></title>

    <style type="text/css">

body {font-family: FreeSans, Arial, Sans, Verdana, Helvetica;}
table { border: thin dotted; }
tr { border: 5 }

.font12px { font-size: 12px; }
.tblborder { border: thin dotted; }
.tblheader { background-color: black; color: white; }
.lime { background-color: lime; }
.red  { background-color: red; }
.gold { background-color: gold; }

    </style>

    </head>
    <body>
    <h1>Test Result for "<xsl:value-of select="//TestSet/@name" />"</h1>
    <div class="font12px">
    <b>Report Generated: </b><xsl:value-of select="//TestSet/Generated" /> 
    <br />
    <b>Test Set run started: </b> <xsl:value-of select="//TestSet/Started" />
    <br />
    <b>Test Set run finished: </b><xsl:value-of select="//TestSet/Finished" />
    <br />
    </div>

    <xsl:for-each select="//Configuration">
    <div>
    <h3>Configuration: <xsl:value-of select="@name" /></h3> 
    <table>
    <tr class="tblheader">
    <ŧh /> <th>Action</th><th>Status</th>
    </tr>
    <tr>
    <td>Setup</td>
    <td><xsl:value-of select="Setup/@action" /></td>
    <xsl:choose>
        <xsl:when test="Setup/@status='pass'">
    <td class="lime"><xsl:value-of select="Setup/@status" /></td>
        </xsl:when>
        <xsl:when test="Setup/@status='fail'">
    <td class="red"><xsl:value-of select="Setup/@status" /></td>
        </xsl:when>
        <xsl:when test="Setup/@status='not tested'">
    <td class="gold"><xsl:value-of select="Setup/@status" /></td>
        </xsl:when>
        <xsl:otherwise>
    <td><xsl:value-of select="Setup/@status" /></td>
        </xsl:otherwise>
    </xsl:choose>
    </tr>
    <tr>
    <td>Cleanup</td>
    <td><xsl:value-of select="Cleanup/@action" /></td>
    <xsl:choose>
        <xsl:when test="Cleanup/@status='pass'">
    <td class="lime"><xsl:value-of select="Cleanup/@status" /></td>
        </xsl:when>
        <xsl:when test="Cleanup/@status='fail'">
    <td class="red"><xsl:value-of select="Cleanup/@status" /></td>
        </xsl:when>
        <xsl:when test="Cleanup/@status='not tested'">
    <td class="gold"><xsl:value-of select="Cleanup/@status" /></td>
        </xsl:when>
        <xsl:otherwise>
    <td><xsl:value-of select="Cleanup/@status" /></td>
        </xsl:otherwise>
    </xsl:choose>
    </tr>
    </table>
    <p />

        <table class="tblborder" >
        <tr class="tblheader">
        <th>Test Cases</th><th>Test Steps</th><th>Action</th>
                    <th>Expected Status</th><th>Status</th>
        </tr>
        <xsl:for-each select="TestCase">
            <xsl:choose>
                <xsl:when test="@status='pass'">
        <tr class="lime">
        <td>    <xsl:value-of select="@name" /></td><td></td><td></td><td></td>
        <td>    <xsl:value-of select="@status" /></td>
        </tr>
                </xsl:when>
                <xsl:when test="@status='fail'">
        <tr class="red">
        <td>    <xsl:value-of select="@name" /></td><td></td><td></td><td></td>
        <td>    <xsl:value-of select="@status" /></td>
        </tr>
                </xsl:when>
                <xsl:when test="@status='not tested'">
        <tr class="gold">
        <td>    <xsl:value-of select="@name" /></td><td></td><td></td><td></td>
        <td>    <xsl:value-of select="@status" /></td>
        </tr>
                </xsl:when>
                <xsl:otherwise>
        <tr>
        <td>    <xsl:value-of select="@name" /></td><td></td><td></td><td></td>
        <td>    <xsl:value-of select="@status" /></td>
        </tr>
                </xsl:otherwise>
            </xsl:choose>
        <tr>
        <td /><td>Setup</td><td><xsl:value-of select="Setup/@action" /></td>
            <xsl:choose>
                <xsl:when test="Setup/@status='pass'">
        <td class="lime"></td>
        <td class="lime"><xsl:value-of select="Setup/@status" /></td>
                </xsl:when>
                <xsl:when test="Setup/@status='fail'">
        <td class="red"></td>
        <td class="red"><xsl:value-of select="Setup/@status" /></td>
                </xsl:when>
                <xsl:when test="Setup/@status='not tested'">
        <td class="gold"></td>
        <td class="gold"><xsl:value-of select="Setup/@status" /></td>
                </xsl:when>
                <xsl:otherwise>
        <td></td>
        <td><xsl:value-of select="Setup/@status" /></td>
                </xsl:otherwise>
            </xsl:choose>
        </tr>
            <xsl:for-each select="TestStep">
            <tr>
            <td />
            <td><xsl:value-of select="@name" /></td>
            <td><xsl:value-of select="@action" /></td>
                <xsl:choose>
                    <xsl:when test="@status='pass'">
                        <xsl:if test="@expected-status='pass'">
            <td class="lime"><xsl:value-of select="@expected-status" /></td>
            <td class="lime"><xsl:value-of select="@status" /></td>
                        </xsl:if>
                        <xsl:if test="@expected-status='xfail'">
            <td class="red"><xsl:value-of select="@expected-status" /></td>
            <td class="red"><xsl:value-of select="@status" /></td>
                        </xsl:if>
                    </xsl:when>
                    <xsl:when test="@status='not tested'">
            <td class="gold"><xsl:value-of select="@expected-status" /></td>
            <td class="gold"><xsl:value-of select="@status" /></td>
                    </xsl:when>
                    <xsl:when test="@status='fail'">
                        <xsl:if test="@expected-status='pass'">
            <td class="red"><xsl:value-of select="@expected-status" /></td>
            <td class="red"><xsl:value-of select="@status" /></td>
                        </xsl:if>
                        <xsl:if test="@expected-status='xfail'">
            <td class="lime"><xsl:value-of select="@expected-status" /></td>
            <td class="lime"><xsl:value-of select="@status" /></td>
                        </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>
            <td><xsl:value-of select="@status" /></td>
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
            </xsl:for-each> <!-- for-each teststep -->
        <tr>
        <td /><td>Cleanup</td><td><xsl:value-of select="Cleanup/@action" /></td>
            <xsl:choose>
                <xsl:when test="Cleanup/@status='pass'">
        <td class="lime"></td>
        <td class="lime"><xsl:value-of select="Cleanup/@status" /></td>
                </xsl:when>
                <xsl:when test="Cleanup/@status='fail'">
        <td class="red"></td>
        <td class="red"><xsl:value-of select="Cleanup/@status" /></td>
                </xsl:when>
                <xsl:when test="Cleanup/@status='not tested'">
        <td class="gold"></td>
        <td class="gold"><xsl:value-of select="Cleanup/@status" /></td>
                </xsl:when>
                <xsl:otherwise>
        <td />
        <td><xsl:value-of select="Cleanup/@status" /></td>
                </xsl:otherwise>
            </xsl:choose>
        </tr>
        </xsl:for-each> <!-- for-each testcase -->
        </table>
    </div>
    </xsl:for-each> <!-- for-each configuration -->

    </body>
    </html>
</xsl:template>

</xsl:stylesheet> 
