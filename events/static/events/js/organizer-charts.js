
    // document.addEventListener("DOMContentLoaded", function () {
    //     const ticketSalesCtx = document.getElementById("ticketSalesChart").getContext("2d");
    //     const revenueCtx = document.getElementById("revenueChart").getContext("2d");
    //     const categoryCtx = document.getElementById("categoryChart").getContext("2d");

    //     // Data from Django
    //     const eventLabels = {{ event_labels|safe }};
    //     const salesData = {{ sales_data|safe }};
    //     const revenueData = {{ revenue_data|safe }};
    //     const categoryLabels = {{ category_labels|safe }};
    //     const categorySales = {{ category_sales|safe }};

    //     // Ticket Sales Chart
    //     new Chart(ticketSalesCtx, {
    //         type: "bar",
    //         data: {
    //             labels: eventLabels,
    //             datasets: [{
    //                 label: "Tickets Sold",
    //                 data: salesData,
    //                 backgroundColor: "rgba(54, 162, 235, 0.6)"
    //             }]
    //         }
    //     });

    //     // Revenue Chart
    //     new Chart(revenueCtx, {
    //         type: "line",
    //         data: {
    //             labels: eventLabels,
    //             datasets: [{
    //                 label: "Revenue ($)",
    //                 data: revenueData,
    //                 borderColor: "rgba(255, 99, 132, 1)",
    //                 backgroundColor: "rgba(255, 99, 132, 0.2)",
    //                 fill: true
    //             }]
    //         }
    //     });

    //     // Attendee Demographics Chart
    //     new Chart(categoryCtx, {
    //         type: "pie",
    //         data: {
    //             labels: categoryLabels,
    //             datasets: [{
    //                 label: "Ticket Sales by Category",
    //                 data: categorySales,
    //                 backgroundColor: [
    //                     "rgba(255, 99, 132, 0.6)",
    //                     "rgba(54, 162, 235, 0.6)",
    //                     "rgba(255, 206, 86, 0.6)",
    //                     "rgba(75, 192, 192, 0.6)",
    //                     "rgba(153, 102, 255, 0.6)",
    //                     "rgba(255, 159, 64, 0.6)"
    //                 ]
    //             }]
    //         }
    //     });
    // });

    