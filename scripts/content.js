window.renderContent = async (content) => {
  const short = await (async () => {
    const whitelist = [
      "about", "youtube", "contact", "blog", "cv", "challenges",
      "flag{congrats_you_found_a_meaningless_flag_from_a_meaningless_repository_in_github}"
    ]
    if (whitelist.includes(content)) {
      return await (await fetch(`../contents/${content}.html`)).text();
    } else {
      if ([".", "/", "{", "}", "]", "[", ")", "("].filter(str => content?.includes(str)).length > 0) {
        return "<span style=\"width: 100%;\"><center>Hacker, please dont attack me :(</center></span>"
      } else {
        const { origin } = new URL(document.location.href);
        window.location = `${origin}/404.html`;
      }
    }
  })()

  const contentPreTag =
    document.getElementsByClassName("content")[0].children[0];

  const renderWrapper = () => {
    // Setup the wrapper
    let wrapper = "";
    for (const element of [...Array(parseInt(contentPreTag.clientHeight / 14)).keys()]) {
      wrapper += " |                                                                                                         |\n";
    }

    // Render the wrapper
    const containerDivTag =
      document.getElementsByClassName("content-container")[0];
    const containerPreTag = document.createElement("pre");
    containerPreTag.textContent = wrapper;
    containerDivTag.appendChild(containerPreTag);
  }

  // Wait for until the content is rendered along with the css by
  // observing the mutations (which in this case is the height changes)
  const observer = new MutationObserver((mutationsList, _) => {
    const additionalStyles = document.getElementsByClassName("additional-style");
    if (additionalStyles.length > 0) {
      for (const style of additionalStyles) {
        style.addEventListener("load", renderWrapper);
      }
    } else {
      renderWrapper();
    }
  });

  observer.observe(contentPreTag, {
    attributes: true,
    childList: true,
    characterData: true
  });

  const parser = new DOMParser();
  const doc = parser.parseFromString(short, 'text/html');
  const scripts = doc.querySelectorAll("script");

  const newShort = doc;
  newShort.querySelectorAll("script").forEach((script) => script.remove());

  // Render the content
  contentPreTag.innerHTML = `\n${newShort.body.innerHTML.trim()}`;

  // Execute script tags inside the content
  scripts.forEach((script) => {
    const newScript = document.createElement("script");

    // Copy all attributes
    for (const attr of script.attributes) {
      newScript.setAttribute(attr.name, attr.value);
    }

    if (script.src) {
      // For external scripts
      newScript.src = script.src;
    } else {
      // For inline scripts
      newScript.text = script.textContent;
    }

    // Append to trigger execution
    document.body.appendChild(newScript);

    // Clean up
    newScript.remove();
  });
}
