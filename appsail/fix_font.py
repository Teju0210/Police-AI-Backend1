import os

def fix_fonts():
    with open('dashboard_template.html', 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace("'Barlow Condensed',sans-serif", "system-ui, sans-serif")
    content = content.replace("'JetBrains Mono',monospace", "ui-monospace, monospace")
    content = content.replace("font-family:'Inter',sans-serif;", "font-family:system-ui, sans-serif;")
    
    with open('dashboard_template.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    fix_fonts()
