# Introduction

In an online landscape of ever increasing censorship, creators on YouTube providing "controversial" or "dangerous" information disappear from the platform on a daily basis.
This script was created to preserve this knowledge locally on a user's machine, and to prevent Big Tech from completely silencing these creators.

# Disclaimer

**USE AT YOUR OWN RISK!!!** 

This script circumnavigates the YouTube API, and instead scrapes links from YouTube with Selenium. This might be against Google/YouTube policies.
Due to the use of Selenium to gather links, if YouTube changes the structure of their website, this script might stop working.
Also, this is meant to be used as an archive tool, not as a tool to steal intellectual property from YouTube creators. 
The creator of this script is not responsible for how you use it.

**YOU HAVE BEEN WARNED!!!**

# Prerequisites

The following packages are required to run this script:
```
requests
pytube
schedule
selenium
```
They can be installed like so: `pip install <package name>`

# Usage

Open the script and add the links to the YouTube channels you wish to monitor to the `channel_urls` list. Next, change the `download_root_path` to your desired download directory.

This is intended to run on a dedicated machine/server.

# Version Notes

## v1.0
- Initial release
