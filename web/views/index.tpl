<!DOCTYPE html> 
<html lang="en"> 
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE-edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Pyrus Home</title>

<!-- include jquery & bootstrap: 'views/includes.tpl' -->
%include includes

    </head>

    <body>

    <div class="container-fluid">
<!-- include header: 'views/header.tpl' -->
%include header
<!-- include navigation bar: 'views/nav_bar.tpl' -->
%include nav_bar

        <div class="row-fluid" id="main">
            <div class="span8">

            index: it works! 

            </div>
        </div>

<!-- include footer template: 'views/footer.tpl' -->
%include footer

    </div> <!-- container-fluid -->

    </body>
</html>
