#!/usr/bin/env ython
#
#_____.___.           ___________   ___.
#\__  |   | ____  __ _\__    ___/_ _\_ |__   ____
# /   |   |/  _ \|  |  \|    | |  |  \ __ \_/ __ \
# \____   (  <_> )  |  /|    | |  |  / \_\ \  ___/
# / ______|\____/|____/ |____| |____/|___  /\___  >
# \/                                     \/     \/
#__________                                          .__               __
#\______   \_______   ____   ______ ______________  _|__| ____ _____ _/  |_  ___________
# |     ___/\_  __ \_/ __ \ /  ___// __ \_  __ \  \/ /  |/    \\__  \\   __\/  _ \_  __ \
# |    |     |  | \/\  ___/ \___ \\  ___/|  | \/\   /|  |   |  \/ __ \|  | (  <_> )  | \/
# |____|     |__|    \___  >____  >\___  >__|    \_/ |__|___|  (____  /__|  \____/|__|   v1.0
#
# By Brad Nelson (Squ1rr3l)

import os
import requests
import schedule
import time
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome

channel_urls = ['CHANGE_ME', 'AND_CHANGE_ME']   # Change to the desired YouTube channel URLs separated by commas.
download_root_path = 'CHANGE_ME'                # Change to desired file path to save videos to.

def get_channel_video_links(channel_url):
    print('Checking for videos on ' + channel_url + '...')
    response = requests.get(channel_url)

    # Check to make sure YouTube Channel exists
    if response.status_code != 200:
        print(f'Failed to retrieve the channel page. Status code: {response.status_code}')
        return []

    # Check to make sure the videos section exists
    uploads_playlist_url = channel_url + '/videos'
    uploads_response = requests.get(uploads_playlist_url)
    if uploads_response.status_code != 200:
        print(f'Failed to retrieve the "Videos" list. Status code: {uploads_response.status_code}')
        return []

    # Get the links to all the videos on the channel
    print('Getting all them video links...')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.page_load_strategy = 'none'
    driver = Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(uploads_playlist_url)
    time.sleep(20)
    lnks=driver.find_elements(By.ID,'video-title-link')

    # Put them links in a list!
    print('Video links found: \n')
    video_links = []
    for lnk in lnks:
        print(lnk.get_attribute('href'))
        video_links.append(lnk.get_attribute('href'))
    driver.quit()

    return video_links

def download_video(video_url, output_path='.'):
    try:
        yt = YouTube(video_url)
        title = yt.title
        video_stream = yt.streams.get_highest_resolution()

        # Create a directory for the channel if it doesn't exist
        channel_directory = os.path.join(output_path, yt.author)
        if not os.path.exists(channel_directory):
            os.makedirs(channel_directory)

        # Download the video and place it in the channel directory
        download_path = os.path.join(channel_directory, f'{title}.mp4')
        print(f'Downloading: {title}')
        print(f'Resolution: {video_stream.resolution}')
        print(f'Size: {round(video_stream.filesize / (1024 * 1024), 2)} MB')
        video_stream.download(download_path)
        print('Download complete!')

    except Exception as e:
        print(f'Error: {e}')

def check_for_new_videos(channel_url, download_path='.'):
    print(f'Checking for new videos on {channel_url}...')
    new_video_links = get_channel_video_links(channel_url)

    # Compare with the previously stored video links
    new_videos = list(set(new_video_links) - set(previous_video_links[channel_url]))

    if new_videos:
        print('New videos found:')
        for link in new_videos:
            print(link)
            download_video(link, download_path)
    else:
        print('No new videos found.')

    # Update the previous_video_links list for this channel
    previous_video_links[channel_url].extend(new_video_links)

if __name__ == '__main__':

    first_time = 'y'
    
    # Check if it's the first time starting this script
    if first_time == 'y':

        # Initial download
        for channel_url in channel_urls:
            video_urls = get_channel_video_links(channel_url)

            for video_url in video_urls:
                download_video(video_url, download_root_path)

        first_time = 'n'
    
    # After first go through
    else:
        # Set up a schedule to check for new videos for each channel once a day
        for channel_url in channel_urls:
            schedule.every().hour.do(check_for_new_videos, channel_url=channel_url, download_path=download_root_path)


        # Get video links to compare with new links
        previous_video_links = {channel_url: get_channel_video_links(channel_url) for channel_url in channel_urls}

        # Run the schedule loop
        while True:
            schedule.run_pending()
            time.sleep(1)
