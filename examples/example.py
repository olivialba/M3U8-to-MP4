from m3u8_to_mp4.m3u8 import M3U8_Playlist

## EXAMPLE from local file 
m3u8 = M3U8_Playlist('playlist-1.m3u8')
m3u8.to_mp4('test-1.mp4')

## EXAMPLE with URL and added segment
# The m3u8 playlist from this URL has segments that don't have a full link, 
# so we need to append the initial part of the link to the segments
m3u8 = M3U8_Playlist('URL:https://vz-cea98c59-23c.b-cdn.net/c309129c-27b6-4e43-8254-62a15c77c5ee/842x480/video.m3u8')
m3u8.append_to_segments('https://vz-cea98c59-23c.b-cdn.net/c309129c-27b6-4e43-8254-62a15c77c5ee/842x480/')
m3u8.to_mp4('test-2.mp4')