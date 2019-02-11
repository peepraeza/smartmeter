var p1 = [];
var p2 = [];
var p3 = [];
var p4 = [];
var q1 = [];
var q2 = [];
var q3 = [];
var q4 = [];
var i1 = [];
var i2 = [];
var i3 = [];
var i4 = [];
var s1 = [];
var s2 = [];
var s3 = [];
var s4 = [];
var pf1 = [];
for(var i=0;i<e.length;i++){
    var time = e[i]["time"]*1000;
    p1.push([time, e[i]["P1"]]);
    p2.push([time, e[i]["P2"]]);
    p3.push([time, e[i]["P3"]]);
    p4.push([time, e[i]["P4"]]);
    
    q1.push([time, e[i]["Q1"]]);
    q2.push([time, e[i]["Q2"]]);
    q3.push([time, e[i]["Q3"]]);
    q4.push([time, e[i]["Q4"]]);
    
    i1.push([time, e[i]["I1"]]);
    i2.push([time, e[i]["I2"]]);
    i3.push([time, e[i]["I3"]]);
    i4.push([time, e[i]["I4"]]);

    s1.push([time, e[i]["S1"]]);
    s2.push([time, e[i]["S2"]]);
    s3.push([time, e[i]["S3"]]);
    s4.push([time, e[i]["S4"]]);

    // pf1.push([time, e[i]["PF"]]);
}
// var wp1 =
// alert(e[e.length-1]["whole_p1"]-dec_time1)
var val_p1 = (e[e.length-1]["P1_wh"] - dec_time1)/1000;
var val_p2 = (e[e.length-1]["P2_wh"] - dec_time2)/1000;
var val_p3 = (e[e.length-1]["P3_wh"] - dec_time3)/1000;
var val_p4 = (e[e.length-1]["P4_wh"] - dec_time4)/1000;
$('#pv1').text(val_p1.toFixed(2));
$('#pv2').text(val_p2.toFixed(2));
$('#pv3').text(val_p3.toFixed(2));
$('#pv4').text(val_p4.toFixed(2));

var val_pp1 = (e[e.length-1]["P1_wh"])/1000;
var val_pp2 = (e[e.length-1]["P2_wh"])/1000;
var val_pp3 = (e[e.length-1]["P3_wh"])/1000;
var val_pp4 = (e[e.length-1]["P4_wh"])/1000;
$('#ppm1').text(val_pp1.toFixed(2));
$('#ppm2').text(val_pp2.toFixed(2));
$('#ppm3').text(val_pp3.toFixed(2));
$('#ppm4').text(val_pp4.toFixed(2));
// $('#sv1').text(s1[e.length-1][1]);
// $('#sv2').text(s2[e.length-1][1]);
// $('#sv3').text(s3[e.length-1][1]);
// $('#sv4').text(s4[e.length-1][1]);
// $('#iv1').text(i1[e.length-1][1]);
// $('#iv2').text(i2[e.length-1][1]);
// $('#iv3').text(i3[e.length-1][1]);
// $('#iv4').text(i4[e.length-1][1]);

