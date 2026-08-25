(() => {
  const navigation = document.querySelector('.topnav');
  const links = [...document.querySelectorAll('.topnav a[href^="#"]')];
  const linkedIds = new Set(links.map((link) => link.hash.slice(1)));
  const targets = [...document.querySelectorAll('section[id]')].filter((section) =>
    linkedIds.has(section.id),
  );

  const dayCards = [...document.querySelectorAll('.day-card')];

  const setDayExpanded = (dayCard, expanded) => {
    const toggle = dayCard.querySelector(':scope > h2 .day-toggle');
    const content = dayCard.querySelector(':scope > .day-content');
    const inner = content?.querySelector(':scope > .day-content-inner');

    if (!toggle || !content || !inner) return;

    dayCard.classList.toggle('is-expanded', expanded);
    toggle.setAttribute('aria-expanded', String(expanded));
    content.setAttribute('aria-hidden', String(!expanded));
    inner.toggleAttribute('inert', !expanded);
  };

  for (const dayCard of dayCards) {
    const heading = dayCard.querySelector(':scope > h2');
    if (!heading || !dayCard.id) continue;

    const toggle = document.createElement('button');
    const content = document.createElement('div');
    const inner = document.createElement('div');
    const toggleId = `${dayCard.id}-toggle`;
    const contentId = `${dayCard.id}-content`;

    toggle.className = 'day-toggle';
    toggle.type = 'button';
    toggle.id = toggleId;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', contentId);

    while (heading.firstChild) toggle.append(heading.firstChild);
    heading.append(toggle);

    content.className = 'day-content';
    content.id = contentId;
    content.setAttribute('role', 'region');
    content.setAttribute('aria-labelledby', toggleId);
    inner.className = 'day-content-inner';

    while (heading.nextSibling) inner.append(heading.nextSibling);
    content.append(inner);
    dayCard.append(content);
    dayCard.classList.add('is-collapsible');
    setDayExpanded(dayCard, false);

    toggle.addEventListener('click', () => {
      setDayExpanded(dayCard, toggle.getAttribute('aria-expanded') !== 'true');
    });
  }

  const revealHashTarget = () => {
    if (!location.hash) return;
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    const dayCard = target?.closest('.day-card');
    if (dayCard) setDayExpanded(dayCard, true);
  };

  for (const link of links) {
    link.addEventListener('click', () => {
      const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      const dayCard = target?.closest('.day-card');
      if (dayCard) setDayExpanded(dayCard, true);
    });
  }

  revealHashTarget();

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
  addEventListener('hashchange', () => {
    revealHashTarget();
    scheduleUpdate();
  });
})();
