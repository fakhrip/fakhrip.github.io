from datetime import datetime
from subprocess import check_output
from os.path import isfile, join
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
        print("[|] Directory " , "/blogs" ,  " Created ")
    else:    
        print("[|] Directory " , "/blogs" ,  " already exists")
    
    print("[+] ===")
    print("[+] Converting /sites to /blogs")
    for site in allSites :
        print("[|] Working on '{}'".format(site))
        siteFile = open("./sites/" + site, "r")
        blogFile = open("./blogs/" + site.replace(".md","") + ".html", "w+")
        
        siteContent = siteFile.read()
        siteMD = siteContent.split("--+--+--+--\n")[1]
        siteMeta = siteContent.split("--+--+--+--\n")[0]
        convertedSite = markdown2.markdown(siteMD, extras = [
            "footnotes", 
            "fenced-code-blocks", 
            "tables", 
            "markdown-in-html",
            "target-blank-links"
        ])

        siteFile.close()

        for meta in siteMeta.split("\n"):
            if "Tags" == meta.split(": ")[0] :
                tags = meta.split(": ")[1].split("|")
            if "Times" == meta.split(": ")[0] :
                times = markdown2.markdown(meta.split(": ")[1], extras = [
                    "footnotes", 
                    "fenced-code-blocks", 
                    "tables", 
                    "markdown-in-html",
                    "target-blank-links"
                ])
            if "TLDR" == meta.split(": ")[0] :
                desc = meta.split(": ")[1]
                tldr = markdown2.markdown(meta.split(": ")[1], extras = [
                    "footnotes", 
                    "fenced-code-blocks", 
                    "tables", 
                    "markdown-in-html",
                    "target-blank-links"
                ])

        renderedResult = Template(ARTICLE_TEMPLATE).render(
            contents = convertedSite,
            updatedDate = datetime.fromtimestamp(blogLastUpdated, tz=timezone('Asia/Jakarta')).strftime("%B %d, %Y"),
            updatedTime = datetime.fromtimestamp(blogLastUpdated, tz=timezone('Asia/Jakarta')).strftime("%H:%M:%S"),
            tags = tags,
            times = times,
            tldr = tldr,
            site = site,
            desc = desc,
            title = site.replace('-',' ').replace('.md','')
        )

        blogFile.write(renderedResult)
        blogFile.close()

    print("[+] ===")
    print("[+] Injecting all sites to blogs.html")
    allBlogs = [f for f in os.listdir("./blogs") if isfile(join("./blogs", f))]
    allBlogs = sorted(allBlogs)
    
    with open("./templates/blogsTemplate.html", "r") as blogsHTMLFile :
        blogsHTMLTemplate = blogsHTMLFile.read()
    
        renderedResult = Template(blogsHTMLTemplate).render(sites = allBlogs)
        
        blogsFile = open("./blogs.html", "w+")
        blogsFile.write(renderedResult)
        blogsFile.close()

    print("[+] Updating date and time in index.html")
    cur_date = datetime.now(timezone('Asia/Jakarta')).strftime("%B %d, %Y")
    cur_time = datetime.now(timezone('Asia/Jakarta')).strftime("%H:%M:%S")

    github_urls = check_output('curl "https://api.github.com/users/fakhrip/repos?per_page=100" | jq "[ .[] | select(.archived == \"false\") | .html_url ]"', shell=True)
    github_urls = [url for url in json.loads(github_urls)]
    github_urls = sorted(github_urls)
    
    with open("./templates/indexTemplate.html", "r") as indexHTMLFile :
        indexHTMLTemplate = indexHTMLFile.read()

        renderedResult = Template(indexHTMLTemplate).render(
            github_urls = github_urls,
            updatedDate = cur_date, 
            updatedTime = cur_time
        )
        
        indexFile = open("./index.html", "w+")
        indexFile.write(renderedResult)
        indexFile.close()

if __name__ == "__main__" :
    main()