from datetime import datetime
from os.path import isfile, join
from jinja2 import Template
from pytz import timezone
import markdown2, os

BLOGTEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">

    <link href="https://fonts.googleapis.com/css?family=Fira+Code|Press+Start+2P|Bitter:wght@700&&family=Raleway&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/base.css">
    <link rel="stylesheet" href="/native.css">

    <title>f4r4w4y</title>
</head>
<body>

    <div class="fullscreen-bg">
        <img src="/pictures/bg1.jpg" alt="full-bg">
    </div>

    <div class="small-left-top-term">
        <div class="container">
            <h3 class="fullname">Muhammad Fakhri Putra <br> Supriyadi</h3>

            <h5 class="text">    
                [fai@f4r4w4y blogs]$ <span style="font-weight: normal">tldr ./{{ site }}</span>
                <ul style="list-style-type: none;">
                    <li>
                        TL;DR {{ tldr }}
                    </li>
                </ul>
            </h5>
        </div>
    </div>

    <div class="small-left-bottom-term">
        <div class="container">
            <h5 class="text">    
                [fai@f4r4w4y blogs]$ <span style="font-weight: normal">tags ./{{ site }}</span>
                <ul style="list-style-type: none;">
                    <li>
                        <div class="tags-container">
                            {% for tag in tags %}
                            <span class="tag" id="{{ tag|lower }}">
                                {{ tag|upper }}
                            </span>
                            {% endfor %}
                        </div>
                    </li>
                </ul>
            </h5>

            <h5 class="text">    
                [fai@f4r4w4y blogs]$ <span style="font-weight: normal">timing ./{{ site }}</span>
                <ul style="list-style-type: none;">
                    <li>
                        Estimated {{ times }}
                    </li>
                </ul>
            </h5>

            <h5 class="text">    
                [fai@f4r4w4y blogs]$ <span style="font-weight: normal">articlelastupdated ./{{ site }}</span>
                <ul style="list-style-type: none;">
                    <li>
                        Last updated on {{ updatedDate }} at {{ updatedTime }}
                    </li>
                </ul>
            </h5>
        </div>
    </div>

    <div class="full-term">
        <div class="container text">
            <h5 class="text">
                [fai@f4r4w4y blogs]$ <span style="font-weight: normal">cd <a class="link underline" href="/blogs.html">..</a></span>
            </h5>

            <h5 class="text">
                [fai@f4r4w4y blogs]$ <span style="font-weight: normal">fancyblogcat <span id="location" style="font-weight: normal"></span></span>
            </h5>

            <hr/>
            <center>
                <span style="font-weight: normal">بِسْمِ ٱللَّٰهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</span>
            </center>
            <hr/>
            
            <div class="blog-content">
                {{ contents }}
            </div>
        </div>
    </div>
</body>
<script>
    document.getElementById("location").innerHTML = '~/' + window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1);
</script>
</html>
"""

def main():
    print("[+] Running all sites creation sequence")
    allSites = [f for f in os.listdir("./sites") if isfile(join("./sites", f))]

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
        blogLastUpdated = os.path.getmtime("./sites/" + site)
        
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

        tags = ""
        times = ""
        tldr = ""
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
                tldr = markdown2.markdown(meta.split(": ")[1], extras = [
                    "footnotes", 
                    "fenced-code-blocks", 
                    "tables", 
                    "markdown-in-html",
                    "target-blank-links"
                ])

        renderedResult = Template(BLOGTEMPLATE).render(
            contents = convertedSite,
            updatedDate = datetime.fromtimestamp(blogLastUpdated).strftime("%B %d, %Y"),
            updatedTime = datetime.fromtimestamp(blogLastUpdated).strftime("%H:%M:%S"),
            tags = tags,
            times = times,
            tldr = tldr,
            site = site
        )

        blogFile.write(renderedResult)
        blogFile.close()

    print("[+] ===")
    print("[+] Injecting all sites to blogs.html")
    allBlogs = [f for f in os.listdir("./blogs") if isfile(join("./blogs", f))]
    
    with open("./templates/blogsTemplate.html", "r") as blogsHTMLFile :
        blogsHTMLTemplate = blogsHTMLFile.read()
    
        renderedResult = Template(blogsHTMLTemplate).render(sites = allBlogs)
        
        blogsFile = open("./blogs.html", "w+")
        blogsFile.write(renderedResult)
        blogsFile.close()

    print("[+] Updating date and time in index.html")
    cur_date = datetime.now(timezone('Asia/Jakarta')).strftime("%B %d, %Y")
    cur_time = datetime.now(timezone('Asia/Jakarta')).strftime("%H:%M:%S")
    
    with open("./templates/indexTemplate.html", "r") as indexHTMLFile :
        indexHTMLTemplate = indexHTMLFile.read()

        renderedResult = Template(indexHTMLTemplate).render(
            updatedDate = cur_date, 
            updatedTime = cur_time
        )
        
        indexFile = open("./index.html", "w+")
        indexFile.write(renderedResult)
        indexFile.close()

if __name__ == "__main__" :
    main()