Highcharts.stockChart('all', {
chart: {
    events: {
        load: function () {

            // set up the updating of the chart each second
            var series1p = this.series[0];
            var series2p = this.series[1];
            var series3p = this.series[2];
            var series4p = this.series[3];
            
            var series1q = this.series[4];
            var series2q = this.series[5];
            var series3q = this.series[6];
            var series4q = this.series[7];
            
            var series1s = this.series[8];
            var series2s = this.series[9];
            var series3s = this.series[10];
            var series4s = this.series[11];

            var series1i = this.series[12];
            var series2i = this.series[13];
            var series3i = this.series[14];
            var series4i = this.series[15];

            var ref = database.ref("energy");
            ref.orderByChild("time").limitToLast(1).on("child_added", function(snapshot) {
                var changedData = snapshot.val();                        
                var x =  changedData.time*1000;
                var p1 =  changedData.P1;
                var p2 =  changedData.P2;
                var p3 =  changedData.P3;
                var p4 =  changedData.P4;
               
                series1p.addPoint([x, p1], false, true);
                series2p.addPoint([x, p2], false, true);
                series3p.addPoint([x, p3], false, true);
                series4p.addPoint([x, p4], false, true);
                
                var q1 =  changedData.Q1;
                var q2 =  changedData.Q2;
                var q3 =  changedData.Q3;
                var q4 =  changedData.Q4;
               
                series1q.addPoint([x, q1], false, true);
                series2q.addPoint([x, q2], false, true);
                series3q.addPoint([x, q3], false, true);
                series4q.addPoint([x, q4], false, true);
                
                var i1 =  changedData.I1;
                var i2 =  changedData.I2;
                var i3 =  changedData.I3;
                var i4 =  changedData.I4;
               
                series1i.addPoint([x, i1], false, true);
                series2i.addPoint([x, i2], false, true);
                series3i.addPoint([x, i3], false, true);
                series4i.addPoint([x, i4], true, true);

                var s1 =  changedData.S1;
                var s2 =  changedData.S2;
                var s3 =  changedData.S3;
                var s4 =  changedData.S4;
               
                series1s.addPoint([x, s1], false, true);
                series2s.addPoint([x, s2], false, true);
                series3s.addPoint([x, s3], false, true);
                series4s.addPoint([x, s4], true, true);
                
                if(check == true){
                    check = false;
                    dec_time1 = changedData.P1_wh;
                    dec_time2 = changedData.P2_wh;
                    dec_time3 = changedData.P3_wh;
                    dec_time4 = changedData.P4_wh;
                }
                var val_p1 = (changedData.P1_wh - dec_time1)/1000;
                var val_p2 = (changedData.P2_wh - dec_time2)/1000;
                var val_p3 = (changedData.P3_wh - dec_time3)/1000;
                var val_p4 = (changedData.P4_wh - dec_time4)/1000;
                $('#pv1').text(val_p1.toFixed(2));
                $('#pv2').text(val_p2.toFixed(2));
                $('#pv3').text(val_p3.toFixed(2));
                $('#pv4').text(val_p4.toFixed(2));
                
                var val_pp1 = changedData.P1_wh/1000;
                var val_pp2 = changedData.P2_wh/1000;
                var val_pp3 = changedData.P3_wh/1000;
                var val_pp4 = changedData.P4_wh/1000;
                $('#ppm1').text(val_pp1.toFixed(2));
                $('#ppm2').text(val_pp2.toFixed(2));
                $('#ppm3').text(val_pp3.toFixed(2));
                $('#ppm4').text(val_pp4.toFixed(2));
                // $('#sv1').text(s1);
                // $('#sv2').text(s2);
                // $('#sv3').text(s3);
                // $('#sv4').text(s4);
                // $('#iv1').text(i1);
                // $('#iv2').text(i2);
                // $('#iv3').text(i3);
                // $('#iv4').text(i4);
            })
        }
    }
},

time: {
    useUTC: false
},

rangeSelector: {
    buttons: [{
        count: 15,
        type: 'minute',
        text: '15M'
    },{
        count: 30,
        type: 'minute',
        text: '30M'
    },{
        type: 'all',
        text: 'All'
    }],
    selected: 3,
    inputEnabled: false, // ปิดเลือกวันที่
},
legend: {
    enabled : true,
    verticalAlign: 'top',
    align : "right"
},
yAxis: [{
    labels: {
        align: 'right',
        x: -3,
        format: '{value}W'
    },
    title: {
        text: 'Active Power(P)'
    },
    height: '20%',
    lineWidth: 2
}, {
    labels: {
        align: 'right',
        x: -3,
        format: '{value}VAR'
    },
    title: {
        text: 'Reactive Power(Q)'
    },
    top: '25%',
    height: '20%',
    offset: 0,
    lineWidth: 2
}, {
    labels: {
        align: 'right',
        x: -3,
        format: '{value}VA'
    },
    title: {
        text: 'Apparent Power(S)'
    },
    top: '50%',
    height: '20%',
    offset: 0,
    lineWidth: 2
}, {
    labels: {
        align: 'right',
        x: -3,
        format: '{value}A'
    },
    title: {
        text: 'Current(I)'
    },
    top: '75%',
    height: '20%',
    offset: 0,
    lineWidth: 2
}],

credits: {
    enabled: false
},

exporting: {
    enabled: false
},

navigator: {
        enabled: true
},

scrollbar: {
    enabled: false
},
tooltip: {
    valueDecimals: 2,
},

series: [{
    id:"ch1",
    name: ch1_name,
    data: (p1)
},
{
    id:"ch2",
    name: ch2_name,
    data: (p2)
},
{
    id:"ch3",
    name: ch3_name,
    data: (p3)
},{
    id:"ch4",
    name: ch4_name ,
    data: (p4),
},{
    colorIndex:0,
    name: ch1_name,
    linkedTo: "ch1",
    data: (q1),
    yAxis:1,
},{
    colorIndex:1,
    name: ch2_name,
    linkedTo: "ch2",
    data: (q2),
    yAxis:1,
},
{
    colorIndex:2,
    name: ch3_name,
    linkedTo: "ch3",
    data: (q3),
    yAxis:1,
},{
    colorIndex:3,
    name: ch4_name ,
    linkedTo: "ch4",
    data: (q4),
    yAxis:1,
},{
    colorIndex:0,
    name: ch1_name,
    linkedTo: "ch1",
    data: (s1),
    yAxis:2,
},{
    colorIndex:1,
    name: ch2_name,
    linkedTo: "ch2",
    data: (s2),
    yAxis:2,
},
{
    colorIndex:2,
    name: ch3_name,
    linkedTo: "ch3",
    data: (s3),
    yAxis:2,
},{
    colorIndex:3,
    name: ch4_name ,
    linkedTo: "ch4",
    data: (s4),
    yAxis:2,
},{
    colorIndex:0,
    name: ch1_name,
    linkedTo: "ch1",
    data: (i1),
    yAxis:3,
},{
    colorIndex:1,
    name: ch2_name,
    linkedTo: "ch2",
    data: (i2),
    yAxis:3,
},
{
    colorIndex:2,
    name: ch3_name,
    linkedTo: "ch3",
    data: (i3),
    yAxis:3,
},{
    colorIndex:3,
    name: ch4_name ,
    linkedTo: "ch4",
    data: (i4),
    yAxis:3,
}]
});

