$('document').ready(function() {
    update_feed();
    scoregraph();
    setInterval(update_feed, 30000); // Update scores every 5 minutes

})

function update_feed() {
    clean_table();
    populate_scores();
}

function populate_scores(){
    var scoresURL = "/api/scores";
    $.getJSON( scoresURL, function( data ) {
        $.each( data.ranks, function( key, val ) {
            feed_table(val);
        });
    });
}

function clean_table() {
    $('#scores-body').empty();
}

function feed_table(element) {
    $('#scores-body').append(
        `
        <tr>
            <td>${element.rank}</td>
            <td>${element.name}</td>
            <td>${element.points}</td>
        </tr>
        `
    )
}

function cumulativesum (arr) {
    var result = arr.concat();
    for (var i = 0; i < arr.length; i++){
        result[i] = arr.slice(0, i + 1).reduce(function(p, i){ return p + i; });
    }
    return result
}

function scoregraph () {
    $.get('/api/top', function( data ) {
        var places = $.parseJSON(JSON.stringify(data));
        places = places['ranks'];
        if (Object.keys(places).length === 0 ){
            // Replace spinner
            $('#score-graph').html(
                '<div class="text-center"><h3 class="spinner-error">No solves yet</h3></div>'
            );
            return;
        }

        var teams = Object.keys(places);
        var traces = [];
        for(var i = 0; i < teams.length; i++){
            var team_score = [];
            var times = [];
            for(var j = 0; j < places[teams[i]]['solves'].length; j++){
                team_score.push(places[teams[i]]['solves'][j].value);
                var date = moment(places[teams[i]]['solves'][j].time * 1000);
                times.push(date.toDate());
            }
            team_score = cumulativesum(team_score);
            var trace = {
                x: times,
                y: team_score,
                mode: 'lines+markers',
                name: places[teams[i]]['name'],
                marker: {
                    color: colorhash(places[teams[i]]['name'] + places[teams[i]]['id']),
                },
                line: {
                    color: colorhash(places[teams[i]]['name'] + places[teams[i]]['id']),
                }
            };
            traces.push(trace);
        }

        traces.sort(function(a, b) {
            var scorediff = b['y'][b['y'].length - 1] - a['y'][a['y'].length - 1];
            if(!scorediff) {
                return a['x'][a['x'].length - 1] - b['x'][b['x'].length - 1];
            }
            return scorediff;
        });

        var layout = {
            title: 'Top 10 Teams',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            hovermode: 'closest',
            xaxis: {
                showgrid: false,
                showspikes: true,
            },
            yaxis: {
                showgrid: false,
                showspikes: true,
            },
            legend: {
                "orientation": "h"
            }
        };

        $('#score-graph').empty(); // Remove spinners
        Plotly.newPlot('score-graph', traces, layout, {
            // displayModeBar: false,
            displaylogo: false
        });
    });
}

function colorhash(str) {
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
      hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    var colour = '#';
    for (var i = 0; i < 3; i++) {
      var value = (hash >> (i * 8)) & 0xFF;
      colour += ('00' + value.toString(16)).substr(-2);
    }
    return colour;
  }

  String.prototype.hashCode = function() {
    var hash = 0, i, chr, len;
    if (this.length == 0) return hash;
    for (i = 0, len = this.length; i < len; i++) {
        chr   = this.charCodeAt(i);
        hash  = ((hash << 5) - hash) + chr;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
};