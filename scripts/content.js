window.renderContent = async (content) => {
  const short = await (async () => {
    const whitelist = [
      "about", "youtube", "contact", "blog", "cv",
      "flag{congrats_you_found_a_meaningless_flag_from_a_meaningless_repository_in_github}"
    ]
    if (whitelist.includes(content)) {
      return await (await fetch(`../contents/${content}.html`)).text();
    } else {
      if (["..", "{", "}", "]", "[", ")", "("].includes(content)) {
        return "<span style=\"width: 100%;\"><center>Hacker, please dont attack me :(</center></span>"
      } else {
        const { origin } = new URL(document.location.href);
        window.location = `${origin}/404.html`;
      }
    }
  })()

  const contentPreTag =
    document.getElementsByClassName("content")[0].children[0];
  contentPreTag.innerHTML = "\n" + short;

  let wrapper = "";
  for (const element of [...Array(parseInt(contentPreTag.clientHeight / 14)).keys()]) {
    wrapper += " |                                                                                                         |\n";
  }

  const containerDivTag =
    document.getElementsByClassName("content-container")[0];
  const containerPreTag = document.createElement("pre");
  containerPreTag.textContent = wrapper;
  containerDivTag.appendChild(containerPreTag);
}
