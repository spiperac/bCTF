$('document').ready(function() {
    populate_scores();
})

function populate_scores(){
    var scoresURL = "/api/scores";
    $.getJSON( scoresURL, function( data ) {
        $.each( data.ranks, function( key, val ) {
            feed_table(val);
        });
    });
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
    console.log(element);
}