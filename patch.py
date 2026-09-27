import os

files = ['index.html', 'onboarding.html', 'wellbeing.html']
for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # We replace href="#" with the actual pages based on data-path
        content = content.replace('href="#" data-path="onboarding-and-persona"', 'href="onboarding.html" data-path="onboarding-and-persona"')
        content = content.replace('data-path="onboarding-and-persona" href="#"', 'data-path="onboarding-and-persona" href="onboarding.html"')
        
        content = content.replace('href="#" data-path="daily-command-hub"', 'href="index.html" data-path="daily-command-hub"')
        content = content.replace('data-path="daily-command-hub" href="#"', 'data-path="daily-command-hub" href="index.html"')
        
        content = content.replace('href="#" data-path="wellbeing-and-brain-gym"', 'href="wellbeing.html" data-path="wellbeing-and-brain-gym"')
        content = content.replace('data-path="wellbeing-and-brain-gym" href="#"', 'data-path="wellbeing-and-brain-gym" href="wellbeing.html"')
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
