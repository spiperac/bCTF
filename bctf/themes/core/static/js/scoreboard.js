$('document').ready(function() {
    update_feed();
    setInterval(update_feed, 120000); // Update scores every 2 minutes
})

function update_feed() {
    clean_table();
    scores_graph();
    populate_scores();
}

function populate_scores(){
    var scoresURL = "/api/scores/";
    $.getJSON( scoresURL, function( data ) {
        for (var i = 0; i < data.ranks.length; i++) {
            feed_table(data.ranks[i]);
        }
    });
}

function clean_table() {
    $('#scores-body').empty();
}

function feed_table(element) {
    if (element.country) {
        var show_county = `<i class="flag2x ${element.country}"></i>`;
    } else {
        var show_county = ``;
    }
    if (element.rank == 1 ) {
        $('#scores-body').append(
            `
            <tr>
                <td>${element.rank}</td>
                <td>
                    <div id="avatar" style="float:left">
                        <img src="${element.avatar}" height="50" width="50" class="img-fluid">
                    </div>
                    <div id="team_info" style="margin-left: 70px;">
                        <a href="/accounts/profile/${element.id}">${element.name}</a>
                        <p>Solved ${element.precentage}%</p>
                    </div>
                </td>
                <td>${show_county}</td>
                <td class="td-points">${element.points}</td>
            </tr>
            `
        )
    } else {
        $('#scores-body').append(
            `
            <tr>
                <td>${element.rank}</td>
                <td>
                    <div id="avatar" style="float:left">
                        <img src="${element.avatar}" height="50" width="50" class="img-fluid">
                    </div>
                    <div id="team_info" style="margin-left: 70px;">
                        <a href="/accounts/profile/${element.id}">${element.name}</a>
                        <p>Solved ${element.precentage}%</p>
                    </div>
                </td>
                <td>${show_county}</td>
                <td class="td-points">${element.points}</td>
            </tr>
            `
        )
    }
}

function scores_graph() {
    $.get('/api/top/', function( data ) {
        var parsed_data = $.parseJSON(JSON.stringify(data));
        ranks = parsed_data.ranks;

        if (Object.keys(ranks).length === 0 ){
            // If no one scored, set no solves
            $('#scoreboard').html(
                '<div class="center-align"><h3>No solves yet</h3></div>'
            );
            return;
        }
        var teams = Object.keys(ranks);

        var datasets = []

        for (var x=0; x < teams.length; x += 1) {
            var team = ranks[teams[x]];
            var team_color = colorhash(team.name + team.id);

            var scores = []
            var times = []
            // Organise team data into sets
            for (var i = 0; i < team.solves.length; i++){
                scores.push(team.solves[i].value)
                var date = moment(team.solves[i].time * 1000);
                times.push(date.toDate())
            }

            final_scores = cumulativesum(scores);
            axes = []
            for (var c = 0; c < final_scores.length; c++) {
                var tmp_data = {
                    x: times[c],
                    y: final_scores[c]
                }
                axes.push(tmp_data);
            }
            dataset = {
                label: team.name,
                showLine:true,
                data: axes,
                backgroundColor: team_color,
                borderColor: team_color,
                showLine: true,
                pointRadius: 5,
                pointHoverRadius: 5,
                fill: false,
            }

            datasets.push(dataset);

        }

        var chartData = {
            datasets: datasets,
        }

        $('#loaderScoreboard').hide();
        var ctx = document.getElementById('score-graph-live').getContext('2d');
        window.scoreboardChart = new Chart(ctx , {
            type: "scatter",
            data: chartData, 
            responsive: true,
            maintainAspectRatio: false,

            options: {
 
                legend: {
                    position: false,
                    labels: {
                        usePointStyle: true,
                    }
                },
                legendCallback: function(chart) { 
                    var text = []; 
                    text.push('<ul class="' + chart.id + '-legend">');
                    for (var i = 0; i < chart.data.datasets.length; i++) { 
                        text.push('<li class="truncate" onclick="updateDataset(event, ' + '\'' + i + '\'' + ')"><i class="material-icons left" style="color:' +
                                   chart.data.datasets[i].backgroundColor + 
                                   '">flag</i> ');
                        if (chart.data.datasets[i].label) { 
                            text.push(chart.data.datasets[i].label); 
                        } 
                        text.push('</li>'); 
                    } 
                    text.push('</ul>'); 
                    return text.join(''); 
                },                 
                title: {
                    display: true,
                    text: 'Top 10 Teams',
                    fontSize: 18,
                    fontColor: "#fff",
                },
                scales: {
                    xAxes: [{
                        type: 'time',
                        ticks: {
                            fontColor: "#fff",
                            beginAtZero: false
                        },
                        gridLines: {
                            display:false
                        } 
                    }],
                    yAxes: [{
                        ticks: {
                            fontColor: "#fff",
                        },
                        gridLines: {
                            display:false
                        }   
                    }]
                }
            }
        });
        $('#chart-legend').html(scoreboardChart.generateLegend());
        
    });
}

// Show/hide chart by click legend
updateDataset = function(e, datasetIndex) {
    var index = datasetIndex;
    var ci = e.view.scoreboardChart;
    var meta = ci.getDatasetMeta(index);

    // See controller.isDatasetVisible comment
    meta.hidden = meta.hidden === null? !ci.data.datasets[index].hidden : null;

    // We hid a dataset ... rerender the chart
    ci.update();
};

function cumulativesum (arr) {
    var result = arr.concat();
    for (var i = 0; i < arr.length; i += 1){
        result[i] = arr.slice(0, i + 1).reduce(function(p, i){ return p + i; });
    }
    return result
}

function colorhash(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i += 1) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    var colour = '#';
    for (var i = 0; i < 3; i += 1) {
      var value = (hash >> (i * 8)) & 0xFF;
      colour += ('00' + value.toString(16)).substr(-2);
    }
    return colour;
  }

  String.prototype.hashCode = function() {
    var hash = 0, i, chr, len;
    if (this.length == 0) {
        return hash;
    }
    for (i = 0, len = this.length; i < len; i += 1) {
        chr   = this.charCodeAt(i);
        hash  = ((hash << 5) - hash) + chr;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
};
