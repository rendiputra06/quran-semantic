
$(document).ready(function() {
    // Ambil data evaluasi dari backend
    $.get(api_url+'/get_evaluation/0', function(data) {
        // Siapkan data untuk grafik
        let labels = [];
        let precisionData = [];
        let recallData = [];
        let f1_scoreData = [];
        let mapData = [];
        let ndcgData = [];

        // Iterasi melalui data yang diterima
        data.forEach(function(evaluation) {
            labels.push(evaluation.query);
            precisionData.push(evaluation.metrics.precision);
            recallData.push(evaluation.metrics.precision);
            f1_scoreData.push(evaluation.metrics.precision);
            mapData.push(evaluation.metrics.precision);
            ndcgData.push(evaluation.metrics.precision);
        });

        // Menampilkan grafik
        var ctx = document.getElementById('evaluationChart').getContext('2d');
        var precisionChart = new Chart(ctx, {
            type: 'bar',  // Jenis grafik: Bar Chart
            data: {
                labels: labels,  // Label untuk sumbu x (nama query)
                datasets: [{
                    label: 'Precision',
                    data: precisionData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Recall',
                    data: recallData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(75, 192, 192, 0.2)', borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'F1 Score',
                    data: f1_scoreData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(153, 102, 255, 0.2)', borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                },
                {
                    label: 'map',
                    data: mapData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(255, 206, 86, 0.2)', borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                },
                {
                    label: 'ndcg',
                    data: ndcgData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(255, 99, 132, 0.2)', borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
            ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
    $.get(api_url+'/get_evaluation/1', function(data) {
        // Siapkan data untuk grafik
        let labels = [];
        let precisionData = [];
        let recallData = [];
        let f1_scoreData = [];
        let mapData = [];
        let ndcgData = [];

        // Iterasi melalui data yang diterima
        data.forEach(function(evaluation) {
            labels.push(evaluation.query);
            precisionData.push(evaluation.metrics.precision);
            recallData.push(evaluation.metrics.precision);
            f1_scoreData.push(evaluation.metrics.precision);
            mapData.push(evaluation.metrics.precision);
            ndcgData.push(evaluation.metrics.precision);
        });

        // Menampilkan grafik
        var ctx = document.getElementById('semanticChart').getContext('2d');
        var precisionChart = new Chart(ctx, {
            type: 'bar',  // Jenis grafik: Bar Chart
            data: {
                labels: labels,  // Label untuk sumbu x (nama query)
                datasets: [{
                    label: 'Precision',
                    data: precisionData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Recall',
                    data: recallData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(75, 192, 192, 0.2)', borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'F1 Score',
                    data: f1_scoreData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(153, 102, 255, 0.2)', borderColor: 'rgba(153, 102, 255, 1)',
                    borderWidth: 1
                },
                {
                    label: 'map',
                    data: mapData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(255, 206, 86, 0.2)', borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                },
                {
                    label: 'ndcg',
                    data: ndcgData.flat(),  // Mengubah array 2D menjadi 1D
                    backgroundColor: 'rgba(255, 99, 132, 0.2)', borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
            ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });
});