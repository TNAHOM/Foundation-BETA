//var xValues = [10, 20, 30, 40, 50,60,70,80,90,100];
//var yValues = [0, 0, 2, 5, 3, 22, 126, 174, 101, 31];
//
//new Chart("myChart", {
//  type: "line",
//  data: {
//    labels: xValues,
//    datasets: [{
//      fill: false,
//      lineTension: 0,
//      backgroundColor: "rgba(0,0,255,1.0)",
//      borderColor: "rgba(0,0,255,0.1)",
//      data: yValues
//    }]
//  },
//  options: {
//    legend: {display: false},
//    scales: {
//      yAxes: [{ticks: {min: 0, max:10}}],
//    }
//  }
//});
//

const labels = [0, 20, 30, 40, 50, 60,70, 80, 90, 100];

const data = {
  labels: labels,
  datasets:[{
    label:'first',
    borderColor: 'rgb(255, 99, 132)',
    backgroundColor: 'rgb(255, 99, 132)',
    data: [0, 20, 34, 21, 13, 68, 104, 150, 110, 21],
  }]
};

const config = {
  type: 'line',
  data,
  options:{
    plugins: {
      legend: {
        display: false
      }
    }
  }
};

var myChart = new Chart(
  document.getElementById('myChart'), config
);
