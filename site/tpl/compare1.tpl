<html>
<head>
<script src="js/jquery-min.js" type="text/javascript" charset="utf-8"></script>
<script src="js/raphael-min.js" type="text/javascript" charset="utf-8"></script>
<script src="js/elycharts-min.js" type="text/javascript" charset="utf-8"></script>


<script  type="text/javascript">
(function ($) {
 
$.elycharts.templates['line_basic_2'] = {
  type : 'line',
  margins : [10, 20, 50, 50],
  defaultSeries : {
    plotProps : {
      "stroke-width" : 4
    },
    dot: true,
    dotProps : {
      stroke : "white",
      "stroke-width" : 2
    }
  },
  series : {
    serie1 : { color : 'red' },
    serie2 : { color : 'blue' }
  },
  defaultAxis : {
    labels : true
  },
  features : {
    grid : {
      draw: [true, false],
      props : {
        "stroke-dasharray" : "-"
      }
    },
    legend : {
      horizontal : false,
      width: 180,
      height: 50,
      x : 220,
      y : 250,
      dotType : 'circle',
      dotProps : {
        stroke : 'white',
        "stroke-width" : 2
      },
      borderProps : {
        opacity : .3,
        fill: '#c0c0c0',
        "stroke-width": 0
      }
    }
  }
};
 
})(jQuery);

function get_univ (which) {
   return document.getElementById ("univ" + which).value;
}

function getFloat (id, attr) {
   o = document.getElementById (id)
   if (o) {
        return parseFloat (o.getAttribute (attr)).toFixed (2);
   } else {
        return 0;
   }
}

function get_data (which) {
   var data = [];
   for (var i = 2006; i <= 2011; i++) {
       data[i - 2006] = getFloat ("data_" + which + "_" + i, "total");
   }
   return data;
}

function get_tooltip (which) {
   var data = [];
   for (var i = 2006; i <= 2011; i++) {
       data[i - 2006] = 
	"<span style=color:#5AF> Conference: </span>" + getFloat ("data_" + which + "_" + i, "conf") + "<br>" + 
	"<span style=color:#F80> Journals: </span>" + getFloat ("data_" + which + "_" + i, "journal");
   }
   return data;
}

$(document).ready(function(){


$("#chart").chart({
 template : "line_basic_2",
 tooltips : {
  serie1 : get_tooltip ("1"),
  serie2 : get_tooltip ("2")
 },
 labels : ["2006", "2007", "2008", "2009", "2010", "2011"],
 values : {
  serie1 : get_data ("1"),
  serie2 : get_data ("2")
 },
 axis : {

  l : {title : 'Publications', titleDistance: 40 }
 },
 defaultSeries : {
  fill : true,
  stacked : false,
  highlight : {
   scale : 2
  },
  startAnimation : {
   active : true,
   type : "grow",
   easing : "bounce"
  }
 },
 legend : {
   serie1: get_univ ("1"), 
   serie2: get_univ ("2")
 }
});

});
</script>

<style type="text/css">
body {
    color: black;
}
#content {
    text-align : center;
    margin-top: 15px; 
}
#content h2 {
    font-size: 15px;
    font-family: arial,helvetica,verdana;
}
#chart {
    margin: 10px auto;
    align: center;
    height: 400px;
    width: 1000px;
    background-color: #F0F0F0;
}
</style>
</head>

<body>
	<div id="content">
