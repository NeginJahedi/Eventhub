document.addEventListener("DOMContentLoaded", function () {
    let currentOrder = {}; // Store sorting order per column

    function renderTable() {
        let tableBody = document.querySelector("tbody");
        tableBody.innerHTML = ""; // Clear table before rendering

        tickets.forEach(ticket => {
            let row = `
                <tr>
                    <td>${ticket.attender}</td>
                    <td>${ticket.event}</td>
                    <td>${ticket.quantity}</td>
                    <td>${ticket.purchased_on}</td>
                    <td>
                        <form method="POST" action="">
                            <button type="submit" class="btn btn-danger btn-sm">Refund</button>
                        </form>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }

    function sortTickets(column) {
        // Toggle sorting order
        currentOrder[column] = currentOrder[column] === "asc" ? "desc" : "asc";
        let orderFactor = currentOrder[column] === "asc" ? 1 : -1;

        tickets.sort((a, b) => {
            let valA = a[column];
            let valB = b[column];

            // Convert date strings to Date objects for correct sorting
            if (column === "purchased_on") {
                valA = new Date(valA);
                valB = new Date(valB);
            }

            // Numeric sorting
            if (!isNaN(valA) && !isNaN(valB)) {
                return (valA - valB) * orderFactor;
            } 
            // String sorting
            else {
                return valA.localeCompare(valB) * orderFactor;
            }
        });

        renderTable();
    }

    // Add event listeners to sortable table headers
    document.querySelectorAll(".sortable").forEach(header => {
        header.addEventListener("click", function () {
            let column = this.dataset.column;
            sortTickets(column);

            // Update arrow indicator
            document.querySelectorAll(".sortable i").forEach(icon => icon.className = "fas fa-sort");
            let icon = this.querySelector("i");
            icon.className = currentOrder[column] === "asc" ? "fas fa-sort-up" : "fas fa-sort-down";
        });
    });

    renderTable(); // Initial table render
});



//sorting in server via APUI call
// document.addEventListener("DOMContentLoaded", function () {
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
//     document.querySelectorAll(".sort").forEach((link) => {
//         link.addEventListener("click", function (event) {
//             event.preventDefault();
//             let column = this.getAttribute("data-column");
//             let order = this.getAttribute("data-order");
//             console.log(`/tickets/sort?column=${column}&order=${order}`)
            // fetch(`/tickets/sort?column=${column}&order=${order}`,{
            //     method: 'POST',
            //     headers: { 
            //         'Content-Type': 'application/json',
            //         'X-CSRFToken': csrftoken 
            //     },
            //     body: JSON.stringify({ tickets: tickets })
            // })
            //     .then(res => res.json())
            //     .then((response) => response.json())
            //     .then((data) => {
            //         let tableBody = document.querySelector("tbody");
            //         tableBody.innerHTML = ""; 

            //         data.tickets.forEach((ticket) => {
            //             let row = `
            //                 <tr>
            //                     <td>${ticket.attender}</td>
            //                     <td>${ticket.event}</td>
            //                     <td>${ticket.quantity}</td>
            //                     <td>${ticket.purchased_on}</td>
            //                     <td>
            //                         <form method="POST" action="">
            //                             <button type="submit" class="btn btn-danger btn-sm">Refund</button>
            //                         </form>
            //                     </td>
            //                 </tr>
            //             `;
            //             tableBody.innerHTML += row;
            //         });

            //         // Toggle sorting order
            //         let newOrder = order === "asc" ? "desc" : "asc";
            //         this.setAttribute("data-order", newOrder);
            //     })
            //     .catch(error => console.error('Error:', error));
//         });
//     });
// });
