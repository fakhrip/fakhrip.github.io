// https://stackoverflow.com/questions/68365106/fade-in-and-fade-out-using-pure-javascript-in-a-simple-way
const fadeOutElement = (element, duration = 500) => {
  const fromValue = parseFloat(element.style.opacity) || 1;
  const startTime = Date.now();
  const framerate = 1000 / 60; // 60fps

  let interval = setInterval(() => {
    const currentTime = Date.now();
    const timeDiff = (currentTime - startTime) / duration;
    const value = fromValue - fromValue * timeDiff;

    if (timeDiff >= 1) {
      clearInterval(interval);
      interval = 0;
    }

    element.style.opacity = value.toString();
  }, framerate);
};

const getRandomAsciiChar = () => {
  // ASCII printable characters range from 33 to 126 (excluding space)
  const min = 33;
  const max = 126;

  const randomAsciiCode = Math.floor(Math.random() * (max - min + 1)) + min;
  return String.fromCharCode(randomAsciiCode);
};

const getRandomNumber = (min = 0, max = 10) => {
  // Ensure min and max are inclusive
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

window.addEventListener("load", () => {
  let lastCursorX = -1,
    lastCursorY = -1;

  const asciiBoxes = [];

  // https://stackoverflow.com/questions/7790725/javascript-track-mouse-position
  document.onmousemove = (event) => {
    var eventDoc, doc, body;

    event = event || window.event; // IE-ism

    // If pageX/Y aren't available and clientX/Y are,
    // calculate pageX/Y - logic taken from jQuery.
    // (This is to support old IE)
    if (event.pageX == null && event.clientX != null) {
      eventDoc = (event.target && event.target.ownerDocument) || document;
      doc = eventDoc.documentElement;
      body = eventDoc.body;

      event.pageX =
        event.clientX +
        ((doc && doc.scrollLeft) || (body && body.scrollLeft) || 0) -
        ((doc && doc.clientLeft) || (body && body.clientLeft) || 0);
      event.pageY =
        event.clientY +
        ((doc && doc.scrollTop) || (body && body.scrollTop) || 0) -
        ((doc && doc.clientTop) || (body && body.clientTop) || 0);
    }

    const cursorX = event.pageX;
    const cursorY = event.pageY;

    // Skip all box operations if the cursor didnt
    // move far enough from the last positions
    if (
      Math.abs(lastCursorX - cursorX) < 40 &&
      Math.abs(lastCursorY - cursorY) < 40
    ) {
      return;
    } else {
      lastCursorX = cursorX;
      lastCursorY = cursorY;
    }

    const asciiBox = document.createElement("pre");

    // Set box Id
    const lastId = asciiBoxes.slice(-1)[0] ?? 0;
    const newId = lastId + 1;
    asciiBox.classList.add(`ascii-${newId}`);
    asciiBoxes.push(newId);

    Object.assign(asciiBox.style, {
      position: "absolute",
      display: "flex",
      margin: "0",

      "font-family": "Julia, monospace",
      "font-weight": 200,
      "font-size": "12px",
      "font-style": "normal",
      "user-select": "none",
      "justify-content": "center",

      // Set box position
      top: `${cursorY - 50}px`,
      left: `${cursorX - 50}px`,
    });

    const boxSizeY = 5 + getRandomNumber();
    const boxSizeX = 10 + getRandomNumber();
    const charPosX = getRandomNumber(0, boxSizeX - 1);
    const charPosY = getRandomNumber(0, boxSizeY - 1);

    // Set box content
    for (const y of [...Array(boxSizeY).keys()]) {
      for (const x of [...Array(boxSizeX).keys()]) {
        if (x == charPosX && y == charPosY) {
          asciiBox.textContent += getRandomAsciiChar();
        } else {
          asciiBox.textContent += " ";
        }
      }
      asciiBox.textContent += "\n";
    }

    // Add to box body
    document.body.appendChild(asciiBox);

    // Fadeout the box
    const duration = getRandomNumber(100, 3000);
    fadeOutElement(asciiBox, duration);
    setTimeout(() => {
      document.body.removeChild(asciiBox);
      asciiBox.remove();

      // Remove the box from boxes list
      const boxId = asciiBoxes.indexOf(newId);
      if (boxId > -1) {
        asciiBoxes.splice(boxId, 1);
      }
    }, duration);
  };
});