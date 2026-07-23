import json
from pathlib import Path

DATA_PATH = Path("output/dashboard_data.json")
TEMPLATE_PATH = Path("dashboard_template.html")
OUT_PATH = Path("output/dashboard.html")

def main():
    if not DATA_PATH.exists():
        raise SystemExit("output/dashboard_data.json not found -- run 2_build_analytics.py first")

    data = DATA_PATH.read_text()
    json.loads(data)  # fail fast if it's not valid JSON

    template = TEMPLATE_PATH.read_text()
    if "__DATA_JSON__" not in template:
        raise SystemExit("Placeholder __DATA_JSON__ not found in template")

    final_html = template.replace("__DATA_JSON__", data)
    OUT_PATH.write_text(final_html)
    print(f"Wrote {OUT_PATH} ({len(final_html)/1024:.1f} KB)")

if __name__ == "__main__":
    main()
