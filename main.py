from flask import Flask, render_template, jsonify
import json
import os
import re

app = Flask(__name__)

# Путь к data.json — рядом с app.py
DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")


def load_catalog():
    """Читает data.json и возвращает список аниме."""
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    """Главная (лендинг)."""
    return render_template("index.html")


@app.route("/app")
def app_page():
    """Основной экран приложения."""
    return render_template("app.html")


@app.route("/progress")
def progress():
    """Страница прогресса: статистика по каталогу."""
    items = load_catalog()
    total = len(items)
    by_decade = {}
    for it in items:
        m = str(it.get("year") or "")
        match = re.search(r"\d{4}", m)
        if match:
            decade = int(match.group(0)) // 10 * 10
            by_decade[decade] = by_decade.get(decade, 0) + 1
    by_decade = dict(sorted(by_decade.items(), reverse=True))
    return render_template("progress.html", total=total, by_decade=by_decade)


@app.route("/api/catalog")
def api_catalog():
    """JSON-эндпоинт для JS. Отдаёт каталог из data.json."""
    return jsonify(load_catalog())


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000)) # Render даст свой порт, локально будет 5000
    app.run(host="0.0.0.0", port=port) 