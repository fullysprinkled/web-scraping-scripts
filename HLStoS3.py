import boto3
import subprocess
from urllib.parse import urlparse, unquote
import ffmpeg

# aws creds
aws_access_key = 'YOURS_HERE'
aws_secret_key = 'YOURS_HERE'
aws_s3_bucket = 'YOURS_HERE'
aws_s3_path = 'YOURS_HERE'

# create s3 instance with boto3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

# convert the hls stream from m3u8 url
def download_and_convert_hls_video(hls_url):
    # Parse the URL to get the video filename
    parsed_url = urlparse(hls_url)
    video_filename = unquote(parsed_url.path.split('/')[-1]).replace('.m3u8', '.mp4')

    # download and convert the video in memory using ffmpeg
    try:
        input_stream = ffmpeg.input(hls_url)
        output_stream = ffmpeg.output(input_stream, video_filename, vcodec='libx264', acodec='aac', audio_bitrate='128k', preset='fast', crf='22', f='mp4', movflags='faststart')
        ffmpeg.run(output_stream, overwrite_output=True)
    except ffmpeg.Error as e:
        raise Exception(f'Error downloading and converting video: {str(e)}')

    # store the video in memory
    with open(video_filename, 'rb') as f:
        mp4_data = f.read()

    return video_filename, mp4_data


# download & convert 
hls_url = 'https://assets.afcdn.com/video49/20210722/v_645516.m3u8' #this is a sample
mp4_filename, mp4_data = download_and_convert_hls_video(hls_url)
s3_path = aws_s3_path + mp4_filename
s3.upload_fileobj(mp4_data, aws_s3_bucket, s3_path)
print(f'{mp4_filename} uploaded to S3 at {s3_path}')
