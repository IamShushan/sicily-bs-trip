(() => {
  const navigation = document.querySelector('.topnav');
  const links = [...document.querySelectorAll('.topnav a[href^="#"]')];
  const linkedIds = new Set(links.map((link) => link.hash.slice(1)));
  const targets = [...document.querySelectorAll('section[id]')].filter((section) =>
    linkedIds.has(section.id),
  );

  const supportingSectionIds = [
    'kids',
    'evenings',
    'actions',
    'bookings',
    'checks',
    'source-challenge',
    'mustfix',
  ];
  const collapsibleSections = [
    ...document.querySelectorAll('.day-card'),
    ...supportingSectionIds.map((id) => document.getElementById(id)).filter(Boolean),
  ];
  const longDetailCards = [
    ...document.querySelectorAll(
      '.day-card .planb, .day-card .warn, .day-card .child, .day-card .note',
    ),
  ].filter(
    (card) =>
      card.textContent.trim().length >= 500 &&
      card.querySelector(':scope > strong:first-child'),
  );

  const setDetailExpanded = (card, expanded) => {
    const toggle = card.querySelector(':scope > .large-card-toggle');
    const content = card.querySelector(':scope > .large-card-content');
    const inner = content?.querySelector(':scope > .large-card-content-inner');

    if (!toggle || !content || !inner) return;

    card.classList.toggle('is-detail-expanded', expanded);
    toggle.setAttribute('aria-expanded', String(expanded));
    content.setAttribute('aria-hidden', String(!expanded));
    inner.toggleAttribute('inert', !expanded);
  };

  longDetailCards.forEach((card, index) => {
    const toggle = document.createElement('button');
    const content = document.createElement('div');
    const inner = document.createElement('div');
    const cardOwner = card.closest('.day-card')?.id ?? 'detail';
    const toggleId = `${cardOwner}-detail-${index + 1}-toggle`;
    const contentId = `${cardOwner}-detail-${index + 1}-content`;

    toggle.className = 'large-card-toggle';
    toggle.type = 'button';
    toggle.id = toggleId;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', contentId);

    while (card.firstChild) {
      const node = card.firstChild;
      const tagName = node.nodeType === Node.ELEMENT_NODE ? node.tagName : '';

      if (tagName === 'BR') {
        node.remove();
        break;
      }

      if (['DIV', 'P', 'UL', 'OL', 'TABLE'].includes(tagName)) break;
      toggle.append(node);
    }

    content.className = 'large-card-content';
    content.id = contentId;
    content.setAttribute('role', 'region');
    content.setAttribute('aria-labelledby', toggleId);
    inner.className = 'large-card-content-inner';

    while (card.firstChild) inner.append(card.firstChild);
    content.append(inner);
    card.append(toggle, content);
    card.classList.add('is-detail-collapsible');
    setDetailExpanded(card, false);

    toggle.addEventListener('click', () => {
      setDetailExpanded(card, toggle.getAttribute('aria-expanded') !== 'true');
    });
  });

  const setSectionExpanded = (section, expanded) => {
    const toggle = section.querySelector(':scope > h2 .section-toggle');
    const content = section.querySelector(':scope > .section-content');
    const inner = content?.querySelector(':scope > .section-content-inner');

    if (!toggle || !content || !inner) return;

    section.classList.toggle('is-expanded', expanded);
    toggle.setAttribute('aria-expanded', String(expanded));
    content.setAttribute('aria-hidden', String(!expanded));
    inner.toggleAttribute('inert', !expanded);
  };

  for (const section of collapsibleSections) {
    const heading = section.querySelector(':scope > h2');
    if (!heading || !section.id) continue;

    const toggle = document.createElement('button');
    const content = document.createElement('div');
    const inner = document.createElement('div');
    const toggleId = `${section.id}-toggle`;
    const contentId = `${section.id}-content`;

    toggle.className = 'section-toggle';
    toggle.type = 'button';
    toggle.id = toggleId;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', contentId);

    while (heading.firstChild) toggle.append(heading.firstChild);
    heading.append(toggle);

    content.className = 'section-content';
    content.id = contentId;
    content.setAttribute('role', 'region');
    content.setAttribute('aria-labelledby', toggleId);
    inner.className = 'section-content-inner';

    while (heading.nextSibling) inner.append(heading.nextSibling);
    content.append(inner);
    section.append(content);
    section.classList.add('is-collapsible');
    setSectionExpanded(section, false);

    toggle.addEventListener('click', () => {
      setSectionExpanded(section, toggle.getAttribute('aria-expanded') !== 'true');
    });
  }

  const revealHashTarget = () => {
    if (!location.hash) return;
    const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    const section = target?.closest('.is-collapsible');
    if (section) setSectionExpanded(section, true);
  };

  for (const link of links) {
    link.addEventListener('click', () => {
      const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
      const section = target?.closest('.is-collapsible');
      if (section) setSectionExpanded(section, true);
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
