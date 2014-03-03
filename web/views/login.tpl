<!DOCTYPE html> 
<html> 
    <head>
        <title>Pyrus Login</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="bootstrap.css" />
        <link rel="stylesheet" type="text/css" href="additional.css" />

<!-- jQuery (necessary for Bootstrap's JavaScript plugins) --> 
<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js">
</script> 
<!--    <script source="jquery.min.js"></script> -->
<!-- 
Include all compiled plugins (below), or include individual files as needed 
-->
<script 
    src="http://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js">
</script>

    </head>

    <body>

    <div class="container">
<!-- include header template: 'views/header.tpl' -->
%include header

<!-- main content -->
<!--
    <div class="row-fluid" id="main">
        <div class="span7 offset1">
        <h3>Pyrus Login</h3> 
        </div>
    </div>
-->

    <div class="row" style="margin-top:1em">
    <div class="col-xs-12 col-sm-10 col-md-8"> 
    <form class="form-vertical" role="form" method="post" id="loginform">

        <h2 class="form-heading">Please log in</h2>
        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
        <input type="text" class="form-control input-sm" name="username" 
                                placeholder="Username" required autofocus>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="form-group">
        <input type="password" class="form-control input-sm" name="password" 
                                placeholder="Password" required>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-4">
                <div class="form-group">
        <button class="btn btn-default" type="submit">Login</button>
                </div>
            </div>
        </div>

    </form>
    </div> 
    </div> 

<!-- main content end -->

<!-- include footer template: 'views/footer.tpl' -->
%include footer

    </div> <!-- container-fluid -->
    </body>
</html>
