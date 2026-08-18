# Sicily Family Trip 2026

הייתי צריך מקום אחד מעודכן למסלול, במקום לשלוח כל פעם קובץ חדש 🤷🏽

## מקור התוכן

[`index.html`](index.html) הוא הגרסה הפעילה והקנונית של המסלול. קבצים ישנים והיסטוריית Git הם חומר היסטורי בלבד ואין להחזיר מהם מידע שסותר את הגרסה הפעילה.

לפני שינוי תוכן יש לקרוא:

- [`AGENTS.md`](AGENTS.md) — כללי העבודה בפרויקט.
- [`docs/TRIP_REQUIREMENTS.md`](docs/TRIP_REQUIREMENTS.md) — דרישות ואילוצים קבועים.
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — החלטות משמעותיות.

## הרצה מקומית

אין dependencies ואין שלב build. אפשר לפתוח את `index.html` ישירות בדפדפן, או להפעיל שרת מקומי משורש הפרויקט:

```bash
python3 -m http.server 8000
```

לאחר מכן פותחים `http://localhost:8000`.

## מבנה הפרויקט

```text
.
├── .github/
│   └── workflows/
│       └── release.yml
├── AGENTS.md
├── README.md
├── index.html
└── docs/
    ├── DECISIONS.md
    └── TRIP_REQUIREMENTS.md
```

ה־CSS נמצא כרגע בתוך `index.html`, כפי שהיה בקובץ הקנוני המקורי. אין JavaScript או assets מקומיים חיצוניים.

## פרסום

GitHub Pages מוגדר לפרסום מענף `main` ומתיקיית השורש (`/`). כל שינוי מאומת שנדחף ל־`main` מתפרסם באותה כתובת קבועה.

לפני push יש לוודא שאין מידע רגיש, קישורים פנימיים שבורים או פגיעה בתצוגת מובייל ו־desktop.

## גרסאות ושחזור

הגרסה הפעילה הראשונה מתועדת כ־`v0.1.0 — Baseline`. כל merge נוסף ל־`main` יוצר אוטומטית patch release חדש, למשל `v0.1.1 — Release`. כותרות ה־Releases נכתבות באנגלית; מעבר לגרסת minor או major נעשה רק בהחלטה מפורשת.

כדי לחזור משינוי בעייתי, יוצרים branch חדש מ־`main`, מבטלים את ה־commit או את מיזוג ה־PR באמצעות `git revert`, ובודקים וממזגים את התיקון דרך PR רגיל. אין להזיז tag קיים או לבצע force-push ל־`main`; ה־rollback מתפרסם כגרסה חדשה ושומר את ההיסטוריה המלאה.
