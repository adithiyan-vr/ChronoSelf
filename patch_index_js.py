import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_script = """<script>
    // Load Telemetry on start
    document.addEventListener('DOMContentLoaded', () => {
        const telemetryRaw = localStorage.getItem('chronoself_telemetry');
        if (telemetryRaw) {
            try {
                const telemetry = JSON.parse(telemetryRaw);
                // Update persona in header if element exists
                const personaSpan = document.querySelector('.flex.items-center.gap-space-xs span.font-body-sm.text-on-surface');
                if (personaSpan && telemetry.persona && telemetry.persona.name) {
                    personaSpan.textContent = telemetry.persona.name;
                }
            } catch (e) {
                console.error('Failed to parse telemetry', e);
            }
        }
        loadTasks();
    });

    // Task State Management
    function loadTasks() {
        const tasksRaw = localStorage.getItem('chronoself_tasks');
        if (tasksRaw) {
            try {
                const tasks = JSON.parse(tasksRaw);
                const container = document.getElementById('todoContainer');
                if (container && tasks.length > 0) {
                    container.innerHTML = '';
                    tasks.forEach(t => {
                        const newDiv = document.createElement('div');
                        newDiv.className = "todo-item p-space-sm rounded-lg bg-surface-container-low/70 hover:bg-surface-container-high transition-all flex items-start gap-space-sm cursor-pointer group";
                        newDiv.onclick = function(e) { toggleTask(this, e); };
                        
                        const checkedAttr = t.completed ? 'checked' : '';
                        const textClass = t.completed ? 'line-through opacity-60 text-on-surface' : 'text-primary';
                        
                        newDiv.innerHTML = `
                          <input type="checkbox" ${checkedAttr} class="mt-1 h-4 w-4 rounded bg-surface-container-highest border-0 accent-primary-container cursor-pointer">
                          <div class="flex-1 min-w-0">
                            <span class="font-body-md text-body-md font-semibold ${textClass} block truncate">${t.title}</span>
                            <div class="flex items-center gap-space-xs font-label-numeric text-label-numeric text-on-surface-variant text-body-sm">
                              <span class="text-tertiary-fixed">+${t.xp || 60} ChronoXP</span>
                              <span>• ${t.tag || 'Active Sprint'}</span>
                            </div>
                          </div>
                        `;
                        container.appendChild(newDiv);
                    });
                }
            } catch (e) {}
        }
    }

    function saveTasks() {
        const container = document.getElementById('todoContainer');
        if (!container) return;
        const tasks = [];
        container.querySelectorAll('.todo-item').forEach(item => {
            const checkbox = item.querySelector('input[type="checkbox"]');
            const titleSpan = item.querySelector('span.font-body-md');
            if (checkbox && titleSpan) {
                tasks.push({
                    title: titleSpan.textContent.trim(),
                    completed: checkbox.checked,
                    xp: 60,
                    tag: 'Active Sprint'
                });
            }
        });
        localStorage.setItem('chronoself_tasks', JSON.stringify(tasks));
    }

    // Task check/uncheck logic with visual transition
    function toggleTask(element, event) {
      const checkbox = element.querySelector('input[type="checkbox"]');
      const textSpan = element.querySelector('span.font-body-md');
      
      if (event && event.target !== checkbox) {
        checkbox.checked = !checkbox.checked;
      }
      if (checkbox.checked) {
        textSpan.classList.add('line-through', 'opacity-60');
        textSpan.classList.remove('text-primary');
      } else {
        textSpan.classList.remove('line-through', 'opacity-60');
        textSpan.classList.add('text-primary');
      }
      saveTasks();
    }

    // Dismiss Swap Suggestion
    function dismissSwap(cardId) {
      const card = document.getElementById(cardId);
      if (card) {
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';
        setTimeout(() => {
          card.remove();
        }, 300);
      }
    }

    // Accept Swap Suggestion & dynamically update radar alignment gauge
    function acceptSwap(cardId, gainPoints) {
      const card = document.getElementById(cardId);
      if (!card) return;

      // Pulse feedback effect
      card.classList.add('bg-tertiary-container/30');

      // Update radar proximity UI
      const proxEl = document.getElementById('proximityValue');
      const radarCircle = document.getElementById('radarCircle');
      if (proxEl && radarCircle) {
        let current = parseInt(proxEl.innerText) || 72;
        let nextVal = Math.min(100, current + gainPoints);
        proxEl.innerText = nextVal;

        // Total circumference is ~414.69
        let offset = 414.69 - (414.69 * (nextVal / 100));
        radarCircle.style.strokeDashoffset = offset;
      }

      // Convert card content to active sprint state
      setTimeout(() => {
        card.innerHTML = `
          <div class="flex items-center justify-between p-space-sm rounded-lg bg-tertiary/10 text-tertiary-fixed w-full">
            <div class="flex items-center gap-space-sm">
              <span class="material-symbols-outlined text-[22px]">check_circle</span>
              <div>
                <span class="font-headline-sm text-body-md font-bold block">Swap Activated & Enqueued</span>
                <span class="font-body-sm text-body-sm text-on-surface-variant">Focus Sprint scheduled. Alignment boosted by +${gainPoints}%.</span>
              </div>
            </div>
            <span class="font-label-numeric text-label-numeric text-primary-fixed">+${gainPoints * 10} XP</span>
          </div>
        `;
      }, 350);
    }

    function addNewTaskPrompt() {
      const taskTitle = prompt("Enter high-leverage cognitive task description:");
      if (!taskTitle || !taskTitle.trim()) return;

      const container = document.getElementById('todoContainer');
      const newDiv = document.createElement('div');
      newDiv.className = "todo-item p-space-sm rounded-lg bg-surface-container-low/70 hover:bg-surface-container-high transition-all flex items-start gap-space-sm cursor-pointer group";
      newDiv.onclick = function(e) { toggleTask(this, e); };
      newDiv.innerHTML = `
        <input type="checkbox" class="mt-1 h-4 w-4 rounded bg-surface-container-highest border-0 accent-primary-container cursor-pointer">
        <div class="flex-1 min-w-0">
          <span class="font-body-md text-body-md font-semibold text-primary block truncate">${taskTitle.trim()}</span>
          <div class="flex items-center gap-space-xs font-label-numeric text-label-numeric text-on-surface-variant text-body-sm">
            <span class="text-tertiary-fixed">+60 ChronoXP</span>
            <span>&bull; Manual Enqueue</span>
          </div>
        </div>
      `;
      container.prepend(newDiv);
      saveTasks();
    }

    // Attach quick log buttons
    document.getElementById('quickLogDistractionBtn')?.addEventListener('click', () => {
      const reason = prompt("Log Detected Distraction / Context Friction:", "Quick Slack rabbit hole");
      if (reason) {
        alert("Distraction recorded in gap telemetry. Neural engine re-calibrating next sprint recommendations.");
      }
    });

    document.getElementById('quickNewTaskBtn')?.addEventListener('click', () => {
      addNewTaskPrompt();
    });
</script>"""

# Replace the existing script tag with the new one
content = re.sub(r'<script>\s*// Task check/uncheck logic.*?</script>', new_script, content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
