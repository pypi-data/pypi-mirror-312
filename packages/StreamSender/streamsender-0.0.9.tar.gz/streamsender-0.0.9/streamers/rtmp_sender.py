import av
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from time import time
from loguru import logger
from datetime import timedelta
import numpy as np
import io
import soundfile as sf
import librosa

class RTMPSender:
    def __init__(self, frame_size, rtmp_url, sample_rate, my_logger=None, gop=25, hard_encode=False, open_log=False, days=7, stdout=False, log_dir='./rtmp_logs/', bit_rate=600000):
        self.image_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        self.hard_encode = hard_encode
        self.open_log = open_log
        self.gop = gop
        self.logger = my_logger
        self.rtmp_url = rtmp_url
        self.original_sample_rate = sample_rate

        # 默认video img RTMP header参数
        self.RTMP_VIDEO_IMG_TIMESTAMP = 0
        # 默认音频bytes RTMP header 参数
        self.RTMP_AUDIO_BYTES_TIMESTAMP = 0

        self.img_rtmp_sent_total_time = 0
        self.img_rtmp_sent_total_cnt = 0
        self.img_encode_total_time = 0
        self.img_encode_total_cnt = 0
        self.audio_rtmp_sent_total_time = 0
        self.audio_rtmp_sent_total_cnt = 0
        self.audio_encode_total_time = 0
        self.audio_encode_total_cnt = 0
        self.video_packet_total_cnt = 0
        self.audio_packet_total_cnt = 0

        # 初始化输出容器
        self.output_container = av.open(self.rtmp_url, mode='w', format='flv')

        if self.logger is None:
            if not stdout:
                logger.remove() # 移除默认的日志记录器：控制台打印
            logger.add(
                log_dir + "rtmp_sender.{time:YYYY-MM-DD_HH}.log", 
                rotation="1 hour",  # 每小时创建一个新日志文件
                retention=timedelta(days=days),  # 保留最近days天的日志，默认为7天
                compression=None,  # 不压缩日志文件
                format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {message}"
            )
            self.logger = logger

        # 音频编码器
        self.target_sample_rates = [44100, 48000]
        # 如果原始采样率不在目标采样率列表中，则使用 48kHz 作为目标采样率
        self.target_sample_rate = self.original_sample_rate if self.original_sample_rate in self.target_sample_rates else 48000
        self.audio_stream = self.output_container.add_stream('aac', rate=self.target_sample_rate)
        self.audio_stream.channels = 1
        self.audio_stream.layout = 'mono'  # 声道布局为单声道
        self.audio_stream.format = 'fltp'  # AAC 格式通常使用浮点数据
        # self.audio_stream.bit_rate = 256000

        # 创建视频流
        if self.hard_encode:
            if self.open_log:
                self.logger.info("Using hard encoding...")
            # 视频编码器
            self.video_stream = self.output_container.add_stream('h264_nvenc', rate=25)
            self.video_stream.options = {
                'bf': '0',       # 禁用B帧
                'delay': '0',     # 设置delay为0
                'g': str(self.gop)   # 设置gop大小为25帧
            }
            self.video_stream.pix_fmt = 'yuv420p'
        else:
            if self.open_log:
                self.logger.info("Using soft encoding...")
            self.video_stream = self.output_container.add_stream('libx264', rate=25)
            self.video_stream.options = {'g': str(self.gop), 'tune': 'zerolatency'}  # 设置GOP大小为25帧，实现低延迟

        self.video_stream.bit_rate = bit_rate
        if self.open_log:
            self.logger.info(f'output_container: {self.output_container}')

        if self.open_log:
            self.logger.info(f"Video stream bit rate: {self.video_stream.bit_rate} bps")
        
        if self.open_log:
            self.logger.info(f"Video stream options: {self.video_stream.options}")

        self.video_stream.width = frame_size[0]
        self.video_stream.height = frame_size[1]

        self.stop_event = threading.Event()

        self.video_thread = threading.Thread(target=self.process_video_queue)
        self.audio_thread = threading.Thread(target=self.process_audio_queue)

        self.video_thread.start()
        self.audio_thread.start()

    def stop(self):
        def stop_threads():
            self.stop_event.set()
            self.video_thread.join()
            self.audio_thread.join()
            if self.open_log:
                self.logger.info("All threads have been successfully stopped.")

            self.output_container.close()
            if self.open_log:
                self.logger.info("Output container successfully closed.")

        if self.open_log:
            self.logger.info("Stopping all active threads...")

        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(stop_threads)
        executor.shutdown(wait=False)
    
    def resample_audio_bytes(self, input_bytes, original_rate, target_rate):
        # 将字节数据转换为 numpy 数组（假设 input_bytes 是 PCM s16le 格式）
        pcm_data = np.frombuffer(input_bytes, dtype=np.int16)
        
        # PCM 数据是单声道
        pcm_data = pcm_data.astype(np.float32) / 32768.0  # 将数据归一化到[-1, 1]

        # 重新采样
        resampled_data = librosa.resample(pcm_data, orig_sr=original_rate, target_sr=target_rate)

        # 将重新采样后的数据还原到 PCM s16le 格式
        resampled_data = (resampled_data * 32768.0).astype(np.int16)
        
        # 转换为字节流
        output_buffer = io.BytesIO()
        sf.write(output_buffer, resampled_data, samplerate=target_rate, subtype='PCM_16', format='RAW')

        return output_buffer.getvalue()
    

    def send_video_rtmp_from_img(self, img):
        self.image_queue.put(img)

    def process_video_queue(self):
        if self.open_log:
            self.logger.info("Started processing video queue from image stream.")

        while not self.stop_event.is_set():
            try:
                img = self.image_queue.get(block=True, timeout=5)
                if self.open_log:
                    self.logger.info(f"Current size of image_queue: {self.image_queue.qsize()}.")
            except queue.Empty:
                continue

            encode_begin = time()
            img_frame = av.VideoFrame.from_ndarray(img, format = 'rgb24')
            packets = self.video_stream.encode(img_frame)
            encode_end = time()
            cur_encode_cost_time = (encode_end - encode_begin) * 1000
            self.img_encode_total_time += cur_encode_cost_time
            self.img_encode_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Image encoding #{self.img_encode_total_cnt}: {cur_encode_cost_time:.6f} ms")
                avg_time = self.img_encode_total_time / self.img_encode_total_cnt
                self.logger.info(f"Average image encode time: {avg_time:.6f} ms over {self.img_encode_total_cnt} encodes.")

            send_begin = time()

            for packet in packets:
                self.video_packet_total_cnt += 1
                
                packet.dts = self.RTMP_VIDEO_IMG_TIMESTAMP 
                packet.pts = self.RTMP_VIDEO_IMG_TIMESTAMP
                self.RTMP_VIDEO_IMG_TIMESTAMP += 1
                self.output_container.mux(packet)
                if self.open_log:
                    self.logger.info(f"Video Packet #{self.video_packet_total_cnt} sent successfully.")
                
            send_end = time()
            cur_img_send_cost_time = (send_end - send_begin) * 1000
            self.img_rtmp_sent_total_time += cur_img_send_cost_time
            self.img_rtmp_sent_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Image RTMP send #{self.img_rtmp_sent_total_cnt}: {cur_img_send_cost_time:.6f} ms")
                avg_time = self.img_rtmp_sent_total_time / self.img_rtmp_sent_total_cnt
                self.logger.info(f"Average image RTMP send time: {avg_time:.6f} ms over {self.img_rtmp_sent_total_cnt} sends.")


    def send_audio_rtmp_from_bytes(self, audio_bytes):
        self.audio_queue.put(audio_bytes)


    def process_audio_queue(self):
        if self.open_log:
            self.logger.info("Started processing audio queue from byte stream.")

        while not self.stop_event.is_set():
            try:
                audio_data = self.audio_queue.get(block=True, timeout=5)
                if self.open_log:
                    self.logger.info(f"Current size of audio_queue: {self.audio_queue.qsize()}.")
            except queue.Empty:
                continue
            
            if self.original_sample_rate not in self.target_sample_rates:
                resample_begin = time()
                audio_data = self.resample_audio_bytes(audio_data, original_rate=self.original_sample_rate, target_rate=self.target_sample_rate)
                resample_end = time()
                cur_resample_cost_time = (resample_end - resample_begin) * 1000
                if self.open_log:
                    self.logger.info(f"Audio resampling time: {cur_resample_cost_time:.6f} ms")

            encode_begin = time()
            pcm_array = np.frombuffer(audio_data, dtype=np.int16).reshape(1, -1)
            
            audio_frame = av.AudioFrame.from_ndarray(pcm_array, format="s16", layout='mono')
            audio_frame.sample_rate = self.target_sample_rate

            if not self.audio_stream.codec_context.is_open:
                self.audio_stream.codec_context.open()

            packets = self.audio_stream.encode(audio_frame)
            encode_end = time()
            cur_encode_cost_time = (encode_end - encode_begin) * 1000
            self.audio_encode_total_time += cur_encode_cost_time
            self.audio_encode_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Audio encoding #{self.audio_encode_total_cnt}: {cur_encode_cost_time:.6f} ms")
                avg_time = self.audio_encode_total_time / self.audio_encode_total_cnt
                self.logger.info(f"Average audio encode time: {avg_time:.6f} ms over {self.audio_encode_total_cnt} encodes.")

            audio_send_begin = time()
            for packet in packets:
                self.audio_packet_total_cnt += 1
                packet.dts = self.RTMP_AUDIO_BYTES_TIMESTAMP
                packet.pts = self.RTMP_AUDIO_BYTES_TIMESTAMP
                self.RTMP_AUDIO_BYTES_TIMESTAMP += 1000
                self.output_container.mux(packet)
                if self.open_log:
                    self.logger.info(f"Audio Packet #{self.audio_packet_total_cnt} sent successfully.")

            audio_send_end = time()
            cur_audio_send_cost_time = (audio_send_end - audio_send_begin) * 1000
            self.audio_rtmp_sent_total_time += cur_audio_send_cost_time
            self.audio_rtmp_sent_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Audio RTMP send #{self.audio_rtmp_sent_total_cnt}: {cur_audio_send_cost_time:.6f} ms")
                avg_time = self.audio_rtmp_sent_total_time / self.audio_rtmp_sent_total_cnt
                self.logger.info(f"Average audio RTMP send time: {avg_time:.6f} ms over {self.audio_rtmp_sent_total_cnt} sends.")
