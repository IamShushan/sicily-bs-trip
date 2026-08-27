# Sicily Family Trip 2026

הייתי צריך מקום אחד מעודכן למסלול, במקום לשלוח כל פעם קובץ חדש 🤷🏽

## מקור התוכן

[`index.html`](index.html) הוא הגרסה הפעילה והקנונית של המסלול. קבצים ישנים והיסטוריית Git הם חומר היסטורי בלבד ואין להחזיר מהם מידע שסותר את הגרסה הפעילה.

לפני שינוי תוכן יש לקרוא:

- [`AGENTS.md`](AGENTS.md) — כללי העבודה בפרויקט.
- [`docs/TRIP_REQUIREMENTS.md`](docs/TRIP_REQUIREMENTS.md) — דרישות ואילוצים קבועים.
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — החלטות משמעותיות.
- [`docs/lessons.md`](docs/lessons.md) — דברים לא־מובנים מאליהם שנלמדו במהלך העבודה ושכדאי לא לגלות מחדש.

## הרצה מקומית

אין dependencies ואין שלב build. אפשר לפתוח את `index.html` ישירות בדפדפן, או להפעיל שרת מקומי משורש הפרויקט:

```bash
python3 -m http.server 8000
```

לאחר מכן פותחים `http://localhost:8000`.

## הגנת פרטיות מקומית

לאחר clone חד־פעמי מתקינים את hooks של הפרויקט:

```bash
./scripts/install_hooks.sh
```

ה־hooks חוסמים commit ו־push שמכילים פרטי תשלום, מזהים אישיים, פרטי הזמנה, פרטי קשר פרטיים, credentials או קבצים בינאריים שלא אושרו. אפשר להריץ בדיקה מלאה ידנית:

```bash
python3 scripts/privacy_scan.py --all-files
```

אין לעקוף חסימת פרטיות באמצעות `--no-verify`. ‏GitHub Actions מריץ בדיקה נוספת בכל Pull Request, אך בריפו ציבורי הבדיקה המקומית לפני push היא קו ההגנה הראשון.

## מבנה הפרויקט

```text
.
├── .github/
│   └── workflows/
│       ├── privacy-scan.yml
│       ├── pr-preview.yml
│       └── release.yml
├── .githooks/
├── scripts/
│   ├── install_hooks.sh
│   └── privacy_scan.py
├── tests/
│   └── test_privacy_scan.py
├── AGENTS.md
├── README.md
├── index.html
├── site-design.css
├── site-design.js
└── docs/
    ├── DECISIONS.md
    ├── lessons.md
    └── TRIP_REQUIREMENTS.md
```

`index.html` מכיל את התוכן הקנוני ואת סגנונות הבסיס המבניים. `site-design.css` מוסיף את שכבת העיצוב וההתאמות הרספונסיביות, ו־`site-design.js` מנהל את האינטראקציות בעמוד, כולל קיפול ופתיחה של הסקשנים. שלושת הקבצים סטטיים, ללא dependencies וללא שלב build.

## פרסום

GitHub Pages מוגדר לפרסום מענף `main` ומתיקיית השורש (`/`). כל שינוי מאומת שנדחף ל־`main` מתפרסם באותה כתובת קבועה.

לפני push יש לוודא שאין מידע רגיש, קישורים פנימיים שבורים או פגיעה בתצוגת מובייל ו־desktop.

## גרסאות ושחזור

הגרסה הפעילה הראשונה מתועדת כ־`v0.1.0 — Baseline`. כל merge נוסף ל־`main` יוצר אוטומטית patch release חדש, למשל `v0.1.1 — Release`. כותרות ה־Releases נכתבות באנגלית; מעבר לגרסת minor או major נעשה רק בהחלטה מפורשת.

כדי לחזור משינוי בעייתי, יוצרים branch חדש מ־`main`, מבטלים את ה־commit או את מיזוג ה־PR באמצעות `git revert`, ובודקים וממזגים את התיקון דרך PR רגיל. אין להזיז tag קיים או לבצע force-push ל־`main`; ה־rollback מתפרסם כגרסה חדשה ושומר את ההיסטוריה המלאה.
