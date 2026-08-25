// Keeps the sticky itinerary navigation aligned with the current section.
(() => {
  const navigation = document.querySelector('.topnav');
  const links = [...document.querySelectorAll('.topnav a[href^="#"]')];
  const linkedIds = new Set(links.map((link) => link.hash.slice(1)));
  const targets = [...document.querySelectorAll('section[id]')].filter((section) =>
    linkedIds.has(section.id),
  );

  if (!navigation || !links.length || !targets.length) return;

  let currentId = '';
  let scheduled = false;

  const markCurrentSection = () => {
    scheduled = false;
    const readingLine = window.innerHeight * 0.32;
    let active = targets[0];

    for (const section of targets) {
      if (section.getBoundingClientRect().top <= readingLine) active = section;
      else break;
    }

    if (!active || active.id === currentId) return;
    currentId = active.id;

    for (const link of links) {
      const isCurrent = link.hash === `#${currentId}`;
      if (isCurrent) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  };

  const scheduleUpdate = () => {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(markCurrentSection);
  };

  markCurrentSection();
  addEventListener('scroll', scheduleUpdate, { passive: true });
  addEventListener('resize', scheduleUpdate, { passive: true });
  addEventListener('hashchange', scheduleUpdate);
})();
