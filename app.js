const CATEGORY_COLORS = {
    'Sleep': 'var(--cat-sleep)',
    'Study': 'var(--cat-study)',
    'Screens': 'var(--cat-screens)',
    'Exercise': 'var(--cat-exercise)',
    'Social': 'var(--cat-social)',
    'Other': 'var(--cat-other)'
};

const IDEAL_HOURS = {
    'Sleep': 8,
    'Study': 6,
    'Screens': 2,
    'Exercise': 1,
    'Social': 2,
    'Other': 5
};

const PRESETS = {
    'study': [
        { cat: 'Sleep', hours: 8 },
        { cat: 'Study', hours: 8 },
        { cat: 'Screens', hours: 2 },
        { cat: 'Exercise', hours: 1 },
        { cat: 'Social', hours: 2 },
        { cat: 'Other', hours: 3 }
    ],
    'work': [
        { cat: 'Sleep', hours: 7 },
        { cat: 'Study', hours: 9 },
        { cat: 'Screens', hours: 1 },
        { cat: 'Exercise', hours: 1 },
        { cat: 'Social', hours: 3 },
        { cat: 'Other', hours: 3 }
    ],
    'rest': [
        { cat: 'Sleep', hours: 9 },
        { cat: 'Screens', hours: 4 },
        { cat: 'Exercise', hours: 2 },
        { cat: 'Social', hours: 5 },
        { cat: 'Other', hours: 4 }
    ]
};

let logs = [];
let initialLoad = true;

function init() {
    // Set date
    const dateOptions = { weekday: 'short', month: 'short', day: 'numeric' };
    document.getElementById('current-date').textContent = new Date().toLocaleDateString('en-US', dateOptions);

    // Event listeners
    document.getElementById('log-form').addEventListener('submit', handleLogSubmit);
    document.getElementById('reset-btn').addEventListener('click', resetDay);
    
    document.querySelectorAll('.quick-btn[data-preset]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const presetName = e.target.getAttribute('data-preset');
            loadPreset(presetName);
        });
    });

    loadState();
    
    // Set current hour hand on the dial
    updateCurrentHourHand();
    setInterval(updateCurrentHourHand, 60000); // Update every minute

    renderLegend();
    updateUI();
    
    initialLoad = false;
}

function handleLogSubmit(e) {
    e.preventDefault();
    const cat = document.getElementById('category').value;
    const hours = parseFloat(document.getElementById('hours').value);
    
    if (hours > 0) {
        logs.push({ cat, hours });
        document.getElementById('hours').value = '';
        saveState();
        updateUI();
    }
}

function loadPreset(name) {
    logs = [...PRESETS[name]];
    saveState();
    updateUI();
}

function resetDay() {
    logs = [];
    saveState();
    updateUI();
}

function saveState() {
    localStorage.setItem('timelens_logs', JSON.stringify(logs));
}

function loadState() {
    const saved = localStorage.getItem('timelens_logs');
    if (saved) {
        logs = JSON.parse(saved);
    }
}

function updateUI() {
    renderLogList();
    updateDayDial();
    renderBars();
    generateInsight();
}

function renderLogList() {
    const list = document.getElementById('log-list');
    list.innerHTML = '';
    
    const totals = getCategoryTotals();
    
    for (const [cat, hours] of Object.entries(totals)) {
        if (hours > 0) {
            const li = document.createElement('li');
            li.innerHTML = `
                <span class="color-dot" style="background-color: ${CATEGORY_COLORS[cat]}"></span>
                <span class="log-cat">${cat}</span>
                <span class="log-hours">${hours.toFixed(1)}h</span>
            `;
            list.appendChild(li);
        }
    }
}

function getCategoryTotals() {
    const totals = {
        'Sleep': 0, 'Study': 0, 'Screens': 0, 'Exercise': 0, 'Social': 0, 'Other': 0
    };
    logs.forEach(log => {
        if (totals[log.cat] !== undefined) totals[log.cat] += log.hours;
    });
    return totals;
}

