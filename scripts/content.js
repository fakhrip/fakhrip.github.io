const wrapContent = (text) => {
  const maxLineLength = 101;
  let result = "";

  for (const line of text.split("\n")) {
    let strBuffer = "";

    const loopCount = parseInt(line.length / maxLineLength) + 1;
    for (const multiplier of [...Array(loopCount).keys()]) {
      const croppedLine = line.substring(
        maxLineLength * multiplier,
        maxLineLength * (multiplier + 1)
      );

      if (multiplier === loopCount) {
        break;
      }

      strBuffer += "│  " + croppedLine.padEnd(maxLineLength) + "  │\n";
    }

    result += strBuffer;
  }

  return result.substring(0, result.length - 1); // remove the last carriage return
};

// Export the function by setting it to the window context
window.renderContent = (text) => {
  const divTag = document.getElementsByClassName("content")[0];
  const preTag = document.createElement("pre");

  preTag.textContent = wrapContent(text);

  // Remove any existing childrens
  if (divTag.hasChildNodes()) {
    for (const child of divTag.children) {
      divTag.removeChild(child);
    }
  }

  divTag.appendChild(preTag);
};