document.addEventListener("DOMContentLoaded", function () {
  const tableBody = document.getElementById("eventstable");
  const filterSelect = document.querySelector(".filter"); 
  const searchKeyword = document.querySelector("#searchinput"); 

  let selectedStatus = "";
  let searchQuery = "";

  function fetchAndUpdate() {
    const url = new URL("dashboard/organizer/filter", window.location.origin);
    if (selectedStatus) url.searchParams.set("status", selectedStatus);
    if (searchQuery) url.searchParams.set("q", searchQuery);

    fetch(url)
      .then(response => response.json())
      .then(data => {
        // console.log("API response:", data);
        updateTable(data); 
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }

  filterSelect.addEventListener("change", function(event) {
    event.preventDefault();
    selectedStatus = event.target.value;
    // console.log("Filter selected:", selectedStatus);
    fetchAndUpdate();
  });

  searchKeyword.addEventListener("keyup", function(e) {
    if (e.key === "Enter") {
      e.preventDefault();
      searchQuery = e.target.value.trim();
      // console.log("Search query:", searchQuery);
      fetchAndUpdate();
    }
  });











    function updateTable(data) {
        tableBody.innerHTML = "";  // Clear existing rows
        const events = data.results;
        if (events.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="6" class="text-center">No events found</td></tr>`;
            return;
        }

        events.forEach(event => {
            let row = document.createElement("tr");

            //Format the date properly
            let eventDate = new Date(event.date).toLocaleDateString("en-US", { 
                month: "short", day: "numeric", year: "numeric" 
            });
            

            // Determine badge color based on status
            let statusBadge = "";
            if (event.status === "sold_out") {
                statusBadge = `<span class="badge text-warning">${event.status_display}</span>`;
            } else if (event.status === "canceled") {
                statusBadge = `<span class="badge text-danger">${event.status_display}</span>`;
            } else if (event.status === "active") {
                statusBadge = `<span class="badge text-success">${event.status_display}</span>`;
            } else {
                statusBadge = `<span class="badge text-secondary">${event.status_display}</span>`;
            }
            
            row.innerHTML = `
                <td>
                    <a href="/events/${event.id}" class="text-decoration-none">${event.title}</a>
                </td>
                <td>${eventDate}</td>
                <td>${statusBadge}</td>
                <td>${event.tickets_sold}</td>
                <td>$${event.revenue}</td>
                <td>
                    <div>
                        <a class="btn btn-sm btn-outline-secondary" href="/dashboard/organizer/edit/${event.id}">
                            Manage
                        </a>
                    </div>
                </td>
                <td>
                <div>
                    <a class="btn btn-sm btn-outline-secondary"
                            href="/dashboard/organizer/${event.id}/tickets">
                        Tickets
                    </a>
                </div>
            </td>
            `;

            tableBody.appendChild(row);
        });
    }
});
