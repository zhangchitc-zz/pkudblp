
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

	<div class="row">
		<div class="span12">
			<h2> Step2: Please select the data demonstration utility </h2>
			<br/>
 
            <div class="row">
				<div class="span8 offset2">

					<div id="myCarousel" class="carousel slide">
            			<div class="carousel-inner">
              				<div class="item">
                				<img src="img/trend.png" alt="">
                				<div class="carousel-caption">
                  					<h4>Statistic Trend</h4>
									<div class="row-fluid">
										<div class="span12">
											<div class="span11">
       			           						<p>Demonstrate publication statistics for one single affiliation using paleto diagram</p>
											</div>
											<div class="span1">
												<a class="btn btn-small btn-primary" data-toggle="modal" href="#trendModal" >Next</a>
											</div>
											<br>
											<br>
											<br>

										</div>
									</div>               				
								</div>
              				</div>
              				<div class="item active">
                				<img src="img/rank.png" alt="">
                				<div class="carousel-caption">
                  					<h4>Paper Ranking</h4>
									<div class="row-fluid">
										<div class="span12">
											<div class="span11">
       			           						<p>Rank all affiliations according to their overall publication statistics in the past six years</p>
											</div>
											<div class="span1">
												<form action="/rank" method="post">
													{{!hiddata}}
													<input type="submit" class="btn btn-small btn-primary" value="Rank">
												</form>
											</div>
											<br>
											<br>

										</div>
									</div>                				
								</div>
              				</div>
              				<div class="item">
                				<img src="img/comp.png" alt="">
                				<div class="carousel-caption">
                  					<h4>Affiliation Comparison</h4>
									<div class="row-fluid">
										<div class="span12">
											<div class="span11">
       			           						<p>Compare two affiliations' academic performance using publication statistics in order by year</p>
											</div>
											<div class="span1">
												<a class="btn btn-small btn-primary" data-toggle="modal" href="#compModal" >Next</a>
											</div>
											<br>
											<br>
											<br>

										</div>
									</div>
                				</div>
              				</div>
            			</div>
            			<a class="left carousel-control" href="#myCarousel" data-slide="prev">‹</a>
            			<a class="right carousel-control" href="#myCarousel" data-slide="next">›</a>
          			</div>

				</div>
			</div>

    <hr/>

	<div class="modal hide fade" id="compModal">
  		<div class="modal-header">
    		<button type="button" class="close" data-dismiss="modal">×</button>
    		<h3>Affiliation Comparison</h3>
  		</div>
		<form class="form-horizontal" action="/compare" method="post">
			{{!hiddata}}
  			<div class="modal-body">
				<fieldset>
					<div class="control-group">
      					<label class="control-label" for="sid">Affiliation1</label>
      					<div class="controls">
        					<select class="input-xlarge" id="sid" name="sid">
								{{!affops}}
							</select>
      					</div>
      					<label class="control-label" for="sid2">Affiliation2</label>
      					<div class="controls">
        					<select class="input-xlarge" id="sid2" name="sid2">
								{{!affops}}
							</select>
      					</div>
    				</div>
  				</fieldset>
  			</div>
  			
			<div class="modal-footer">
    			<a href="#" class="btn" data-dismiss="modal">Close</a>
   	 			<input type="submit" class="btn btn-primary" value="Compare">
  			</div>

		</form>

	</div>

	<div class="modal hide fade" id="trendModal">
  		<div class="modal-header">
    		<button type="button" class="close" data-dismiss="modal">×</button>
    		<h3>Statistics Trend</h3>
  		</div>
		<form class="form-horizontal" action="/trend" method="post">
			{{!hiddata}}
  			<div class="modal-body">
				<fieldset>
					<div class="control-group">
      					<label class="control-label" for="sid">Affiliation</label>
      					<div class="controls">
        					<select class="input-xlarge" id="sid" name="sid">
								{{!affops}}
							</select>
      					</div>
    				</div>
  				</fieldset>
  			</div>
  			<div class="modal-footer">
    			<a href="#" class="btn" data-dismiss="modal">Close</a>
   	 			<input type="submit" class="btn btn-primary" value="Show">
  			</div>

		</form>

	</div>



</div>

 
    <!-- Le javascript
    ================================================== --> 
    <!-- Placed at the end of the document so the pages load faster --> 
 

  </body> 
</html> 
