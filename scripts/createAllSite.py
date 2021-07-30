from os.path import isfile, join
from datetime import datetime
from jinja2 import Template
from pytz import timezone
import markdown2, os, json

ARTICLE_TEMPLATE = open("./templates/articleTemplate.html", "r").read()


def main():
    print("[+] Running all sites creation sequence")
    allSites = [f for f in os.listdir("./sites") if isfile(join("./sites", f))]
    allSites = sorted(allSites)

    print("[+] Making sure /blogs exist")
    if not os.path.exists("./blogs"):
        os.mkdir("./blogs")
        print("[|] Directory ", "/blogs", " Created ")
    else:
        print("[|] Directory ", "/blogs", " already exists")

    print("[+] ===")
    print("[+] Converting /sites to /blogs")
    for site in allSites:
        print("[|] Working on '{}'".format(site))

        siteContent = open("./sites/" + site, "r").read()
        siteMD = siteContent.split("--+--+--+--\n")[1]
        siteMeta = siteContent.split("--+--+--+--\n")[0]
        convertedSite = markdown2.markdown(
            siteMD,
            extras=[
                "footnotes",
                "fenced-code-blocks",
                "tables",
                "markdown-in-html",
                "target-blank-links",
            ],
        )

        for meta in siteMeta.split("\n"):
            if "Tags" == meta.split(": ")[0]:
                tags = meta.split(": ")[1].split("|")
            if "Times" == meta.split(": ")[0]:
                times = markdown2.markdown(
                    meta.split(": ")[1],
                    extras=[
                        "footnotes",
                        "fenced-code-blocks",
                        "tables",
                        "markdown-in-html",
                        "target-blank-links",
                    ],
                )
            if "TLDR" == meta.split(": ")[0]:
                desc = meta.split(": ")[1]
                tldr = markdown2.markdown(
                    meta.split(": ")[1],
                    extras=[
                        "footnotes",
                        "fenced-code-blocks",
                        "tables",
                        "markdown-in-html",
                        "target-blank-links",
                    ],
                )

        datetime_res = (
            os.popen(f"echo $(git log -1 --format=%cd ./sites/{site})")
            .read()
            .strip()
            .split()
        )

        renderedResult = Template(ARTICLE_TEMPLATE).render(
            contents=convertedSite,
            updatedDate=f"{datetime_res[1]} {datetime_res[2]}, {datetime_res[4]}",
            updatedTime=f"{datetime_res[3]}",
            tags=tags,
            times=times,
            tldr=tldr,
            site=site,
            desc=desc,
            title=site.replace("-", " ").replace(".md", ""),
        )

        open("./blogs/" + site.replace(".md", "") + ".html", "w+").write(renderedResult)

    print("[+] ===")
    print("[+] Injecting all sites to blogs.html")
    allBlogs = [f for f in os.listdir("./blogs") if isfile(join("./blogs", f))]
    allBlogs = sorted(allBlogs)

    blogsHTMLTemplate = open("./templates/blogsTemplate.html", "r").read()
    open("./blogs.html", "w+").write(Template(blogsHTMLTemplate).render(sites=allBlogs))

    print("[+] Updating date and time in index.html")
    cur_date = datetime.now(timezone("Asia/Jakarta")).strftime("%B %d, %Y")
    cur_time = datetime.now(timezone("Asia/Jakarta")).strftime("%H:%M:%S")

    github_urls = (
        os.popen(
            'curl -s "https://api.github.com/users/fakhrip/repos?per_page=100" | jq "[ .[] | select(.archived == "false") | .html_url ]"'
        )
        .read()
        .strip()
    )
    github_urls = [url for url in json.loads(github_urls)]
    github_urls = sorted(github_urls)

    indexHTMLTemplate = open("./templates/indexTemplate.html", "r").read()
    open("./index.html", "w+").write(
        Template(indexHTMLTemplate).render(
            github_urls=github_urls, updatedDate=cur_date, updatedTime=cur_time
        )
    )


if __name__ == "__main__":
    main()
