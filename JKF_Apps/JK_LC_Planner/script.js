let events = [];
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

// Load events from JSON
async function loadEvents() {
  const res = await fetch('FullListVersion6.json');  
  events = await res.json();

  populateFilter();
  renderCalendar();
  renderEventList();
}

// new for legend
function renderLegend() {
  const legendBox = document.getElementById('legendItems');
  legendBox.innerHTML = '';

  const services = [...new Set(events.map(e => e.ActivityService))];

  services.forEach(service => {
    // const color = (events.find(e => e.ActivityService === service)?.ActSerColor) || '#000';

    const match = events.find(e => e.ActivityService === service);
    const color = match && match.ActSerColor ? match.ActSerColor : '#000';

    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `<span class="legend-dot" style="background-color:${color}"></span> ${service}`;
    legendBox.appendChild(item);
  });
}

// Populate dropdown filter
function populateFilter() {
  const filter = document.getElementById('eventFilter');
  const types = [...new Set(events.map(e => e.ActivityService))];
  types.forEach(type => {
    const option = document.createElement('option');
    option.value = type;
    option.textContent = type;
    filter.appendChild(option);
  });

  filter.addEventListener('change', () => {
    renderCalendar();
    renderEventList();
  });
}

// Get events for a specific date
function getEventsForDay(dateStr) {
  const selectedType = document.getElementById('eventFilter').value;
  return events.filter(e =>
    e.ActivityDate === dateStr && (selectedType === 'all' || e.ActivityService === selectedType)
  );
}

// Render calendar
function renderCalendar() {
  const calendarDays = document.getElementById('calendar-days');
  calendarDays.innerHTML = '';

  const monthLabel = document.getElementById('monthLabel');
  const monthName = new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long' });
  monthLabel.textContent = `${monthName} ${currentYear}`;

  const firstDay = new Date(currentYear, currentMonth, 1);
  const startDay = firstDay.getDay();
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const totalCells = 42;

  for (let i = 0; i < totalCells; i++) {
    const dayNum = i - startDay + 1;
    const dayDiv = document.createElement('div');
    dayDiv.className = 'day';

    // Weekday/weekend styling
    const dayOfWeek = i % 7;
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      dayDiv.classList.add('weekend');
    } else {
      dayDiv.classList.add('weekday');
    }

    if (i < startDay || dayNum > daysInMonth) {
      dayDiv.classList.add('blank');
      calendarDays.appendChild(dayDiv);
      continue;
    }

    dayDiv.innerHTML = `<span class="day-number">${dayNum}</span>`;
    const date = new Date(currentYear, currentMonth, dayNum);
    const dateStr = date.toLocaleDateString('en-CA');

    const dailyEvents = getEventsForDay(dateStr);

    if (dailyEvents.length > 0) {
      dayDiv.classList.add('has-event');
      dayDiv.addEventListener('click', () => showPopup(dailyEvents));

      const dotsContainer = document.createElement('div');
      dotsContainer.className = 'event-dots';

      const uniqueTypes = [...new Set(dailyEvents.map(e => e.ActivityService))];
      uniqueTypes.forEach(type => {
        const dot = document.createElement('div');
        dot.className = 'event-dot';


       // const color = (dailyEvents.find(e => e.ActivityService === type)?.ActSerColor) || '#000';

        const match = dailyEvents.find(e => e.ActivityService === type);
        const color = match && match.ActSerColor ? match.ActSerColor : '#000';

        dot.style.backgroundColor = color;
        dotsContainer.appendChild(dot);
      });

      dayDiv.appendChild(dotsContainer);
    }

    calendarDays.appendChild(dayDiv);
  }
}

// Render list below calendar
function renderEventList() {
  const list = document.getElementById('eventList');
  list.innerHTML = '';
  const selectedType = document.getElementById('eventFilter').value;

  const heading = document.getElementById('eventListHeading');
  const monthName = new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long' });
  heading.textContent = `Planner for ${monthName} ${currentYear}`;

  const monthEvents = events.filter(e => {
    const eventDate = new Date(e.ActivityDate);
    return (
      eventDate.getMonth() === currentMonth &&
      eventDate.getFullYear() === currentYear &&
      (selectedType === 'all' || e.ActivityService === selectedType)
    );
  });

  monthEvents.forEach(e => {
    const li = document.createElement('li');
    const dotColor = e.ActSerColor || '#000';

// ${e.ActivityService}    to test look

    li.innerHTML = `
      <span class="list-dot" style="background-color: ${dotColor};"></span>
      ${e.ActivityDate} | ${e.ActivityName} 
    `;

    li.addEventListener('click', () => showPopup([e]));
    list.appendChild(li);
  });
}

// Show popup with details
function showPopup(eventArray) {
  const container = document.getElementById('popupEventsContainer');
  container.innerHTML = '';

  eventArray.forEach(event => {
    const div = document.createElement('div');
    div.classList.add('popup-event');
    div.innerHTML = `
      <p><strong>Name:</strong> ${event.ActivityName}</p>
      <p><strong>Time:</strong> ${event.ActivityTime}</p>
      <p><strong>Notes:</strong> ${event.ActivityNotes}</p>
      <p><strong>Cost:</strong> ${event.ActivityCost}</p>
    `;
    container.appendChild(div);
  });

  document.getElementById('eventPopup').classList.remove('hidden');
}

// Close popup
document.getElementById('closePopup').addEventListener('click', () => {
  document.getElementById('eventPopup').classList.add('hidden');
});

// Month navigation
document.getElementById('prevMonth').addEventListener('click', () => {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar();
  renderEventList();
});

document.getElementById('nextMonth').addEventListener('click', () => {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  renderCalendar();
  renderEventList();
});

// Load everything on startup
loadEvents();
