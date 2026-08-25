# יומן החלטות

המסמך מתעד החלטות משמעותיות ומתמשכות. יש להוסיף אליו החלטה כאשר היא משנה את מבנה הפרויקט או את המסלול הקנוני.

## Hosting

**Decision:** GitHub Pages.

**Reason:** כתובת קבועה למשפחה ופריסה פשוטה של אתר סטטי.

## Pull request previews

**Decision:** כל Pull Request פנימי יקבל תגובה אוטומטית עם קישור לתצוגת `index.html` דרך `htmlpreview.github.io`, כשהקישור מקובע ל־commit העדכני של ה־PR.

**Reason:** כך אפשר לבדוק את הגרסה המוצעת מרחוק ובמובייל לפני המיזוג, בלי לפרוס את ה־branch מעל האתר הפעיל ב־GitHub Pages.

## Canonical itinerary

**Decision:** הגרסה הפעילה ב־`index.html` היא ה־Source of Truth.

**Reason:** אין יותר ניהול של מספר קובצי `FINAL` מקבילים.

## Lodging structure

**Decision:** 5 לילות ב־Bellini Holiday House במרכז Catania ושני לילות ב־Siracusa / Umbertino.

**Status:** Canonical. ‏Bellini Holiday House היא Confirmed / Booked לתאריכים 26.11–1.12.

**Operational details:** הכניסה באמצעות קודים והגעה סביב 02:00–03:00 אושרה על ידי המארח. המארח יזמין שני מקומות בחניון שמור 24/7 במרחק כמה דקות הליכה, בעלות €20 ליום לרכב (€200 בסך הכול). מחיר הלינה הוא ₪5,423 ללא חניה.

## Etna / Taormina

**Decision:** ניתן להחליף בין 29.11 ו־30.11 לפי התנאים ב־Etna.

## Catania / Noto

**Decision:** Catania משמשת בסיס ראשון ומקבלת יום הליכה רגוע בשבת ללא רכב. Noto היא יעד המעבר הקנוני ב־1.12 במסלול Central Catania → Noto → Cantine Gulino אם תאושר ותשתלב → Siracusa / Umbertino.

**Cantine Gulino:** תוספת קנונית מועדפת שממתינה לאישור, בחלון מבוקש של כ־16:00–16:15. היא אינה תנאי לכך שהיום יעבוד ואינה מסומנת כמאושרת או מוזמנת.

**Reason:** הבסיס המרכזי מאפשר לנצל את שבת לקטניה ברגל, ולכן יום המעבר נשאר רגוע עם ביקור קומפקטי ב־Noto. אם Gulino אינה מתאימה ללוח היום, ממשיכים ישירות ל־Siracusa בלי לדחוס את Noto.

## Architecture

**Decision:** בשלב הנוכחי נשארים עם אתר סטטי פשוט.

**Reason:** אין כרגע צורך אמיתי ב־framework או backend.

## Releases and rollback

**Decision:** המצב הקיים תויג כ־`v0.1.0 — Baseline`. כל merge ל־`main` יוצר אוטומטית patch release חדש בסדרת `v0.1.x`, עם כותרת Release באנגלית. מעבר ל־minor או major version דורש החלטה מפורשת.

**Rollback:** מבטלים את השינוי ב־branch חדש באמצעות `git revert` וממזגים דרך Pull Request. ה־rollback מקבל גרסה חדשה; אין להזיז tags קיימים או לשכתב את היסטוריית `main`.

**Reason:** כך כל גרסה שפורסמה נשארת נקודת שחזור ברורה, בלי להוסיף כלי versioning או dependencies לפרויקט הסטטי הקטן.

## Privacy guardrails

**Decision:** מידע אישי, מסמכי זיהוי, פרטי תשלום, פרטי הזמנה ו־credentials נחסמים בשכבות: סורק מקומי ב־pre-commit וב־pre-push, בדיקת חובה ב־Pull Request ו־Gitleaks לסודות. קבצים בינאריים ותמונות חסומים כברירת מחדל.

**Incident exception:** אם מידע רגיש כבר נכנס להיסטוריה, `git revert` רגיל אינו מספיק. עוצרים שיתוף ופרסום, מבטלים או מחליפים סודות ואמצעי תשלום, ומבצעים ניקוי היסטוריה מתואם. זהו החריג היחיד למדיניות האוסרת שכתוב היסטוריה ו־force-push ל־`main`.

**Reason:** הריפו והאתר ציבוריים; בדיקה שמתרחשת רק אחרי push מאוחרת מדי. ההגנה המקומית מונעת חשיפה ראשונית, והבדיקה המרוחקת מונעת merge במקרה שה־hook לא הותקן או נעקף.
