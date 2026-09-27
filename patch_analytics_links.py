import os
files = ['index.html', 'onboarding.html', 'wellbeing.html']
for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        content = content.replace('href="#" data-path="analytics-and-reports"', 'href="analytics.html" data-path="analytics-and-reports"')
        content = content.replace('data-path="analytics-and-reports" href="#"', 'data-path="analytics-and-reports" href="analytics.html"')
        
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
