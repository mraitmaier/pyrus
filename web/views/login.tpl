<!DOCTYPE html> 
<html> 
    <head>
        <title>Pyrus Login</title>
        <meta charset="utf-8" />
        <link rel="stylesheet" type="text/css" href="bootstrap.min.css" />
        <link rel="stylesheet" type="text/css" href="additional.css" />
        <script source="jquery.min.js"></script> 
        <script source="bootstrap.min.js"></script> 
    </head>

    <body>

    <div class="container-fluid">
<!-- include header template: 'views/header.tpl' -->
%include header

<!-- main content -->
    <div class="row-fluid" id="main">
        <div class="span7 offset1">
        <h3>Pyrus Login</h3> 
        </div>
    </div>

    <div class="row-fluid" id="main">
        <div class="span8">
        <form class="form-horizontal" method="post" id="loginform">
            <div class="control-group">
                <label class="control-label" for="username">Username</label> 
                <div class="controls">
                    <input type="text" name="username" 
                           placeholder="your username here..." required/>
                </div>
            </div>
                     
            <div class="control-group">
                <label class="control-label" for="password">Password</label> 
                <div class="controls">
                    <input type="password" name="password" 
                           placeholder="your password here..." required />
                </div>
            </div>

            <div class="control-group">
                <div class="controls">
                    <button class="btn" type="submit"
                                        id="submit_button">Login</button>
                </div>
            </div>
        </form>
        </div>
    </div> <!-- row-fluid -->
<!-- main content end -->

<!-- include footer template: 'views/footer.tpl' -->
%include footer

    </div> <!-- container-fluid -->
    </body>
</html>