Highcharts.stockChart('activePow', {
chart: {
    events: {
        load: function () {
            // set up the updating of the chart each second
            var series1 = this.series[0];
            var series2 = this.series[1];
            var series3 = this.series[2];
            var series4 = this.series[3];
            var ref = database.ref("energy");
            ref.orderByChild("time").limitToLast(1).on("child_added", function(snapshot) {
                var changedData = snapshot.val();                        
                var x =  changedData.time*1000;
                var p1 =  changedData.P1;
                var p2 =  changedData.P2;
                var p3 =  changedData.P3;
                var p4 =  changedData.P4;
               
                series1.addPoint([x, p1], false, true);
                series2.addPoint([x, p2], false, true);
                series3.addPoint([x, p3], false, true);
                series4.addPoint([x, p4], true, true);
            })
        }
    }
},

time: {
    useUTC: false
},

rangeSelector: {
    buttons: [{
        count: 15,
        type: 'minute',
        text: '15M'
    },{
        count: 30,
        type: 'minute',
        text: '30M'
    },{
        type: 'all',
        text: 'All'
    }],
    selected: 3,
    inputEnabled: false, // ปิดเลือกวันที่
},
legend: {
    enabled : true,
    verticalAlign: 'top',
    align : "right"
},
yAxis: {
  title: {
      text: "Active Power(P)"
  },
  labels: {
      format: '{value}W'
  },
},
tooltip: {
    valueDecimals: 2,
},
credits: {
    enabled: false
},
exporting: {
    enabled: false
},

navigator: {
    enabled: true
},

scrollbar: {
    enabled: false
},

series: [{
    name: ch1_name,
    data: (p1)
},
{
    name: ch2_name,
    data: (p2)
},
{
    name: ch3_name,
    data: (p3)
},{
    name: ch4_name ,
    data: (p4)
}]
});

Highcharts.stockChart('reactivePow', {
chart: {
    events: {
        load: function () {

            // set up the updating of the chart each second
            var series1 = this.series[0];
            var series2 = this.series[1];
            var series3 = this.series[2];
            var series4 = this.series[3];
            var ref = database.ref("energy");
            ref.orderByChild("time").limitToLast(1).on("child_added", function(snapshot) {
                var changedData = snapshot.val();                        
                var x =  changedData.time*1000;
                var q1 =  changedData.Q1;
                var q2 =  changedData.Q2;
                var q3 =  changedData.Q3;
                var q4 =  changedData.Q4;
               
                series1.addPoint([x, q1], false, true);
                series2.addPoint([x, q2], false, true);
                series3.addPoint([x, q3], false, true);
                series4.addPoint([x, q4], true, true);
            })
        }
    }
},

time: {
    useUTC: false
},

rangeSelector: {
    buttons: [{
        count: 1,
        type: 'minute',
        text: '1M'
    },{
        count: 15,
        type: 'minute',
        text: '15M'
    },{
        count: 30,
        type: 'minute',
        text: '30M'
    },{
        type: 'all',
        text: 'All'
    }],
    selected: 3,
    inputEnabled: false, // ปิดเลือกวันที่
},
legend: {
    enabled : true,
    verticalAlign: 'top',
    align : "right"
},
yAxis: {
  title: {
      text: "Reactive Power(Q)"
  },
  labels: {
      format: '{value}VAR'
  },
},
credits: {
    enabled: false
},
exporting: {
    enabled: false
},

navigator: {
        enabled: true
},

scrollbar: {
    enabled: false
},
tooltip: {
    valueDecimals: 2,
},

series: [{
    name: ch1_name,
    data: (q1)
},
{
    name: ch2_name,
    data: (q2)
},
{
    name: ch3_name,
    data: (q3)
},{
    name: ch4_name ,
    data: (q4)
}]
});

