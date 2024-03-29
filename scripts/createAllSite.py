from os.path import isfile, join
from datetime import datetime
from jinja2 import Template
from pytz import timezone
from github import Github

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

    repo = Github(open("token_file", "r").read().strip()).get_repo(
        "fakhrip/fakhrip.github.io"
    )
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

        commits = repo.get_commits(path=f"./sites/{site}")

        if commits.totalCount > 1:
            datetime_res = commits[0].commit.committer.date

        renderedResult = Template(ARTICLE_TEMPLATE).render(
            contents=convertedSite,
            updatedDate=datetime_res.strftime("%B %d, %Y") if datetime_res else "",
            updatedTime=datetime_res.strftime("%H:%M:%S") if datetime_res else "",
            tags=tags,
            times=times,
            tldr=tldr,
            site=site,
            desc=desc,
            title=site.replace("-", " ").replace(".md", ""),
        )

        open("./blogs/" + site.replace(".md", ".html"), "w+").write(renderedResult)

    print("[+] ===")
    print("[+] Injecting all sites to blogs.html")
    allBlogs = [f for f in os.listdir("./blogs") if isfile(join("./blogs", f))]
    allBlogs = sorted(allBlogs)

    blogs = []
    for blog in allBlogs:
        commits = repo.get_commits(path=f"./sites/{blog.replace('.html', '.md')}")

        if commits.totalCount > 1:
            datetime_res = commits[0].commit.committer.date

        blogs.append(
            {
                "title": blog,
                "time": datetime_res.strftime("%B -- %Y") if datetime_res else "",
                "timestamp": int(datetime_res.timestamp() * 1000)
                if datetime_res
                else 0,
            }
        )

    blogs = sorted(blogs, key=lambda d: d["timestamp"])
    allBlogs = [[blog for blog in blogs if blog["time"] == x] for x in list(dict.fromkeys([a["time"] for a in blogs]))]
    allBlogs = [sorted(blog, key=lambda d: d["title"]) for blog in allBlogs]
    blogs = [item for sublist in allBlogs for item in sublist]

    blogsHTMLTemplate = open("./templates/blogsTemplate.html", "r").read()
    open("./blogs.html", "w+").write(Template(blogsHTMLTemplate).render(sites=blogs))

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
