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

body {font-family: Candara, FreeSans, Tahoma, Arial, Sans, Helvetica;}
table { 
    table-layout: auto;
    empty-cells: show;
}
tr { border: 5 }

.font12px { font-size: 12px; }
.tblborder { border: thin dotted; }
.tblheader { background-color: black; color: white; }
.lime { background-color: lime; }
.green { background-color: green; color: white; }
.red  { background-color: red; }
.gold { background-color: gold; }
.black { background-color: black; color: white; }
.blue { background-color: DarkBlue; color: white; }

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
    <p />

    <table>
    <tr class="tblheader">
        <th style="width:15"/> 
        <th style="width:70">Action</th>
        <th style="width:15">Status</th>
    </tr>
    <tr class="blue">
    <td>Setup</td><td /><td />
    </tr>
    <xsl:for-each select="//TestSet/Setup/Action">
    <tr>
    <td />
    <td><xsl:value-of select="@script" /></td>
    <xsl:choose>
        <xsl:when test="@status='pass'">
    <td class="lime"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:when test="@status='fail'">
    <td class="red"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:when test="@status='not tested'">
    <td class="gold"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:otherwise>
    <td><xsl:value-of select="@status" /></td>
        </xsl:otherwise>
    </xsl:choose>
    </tr>
    </xsl:for-each>
    <tr class="blue">
    <td>Cleanup</td><td /><td />
    </tr>
    <xsl:for-each select="//TestSet/Cleanup/Action">
    <tr>
    <td />
    <td><xsl:value-of select="@script" /></td>
    <xsl:choose>
        <xsl:when test="@status='pass'">
    <td class="lime"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:when test="@status='fail'">
    <td class="red"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:when test="@status='not tested'">
    <td class="gold"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:otherwise>
    <td><xsl:value-of select="@status" /></td>
        </xsl:otherwise>
    </xsl:choose>
    </tr>
    </xsl:for-each>
    </table>
    <p />

    </div>

    <xsl:for-each select="//Configuration">
    <div>
    <h3>Configuration: <xsl:value-of select="@name" /></h3> 
    <!-- display test object information -->
    <table class="tblborder">
        <tr class="tblheader">
            <th>Test Object</th>
            <th style="width:80%"></th>
        </tr>
        <tr>
            <td>Name</td>
            <td><xsl:value-of select="TestObject/@name" /></td>
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
            <td>Additional Arguments</td>
            <td><xsl:value-of select="TestObject/Args" /></td>
        </tr>
    </table>
    <p />

    <table>
    <tr class="tblheader">
    <th /> <th>Action</th><th>Status</th>
    </tr>
    <tr class="blue">
    <td>Setup</td><td /><td />
    </tr>
    <xsl:for-each select="Setup/Action">
    <tr>
        <td />
        <td><xsl:value-of select="@script" /></td>
        <xsl:choose>
            <xsl:when test="@status='pass'">
        <td class="lime"><xsl:value-of select="@status" /></td>
            </xsl:when>
            <xsl:when test="@status='fail'">
        <td class="red"><xsl:value-of select="@status" /></td>
            </xsl:when>
            <xsl:when test="@status='not tested'">
        <td class="gold"><xsl:value-of select="@status" /></td>
            </xsl:when>
            <xsl:otherwise>
        <td><xsl:value-of select="@status" /></td>
            </xsl:otherwise>
        </xsl:choose>
    </tr>
    </xsl:for-each>
    <tr class="blue">
    <td>Cleanup</td><td /><td />
    </tr>
    <xsl:for-each select="Cleanup/Action">
    <tr>
    <td />
    <td><xsl:value-of select="@script" /></td>
    <xsl:choose>
        <xsl:when test="@status='pass'">
    <td class="lime"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:when test="@status='fail'">
    <td class="red"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:when test="@status='not tested'">
    <td class="gold"><xsl:value-of select="@status" /></td>
        </xsl:when>
        <xsl:otherwise>
    <td><xsl:value-of select="@status" /></td>
        </xsl:otherwise>
    </xsl:choose>
    </tr>
    </xsl:for-each>
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
        <td /><td class="blue">Setup</td>
              <td class="blue"><xsl:value-of select="Setup/Action/@script" /></td>
            <xsl:choose>
                <xsl:when test="Setup/Action/@status='pass'">
        <td class="lime"></td>
        <td class="lime"><xsl:value-of select="Setup/Action/@status" /></td>
                </xsl:when>
                <xsl:when test="Setup/Action/@status='fail'">
        <td class="red"></td>
        <td class="red"><xsl:value-of select="Setup/Action/@status" /></td>
                </xsl:when>
                <xsl:when test="Setup/Action/@status='not tested'">
        <td class="gold"><xsl:value-of select="Setup/Action/@status" /></td>
                </xsl:when>
                <xsl:otherwise>
        <td></td>
        <td><xsl:value-of select="Setup/Action/@status" /></td>
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
            <td class="green"><xsl:value-of select="@expected-status" /></td>
            <td class="green"><xsl:value-of select="@status" /></td>
                        </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>
            <td><xsl:value-of select="@status" /></td>
                    </xsl:otherwise>
                </xsl:choose>
            </tr>
            </xsl:for-each> <!-- for-each teststep -->
        <tr>
        <td /><td class="blue">Cleanup</td>
        <td class="blue"><xsl:value-of select="Cleanup/Action/@script" /></td>
            <xsl:choose>
                <xsl:when test="Cleanup/Action/@status='pass'">
        <td class="lime"></td>
        <td class="lime"><xsl:value-of select="Cleanup/Action/@status" /></td>
                </xsl:when>
                <xsl:when test="Cleanup/Action/@status='fail'">
        <td class="red"></td>
        <td class="red"><xsl:value-of select="Cleanup/Action/@status" /></td>
                </xsl:when>
                <xsl:when test="Cleanup/Action/@status='not tested'">
        <td class="gold"><xsl:value-of select="Cleanup/Action/@status" /></td>
                </xsl:when>
                <xsl:otherwise>
        <td><xsl:value-of select="Cleanup/Action/@status" /></td>
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
