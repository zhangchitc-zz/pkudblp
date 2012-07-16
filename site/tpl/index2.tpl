    				<div class="tab-pane {{active}}" id="tab{{area}}">

						<div class="row-fluid">
							<div class="span12">

					  			<div class="row-fluid centered-text">
					  				<div class="span8"> 
									</div>

					  				<div class="span2"> 
										<div class="btn btn-large btn-success" onClick="SetAllCheckBoxes('list', '{{area}}', true);">Select All</div>
					  				</div>
					  				<div class="span2"> 
										<div class="btn btn-large btn-danger"  onClick="SetAllCheckBoxes('list', '{{area}}', false);">Select None</div>
					  				</div>
	 
					  			</div>

                                <br/>

								{{!htmlrows}}
							</div>
						</div>
					</div>
