document.addEventListener('DOMContentLoaded', function(){
    document.querySelector('#showAllEvents').addEventListener('click', () => {
        document.querySelector('#searchResults').style.display = 'none';
        document.querySelector('#allEvents').style.display = 'flex';
    });
    
    let search_btn = document.querySelector("#search-btn");
    
    
    if (search_btn){
        search_btn.addEventListener('click', function(event) {
            console.log("search button was clicked.")
            const search_keyword = document.querySelector("#searchkeyword").value;
            const category = document.querySelector("#category").value;
            const start_date = document.querySelector("#startDateFilter").value;
            const end_date = document.querySelector("#endDateFilter").value;
            const min_price = document.querySelector("#minPrice").value;
            const max_price = document.querySelector("#maxPrice").value;
            const location = document.querySelector("#location").value;


            const data = {
                search_keyword: search_keyword,
                category: category,
                start_date: start_date,
                end_date: end_date,
                min_price: min_price,
                max_price: max_price,
                location: location,
            };
            
            // Send data using Fetch API
            fetch(`events/search`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",  // Indicate that we're sending JSON data
                    "X-CSRFToken": getCSRFToken()  // Include CSRF token (for Django)
                },  
                body: JSON.stringify(data) 
            })
            .then(response => response.json())
            .then(data => {
                console.log("Success:", data);  // Handle success
            
                const resultsContainer = document.querySelector("#searchResults");

                // Clear old results
                resultsContainer.innerHTML = "";
                resultsContainer.style.display ='block';

                // Check if results exist
                if (data.results.length === 0) {
                    resultsContainer.innerHTML = "<p>No events found.</p>";
                    return;
                }

                // Create and append new results
                data.results.forEach(event => {
                    const eventElement = document.createElement("div");
                    eventElement.classList.add("event-card"); 
                    eventElement.classList.add("col-md-4");
                    eventElement.classList.add("mb-3");
                    eventElement.innerHTML = `
                    
                    <a href="/Events/${event.id}">
                      <div class="card event-card text-white">
                        <img src="${event.image_url}" class="card-img" alt="Event Image">
                        <div class="card-img-overlay d-flex flex-column justify-content-between">
                          <h5 class="card-title">${event.title}</h5>
                          <div class="event-details text-white">
                            <span><i class="bi bi-calendar"></i> ${event.date}</span>
                            <span><i class="bi bi-geo-alt"></i> ${event.location}</span>
                          </div>
                        </div>
                      </div>
                    </a>
                  
                    `;
                    resultsContainer.appendChild(eventElement);
                    document.querySelector('#searchResults').style.display = 'block';
                    document.querySelector('#allEvents').style.display = 'none';
                });
            })
            .catch(error => {
                console.error("Error:", error);  // Handle errors
            });
            
            // Function to get CSRF token from cookies (needed for Django)
            function getCSRFToken() {
                let cookieValue = null;
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.startsWith("csrftoken=")) {
                        cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                        break;
                    }
                }
                return cookieValue;
            }
            
            
                
        });
    }
});







