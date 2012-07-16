
<!DOCTYPE html> 
<html lang="en"> 
  <head> 
    <meta charset="utf-8"> 
    <title>Welcome to PKU-OS paper ranking system</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1.0"> 
    <meta name="description" content=""> 
    <meta name="author" content=""> 
 
    <!-- Le styles --> 
    <link href="css/bootstrap.css" rel="stylesheet"> 
    <link href="css/bootstrap-responsive.css" rel="stylesheet"> 
    <script src="js/jquery.min.js"></script>
    <script src="js/bootstrap.js"></script>

	<script language="JavaScript"> 
        function SetAllCheckBoxes(FormName, AreaName, CheckValue)
        {
            if(!document.forms[FormName]) return;

            var objCheckBoxes = document.forms[FormName].elements["conf"];
           	if(objCheckBoxes) {
            	var countCheckBoxes = objCheckBoxes.length;
            	if(!countCheckBoxes) objCheckBoxes.checked = CheckValue;
            	else
                 	// set the check value for all check boxes
                 	for(var i = 0; i < countCheckBoxes; i++) {
                 	   // alert (objCheckBoxes[i].value);
					   if (objCheckBoxes[i].id[0] == AreaName)
                 	   	 objCheckBoxes[i].checked = CheckValue;
                 	}
			}

            var objCheckBoxes = document.forms[FormName].elements["journal"];
           	if(objCheckBoxes) {
            	var countCheckBoxes = objCheckBoxes.length;
            	if(!countCheckBoxes) objCheckBoxes.checked = CheckValue;
            	else
                 	// set the check value for all check boxes
                 	for(var i = 0; i < countCheckBoxes; i++) {
                 	   // alert (objCheckBoxes[i].value);
					   if (objCheckBoxes[i].id[0] == AreaName)
                 	   	 objCheckBoxes[i].checked = CheckValue;
                 	}
			}
        }

        function ToggleCheckBox(idName)
        {
			var checkBox = document.getElementById(idName);
            if(!checkBox) return;
			checkBox.checked = !checkBox.checked;
        }

	</script> 
  </head> 
 
  <body> 

<div class="container">

	<div class="row">
		<div class="span12">
			<br>
      		<h1>Welcome to PKU-OS paper ranking system</h1>
      		<p>This is version 1.0.0 released on June 10, 2012.</p>
      		<hr />
    	</div>
	</div>

	<form name="list" action="/select" method="post"> 

	<div class="row">
		<div class="span12">
			<h2> Step1: Please select conferences and journals you are interested </h2>
			<br/>
 
			<div class="tabbable tabs-left">
  				<ul class="nav nav-tabs">
    				<li class="active"><a href="#tab1" data-toggle="tab">Computer Architecture</a></li>
    				<li><a href="#tab2" data-toggle="tab">Network</a></li>
    				<li><a href="#tab3" data-toggle="tab">Security</a></li>
    				<li><a href="#tab4" data-toggle="tab">Theory</a></li>
    				<li><a href="#tab5" data-toggle="tab">Software Engineering</a></li>
    				<li><a href="#tab6" data-toggle="tab">Data Mining</a></li>
    				<li><a href="#tab7" data-toggle="tab">Multimedia</a></li>
    				<li><a href="#tab8" data-toggle="tab">Artificial Intelligence</a></li>

  				</ul>
  				<div class="tab-content">
					{{!tabs}}
  				</div>
			</div>
		</div>
	</div>

    <hr/>

    <div class="centered-text">
    	<button class="btn btn-large btn-primary"> Next </button>
	</div>
    <br/>
    <br/>
    <br/>
    <br/>
    <br/>


</form>

</div>

 

  </body> 
</html> 
