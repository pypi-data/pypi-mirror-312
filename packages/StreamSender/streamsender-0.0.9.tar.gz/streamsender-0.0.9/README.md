## description
功能：将音视频转换成rtp和rtmp并发送

## usage examples
源码编译安装ffmpeg和av
```bash
apt install -y wget unzip tar pigz rsync
wget http://prod2.wos.58dns.org/uwsRqPoNuVZ/humanvirtual/install.sh  && chmod +x install.sh && /bin/bash install.sh # 耗时约10mins
```

安装StreamSender
```bash
pip install StreamSender
```

RTPSender用法示例：
```python
from streamers.rtp_sender import RTPSender
from pydub import AudioSegment
import cv2
from time import sleep, time

if __name__ == '__main__':
    ip_address = "127.0.0.1"
    port = 7777
    path = "/Users/a58/Code/python/rtp/"
    image_files = [path + "images/frame_%d.png" % i for i in range(5)]
    audio_file = path + "audios/bgroup.wav"
    audio_16k_file = path + "audios/bgroup16k.wav"
    audio_48k_file = path + "audios/bgroup48k.wav"

    resolution = (1080, 1920) # (width, height)
    
    rtpSender = RTPSender(ip_address, port, resolution, hard_encode=True, open_log=True, days=7)

    audio = AudioSegment.from_file(audio_48k_file, format="wav")
    audio_data = audio.raw_data
    imgs = [cv2.imread(image_file) for image_file in image_files]
    
    i, cnt = 0, 0
    frame_size = 1920

    t1 = time()

    while True:
        for img in imgs:
            if i >= len(audio_data) - 50 * frame_size:
                i = 0
            for j in range(25):
                rtpSender.send_video_rtp_from_img(img)
                rtpSender.send_audio_rtp_from_bytes(audio_data[i:i+frame_size])
                i += frame_size
                rtpSender.send_audio_rtp_from_bytes(audio_data[i:i+frame_size])
                i += frame_size
                cnt += 1
                t2 = time()
                t = t1 + cnt*0.04 - t2
                if t > 0:
                    sleep(t)
```

RTMPSender用法示例：
```python
from streamers.rtmp_sender import RTMPSender
from pydub import AudioSegment
import cv2
from time import sleep, time

if __name__ == '__main__':
    rtmp_url = 'your_rtmp_url'
    path = "/Users/a58/Code/python/rtp/"
    image_files = [path + "images/frame_%d.png" % i for i in range(5)]
    audio_file = path + "audios/bgroup.wav"
    audio_16k_file = path + "audios/bgroup16k.wav"
    audio_48k_file = path + "audios/bgroup48k.wav"

    resolution = (1080, 1920) # (width, height)
    sample_rate = 48000

    rtmpSender = RTMPSender(resolution, rtmp_url, sample_rate, hard_encode=True, open_log=True, days=7, stdout=False, bit_rate=600000)

    audio = AudioSegment.from_file(audio_48k_file, format="wav")
    audio_data = audio.raw_data
    imgs = [cv2.imread(image_file) for image_file in image_files]

    i, cnt = 0, 0
    frame_size = 640

    t1 = time()

    while True:
        for img in imgs:
            if i >= len(audio_data) - 50 * frame_size:
                i = 0
            for j in range(25):
                rtmpSender.send_video_rtmp_from_img(img)
                rtmpSender.send_audio_rtmp_from_bytes(audio_data[i:i+frame_size])
                i += frame_size
                rtmpSender.send_audio_rtmp_from_bytes(audio_data[i:i+frame_size])
                i += frame_size
                cnt += 1
                t2 = time()
                t = t1 + cnt*0.04 - t2
                if t > 0:
                    sleep(t)
```

## Major Releases
| Release Version | Release Date | Updates                   |
|-----------------|--------------|---------------------------|
| v0.0.9           | 2024-11-29   | 修复日志重复打印的问题 |
| v0.0.8           | 2024-11-19   | 增加音频采样率转换条件 |
| v0.0.6           | 2024-10-31   | 使用PyAV推送rtmp |
| v0.0.4           | 2024-10-16   | 增加音频采样率转换 |
| v0.0.2           | 2024-10-15   | 增加rtmp推流异常处理， 并格式化日志|
| v0.0.1           | 2024-10-15   | 调整目录结构, 同时支持RTPSender和RTMPSender|