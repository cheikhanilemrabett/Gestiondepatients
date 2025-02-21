document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('statsChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Patients', 'Doctors', 'Appointments'],
            datasets: [{
                label: 'Statistics',
                data: [total_patients, total_doctors, total_appointments],
                backgroundColor: ['#ff6384', '#36a2eb', '#ffce56'],
                borderColor: ['#d32f2f', '#1565c0', '#ff9800'],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
