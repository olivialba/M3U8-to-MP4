# M3U8-to-MP4
Python package to convert m3u8 playlists to mp4 videos using FFMPEG

## Install
Install using `pip install py-m3u8-to-mp4`

It also requires the user to have FFMPEG in their PATH, Download it [here](https://ffmpeg.org/download.html)

## Usage
Create an object using **`file = M3U8_Playlist('path_to_file.m3u8')`**\
For the path you can input a path to a local m3u8 file or a remote web link to it by using the prefix  "*URL:*"

Afterward, to convert the playlist to mp4, you can call **`file.to_mp4('output.mp4')`**.

*NOTE*: Using a weblink will automatically download the m3u8 file temporarily; the file will then get deleted when the mp4 is compiled.

Example:
```
m3u8 = M3U8_Playlist('playlist-1.m3u8')
m3u8.to_mp4('test-1.mp4')
```
### Special Case:
Segments without full links
```
m3u8 = M3U8_Playlist('URL:https://vz-cea98c59-23c.b-cdn.net/c309129c-27b6-4e43-8254-62a15c77c5ee/842x480/video.m3u8')
m3u8.append_to_segments('https://vz-cea98c59-23c.b-cdn.net/c309129c-27b6-4e43-8254-62a15c77c5ee/842x480/')
m3u8.to_mp4('test-2.mp4')
```
In this case, the link used as path will link to a m3u8 that has segments without full links:
```
#EXTINF:4.000000,
video0.ts
#EXTINF:4.000000,
video1.ts
#EXTINF:4.000000,
video2.ts
```
To get the .ts files of those segments and compile them together to a mp4, we need to get the full link\
You can use **append_to_segments()** to append a starting URL to each; which will result in this:
```
#EXTINF:4.000000,
https://vz-cea98c59-23c.b-cdn.net/c309129c-27b6-4e43-8254-62a15c77c5ee/842x480/video0.ts
#EXTINF:4.000000,
https://vz-cea98c59-23c.b-cdn.net/c309129c-27b6-4e43-8254-62a15c77c5ee/842x480/video1.ts
#EXTINF:4.000000,
https://vz-cea98c59-23c.b-cdn.net/c309129c-27b6-4e43-8254-62a15c77c5ee/842x480/video2.ts
```
Now we can call **to_mp4()** to compile it into a full mp4 video

## Details
`to_mp4(destination, delete_after, frame_rate, whitelist, run_async)`\
Convert the playlist to a mp4 video
- *destination* - path to the output mp4 file
- *delete_after* - will delete the m3u8 file after conversion, default for links ( URL: ) supplied as path is true
- *frame_rate* - frame/seconds of the resulting video
- *whitelist* - string of protocols allowed
- *run_async* - run conversion asynchronously

`append_to_segments(append_str)`\
Some m3u8 file may not have full URLs for each segments, use this to append a starting URL to the start of each segment in the m3u8 playlist.
This function will check if each segment starts with a valid http link. If it does, it will not append!
- *append_str* - prefix that is appended to each segment

`setHeaders(headers)`\
Set the header that will be used when making a GET request in the case of using a weblink for the m3u8 file and not local
- *headers* - header used for get request