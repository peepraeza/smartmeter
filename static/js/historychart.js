
var chart_year = Highcharts.chart('container', {
    chart: {
        type: 'column'
    },
    xAxis: {
        categories: [
            '2012',
            '2013',
        ],
        crosshair: true
    },
    yAxis: {
        min: 0,
        title: {
            text: 'Energy (kwh)'
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
        footerFormat: '</table>',
        shared: true,
        useHTML: true
    },
    plotOptions: {
        column: {
            pointPadding: 0.2,
            borderWidth: 0
        },
        series: {
            cursor: 'pointer',
            point: {
                    events: {
                        click: function () {
                            alert('Category: ' + this.category);
                        }
                    }
                }
        }
    },
    series: [{
        name: 'ap1',
        data: [{
            name: '2012',
            y : 25,
        },{
            name: '2013',
            y : 50,
        }],
        

    }, {
        name: 'ap2',
        data: [{
            name: '2012',
            y : 35,
        },{
            name: '2013',
            y : 40,
        }],
    },{
        name: 'ap3',
        data: [{
            name: '2012',
            y : 45,
        },{
            name: '2013',
            y : 50,
        }],
    },{
        name: 'ap4',
        data: [{
            name: '2012',
            y : 55,
        },{
            name: '2013',
            y : 60,
        }],

    }],
});

$("#container .highcharts-axis-labels:first text").click(function() {
    alert($(this).text());
});