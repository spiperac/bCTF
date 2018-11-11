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
            text: 'Solved',
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
