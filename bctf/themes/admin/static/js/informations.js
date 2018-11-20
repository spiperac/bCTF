function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function randomColors(data_length) {
    var colors = [];
    for (var i = 0; i < data_length; i++ ) {
        colors.push(getRandomColor());
    }
    return colors;
}

 function solvedChart(ctx, data) {

    data = {
        datasets: [{
            data: data,
            backgroundColor: ['green', 'red']
        }],

        labels: [
            'Solved',
            'Not Solved'
        ]
    };

    options = {
        maintainAspectRatio : false,
        title: {
            display: true,
            text: 'Challenges solved',
            fontSize: 30,
            fontColor: 'white'
        },
        legend: {
            labels: {
                fontColor: "white",
                fontSize: 15
            }
        }
    }

    var solvedChart = new Chart(ctx,{
        type: 'doughnut',
        data: data,
        options: options
    });

 }  


  function solvedAtLeastOne(ctx, data) {

    data = {
        datasets: [{
            data: data,
            backgroundColor: ['green', 'red']
        }],

        labels: [
            'One or more',
            'Nope'
        ]
    };

    options = {
        maintainAspectRatio : false,
        title: {
            display: true,
            text: 'Teams scored!',
            fontSize: 30,
            fontColor: 'white'
        },
        legend: {
            labels: {
                fontColor: "white",
                fontSize: 15
            }
        }
    }

    var solvedChart = new Chart(ctx,{
        type: 'doughnut',
        data: data,
        options: options
    });

 }  

  function firstBloods(ctx, labels, data) {
    data = {
        datasets: [{
            data: data,
            backgroundColor: randomColors(data.length)
        }],
        borderWidth: 1,
        labels: labels,
    };

    options = {
        maintainAspectRatio : false,

        title: {
            display: true,
            text: 'First Bloods!',
            fontSize: 30,
            fontColor: 'white'
        },
        legend: {
            labels: {
                fontColor: "white",
                fontSize: 15
            }
        }
    }

    var solvedChart = new Chart(ctx,{
        type: 'pie',
        data: data,
        options: options
    });

 }  

 function topTeams(ctx, data) {
 
    data = {
        datasets: [{
            data: data,
            backgroundColor: randomColors(data.length)
        }],
        borderWidth: 1,
        labels: labels,
    };
    
    options = {
        maintainAspectRatio : false,

        title: {
            display: true,
            text: 'Top Teams',
            fontSize: 30,
            fontColor: 'white'
        },
        legend: {
            labels: {
                fontColor: "white",
                fontSize: 15
            }
        }
    }
    var topTeamsChart = new Chart(ctx,{
        type: 'bar',
        data: data,
        options: options
    });
}
