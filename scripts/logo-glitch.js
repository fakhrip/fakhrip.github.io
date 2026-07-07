const GLITCH_CHARS = "@%#*+=-:.";
const LOGO_START = "=-*@@@@@@";
const LOGO_END = "..-===*##*+==-..";
const TICK_MS = 80;
const GLITCH_LIFETIME_MS = 160;
const GLITCHES_PER_TICK = 4;
const HOVER_THROTTLE_MS = 45;
const HOVER_DURATION_MS = 430;
const HOVER_STEPS = 5;
const HOVER_RADIUS_X = 6;
const HOVER_RADIUS_Y = 3;

const getRandomItem = (items) => items[Math.floor(Math.random() * items.length)];

const getTargetKey = ({ line, column }) => `${line}:${column}`;

const replaceAt = (text, index, char) => {
  return `${text.slice(0, index)}${char}${text.slice(index + 1)}`;
};

const writeTargetChar = (target, char) => {
  target.node.data = replaceAt(target.node.data, target.offset, char);
};

const measurePreCell = (pre) => {
  const probe = document.createElement("span");
  const styles = window.getComputedStyle(pre);

  probe.textContent = "@".repeat(100);

  Object.assign(probe.style, {
    position: "absolute",
    visibility: "hidden",
    whiteSpace: "pre",
    fontFamily: styles.fontFamily,
    fontSize: styles.fontSize,
    fontStyle: styles.fontStyle,
    fontWeight: styles.fontWeight,
    letterSpacing: styles.letterSpacing,
    lineHeight: styles.lineHeight,
  });

  document.body.appendChild(probe);

  const rect = probe.getBoundingClientRect();
  const charWidth = rect.width / probe.textContent.length;
  const lineHeight =
    styles.lineHeight === "normal"
      ? parseFloat(styles.fontSize) * 1.2
      : parseFloat(styles.lineHeight);

  probe.remove();

  return { charWidth, lineHeight };
};

const getLogoBounds = (text) => {
  const lines = text.split("\n");
  const startLine = lines.findIndex((line) => line.includes(LOGO_START));
  const endLine = lines.findIndex((line) => line.includes(LOGO_END));

  if (startLine === -1 || endLine === -1 || startLine > endLine) {
    return null;
  }

  return { startLine, endLine };
};

const getTextNodePositions = (root) => {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  const positions = [];
  let line = 0;
  let column = 0;

  while (walker.nextNode()) {
    const node = walker.currentNode;

    for (let offset = 0; offset < node.data.length; offset += 1) {
      positions.push({ node, offset, line, column, char: node.data[offset] });

      if (node.data[offset] === "\n") {
        line += 1;
        column = 0;
      } else {
        column += 1;
      }
    }
  }

  return positions;
};

const collectLogoTargets = (pre) => {
  const bounds = getLogoBounds(pre.textContent);

  if (!bounds) {
    return [];
  }

  return getTextNodePositions(pre)
    .filter(({ line, column, char }) => {
      return (
        line >= bounds.startLine &&
        line <= bounds.endLine &&
        column >= 25 &&
        column <= 95 &&
        GLITCH_CHARS.includes(char)
      );
    })
    .map((target) => ({
      ...target,
      baseChar: target.char,
      key: getTargetKey(target),
    }));
};

const getPreGridMetrics = (pre, cell) => {
  const rect = pre.getBoundingClientRect();

  return {
    rect,
    charWidth: cell.charWidth,
    lineHeight: cell.lineHeight,
  };
};

const getHoveredGridPosition = (pre, cell, event) => {
  const { rect, charWidth, lineHeight } = getPreGridMetrics(pre, cell);

  return {
    column: Math.round((event.clientX - rect.left) / charWidth),
    line: Math.round((event.clientY - rect.top) / lineHeight),
  };
};

