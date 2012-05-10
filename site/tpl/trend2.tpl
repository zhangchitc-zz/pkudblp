        <div class="chart_container_centered">

            <canvas id="chart" width="1000" height="400">
                Your web-browser does not support the HTML 5 canvas element.
            </canvas>

        </div>

        <script type="application/javascript">

function get_univ (which) {
   return document.getElementById ("univ" + which).value;
}

function get_data (which) {
   var data = [];
   for (var i = 2006; i <= 2011; i++) {
	    o = document.getElementById ("data_" + which + "_" + i);
        if (o) {
            data[i - 2006] = parseFloat (o.getAttribute ("total"));
            data[i - 2006] = Math.round (data[i - 2006] * 100) / 100;
        } else {
            data[i - 2006] = 0;
        }
   }
   return data;
}

function get_tooltip (which) {
   var data = [];
   for (var i = 2006; i <= 2011; i++) {
       data[i - 2006] = 
	"<span style=color:#5AF> Conference: </span>" + document.getElementById ("data_" + which + "_" + i).getAttribute ("conf") + "<br>" + 
	"<span style=color:#F80> Journals: </span>" + document.getElementById ("data_" + which + "_" + i).getAttribute ("journal");
   }
   return data;
}

        
            var chart13 = new AwesomeChart('chart');
            chart13.chartType = "pareto";
            chart13.title = "Publication statistics for " + get_univ ("1");
            chart13.data = get_data ("1");
            chart13.labels = ['2006','2007','2008','2009','2010','2011'];
            chart13.colors = ['#006CFF', '#FF6600', '#34A038', '#945D59', '#93BBF4', '#F493B8'];
            chart13.chartLineStrokeStyle = 'rgba(0, 0, 200, 0.5)';
            chart13.chartPointFillStyle = 'rgb(0, 0, 200)';
            chart13.draw();
        </script>
        
    </body>
</html>

