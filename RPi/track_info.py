import os
from metadata_by_track_id import metadata
from PIL import Image, ImageDraw, ImageFont
import urllib.request


home_path="/home/pi/metadata/"

screensize=(1920, 1080)

track_info=metadata(os.environ["TRACK_ID"])

print(track_info["title"][0])
track_title=str(track_info["title"][0])


#new line of track_title is too long
new_line=0.0
line_br=len(track_title)//29
if line_br != 0:
    x1_len=0
    x2_len=29
    new_track_title=""
    for i in range(line_br):
        new_track_title+=track_title[x1_len:x2_len]+"\n"
        x1_len+=29
        x2_len+=29
    
    track_title=new_track_title+track_title[x1_len:]
    new_line=line_br*0.5


track_artists=""
for art in range(len(track_info["artists"])):
    track_artists+=str(track_info["artists"][art])+", "
track_artists=track_artists[0:-2]

#new line of track_artists is too long
line_br_artists=len(track_artists)//47
if line_br_artists != 0:
    ax1_len=0
    ax2_len=47
    new_track_artists=""
    for i in range(line_br_artists):
        new_track_artists=track_artists[ax1_len:ax2_len]+"\n"
        ax1_len+=47
        ax2_len+=47

    track_artists=new_track_artists+track_artists[ax1_len:]

print(screensize)

#get cover
urllib.request.urlretrieve("https://"+str(track_info["cover_url"][0]), f"{home_path}cache/cover_art.png")
cover_art=Image.open(f"{home_path}cache/cover_art.png")

img=Image.new("RGB", screensize, color="black")
#img.save("cache/test.png")

font_title=ImageFont.truetype("DejaVuSansMono.ttf", 65)
font_artists=ImageFont.truetype("DejaVuSansMono.ttf", 40)

d=ImageDraw.Draw(img)
d.text((screensize[0]/2.7, screensize[1]/(2+new_line)), track_title, font=font_title, fill=(255,255,255))
d.text((screensize[0]/2.7, screensize[1]/1.75), track_artists, font=font_artists, fill=(255,255,255))

img.paste(cover_art, (int(screensize[0]/5.1), int(screensize[1]/2.75)))

img.save(f"{home_path}cache/current_info.png")

os.system("sudo killall -9 fbi")
os.system("sudo fbi --noverbose -T 1 -d /dev/fb0 /home/pi/metadata/cache/current_info.png")
