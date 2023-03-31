function formatDate(date) {
    const yyyy = date.getFullYear();
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    return yyyy + '/' + mm + '/' + dd;
  }
  
  function filterEventsByDate(events, currentDate) {
    return events.filter(event => {
      const eventDate = new Date(event.date + ' ' + event.time);
      return formatDate(eventDate) === currentDate;
    });
  }
  
  async function fetchEvents() {
    try {
      const response = await fetch('/api/events'); // Replace with your API endpoint
      let events = await response.json();
      const now = new Date();
      const currentDate = formatDate(now);
      events = filterEventsByDate(events, currentDate);
      const eventTable = document.querySelector(".table tbody");
      eventTable.innerHTML = '';
    
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  }
  
  function highlightCurrentTime() {
    const now = new Date();
    const currentDate = formatDate(now);
    const currentTime = formatTime(now);
    const eventRows = document.querySelectorAll(".event-row");
  
    eventRows.forEach(row => {
      row.classList.remove("bg-primary", "text-white");
  
      const eventDateTime = row.getAttribute("data-datetime");
      const eventDate = new Date(eventDateTime);
  
      if (formatDate(eventDate) === currentDate && formatTime(eventDate) === currentTime) {
        row.classList.add("bg-primary", "text-white");
      }
    });
  }
  
  
  
  async function fetchEvents() {
    try {
      const response = await fetch('/api/events'); // Replace with your API endpoint
      const events = await response.json();
      const eventTable = document.querySelector(".table tbody");
      eventTable.innerHTML = '';
  
      for (const event of events) {
        const eventRow = `
          <tr class="event-row" data-time="${event.time}">
            <td class="w-30">
              <div class="d-flex px-2 py-1 align-items-center">
                <div>
                  <img src="./assets/img/icons/flags/${event.flag}.png" alt="Country flag">
                </div>
                <div class="ms-4">
                  <p class="text-xs font-weight-bold mb-0">Topic</p>
                  <h6 class="text-sm mb-0">${event.topic}</h6>
                </div>
              </div>
            </td>
            <td>
              <div class="text-center">
                <p class="text-xs font-weight-bold mb-0">Time</p>
                <h6 class="text-sm mb-0">${event.time}</h6>
              </div>
            </td>
            <td>
              <div class="text-center">
                <p class="text-xs font-weight-bold mb-0">Speaker</p>
                <h6 class="text-sm mb-0">${event.speaker}</h6>
              </div>
            </td>
            <td class="align-middle text-sm">
              <div class="col text-center">
                <p class="text-xs font-weight-bold mb-0">Room</p>
                <h6 class="text-sm mb-0">${event.room}</h6>
                </div>
            </td>
            </tr>`;
        eventTable.insertAdjacentHTML('beforeend', eventRow);
        }
        highlightCurrentTime();
    } catch (error) {
        console.error("Error fetching events:", error);
        }
    }
    
    document.addEventListener('DOMContentLoaded', fetchEvents);
    setInterval(highlightCurrentTime, 60 * 1000);