const getHoverBlobTargets = (targets, center) => {
  return targets.filter((target) => {
    const x = (target.column - center.column) / HOVER_RADIUS_X;
    const y = (target.line - center.line) / HOVER_RADIUS_Y;
    const distance = x * x + y * y;

    return distance <= 1 && Math.random() > distance * 0.45;
  });
};

const getHoverDelay = (step) => {
  const progress = step / (HOVER_STEPS - 1);

  return Math.round(HOVER_DURATION_MS * progress * progress);
};

const getGlitchChar = (originalChar) => {
  let nextChar = getRandomItem(GLITCH_CHARS);

  while (nextChar === originalChar) {
    nextChar = getRandomItem(GLITCH_CHARS);
  }

  return nextChar;
};

const animateHoverTarget = (target, activeGlitches, activeHovers) => {
  if (activeHovers.has(target.key)) {
    return;
  }

  if (activeGlitches.has(target.key)) {
    activeGlitches.delete(target.key);
  }

  const timeouts = [];

  for (let step = 0; step < HOVER_STEPS; step += 1) {
    const timeout = window.setTimeout(() => {
      const char =
        step === HOVER_STEPS - 1
          ? target.baseChar
          : getGlitchChar(target.baseChar);

      writeTargetChar(target, char);

      if (step === HOVER_STEPS - 1) {
        activeHovers.delete(target.key);
      }
    }, getHoverDelay(step));

    timeouts.push(timeout);
  }

  activeHovers.set(target.key, timeouts);
};

const isInsideLogo = (targetByKey, position) => {
  for (
    let line = position.line - HOVER_RADIUS_Y;
    line <= position.line + HOVER_RADIUS_Y;
    line += 1
  ) {
    for (
      let column = position.column - HOVER_RADIUS_X;
      column <= position.column + HOVER_RADIUS_X;
      column += 1
    ) {
      if (targetByKey.has(`${line}:${column}`)) {
        return true;
      }
    }
  }

  return false;
};

const startHoverGlitch = (
  pre,
  cell,
  targets,
  targetByKey,
  activeGlitches,
  activeHovers,
) => {
  let lastHoverAt = 0;

  pre.addEventListener("mousemove", (event) => {
    const now = Date.now();

    if (now - lastHoverAt < HOVER_THROTTLE_MS) {
      return;
    }

    const position = getHoveredGridPosition(pre, cell, event);

    if (!isInsideLogo(targetByKey, position)) {
      return;
    }

    lastHoverAt = now;

    for (const target of getHoverBlobTargets(targets, position)) {
      animateHoverTarget(target, activeGlitches, activeHovers);
    }
  });
};

const startIdleGlitch = (targets, activeGlitches, activeHovers) => {
  window.setInterval(() => {
    const now = Date.now();

    for (const [key, glitch] of activeGlitches) {
      if (glitch.expiresAt <= now) {
        writeTargetChar(glitch.target, glitch.target.baseChar);
        activeGlitches.delete(key);
      }
    }

    for (let i = 0; i < GLITCHES_PER_TICK; i += 1) {
      const target = getRandomItem(targets);

      if (activeGlitches.has(target.key) || activeHovers.has(target.key)) {
        continue;
      }

      writeTargetChar(target, getGlitchChar(target.baseChar));

      activeGlitches.set(target.key, {
        target,
        expiresAt: now + GLITCH_LIFETIME_MS,
      });
    }
  }, TICK_MS);
};

window.addEventListener("load", () => {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  const pre = document.querySelector(".content pre");

  if (!pre) {
    return;
  }

  const targets = collectLogoTargets(pre);

  if (targets.length === 0) {
    return;
  }

  const activeGlitches = new Map();
  const activeHovers = new Map();
  const targetByKey = new Map(targets.map((target) => [target.key, target]));
  const cell = measurePreCell(pre);

  startHoverGlitch(pre, cell, targets, targetByKey, activeGlitches, activeHovers);
  startIdleGlitch(targets, activeGlitches, activeHovers);
});
