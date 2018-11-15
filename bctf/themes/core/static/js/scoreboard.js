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
    if (element.country) {
        var show_county = `<img src="${element.country}" alt="None" width="25px" height="15px" />`;
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
                        <img src="${element.avatar}" eight="50px" width="50px" class="img-fluid">
                    </div>
                    <div id="team_info" style="margin-left: 70px;">
                        <a href="/accounts/profile/${element.id}">${element.name}</a> <span class="badge badge-secondary"><i class="fas fa-crown" style="color:gold"></i></span>
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
                        <img src="${element.avatar}" height="50px" width="50px" class="img-fluid">
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

function cumulativesum (arr) {
    var result = arr.concat();
    for (var i = 0; i < arr.length; i++){
        result[i] = arr.slice(0, i + 1).reduce(function(p, i){ return p + i; });
    }
    return result
}

function scores_graph() {
    $.get('/api/top', function( data ) {
        var parsed_data = $.parseJSON(JSON.stringify(data));
        ranks = parsed_data['ranks'];

        if (Object.keys(ranks).length === 0 ){
            // If no one scored, set no solves
            $('#score-graph-placeholder').html(
                '<div class="text-center"><h3 class="spinner-error">No solves yet</h3></div>'
            );
            return;
        }
        var teams = Object.keys(ranks);

        var datasets = []

        for (var x=0; x < teams.length; x++) {
            var team = ranks[teams[x]];
            var team_color = colorhash(team.name + team.id);

            var scores = []
            var times = []
            // Organise team data into sets
            for (i in team.solves){
                scores.push(team.solves[i].value)
                var date = moment(team.solves[i].time * 1000);
                times.push(date.toDate())
            }

            final_scores = cumulativesum(scores);
            axes = []
            for (var c in final_scores) {
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

        var lineChartData = {
            datasets: datasets,
        }

        $('#loaderScoreboard').hide();
        var ctx = document.getElementById('score-graph-live').getContext('2d');
        var LineChartDemo = new Chart(ctx , {
            type: "scatter",
            data: lineChartData, 
            options: {
                legend: {
                    labels: {
                        fontColor: "#fff",
                        fontSize: 15
                    }
                },
                title: {
                    display: true,
                    text: 'Top 10 Teams',
                    fontSize: 18,
                    fontColor: '#fff'
                },
                scales: {
                    xAxes: [{
                        type: 'time',
                        ticks: {
                            fontColor: "#fff",
                        },
                        gridLines: {
                            display:false
                        } 
                    }],
                    yAxes: [{
                        ticks: {
                            fontColor: "#fff", // this here
                        },
                        gridLines: {
                            display:false
                        }   
                    }]
                }
            }
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


window.onresize = function () {
    Plotly.Plots.resize(document.getElementById('score-graph'));
};