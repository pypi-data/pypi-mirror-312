import cv2
import av
from pydub import AudioSegment
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
import ctypes
import copy
import socket
from loguru import logger
from datetime import timedelta
from time import time
import sys

class RTPSender:
    def __init__(self, ip_address, port, frame_size, my_logger=None, gop=25, hard_encode=False, open_log=False, days=7, stdout=False, log_dir='./rtp_logs/', bit_rate=600000):
        self.image_queue = queue.Queue()
        self.audio_queue = queue.Queue()
        self.image_queue2 = queue.Queue()
        self.audio_queue2 = queue.Queue()
        self.image_file = ""
        self.audio_file = ""
        self.ip_address = ip_address
        self.port = port
        self.output_path = 'output.mp4'
        self.hard_encode = hard_encode
        self.open_log = open_log
        self.gop = gop
        self.logger = my_logger

        self.RTP_VERSION = 2
        self.RTP_SSRC = 12345

        # 默认video file RTP header参数
        self.RTP_VIDEO_PAYLOAD_TYPE = 96
        self.RTP_VIDEO_FILE_SEQUENCE_NUMBER = 0
        self.RTP_VIDEO_FILE_TIMESTAMP = 0

        # 默认video img RTP header参数
        self.RTP_VIDEO_IMG_SEQUENCE_NUMBER = 0
        self.RTP_VIDEO_IMG_TIMESTAMP = 0

        # 默认音频file RTP header 参数
        self.RTP_AUDIO_PAYLOAD_TYPE = 97
        self.RTP_AUDIO_FILE_SEQUENCE_NUMBER = 0
        self.RTP_AUDIO_FILE_TIMESTAMP = 0

        # 默认音频bytes RTP header 参数
        self.RTP_AUDIO_BYTES_SEQUENCE_NUMBER = 0
        self.RTP_AUDIO_BYTES_TIMESTAMP = 0

        self.max_payload_size = 1400

        self.img_rtp_sent_total_time = 0
        self.img_rtp_sent_total_cnt = 0
        self.img_encode_total_time = 0
        self.img_encode_total_cnt = 0
        self.audio_rtp_sent_total_time = 0
        self.audio_rtp_sent_total_cnt = 0

        # 初始化输出容器
        self.output_container = av.open(self.output_path, mode='w')

        if self.logger is None:
            logger.remove()
            if stdout:
                # 添加控制打印
                logger.add(sys.stdout, format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {message}")
            logger.add(
                log_dir + "rtp_sender.{time:YYYY-MM-DD_HH}.log", 
                rotation="1 hour",  # 每小时创建一个新日志文件
                retention=timedelta(days=days),  # 保留最近days天的日志，默认为7天
                compression=None,  # 不压缩日志文件
                format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {message}"
            )
            self.logger = logger

        # 创建视频流
        if self.hard_encode:
            if self.open_log:
                self.logger.info("Using hard encoding...")
                # print("use hard_encode...")
            self.video_stream = self.output_container.add_stream('h264_nvenc', rate=25)
            self.video_stream.options = {
            # 'preset': 'll',  # 低延迟预设
                'bf': '0',       # 禁用B帧
                'delay': '0',     # 设置delay为0
                'g': str(self.gop)   # 设置gop大小为25帧
            }
            self.video_stream.pix_fmt = 'yuv420p'
        else:
            if self.open_log:
                self.logger.info("Using soft encoding...")
                # print("use soft_encode...")
            self.video_stream = self.output_container.add_stream('libx264', rate=25)
            self.video_stream.options = {'g': str(self.gop), 'tune': 'zerolatency'}  # 设置GOP大小为25帧，实现低延迟
        # self.video_stream = self.output_container.add_stream('h264', rate=25)

        # self.video_stream.options = {'g': str(1)}
        self.video_stream.bit_rate = bit_rate

        if self.open_log:
            self.logger.info(f"Video stream bit rate: {self.video_stream.bit_rate} bps")
        
        if self.open_log:
            self.logger.info(f"Video stream options: {self.video_stream.options}")

        self.video_stream.width = frame_size[0]
        self.video_stream.height = frame_size[1]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 655360)  # 设置为64KB

        self.stop_event = threading.Event()

        # self.video_thread = threading.Thread(target=self.process_video_queue)
        self.video_thread2 = threading.Thread(target=self.process_video_queue2)
        # self.audio_thread = threading.Thread(target=self.process_audio_queue)
        self.audio_thread2 = threading.Thread(target=self.process_audio_queue2)

        # self.video_thread.start()
        self.video_thread2.start()
        # self.audio_thread.start()
        self.audio_thread2.start()

    def stop(self):
        def stop_threads():
            self.stop_event.set()
            # self.video_thread.join()
            self.video_thread2.join()
            # self.audio_thread.join()
            self.audio_thread2.join()
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

    def create_video_file_rtp_packet(self, payload, marker=0):
        rtp_header = bytearray(12)

        # 设置 RTP Header
        rtp_header[0] = (self.RTP_VERSION << 6)
        rtp_header[1] = (marker << 7) | self.RTP_VIDEO_PAYLOAD_TYPE
        rtp_header[2] = (self.RTP_VIDEO_FILE_SEQUENCE_NUMBER >> 8) & 0xFF
        rtp_header[3] = self.RTP_VIDEO_FILE_SEQUENCE_NUMBER & 0xFF
        rtp_header[4] = (self.RTP_VIDEO_FILE_TIMESTAMP >> 24) & 0xFF
        rtp_header[5] = (self.RTP_VIDEO_FILE_TIMESTAMP >> 16) & 0xFF
        rtp_header[6] = (self.RTP_VIDEO_FILE_TIMESTAMP >> 8) & 0xFF
        rtp_header[7] = self.RTP_VIDEO_FILE_TIMESTAMP & 0xFF
        rtp_header[8] = (self.RTP_SSRC >> 24) & 0xFF
        rtp_header[9] = (self.RTP_SSRC >> 16) & 0xFF
        rtp_header[10] = (self.RTP_SSRC >> 8) & 0xFF
        rtp_header[11] = self.RTP_SSRC & 0xFF

        
        return rtp_header + payload
    
    def create_video_img_rtp_packet(self, payload, marker=0):
        rtp_header = bytearray(12)

        # 设置 RTP Header
        rtp_header[0] = (self.RTP_VERSION << 6)
        rtp_header[1] = (marker << 7) | self.RTP_VIDEO_PAYLOAD_TYPE
        rtp_header[2] = (self.RTP_VIDEO_IMG_SEQUENCE_NUMBER >> 8) & 0xFF
        rtp_header[3] = self.RTP_VIDEO_IMG_SEQUENCE_NUMBER & 0xFF
        rtp_header[4] = (self.RTP_VIDEO_IMG_TIMESTAMP >> 24) & 0xFF
        rtp_header[5] = (self.RTP_VIDEO_IMG_TIMESTAMP >> 16) & 0xFF
        rtp_header[6] = (self.RTP_VIDEO_IMG_TIMESTAMP >> 8) & 0xFF
        rtp_header[7] = self.RTP_VIDEO_IMG_TIMESTAMP & 0xFF
        rtp_header[8] = (self.RTP_SSRC >> 24) & 0xFF
        rtp_header[9] = (self.RTP_SSRC >> 16) & 0xFF
        rtp_header[10] = (self.RTP_SSRC >> 8) & 0xFF
        rtp_header[11] = self.RTP_SSRC & 0xFF
        
        return rtp_header + payload
    
    def create_audio_file_rtp_packet(self, payload, marker=0):
        rtp_header = bytearray(12)

        # 设置 RTP Header
        rtp_header[0] = (self.RTP_VERSION << 6)
        rtp_header[1] = (marker << 7) | self.RTP_AUDIO_PAYLOAD_TYPE
        rtp_header[2] = (self.RTP_AUDIO_FILE_SEQUENCE_NUMBER >> 8) & 0xFF
        rtp_header[3] = self.RTP_AUDIO_FILE_SEQUENCE_NUMBER & 0xFF
        rtp_header[4] = (self.RTP_AUDIO_FILE_TIMESTAMP >> 24) & 0xFF
        rtp_header[5] = (self.RTP_AUDIO_FILE_TIMESTAMP >> 16) & 0xFF
        rtp_header[6] = (self.RTP_AUDIO_FILE_TIMESTAMP >> 8) & 0xFF
        rtp_header[7] = self.RTP_AUDIO_FILE_TIMESTAMP & 0xFF
        rtp_header[8] = (self.RTP_SSRC >> 24) & 0xFF
        rtp_header[9] = (self.RTP_SSRC >> 16) & 0xFF
        rtp_header[10] = (self.RTP_SSRC >> 8) & 0xFF
        rtp_header[11] = self.RTP_SSRC & 0xFF
        
        return rtp_header + payload
    
    def create_audio_bytes_rtp_packet(self, payload, marker=0):
        rtp_header = bytearray(12)

        # 设置 RTP Header
        rtp_header[0] = (self.RTP_VERSION << 6)
        rtp_header[1] = (marker << 7) | self.RTP_AUDIO_PAYLOAD_TYPE
        rtp_header[2] = (self.RTP_AUDIO_BYTES_SEQUENCE_NUMBER >> 8) & 0xFF
        rtp_header[3] = self.RTP_AUDIO_BYTES_SEQUENCE_NUMBER & 0xFF
        rtp_header[4] = (self.RTP_AUDIO_BYTES_TIMESTAMP >> 24) & 0xFF
        rtp_header[5] = (self.RTP_AUDIO_BYTES_TIMESTAMP >> 16) & 0xFF
        rtp_header[6] = (self.RTP_AUDIO_BYTES_TIMESTAMP >> 8) & 0xFF
        rtp_header[7] = self.RTP_AUDIO_BYTES_TIMESTAMP & 0xFF
        rtp_header[8] = (self.RTP_SSRC >> 24) & 0xFF
        rtp_header[9] = (self.RTP_SSRC >> 16) & 0xFF
        rtp_header[10] = (self.RTP_SSRC >> 8) & 0xFF
        rtp_header[11] = self.RTP_SSRC & 0xFF
        
        return rtp_header + payload
    
    def send_video_rtp_from_file(self, image_file):

        img = cv2.imread(image_file)
        img_frame = av.VideoFrame.from_ndarray(img, format='rgb24')
        packets = self.video_stream.encode(img_frame)

        for packet in packets:
            buffer_ptr = packet.buffer_ptr
            buffer_size = packet.buffer_size
            buffer = (ctypes.c_char * buffer_size).from_address(buffer_ptr)

            data = self.video_stream.codec_context.extradata
            buffer_copy = copy.deepcopy(buffer)
            self.image_queue.put((buffer_copy, data))


    def process_video_queue(self):
        if self.open_log:
            self.logger.info("Started processing video queue from file.")
        while not self.stop_event.is_set():
            try:
                buffer, data = self.image_queue.get(block=True, timeout=5)
            except queue.Empty:
                self.logger.info("Image queue is empty, waiting for new images.")
                continue

            buffer_bytes = bytes(buffer)

            # 要检查的前缀
            begin = b'\x00\x00\x01\x06'
            end = b'\x00\x00\x00\x01\x65'

            # 判断缓冲区是否以指定前缀开头
            if buffer_bytes.startswith(begin):
                pos = buffer_bytes.find(end)
                if pos != -1:
                    buffer = data + buffer[pos:]
            elif buffer_bytes.startswith(end):
                buffer = data + buffer

            j = 0
            while j < len(buffer):
                payload = buffer[j:j + self.max_payload_size]
                
                # 创建 RTP 包
                marker = 1 if j + self.max_payload_size >= len(buffer) else 0
                rtp_packet = self.create_video_file_rtp_packet(payload, marker)
                
                self.sock.sendto(bytes(rtp_packet), (self.ip_address, self.port))
                
                self.RTP_VIDEO_FILE_SEQUENCE_NUMBER += 1
                j += self.max_payload_size

                if j >= len(buffer):
                    self.RTP_VIDEO_FILE_TIMESTAMP += 3000

    def send_audio_rtp_from_file(self, audio_file, is_16k=False):
        audio = AudioSegment.from_file(audio_file, format="wav")
        audio_data = audio.raw_data
        self.audio_queue.put((audio_data, is_16k))


    def process_audio_queue(self):
        if self.open_log:
            self.logger.info("Started processing audio queue from file.")
        while not self.stop_event.is_set():
            try:
                audio_data, is_16k = self.audio_queue.get(block=True, timeout=5)
            except queue.Empty:
                self.logger.info("Audio queue is empty, waiting for new audios.")
                continue

            frame_size = 640 if is_16k else 1920

            # 将音频数据分割为frame_size字节的帧
            i = 0
            while i < len(audio_data):
                frame_data = audio_data[i:i + frame_size]
                i += frame_size

                j = 0
                while j < len(frame_data):
                    payload = frame_data[j:j + self.max_payload_size]
                    marker = 1 if j + self.max_payload_size >= len(frame_data) else 0

                    # 创建 RTP 包
                    rtp_packet = self.create_audio_file_rtp_packet(payload, marker)
                    
                    self.sock.sendto(bytes(rtp_packet), (self.ip_address, self.port))
                    
                    self.RTP_AUDIO_FILE_SEQUENCE_NUMBER += 1
                    j += self.max_payload_size

                    if j >= len(frame_data):
                        self.RTP_AUDIO_FILE_TIMESTAMP += 3000


    def send_video_rtp_from_img(self, img):
        img_frame = av.VideoFrame.from_ndarray(img, format = 'rgb24')
        self.image_queue2.put(img_frame)


    def process_video_queue2(self):
        if self.open_log:
            self.logger.info("Started processing video queue from img.")

        while not self.stop_event.is_set():
            try:
                img_frame = self.image_queue2.get(block=True, timeout=5)
                if self.open_log:
                    self.logger.info(f"Current size of image_queue2: {self.image_queue2.qsize()}.")
            except queue.Empty:
                continue 

            encode_begin = time()
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

            data = self.video_stream.codec_context.extradata

            for packet in packets:
                buffer_ptr = packet.buffer_ptr
                buffer_size = packet.buffer_size
                buffer = (ctypes.c_char * buffer_size).from_address(buffer_ptr)
                buffer_bytes = bytes(buffer)

                # 要检查的前缀
                begin = b'\x00\x00\x01\x06'
                end = b'\x00\x00\x00\x01\x65'
                p = b'\x00\x00\x00\x01\x61'
                
                # 判断关键帧
                if self.hard_encode:
                    if buffer_bytes.find(begin) != -1:
                        pos = buffer_bytes.find(end)
                        if pos != -1:
                            buffer = data + buffer[pos:]
                        else:
                            pos2 = buffer_bytes.find(p)
                            if pos2 != -1:
                                buffer = buffer[pos2:]
                    elif buffer_bytes.startswith(end):
                        buffer = data + buffer
                else:
                    if buffer_bytes.startswith(begin):
                        pos = buffer_bytes.find(end)
                        if pos != -1:
                            buffer = data + buffer[pos:]
                    elif buffer_bytes.startswith(end):
                        buffer = data + buffer

                j = 0
                while j < len(buffer):
                    payload = buffer[j:j + self.max_payload_size]
                    marker = 1 if j + self.max_payload_size >= len(buffer) else 0
                    
                    # 创建 RTP 包
                    rtp_packet = self.create_video_img_rtp_packet(payload, marker)

                    self.sock.sendto(bytes(rtp_packet), (self.ip_address, self.port))
                    
                    self.RTP_VIDEO_IMG_SEQUENCE_NUMBER += 1
                    j += self.max_payload_size
                    
                    if j >= len(buffer):
                        self.RTP_VIDEO_IMG_TIMESTAMP += 3000
                
            send_end = time()
            cur_img_send_cost_time = (send_end - send_begin) * 1000
            self.img_rtp_sent_total_time += cur_img_send_cost_time
            self.img_rtp_sent_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Image RTP send #{self.img_rtp_sent_total_cnt}: {cur_img_send_cost_time:.6f} ms")
                avg_time = self.img_rtp_sent_total_time / self.img_rtp_sent_total_cnt
                self.logger.info(f"Average image RTP send time: {avg_time:.6f} ms over {self.img_rtp_sent_total_cnt} sends.")

    def send_audio_rtp_from_bytes(self, audio_bytes, is_16k=False):
        self.audio_queue2.put((audio_bytes, is_16k))


    def process_audio_queue2(self):
        if self.open_log:
            self.logger.info("Started processing audio queue from byte stream.")

        while not self.stop_event.is_set():
            try:
                audio_data, is_16k = self.audio_queue2.get(block=True, timeout=5)
                if self.open_log:
                    self.logger.info(f"Current size of audio_queue2: {self.audio_queue2.qsize()}.")
            except queue.Empty:
                # self.logger.info("Audio queue2 is empty, waiting for new audio data.")
                continue 

            frame_size = 640 if is_16k else 1920

            audio_send_begin = time()

            # 将音频数据分割为frame_size字节的帧
            i = 0
            while i < len(audio_data):
                frame_data = audio_data[i:i + frame_size]
                i += frame_size

                j = 0
                while j < len(frame_data):
                    payload = frame_data[j:j + self.max_payload_size]
                    marker = 1 if j + self.max_payload_size >= len(frame_data) else 0

                    rtp_packet = self.create_audio_bytes_rtp_packet(payload, marker)

                    self.sock.sendto(bytes(rtp_packet), (self.ip_address, self.port))

                    self.RTP_AUDIO_BYTES_SEQUENCE_NUMBER += 1
                    j += self.max_payload_size

                    if j >= len(frame_data):
                        self.RTP_AUDIO_BYTES_TIMESTAMP += 3000

            audio_send_end = time()
            cur_audio_send_cost_time = (audio_send_end - audio_send_begin) * 1000
            self.audio_rtp_sent_total_time += cur_audio_send_cost_time
            self.audio_rtp_sent_total_cnt += 1
            if self.open_log:
                self.logger.info(f"No. {self.audio_rtp_sent_total_cnt} audio rtp send time: {cur_audio_send_cost_time}ms")
                self.logger.info(f"Audio RTP send #{self.audio_rtp_sent_total_cnt}: {cur_audio_send_cost_time:.6f} ms")
                avg_time = self.audio_rtp_sent_total_time / self.audio_rtp_sent_total_cnt
                self.logger.info(f"Average audio RTP send time: {avg_time:.6f} ms over {self.audio_rtp_sent_total_cnt} sends.")