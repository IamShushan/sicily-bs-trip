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

**Decision:** 5 לילות ב־Aci Trezza ושני לילות ב־Siracusa / Umbertino.

**Status:** Canonical.

## Etna / Taormina

**Decision:** ניתן להחליף בין 29.11 ו־30.11 לפי התנאים ב־Etna.

## Catania / Noto — 1.12

**Decision:** Catania מחליפה את Noto במסלול הקנוני של 1.12. הביקור ב־Catania נשאר מלא, סביב 10:30–14:15. Noto נשמרת כיעד גיבוי בלבד.

**Cantine Gulino:** תוספת קנונית מועדפת שממתינה לאישור, בחלון מבוקש של כ־16:00–16:15. היא אינה תנאי לכך שהיום יעבוד ואינה מסומנת כמאושרת או מוזמנת.

**Reason:** יום המעבר נשאר רציף וגמיש: Catania מלאה פועלת גם ללא Gulino, ו־Noto נשארת חלופה מוכנה במקום להימחק.

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