function updateDayDial() {
    const totals = getCategoryTotals();
    const totalLogged = Object.values(totals).reduce((a, b) => a + b, 0);
    
    // Update hero stat (biggest category)
    let maxCat = '';
    let maxHours = -1;
    for (const [cat, hours] of Object.entries(totals)) {
        if (hours > maxHours && hours > 0) {
            maxHours = hours;
            maxCat = cat;
        }
    }

    const statTime = document.querySelector('.stat-time');
    const statCaption = document.querySelector('.stat-caption');
    
    if (totalLogged > 0) {
        const hrs = Math.floor(maxHours);
        const mins = Math.round((maxHours - hrs) * 60);
        statTime.textContent = `${hrs}h${mins > 0 ? ' ' + mins + 'm' : ''}`;
        statCaption.textContent = `on ${maxCat.toLowerCase()} today`;
    } else {
        statTime.textContent = '0h 0m';
        statCaption.textContent = 'logged today';
    }

    // Render SVG Segments
    // 24 segments, radius 40. Circumference = 2 * PI * 40 = 251.3274
    const radius = 40;
    const circumference = 2 * Math.PI * radius;
    const dialSegments = document.getElementById('dialSegments');
    dialSegments.innerHTML = ''; // clear

    let currentOffset = 0;
    
    const displayData = [];
    for (const [cat, hours] of Object.entries(totals)) {
        if (hours > 0) {
            displayData.push({ cat, hours });
        }
    }

    const disableAnimation = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    displayData.forEach((item, index) => {
        const hoursToShow = Math.min(item.hours, Math.max(0, 24 - (currentOffset / (circumference / 24))));
        if (hoursToShow <= 0) return;

        const segmentLength = (hoursToShow / 24) * circumference;
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        
        circle.setAttribute("cx", "50");
        circle.setAttribute("cy", "50");
        circle.setAttribute("r", radius);
        circle.setAttribute("class", "dial-segment");
        circle.setAttribute("stroke", CATEGORY_COLORS[item.cat]);
        
        // Dasharray: segmentLength, rest of circumference
        circle.setAttribute("stroke-dasharray", `0 ${circumference}`);
        circle.setAttribute("stroke-dashoffset", -currentOffset);
        
        dialSegments.appendChild(circle);

        if (initialLoad && !disableAnimation) {
            setTimeout(() => {
                circle.setAttribute("stroke-dasharray", `${segmentLength} ${circumference}`);
            }, index * 200 + 100);
        } else {
            setTimeout(() => {
                circle.setAttribute("stroke-dasharray", `${segmentLength} ${circumference}`);
            }, 10);
        }

        currentOffset += segmentLength;
    });
}

function updateCurrentHourHand() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const totalHours = hours + (minutes / 60);
    
    // Hand rotates based on 24-hour clock. 360 / 24 = 15 degrees per hour.
    const degrees = (totalHours / 24) * 360;
    
    const hand = document.getElementById('currentHourHand');
    hand.style.transform = `rotate(${degrees}deg)`;
}

function renderLegend() {
    const legend = document.getElementById('chart-legend');
    legend.innerHTML = '';
    
    Object.keys(CATEGORY_COLORS).forEach(cat => {
        const item = document.createElement('div');
        item.className = 'legend-item';
        item.innerHTML = `
            <span class="color-dot" style="background-color: ${CATEGORY_COLORS[cat]}"></span>
            ${cat}
        `;
        legend.appendChild(item);
    });
}

function renderBars() {
    const container = document.getElementById('bars-container');
    container.innerHTML = '';
    const totals = getCategoryTotals();

    Object.keys(IDEAL_HOURS).forEach(cat => {
        const actual = totals[cat];
        const ideal = IDEAL_HOURS[cat];
        const isOver = actual > ideal;
        const percent = Math.min((actual / Math.max(ideal, 1)) * 100, 100);
        
        const warning = isOver ? '<span class="warning-icon">⚠</span>' : '';
        
        const div = document.createElement('div');
        div.className = 'bar-container';
        div.innerHTML = `
            <div class="bar-header">
                <span>${cat}</span>
                <span class="bar-stats">${actual.toFixed(1)} / ${ideal}h ${warning}</span>
            </div>
            <div class="bar-track">
                <div class="bar-fill ${isOver ? 'over-budget' : ''}" style="width: ${initialLoad ? '0%' : percent + '%'}; background-color: ${isOver ? 'var(--flag-red)' : CATEGORY_COLORS[cat]}"></div>
            </div>
        `;
        container.appendChild(div);

        if (initialLoad) {
            setTimeout(() => {
                const fill = div.querySelector('.bar-fill');
                fill.style.width = percent + '%';
            }, 300);
        }
    });
}

function generateInsight() {
    const card = document.getElementById('insight-card');
    const content = card.querySelector('.insight-content');
    const totals = getCategoryTotals();
    const totalLogged = Object.values(totals).reduce((a, b) => a + b, 0);

    card.style.opacity = '0';
    
    setTimeout(() => {
        card.classList.remove('warning');
        
        if (totalLogged === 0) {
            content.textContent = "Log some activities to see insights about your day.";
        } else if (totals['Screens'] > IDEAL_HOURS['Screens']) {
            card.classList.add('warning');
            content.textContent = `You planned ${IDEAL_HOURS['Screens']}h of screens but logged ${totals['Screens']}h. Try a 25-min walk before your next scroll break.`;
        } else if (totals['Sleep'] < 7 && totalLogged >= 12) {
            card.classList.add('warning');
            content.textContent = `You've only logged ${totals['Sleep']}h of sleep. Consider going to bed earlier tonight.`;
        } else if (totals['Exercise'] === 0 && totalLogged >= 10) {
            content.textContent = "No Exercise logged today. Even a 15-minute walk makes a difference.";
        } else if (totals['Study'] > IDEAL_HOURS['Study']) {
            content.textContent = `You spent ${totals['Study']}h working/studying. Make sure to take breaks to avoid burnout!`;
        } else if (totals['Social'] < IDEAL_HOURS['Social'] && totalLogged >= 12) {
            content.textContent = "You haven't spent much time socializing. Reach out to a friend!";
        } else {
            content.textContent = "Your day is looking balanced according to your ideal targets. Keep it up!";
        }
        
        card.style.opacity = '1';
    }, 150);
}

document.addEventListener('DOMContentLoaded', init);
