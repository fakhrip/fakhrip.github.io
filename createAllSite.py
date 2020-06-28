from datetime import date, datetime
from os.path import isfile, join
from jinja2 import Template
from os import listdir
import markdown2

BLOGTEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">

    <link href="https://fonts.googleapis.com/css?family=Fira+Code|Press+Start+2P&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/base.css">
    <link rel="stylesheet" href="/native.css">

    <title>f4r4w4y</title>
</head>
<body>

    <div class="fullscreen-bg">
        <img src="/pictures/bg1.jpg" alt="full-bg">
    </div>

    <div class="full-term">
        <div class="container text">
            <h5 class="text">
                [fai@f4r4w4y ~]$ cd <a class="link underline" href="/index.html">..</a> 
            </h5>

            <h5 class="text">
                [fai@f4r4w4y ~]$ cat <span id="location" style="font-weight: normal"></span> 
            </h5>

            {{ contents }}
        </div>
    </div>
</body>
<script>
document.getElementById("location").innerHTML = '~' + window.location.pathname;
</script>
</html>
"""

def main():
    print("[+] Running all sites creation sequence")
    allSites = [f for f in listdir("./sites") if isfile(join("./sites", f))]
    
    print("[+] Converting /sites to /blogs")
    for site in allSites :
        siteFile = open("./sites/" + site, "r")
        blogFile = open("./blogs/" + site.replace(".md","") + ".html", "w+")
        
        convertedSite = markdown2.markdown(siteFile.read(), extras = [
            "footnotes", 
            "fenced-code-blocks", 
            "tables", 
            "markdown-in-html",
            "target-blank-links"
        ])

        siteFile.close()

        renderedResult = Template(BLOGTEMPLATE).render(contents = convertedSite)

        blogFile.write(renderedResult)
        blogFile.close()

    print("[+] Injecting all sites to blogs.html")
    allBlogs = [f for f in listdir("./blogs") if isfile(join("./blogs", f))]
    
    with open("./blogs.html", "r") as blogsHTMLFile :
        blogsHTMLTemplate = blogsHTMLFile.read()
    
        renderedResult = Template(blogsHTMLTemplate).render(sites = allBlogs)
        
        blogsFile = open("./blogs.html", "w+")
        blogsFile.write(renderedResult)
        blogsFile.close()

    print("[+] Updating date and time in index.html")
    cur_date = date.today().strftime("%B %d, %Y")
    cur_time = datetime.now().strftime("%H:%M:%S")
    
    with open("./index.html", "r") as indexHTMLFile :
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