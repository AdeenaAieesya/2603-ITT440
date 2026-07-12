from flask import Flask, render_template_string
import pymysql
import os

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'database'),
        user='root',
        password='secretpass',
        database='library_stats',
        cursorclass=pymysql.cursors.DictCursor
    )

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ITT440 Leaderboard</title>
    <style>
        body { font-family: Arial; background: #0f172a; color: white; text-align: center; padding: 40px; }
        h1 { color: #38bdf8; }
        .leaderboard { max-width: 700px; margin: 0 auto; background: #1e293b; padding: 25px; border-radius: 12px; }
        .player { display: flex; justify-content: space-between; padding: 12px; border-bottom: 1px solid #334155; }
        .badge-c { background: #f59e0b; color: #0f172a; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
        .badge-py { background: #10b981; color: #0f172a; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
        .points { font-weight: bold; color: #34d399; }
    </style>
    <script>setInterval(function(){ location.reload(); }, 2000);</script>
</head>
<body>
    <h1>ITT440 Leaderboard</h1>
    <div class="leaderboard">
        {% for row in players %}
        <div class="player">
            <span>#{{ loop.index }} {{ row.user }}</span>
            <span>
                {% if row.user in ['Adeena', 'Fasihah'] %}
                <span class="badge-c">C Primitive Socket</span>
                {% else %}
                <span class="badge-py">Python Multi-Thread</span>
                {% endif %}
                {{ row.points }} pts
            </span>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    try:
        db = get_db()
        with db.cursor() as cur:
            cur.execute("SELECT user, points FROM segmen_mata ORDER BY points DESC")
            players = cur.fetchall()
        db.close()
    except Exception as e:
        print(f"Error: {e}")
        players = []
    return render_template_string(HTML, players=players)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
