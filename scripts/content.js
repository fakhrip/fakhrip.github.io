window.renderContent = async (content) => {
  const short = await (await fetch(`../contents/${content}.html`)).text();
  const contentPreTag =
    document.getElementsByClassName("content")[0].children[0];
  contentPreTag.innerHTML = "\n" + short;

  let wrapper = "|                                                                                                         |\n";
  for (const element of [...Array(parseInt(contentPreTag.clientHeight / 14)).keys()]) {
    wrapper += "|                                                                                                         |\n";
  }

  const containerDivTag =
    document.getElementsByClassName("content-container")[0];
  const containerPreTag = document.createElement("pre");
  containerPreTag.textContent = wrapper;
  containerDivTag.appendChild(containerPreTag);
}