Highcharts.stockChart('current', {
chart: {
    events: {
        load: function () {

            // set up the updating of the chart each second
            var series1 = this.series[0];
            var series2 = this.series[1];
            var series3 = this.series[2];
            var series4 = this.series[3];
            var ref = database.ref("energy");
            ref.orderByChild("time").limitToLast(1).on("child_added", function(snapshot) {
                var changedData = snapshot.val();                        
                var x =  changedData.time*1000;
                var i1 =  changedData.I1;
                var i2 =  changedData.I2;
                var i3 =  changedData.I3;
                var i4 =  changedData.I4;
               
                series1.addPoint([x, i1], false, true);
                series2.addPoint([x, i2], false, true);
                series3.addPoint([x, i3], false, true);
                series4.addPoint([x, i4], true, true);
            })
        }
    }
},

time: {
    useUTC: false
},

rangeSelector: {
    buttons: [{
        count: 15,
        type: 'minute',
        text: '15M'
    },{
        count: 30,
        type: 'minute',
        text: '30M'
    },{
        type: 'all',
        text: 'All'
    }],
    selected: 3,
    inputEnabled: false, // ปิดเลือกวันที่
},
legend: {
    enabled : true,
    verticalAlign: 'top',
    align : "right"
},
yAxis: {
  title: {
      text: "Current(I)"
  },
  labels: {
      format: '{value}A'
  },
},

credits: {
    enabled: false
},

exporting: {
    enabled: false
},

navigator: {
        enabled: true
},

scrollbar: {
    enabled: false
},
tooltip: {
    valueDecimals: 2,
},

series: [{
    name: ch1_name,
    data: (i1)
},
{
    name: ch2_name,
    data: (i2)
},
{
    name: ch3_name,
    data: (i3)
},{
    name: ch4_name ,
    data: (i4)
}]
});

Highcharts.stockChart('apparentPow', {
chart: {
    events: {
        load: function () {

            // set up the updating of the chart each second
            var series1 = this.series[0];
            var series2 = this.series[1];
            var series3 = this.series[2];
            var series4 = this.series[3];
            var ref = database.ref("energy");
            ref.orderByChild("time").limitToLast(1).on("child_added", function(snapshot) {
                var changedData = snapshot.val();                        
                var x =  changedData.time*1000;
                var s1 =  changedData.S1;
                var s2 =  changedData.S2;
                var s3 =  changedData.S3;
                var s4 =  changedData.S4;
               
                series1.addPoint([x, s1], false, true);
                series2.addPoint([x, s2], false, true);
                series3.addPoint([x, s3], false, true);
                series4.addPoint([x, s4], true, true);
            })
        }
    }
},

time: {
    useUTC: false
},

rangeSelector: {
    buttons: [{
        count: 15,
        type: 'minute',
        text: '15M'
    },{
        count: 30,
        type: 'minute',
        text: '30M'
    },{
        type: 'all',
        text: 'All'
    }],
    selected: 3,
    inputEnabled: false, // ปิดเลือกวันที่
},
legend: {
    enabled : true,
    verticalAlign: 'top',
    align : "right"
},
yAxis: {
  title: {
      text: "Apparent Power(S)"
  },
  labels: {
      format: '{value}VA'
  },
},

credits: {
    enabled: false
},

exporting: {
    enabled: false
},

navigator: {
        enabled: true
},

scrollbar: {
    enabled: false
},
tooltip: {
    valueDecimals: 2,
},

series: [{
    name: ch1_name,
    data: (s1)
},
{
    name: ch2_name,
    data: (s2)
},
{
    name: ch3_name,
    data: (s3)
},{
    name: ch4_name ,
    data: (s4)
}]
});