import ffmpeg, os, requests
from m3u8_to_mp4.exceptions import InvalidPathM3U8, InvalidUrlM3U8

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

class M3U8_Playlist():
    """
    Class object for getting and converting a m3u8 file to mp4
    """
    
    EXTENSION = '.m3u8'
    TEMP_FILE = 'TEMPao2_m3u8_to_mp4'
    
    def __init__(self, path: str):
        """
        The `path` argument can also accept a URL by using the prefix `URL:`
        
        The file will be downloaded and deleted after the conversion to mp4 using `to_mp4`.
        
        Examples:
        - `M3U8_Playlist('src/file/playlist.m3u8')`
        - `M3U8_Playlist('URL:https://example.com/videos/video123.m3u8')`
        """
        self.isUrl = False
        self.isReady = False
        self.headers = {'User-Agent': USER_AGENT}
        if path: 
            self.__get_m3u8(path) 
        else: 
            raise InvalidPathM3U8
        
    def setHeaders(self, headers):
        self.headers = headers
    
    def append_to_segments(self, append_str: str):
        """
        Some m3u8 file may not have full URLs for each segments, use this to append a starting URL
        to the start of each segment in the m3u8 playlist.
        
        `append_to_segments` will check if each segment starts with a valid http link. If it does, it will not append!
        
        Example:
        - Segment: `video0.ts`
        - Call: `append_to_segments('https://vz-cea98c59-23c.b-cdn.net/840x720/')`
        - Segment: `https://vz-cea98c59-23c.b-cdn.net/840x720/video0.ts`
        """
        with open(self.m3u8_path, 'r') as f:
            lines = f.readlines()

        with open(self.m3u8_path, 'w') as f:
            for line in lines:
                stripped_line = line.strip()
                if stripped_line.startswith('#'):
                    # Special handling for audio playlist references
                    if 'URI=' in stripped_line:
                        # Find the URI part and replace it with the full URL
                        parts = stripped_line.split('URI="')
                        if len(parts) > 1:
                            uri_part = parts[1].rsplit('"', 1)[0]
                            if not uri_part.startswith('http'):
                                new_uri = append_str + uri_part
                                f.write(parts[0] + 'URI="' + new_uri + '"\n')
                                continue
                    f.write(line)
                else:
                    # Handle regular segments
                    if stripped_line and not stripped_line.startswith('http'):
                        f.write(append_str + line)
                    else:
                        f.write(line)

                        
    def to_mp4(self, destination: str, delete_after: bool=None, frame_rate: int=30, whitelist: str='file,tcp,tls,http,https', run_async: bool=False):
        """
        - `destination` is the path to the output mp4 file.
        - `delete_after` will delete the m3u8 file after conversion, default for links ( URL: ) supplied as path is true.
        - `frame_rate` frame/seconds of the resulting video.
        - `whitelist` string of protocols allowed.
        - `run_async` run conversion asynchronously.
        """
        if not self.isReady: return
        if not os.path.exists(self.m3u8_path): raise InvalidPathM3U8
        input_m3u8 = self.m3u8_path
        try:
            playlist = ffmpeg.input(input_m3u8, protocol_whitelist=whitelist)
            playlist = ffmpeg.output(
                playlist,
                destination,
                r=frame_rate,
                vcodec='copy', # Copy video stream without re-encoding
                acodec='aac'  # Use AAC codec for audio
            )

            if run_async:
                playlist.run_async()
            else:
                playlist.run()
        finally:
            if self.__should_delete(delete_after) and os.path.isfile(input_m3u8):
                os.remove(input_m3u8)



    ### PRIVATE ###
    
    def __get_m3u8(self, m3u8):
        # If path is URL
        if m3u8.startswith("URL:"):
            # Get URL link
            m3u8_url = m3u8[len('URL:'):] 
            self.isUrl = True
            
            # Get name for new file to download
            self.m3u8_path = self.__get_temp_filename()
            
            # GET request with arguments, if they were set
            response = requests.get(m3u8_url, headers=self.headers)
                
            # Write to m3u8 file
            if response.status_code < 300:
                with open(self.m3u8_path, 'wb') as f:
                    f.write(response.content)
                self.isReady = True
            else:
                self.isReady = False
                raise InvalidUrlM3U8
            return
        
        # If path is not URL
        self.isUrl = False
        if os.path.isfile(m3u8) and os.path.splitext(m3u8)[1] == self.EXTENSION:
            self.m3u8_path = m3u8
            self.isReady = True
        else:
            self.isReady = False
            raise InvalidPathM3U8

    def __should_delete(self, delete_after):
        if ((self.isUrl and delete_after is None) or delete_after is True):
            return True
        else:
            return False
    
    def __get_temp_filename(self) -> str:
        count = 0
        while os.path.exists(self.TEMP_FILE + str(count) + self.EXTENSION):
            count += 1
        return self.TEMP_FILE + str(count) + self.EXTENSION