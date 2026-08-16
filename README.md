# Sicily Family Trip 2026

אתר המסלול המשפחתי לסיציליה בתאריכים 26.11.2026–3.12.2026. האתר סטטי ומפורסם באמצעות GitHub Pages.

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
