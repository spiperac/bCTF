$('document').ready(function() {
    update_events();
    setInterval(events, 120000); // Update scores every 2 minutes

})

function populate_events(){
    var scoresURL = "/api/events/";
    $.getJSON( scoresURL, function( data ) {
        $.each( data.events, function( key, val ) {
            feed_events(val);
        });
    });
}

function clean_events() {
    $('#events').empty();
}

function feed_events(element) {
    $('#events').append(
        `
        <li class="collection-item avatar">
        <i class="material-icons circle red">place</i>
        <span class="title">[${element.time}]</span>
        <p><a href="/accounts/profile/${element.team_id}">${element.team}</a>  just captured  <a href="/challenges/#${element.challenge_id}" target="_blank">${element.challenge}</a>!</p>
        </li>
        `
    )
}

function update_events() {
    clean_events();
    populate_events();
}