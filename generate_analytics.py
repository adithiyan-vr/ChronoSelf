import os

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract head and header
head_end = html.find('</header>') + len('</header>')
head_and_header = html[:head_end]

# Extract footer
footer_start = html.find('<footer')
footer = html[footer_start:]

# Fix navigation active state in header
# Remove active state from daily command hub
head_and_header = head_and_header.replace('aria-current="page" class="px-space-md py-space-sm rounded-lg transition-all duration-200 bg-surface-container-high text-primary font-headline-sm text-body-md" data-path="daily-command-hub"', 'class="px-space-md py-space-sm rounded-lg text-on-surface-variant font-body-md text-body-md transition-all duration-200 hover:bg-surface-container-high hover:text-on-surface" data-path="daily-command-hub"')
# Add active state to analytics
head_and_header = head_and_header.replace('class="px-space-md py-space-sm rounded-lg text-on-surface-variant font-body-md text-body-md transition-all duration-200 hover:bg-surface-container-high hover:text-on-surface" data-path="analytics-and-reports"', 'aria-current="page" class="px-space-md py-space-sm rounded-lg transition-all duration-200 bg-surface-container-high text-primary font-headline-sm text-body-md" data-path="analytics-and-reports"')

# Fix links
head_and_header = head_and_header.replace('href="#" data-path="analytics-and-reports"', 'href="analytics.html" data-path="analytics-and-reports"')
head_and_header = head_and_header.replace('data-path="analytics-and-reports" href="#"', 'data-path="analytics-and-reports" href="analytics.html"')

main_content = """
<main class="w-full pt-20 bg-background">
  <div class="flex flex-col w-full px-margin py-space-lg gap-space-lg max-w-7xl mx-auto">
    <!-- Header Stream / Telemetry Context -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-space-md p-space-lg rounded-xl bg-surface-container/70 backdrop-blur-xl shadow-xl">
      <div class="flex flex-col gap-space-xs">
        <div class="flex items-center gap-space-sm">
          <span class="px-space-sm py-0.5 rounded-full bg-primary-container/20 text-primary-fixed text-label-caps font-label-caps tracking-wider uppercase">Telemetry Engine</span>
        </div>
        <h1 class="font-headline-lg text-headline-lg text-primary tracking-tight">Analytics &amp; Reports</h1>
        <p class="font-body-md text-body-md text-on-surface-variant max-w-2xl">
          Historical performance and deep cognitive analytics based on your Ideal Self archetype.
        </p>
      </div>
    </div>
    
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-space-lg">
      <!-- Task Analytics -->
      <div class="p-space-lg rounded-xl bg-surface-container/70 backdrop-blur-xl shadow-xl flex flex-col gap-space-md">
        <div class="flex items-center justify-between">
          <h2 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
            <span class="material-symbols-outlined text-primary-container">analytics</span>
            Task Completion Velocity
          </h2>
        </div>
        <div class="flex items-end gap-space-md h-48 border-b border-surface-container-highest pb-2 px-2" id="barChartContainer">
          <!-- Bars will be inserted via JS -->
        </div>
        <div class="flex justify-between font-label-numeric text-label-numeric text-outline mt-2" id="barChartLabels">
          <!-- Labels will be inserted via JS -->
        </div>
      </div>
      
      <!-- Stats Overview -->
      <div class="p-space-lg rounded-xl bg-surface-container/70 backdrop-blur-xl shadow-xl flex flex-col gap-space-md">
         <h2 class="font-headline-sm text-headline-sm text-on-surface flex items-center gap-2">
            <span class="material-symbols-outlined text-tertiary-fixed">query_stats</span>
            ChronoXP Metrics
          </h2>
          
          <div class="grid grid-cols-2 gap-space-md h-full">
             <div class="p-space-md rounded-lg bg-surface-container-low/70 flex flex-col justify-center">
               <span class="font-label-caps text-label-caps text-outline uppercase">Total XP Earned</span>
               <span class="font-headline-lg text-primary" id="totalXpDisplay">0</span>
             </div>
             <div class="p-space-md rounded-lg bg-surface-container-low/70 flex flex-col justify-center">
               <span class="font-label-caps text-label-caps text-outline uppercase">Completed Tasks</span>
               <span class="font-headline-lg text-tertiary" id="completedTasksDisplay">0</span>
             </div>
             <div class="p-space-md rounded-lg bg-surface-container-low/70 flex flex-col justify-center">
               <span class="font-label-caps text-label-caps text-outline uppercase">Pending Tasks</span>
               <span class="font-headline-lg text-error" id="pendingTasksDisplay">0</span>
             </div>
             <div class="p-space-md rounded-lg bg-surface-container-low/70 flex flex-col justify-center">
               <span class="font-label-caps text-label-caps text-outline uppercase">Persona Match</span>
               <span class="font-headline-lg text-secondary-fixed" id="personaMatchDisplay">N/A</span>
             </div>
          </div>
      </div>
    </div>
  </div>
  
  <script>
    document.addEventListener("DOMContentLoaded", () => {
        // Load tasks
        const tasksRaw = localStorage.getItem('chronoself_tasks');
        let completed = 0;
        let pending = 0;
        let totalXp = 0;
        
        if (tasksRaw) {
            try {
                const tasks = JSON.parse(tasksRaw);
                tasks.forEach(t => {
                    if(t.completed) {
                        completed++;
                        totalXp += (t.xp || 60);
                    } else {
                        pending++;
                    }
                });
            } catch(e) {}
        }
        
        document.getElementById('totalXpDisplay').textContent = totalXp;
        document.getElementById('completedTasksDisplay').textContent = completed;
        document.getElementById('pendingTasksDisplay').textContent = pending;
        
        // Load persona
        const telemetryRaw = localStorage.getItem('chronoself_telemetry');
        if (telemetryRaw) {
            try {
                const telemetry = JSON.parse(telemetryRaw);
                if(telemetry.persona && telemetry.persona.efficiency) {
                    document.getElementById('personaMatchDisplay').textContent = telemetry.persona.efficiency + '%';
                }
            } catch(e) {}
        }
        
        // Render fake chart for aesthetics
        const container = document.getElementById('barChartContainer');
        const labels = document.getElementById('barChartLabels');
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
        const values = [45, 60, 30, 80, 50, 90, 70]; // Random heights
        
        days.forEach((day, i) => {
            // bar
            const div = document.createElement('div');
            div.className = 'w-full bg-primary-container/20 hover:bg-primary-container rounded-t-sm transition-all duration-300 relative group';
            div.style.height = values[i] + '%';
            
            // tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute -top-8 left-1/2 -translate-x-1/2 bg-surface-container-highest text-on-surface px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity';
            tooltip.textContent = values[i] * 10 + ' XP';
            div.appendChild(tooltip);
            
            container.appendChild(div);
            
            // label
            const lbl = document.createElement('div');
            lbl.textContent = day;
            lbl.className = 'flex-1 text-center';
            labels.appendChild(lbl);
        });
    });
  </script>
</main>
"""

analytics_html = head_and_header + main_content + footer

with open('analytics.html', 'w', encoding='utf-8') as f:
    f.write(analytics_html)
