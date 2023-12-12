import sys
import os
#import sound_input1
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QIcon
from PyQt5.QtGui import QPixmap, QImage
import threading
import Adafruit_DHT
import subprocess
from pathlib import Path
import psutil
import pyaudio
import wave
import os
import noisereduce as nr
import numpy as np
import librosa
import tensorflow as tf
from keras.models import load_model
import cv2
from ultralytics import YOLO
from time import sleep
import time
from datetime import datetime
import torch


# GPU가 사용 가능한지 확인
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("GPU를 사용합니다.")
else:
    device = torch.device("cpu")
    print("GPU를 사용할 수 없습니다. CPU를 사용합니다.")

# 모델 파일 로드
model_file_path = 'Soundtest.h5'  # 모델 파일 경로를 적절히 수정하세요.
model = load_model(model_file_path)
# 카메라
model_camera = YOLO("yolov8s.pt")

#pyinstaller --onefile --add-data "./resource/;resource/" main.py

##################################################################################################

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', Path(__file__).resolve().parent)
    return str(base_path / Path(relative_path)).replace('\\', '/')



#################################################################################################
logo_path = resource_path("./resource/image/logo.png")
play_back_path = resource_path("./resource/image/play_back.png")
play_button_path = resource_path("./resource/image/play_button.png")
push_play_path = resource_path("./resource/image/push_play.png")
push_stop_path = resource_path("./resource/image/push_stop.png")
stop_button_path = resource_path("./resource/image/stop_button.png")
statistics_path = resource_path("./resource/image/statistics.png")
setting_path = resource_path("./resource/image/setting.png")
icon_path = resource_path("./resource/image/icon.png")
camera_path = resource_path("./resource/image/camera.png")
##############################
detect_fire = resource_path("./resource/image/firesiren.jpg")
detect_boom = resource_path("./resource/image/boom.png")
detect_gun = resource_path("./resource/image/gun.png")
detect_emer = resource_path("./resource/image/emer.jpg")
detect_siren = resource_path("./resource/image/siren.jpg")
detect_car = resource_path("./resource/image/car.png")
#############################

############## Main 윈도우 ###########################
form_main = resource_path("./resource/ui/main.ui")
form_main_class = uic.loadUiType(form_main)[0]

#####################################################

#####################################################
class AudioProcessingThread(QThread):
    detected_class_signal = pyqtSignal(str)  # 감지된 클래스를 메인 윈도우에 전달할 시그널
    finished = pyqtSignal()  # 스레드가 종료될 때 발생하는 시그널
    

    def __init__(self):
        super().__init__()
        
        self.is_recording = True  # 녹음 중 여부를 나타내는 플래그
        self.recording_thread = None  # 녹음 작업을 실행할 스레드   

    def get_sound(self, path):
        external_sound, sr = librosa.load('output.wav')  # 외부 사운드 파일 경로를 넣어주세요.

        # 전처리
        n_columns = 174
        n_row = 40
        n_channels = 1

        # 외부 사운드를 모델의 입력 형식에 맞게 변환
        external_sound_features = librosa.feature.mfcc(y=external_sound, sr=sr, n_mfcc=n_row)
        external_sound_features = np.pad(external_sound_features, ((0, 0), (0, n_columns - len(external_sound_features[0]))), mode='constant')
        external_sound_features = np.reshape(external_sound_features, (1, n_row, n_columns, n_channels))

        # 예측 수행
        predictions = model.predict(external_sound_features)

        # 예측 결과 출력
        class_labels = ["BOMB", "EAI", "FASTEMERGENCY", "FIRE", "gun_shot"]  # 클래스 레이블 리스트를 적절히 수정하세요.
        predicted_class_index = np.argmax(predictions)
        predicted_class_label = class_labels[predicted_class_index]
        predicted_class_probability = np.max(predictions) * 100  # 예측 확률 계산

        return predicted_class_label, predicted_class_probability
    
    def run(self):
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        CHUNK = 1024
        RECORD_SECONDS = 2
        WAVE_OUTPUT_FILENAME = "output.wav"
        THRESHOLD = 70  # 예측 확률 임계값 (70% 이상인 경우에만 출력)
        DESIRED_DB_THRESHOLD = 0  # 원하는 데시벨 임계값

        audio = pyaudio.PyAudio()

        def get_decibel_level(audio_data):
            rms = np.sqrt(np.mean(np.square(audio_data)))
            decibel = 20 * np.log10(rms)
            return decibel

        # 이전에 감지한 클래스와 카운트를 저장할 변수
        previous_detected_class = None
        class_count = 0
        class_check = ""

        while self.is_recording:
            print("녹음 중...")
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            print("녹음 완료.")

            # 녹음된 오디오 데이터를 불러옵니다.
            audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)

            # 데시벨 값을 측정하여 임계값을 초과하는지 확인
            decibel_level = get_decibel_level(audio_data)

            # 노이즈 제거를 위해 noisereduce 라이브러리를 사용합니다.
            reduced_noise = nr.reduce_noise(y=audio_data, sr=RATE)

            # 노이즈 제거된 오디오를 다시 저장합니다.
            reduced_wf = wave.open("output.wav", 'wb')
            reduced_wf.setnchannels(CHANNELS)
            reduced_wf.setsampwidth(audio.get_sample_size(FORMAT))
            reduced_wf.setframerate(RATE)
            reduced_wf.writeframes(reduced_noise.tobytes())
            reduced_wf.close()

            if decibel_level >= DESIRED_DB_THRESHOLD:
                sound_detected_class, probability = self.get_sound('output.wav')
                # 정확도가 THRESHOLD 이상인 경우에만 클래스를 추적
                if probability >= THRESHOLD:
                    # 이전에 감지한 클래스와 현재 감지한 클래스가 같을 경우 카운트 증가
                    if sound_detected_class == previous_detected_class:
                        print("count up")
                        class_count += 1
                        
                    else:
                        # 이전에 감지한 클래스와 다른 클래스를 감지한 경우 카운트 초기화
                        previous_detected_class = sound_detected_class
                        class_count = 0
                        print("count reset")
                        self.detected_class_signal.emit("down")
                    
                    # 같은 클래스가 연속으로 3번 이상 감지되면 출력
                    if class_count >= 1:
                        #print("예측된 클래스:", detected_class)
                        print("count if in")
                        
                        if class_check == sound_detected_class:
                            print("같음")
                        else :
                            print("seam else")
                            self.detected_class_signal.emit("down")
                            self.detected_class_signal.emit(sound_detected_class)
                            class_check = sound_detected_class
                            #class_count = 0  # 클래스가 출력되면 카운트 초기화
                    else:
                        self.detected_class_signal.emit("down")
                        print("count else")
                else:
                    print("elseelse")
                    self.detected_class_signal.emit("down")
                    class_count = 0
            else:
                print(decibel_level, "음성 없음")
                self.detected_class_signal.emit("down")
    def stop(self):
        self.is_recording = False  # 스레드를 종료하기 위해 플래그 설정 
        self.finished.emit()  # 스레드 종료 시그널 발생

########### Calendar 클래스 ##################


class MainClass(QDialog, QWidget, form_main_class):
    def __init__(self):
        global save_class
        save_class = ""
        super().__init__()
        self.initUI()

        self.is_recording = False  # 녹음 중 여부를 나타내는 플래그
        self.recording_thread = None  # 녹음 작업을 실행할 스레드

        self.is_camera = False  # 카메라 중 여부를 나타내는 플래그
        self.camera_thread = None  # 카메라 작업을 실행할 스레드

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_temp_humidity)
        self.timer.start(1000)  # 1초마다 업데이트

        # th = threading.Thread(target=self.run)
        # th.start()

    def initUI(self):
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle('실시간 소리인식 서비스')
        self.program_name.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        self.text1.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 18))
        self.text2.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 10))

        self.statistics.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 11))
        self.setting.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 11))
        self.camera_on.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 11))

        self.text3.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        self.text4.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        self.text5.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        #self.text6.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        self.is_sound_01.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_02.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_03.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_04.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_05.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        
        self.sta_enter.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 11))
       
        self.hide_setting()

        self.alarm.hide()
       
        self.sample_hide()
        self.sample_hide_1()
        self.sample_hide_2()
        self.sample_hide_3()
        self.sample_hide_4()
        self.sample_hide_5()
        

        # QGraphicsDropShadowEffect 객체 생성
        effect = QGraphicsDropShadowEffect(self)

        # 그림자 색상 설정
        effect.setColor(QColor(11, 58, 101))

        # 그림자의 X, Y offset 설정, Y offset을 음수로 설정하여 위로 그림자 생성
        effect.setOffset(-4, -5)

        # 그림자의 반경 설정
        effect.setBlurRadius(10)

        # QLabel에 그림자 효과 적용
        self.alarm.setGraphicsEffect(effect)



        self.setting_screen.hide()
        self.statistics_screen.hide()
        self.camera_screen.hide()

        self.mic_slider.setSingleStep(5)


        self.logo.setStyleSheet(
            f''' border-image: url("{logo_path}");
                 background : transparent;''')

        self.logo_2.setStyleSheet(
            f''' border-image: url("{statistics_path}");
                         background : transparent;''')
        self.logo_3.setStyleSheet(
            f''' border-image: url("{setting_path}");
                                 background : transparent;''')
        self.cameralogo.setStyleSheet(
            f''' border-image: url("{camera_path}");
                                 background : transparent;''')
        self.play_back.setStyleSheet(
            f''' border-image: url("{play_back_path}");
                 background : transparent;''')

        self.play.setStyleSheet(
            f''' QPushButton {{
                border-image: url("{play_button_path}");
                background : transparent;
                }}
                QPushButton:pressed {{
                border-image: url("{push_play_path}");
                background : transparent;
                }}''')

#####################################################################

        self.detect_image.setStyleSheet(
            f''' border-image: url("{detect_fire}");
                         background : transparent0;''')
        
        self.detect_image_1.setStyleSheet(
            f''' border-image: url("{detect_boom}");
                         background : transparent1;''')
        
        self.detect_image_2.setStyleSheet(
            f''' border-image: url("{detect_gun}");
                         background : transparent2;''')
        
        self.detect_image_3.setStyleSheet(
            f''' border-image: url("{detect_emer}");
                         background : transparent3;''')
        
        self.detect_image_4.setStyleSheet(
            f''' border-image: url("{detect_siren}");
                         background : transparent4;''')
        
        self.detect_image_5.setStyleSheet(
            f''' border-image: url("{detect_car}");
                         background : transparent5;''')
        
        

######################################################################
        self.is_play=False
        self.progressBar.hide()
        self.text2.hide()
        print(logo_path)
        print(f''' border-image: url("{logo_path}");
                 background : transparent;''')
        self.center()
        self.show()

    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key_E:
    #         if not self.is_camera:
    #             print("EEEEE")
    #         # 녹음 중이 아닐 때만 녹음 시작
    #             self.is_camera = True
    #             self.camera_thread = CameraProcessingThread(self)
    #             self.camera_thread.start()
    #         else :
    #             if self.is_camera:
    #                 self.is_camera = False
    #             if self.camera_thread:
    #                 self.camera_thread.stop()  # 스레드 종료 메서드 호출

    def update_temp_humidity(self):
        sensor = Adafruit_DHT.DHT11
        pin = 4  # GPIO 핀 번호, 라즈베리파이에 따라 다를 수 있음

        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        
        if humidity is not None and temperature is not None:
            # 값이 유효할 때만 업데이트
            # LCD에 온도 표시
            self.temperature_label.setText(f'온도: {temperature:0.1f}C')
            self.humidity_label.setText(f'습도: {humidity:0.1f}%')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start(self):
        if self.is_play:
            QTimer.singleShot(200, self.setPlayMode)

        else :
            QTimer.singleShot(200, self.setStopMode)

    def hide_alert(self):
        # 텍스트 숨기기
        self.label.hide()

    def day_data(self):
        now = datetime.now()
        time_text = now.strftime("%H:%M:%S")

        return time_text

    global count
    count = 0

    def detect_statistics_count(self):
        global count
        count+=1
        return count

    def show_alarm(self, detected_class):
        global save_class
        print(detected_class)
        if detected_class == "FIRE":  # 키보드 A키 화재경보 소리
            save_class = "FIRE"
            self.alarm.show()
            self.animation3 = QPropertyAnimation(self.alarm, b"geometry")
            self.animation3.setDuration(400)
            self.animation3.setStartValue(QRect(360, 800, 561, 261))
            self.animation3.setEndValue(QRect(360, 580, 561, 261))
            self.animation3.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation3.start()

            self.detect_image.show()
            self.animation4 = QPropertyAnimation(self.detect_image, b"geometry")
            self.animation4.setDuration(400)
            self.animation4.setStartValue(QRect(540, 820, 211, 151))
            self.animation4.setEndValue(QRect(540, 600, 211, 151))
            self.animation4.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation4.start()

            self.label = QLabel("화재 경보 소리 알림", self)
            self.label.setStyleSheet("color: white; background-color : #1fbafc;")
            self.label.show()
            self.animation41 = QPropertyAnimation(self.label, b"geometry")
            self.animation41.setDuration(1000)
            self.animation41.setStartValue(QRect(580, 755,142 , 20))
            self.animation41.setEndValue(QRect(580, 755, 142, 20))
            self.animation41.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation41.start()

            TIME_TEXT=self.day_data()
            statistics_label = QLabel(f"화재 경보 소리 - {TIME_TEXT}", self.statistics_screen)
            statistics_label.setStyleSheet("color: white; font-size: 16px;")
            c = self.detect_statistics_count()
            statistics_label.setGeometry(10, 10 + c * 40, 200, 30)
            statistics_label.show()

        elif detected_class == "BOMB":  # 키보드 S키 폭발 소리 알림
            save_class = "BOMB"
            self.alarm.show()
            self.animation7 = QPropertyAnimation(self.alarm, b"geometry")
            self.animation7.setDuration(400)
            self.animation7.setStartValue(QRect(360, 800, 561, 261))
            self.animation7.setEndValue(QRect(360, 580, 561, 261))
            self.animation7.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation7.start()

            self.detect_image_1.show()
            self.animation8 = QPropertyAnimation(self.detect_image_1, b"geometry")
            self.animation8.setDuration(400)
            self.animation8.setStartValue(QRect(540, 820, 211, 151))
            self.animation8.setEndValue(QRect(540, 600, 211, 151))
            self.animation8.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation8.start()

            self.label = QLabel("폭발 소리 알림", self)
            self.label.setStyleSheet("color: white;background-color : #1fbafc;")
            self.label.show()
            self.animation42 = QPropertyAnimation(self.label, b"geometry")
            self.animation42.setDuration(1000)
            self.animation42.setStartValue(QRect(596, 755,105 , 20))
            self.animation42.setEndValue(QRect(596, 755, 105, 20))
            self.animation42.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation42.start()

            TIME_TEXT=self.day_data()
            statistics_label = QLabel(f"폭발 소리 - {TIME_TEXT}", self.statistics_screen)
            statistics_label.setStyleSheet("color: white; font-size: 16px;")
            c = self.detect_statistics_count()
            statistics_label.setGeometry(10, 10 + c * 40, 200, 30)
            statistics_label.show()
        
        elif detected_class == "gun_shot":  #키보드 D키 총 소리 알림
            save_class = "gun_shot"
            self.alarm.show()
            self.animation11 = QPropertyAnimation(self.alarm, b"geometry")
            self.animation11.setDuration(400)
            self.animation11.setStartValue(QRect(360, 800, 561, 261))
            self.animation11.setEndValue(QRect(360, 580, 561, 261))
            self.animation11.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation11.start()

            self.detect_image_2.show()
            self.animation12 = QPropertyAnimation(self.detect_image_2, b"geometry")
            self.animation12.setDuration(400)
            self.animation12.setStartValue(QRect(540, 820, 211, 151))
            self.animation12.setEndValue(QRect(540, 600, 211, 151))
            self.animation12.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation12.start()

            self.label = QLabel("총 소리 알림", self)
            self.label.setStyleSheet("color: white;background-color : #1fbafc;")
            self.label.show()
            self.animation43 = QPropertyAnimation(self.label, b"geometry")
            self.animation43.setDuration(1000)
            self.animation43.setStartValue(QRect(605, 755,90 , 20))
            self.animation43.setEndValue(QRect(605, 755, 90, 20))
            self.animation43.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation43.start()
            
            TIME_TEXT=self.day_data()
            statistics_label = QLabel(f"총 소리 - {TIME_TEXT}", self.statistics_screen)
            statistics_label.setStyleSheet("color: white; font-size: 16px;")
            c = self.detect_statistics_count()
            statistics_label.setGeometry(10, 10 + c * 40, 200, 30)
            statistics_label.show()
        
        elif detected_class == "FASTEMERGENCY": #키보드 F키 긴급한 소리 알림
            save_class = "FASTEMERGENCY"
            self.alarm.show()
            self.animation15 = QPropertyAnimation(self.alarm, b"geometry")
            self.animation15.setDuration(400)
            self.animation15.setStartValue(QRect(360, 800, 561, 261))
            self.animation15.setEndValue(QRect(360, 580, 561, 261))
            self.animation15.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation15.start()

            self.detect_image_3.show()
            self.animation16 = QPropertyAnimation(self.detect_image_3, b"geometry")
            self.animation16.setDuration(400)
            self.animation16.setStartValue(QRect(540, 820, 211, 151))
            self.animation16.setEndValue(QRect(540, 600, 211, 151))
            self.animation16.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation16.start()

            self.label = QLabel("긴급자동차 소리 알림", self)
            self.label.setStyleSheet("color: white;background-color : #1fbafc;")
            self.label.show()
            self.animation44 = QPropertyAnimation(self.label, b"geometry")
            self.animation44.setDuration(1000)
            self.animation44.setStartValue(QRect(570, 755,155, 20))
            self.animation44.setEndValue(QRect(570, 755, 155, 20))
            self.animation44.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation44.start()

            TIME_TEXT=self.day_data()
            statistics_label = QLabel(f"긴급자동차 소리 - {TIME_TEXT}", self.statistics_screen)
            statistics_label.setStyleSheet("color: white; font-size: 16px;")
            c = self.detect_statistics_count()
            statistics_label.setGeometry(10, 10 + c * 40, 200, 30)
            statistics_label.show()
        
        elif detected_class == "EAI":  #키보드 G키 사이렌 소리 알림
            save_class = "EAI"
            self.alarm.show()
            self.animation19 = QPropertyAnimation(self.alarm, b"geometry")
            self.animation19.setDuration(400)
            self.animation19.setStartValue(QRect(360, 800, 561, 261))
            self.animation19.setEndValue(QRect(360, 580, 561, 261))
            self.animation19.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation19.start()

            self.detect_image_4.show()
            self.animation20 = QPropertyAnimation(self.detect_image_4, b"geometry")
            self.animation20.setDuration(400)
            self.animation20.setStartValue(QRect(540, 820, 211, 151))
            self.animation20.setEndValue(QRect(540, 600, 211, 151))
            self.animation20.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation20.start()

            self.label = QLabel("사이렌 소리 알림", self)
            self.label.setStyleSheet("color: white;background-color : #1fbafc;")
            self.label.show()
            self.animation45 = QPropertyAnimation(self.label, b"geometry")
            self.animation45.setDuration(1000)
            self.animation45.setStartValue(QRect(595, 755,123 , 20))
            self.animation45.setEndValue(QRect(595, 755, 123, 20))
            self.animation45.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation45.start()

            TIME_TEXT=self.day_data()
            statistics_label = QLabel(f"사이렌 소리 - {TIME_TEXT}", self.statistics_screen)
            statistics_label.setStyleSheet("color: white; font-size: 16px;")
            c = self.detect_statistics_count()
            statistics_label.setGeometry(10, 10 + c * 40, 200, 30)
            statistics_label.show()

        elif detected_class == "car_": #키보드 F키 긴급한 소리 알림
            save_class = "car_"
            print("car############################################################################################")
            self.alarm.show()
            self.animation15 = QPropertyAnimation(self.alarm, b"geometry")
            self.animation15.setDuration(400)
            self.animation15.setStartValue(QRect(360, 800, 561, 261))
            self.animation15.setEndValue(QRect(360, 580, 561, 261))
            self.animation15.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation15.start()

            self.detect_image_5.show()
            self.animation16 = QPropertyAnimation(self.detect_image_3, b"geometry")
            self.animation16.setDuration(400)
            self.animation16.setStartValue(QRect(540, 820, 211, 151))
            self.animation16.setEndValue(QRect(540, 600, 211, 151))
            self.animation16.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation16.start()

            self.label = QLabel("자동차 소리 알림", self)
            self.label.setStyleSheet("color: white;background-color : #1fbafc;")
            self.label.show()
            self.animation46 = QPropertyAnimation(self.label, b"geometry")
            self.animation46.setDuration(1000)
            self.animation46.setStartValue(QRect(587, 755,124 , 20))
            self.animation46.setEndValue(QRect(587, 755, 124, 20))
            self.animation46.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation46.start()

            TIME_TEXT=self.day_data()
            statistics_label = QLabel(f"자동차 소리 - {TIME_TEXT}", self.statistics_screen)
            statistics_label.setStyleSheet("color: white; font-size: 16px;")
            c = self.detect_statistics_count()
            statistics_label.setGeometry(10, 10 + c * 40, 200, 30)
            statistics_label.show()

            self.hide_alert()
            QTimer.singleShot(1000, self.down_alarm_5)
            
        elif detected_class == "down":
            print(save_class)
            if save_class != "":
                if save_class == "FIRE":
                    print("f")
                    self.hide_alert()
                    QTimer.singleShot(1000, self.down_alarm)
                    save_class = ""
                elif save_class == "BOMB":
                    print("b")
                    self.hide_alert()
                    QTimer.singleShot(1000, self.down_alarm_1)
                    save_class = ""
                elif save_class == "gun_shot":
                    print("g")
                    self.hide_alert()
                    QTimer.singleShot(1000, self.down_alarm_2)
                    save_class = ""
                elif save_class == "FASTEMERGENCY":
                    print("F")
                    self.hide_alert()
                    QTimer.singleShot(1000, self.down_alarm_3)
                    save_class = ""
                elif save_class == "EAI":
                    print("E")
                    self.hide_alert()
                    QTimer.singleShot(1000, self.down_alarm_4)
                    save_class = ""

    def down_alarm(self):
        self.animation23 = QPropertyAnimation(self.alarm, b"geometry")
        self.animation23.setDuration(500)
        self.animation23.setStartValue(QRect(360, 580, 561, 261))
        self.animation23.setEndValue(QRect(360, 850, 561, 261))
        self.animation23.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation23.start()

        self.animation24 = QPropertyAnimation(self.detect_image, b"geometry")
        self.animation24.setDuration(400)
        self.animation24.setStartValue(QRect(540, 600, 211, 151))
        self.animation24.setEndValue(QRect(540, 820, 211, 151))
        self.animation24.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation24.start()

    def down_alarm_1(self):
        self.animation27 = QPropertyAnimation(self.alarm, b"geometry")
        self.animation27.setDuration(500)
        self.animation27.setStartValue(QRect(360, 580, 561, 261))
        self.animation27.setEndValue(QRect(360, 850, 561, 261))
        self.animation27.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation27.start()


        self.animation28 = QPropertyAnimation(self.detect_image_1, b"geometry")
        self.animation28.setDuration(400)
        self.animation28.setStartValue(QRect(540, 600, 211, 151))
        self.animation28.setEndValue(QRect(540, 820, 211, 151))
        self.animation28.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation28.start()

    def down_alarm_2(self):
        self.animation31 = QPropertyAnimation(self.alarm, b"geometry")
        self.animation31.setDuration(500)
        self.animation31.setStartValue(QRect(360, 580, 561, 261))
        self.animation31.setEndValue(QRect(360, 850, 561, 261))
        self.animation31.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation31.start()


        self.animation32 = QPropertyAnimation(self.detect_image_2, b"geometry")
        self.animation32.setDuration(400)
        self.animation32.setStartValue(QRect(540, 600, 211, 151))
        self.animation32.setEndValue(QRect(540, 820, 211, 151))
        self.animation32.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation32.start()

    def down_alarm_3(self):
        self.animation35 = QPropertyAnimation(self.alarm, b"geometry")
        self.animation35.setDuration(500)
        self.animation35.setStartValue(QRect(360, 580, 561, 261))
        self.animation35.setEndValue(QRect(360, 850, 561, 261))
        self.animation35.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation35.start()


        self.animation36 = QPropertyAnimation(self.detect_image_3, b"geometry")
        self.animation36.setDuration(400)
        self.animation36.setStartValue(QRect(540, 600, 211, 151))
        self.animation36.setEndValue(QRect(540, 820, 211, 151))
        self.animation36.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation36.start()

    def down_alarm_4(self):
        self.animation39 = QPropertyAnimation(self.alarm, b"geometry")
        self.animation39.setDuration(500)
        self.animation39.setStartValue(QRect(360, 580, 561, 261))
        self.animation39.setEndValue(QRect(360, 850, 561, 261))
        self.animation39.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation39.start()


        self.animation40 = QPropertyAnimation(self.detect_image_4, b"geometry")
        self.animation40.setDuration(400)
        self.animation40.setStartValue(QRect(540, 600, 211, 151))
        self.animation40.setEndValue(QRect(540, 820, 211, 151))
        self.animation40.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation40.start()
        
    def down_alarm_5(self):
        self.animation39 = QPropertyAnimation(self.alarm, b"geometry")
        self.animation39.setDuration(500)
        self.animation39.setStartValue(QRect(360, 580, 561, 261))
        self.animation39.setEndValue(QRect(360, 850, 561, 261))
        self.animation39.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation39.start()


        self.animation40 = QPropertyAnimation(self.detect_image_5, b"geometry")
        self.animation40.setDuration(400)
        self.animation40.setStartValue(QRect(540, 600, 211, 151))
        self.animation40.setEndValue(QRect(540, 820, 211, 151))
        self.animation40.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation40.start()

    def sample_hide(self):
        self.detect_image.hide()
        self.alarm.hide()
        
    def sample_hide_1(self):
        self.detect_image_1.hide()
        self.alarm.hide()

    def sample_hide_2(self):
        self.detect_image_2.hide()
        self.alarm.hide()
        
    def sample_hide_3(self):
        self.detect_image_3.hide()
        self.alarm.hide()

    def sample_hide_4(self):
        self.detect_image_4.hide()
        self.alarm.hide()
        
    def sample_hide_5(self):
        self.detect_image_5.hide()
        self.alarm.hide()

    def setPlayMode(self):
        self.play.setStyleSheet(
            f''' QPushButton {{
                border-image: url("{play_button_path}");
                background : transparent;
                }}
                QPushButton:pressed {{
                border-image: url("{push_play_path}");
                background : transparent;
                }}''')
        self.progressBar.hide()
        self.text2.hide()
        self.text1.show()
        self.is_play = False
        self.show_alarm("down")
        if self.is_recording:
            self.is_recording = False
            if self.recording_thread:
                self.recording_thread.stop()  # 스레드 종료 메서드 호출



    def setStopMode(self):
        if not self.is_recording:
            # 녹음 중이 아닐 때만 녹음 시작
            self.is_recording = True
            self.recording_thread = AudioProcessingThread()
            self.recording_thread.detected_class_signal.connect(self.show_alarm)
            self.recording_thread.start()
        self.play.setStyleSheet(
            f''' QPushButton {{
                border-image: url("{stop_button_path}");
                background : transparent;
                }}
                QPushButton:pressed {{
                border-image: url("{push_stop_path}");
                background : transparent;
                }}''')
        self.progressBar.show()
        self.text2.show()
        self.text1.hide()
        self.is_play = True

    def settings(self):
        if self.setting.isChecked():
            self.setting_screen.show()
            self.animation1 = QPropertyAnimation(self.setting_screen, b"geometry")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(QRect(890, 50, 401, 0))
            self.animation1.setEndValue(QRect(890, 50, 401, 731))
            self.animation1.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation1.start()
            QTimer.singleShot(400, self.show_setting)

        else:
            self.animation1 = QPropertyAnimation(self.setting_screen, b"geometry")
            self.animation1.setDuration(500)
            self.animation1.setStartValue(QRect(890, 50, 401, 731))
            self.animation1.setEndValue(QRect(890, 50, 401, 0))
            self.animation1.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation1.start()
            self.hide_setting()

    def show_setting(self):
        self.text3.show()
        self.text4.show()
        self.text5.show()
        self.is_sound_01.show()
        self.is_sound_02.show()
        self.is_sound_03.show()
        self.is_sound_04.show()
        self.is_sound_05.show()
        self.sta_enter.show()
        self.background.show()
        self.background_2.show()
        self.background_3.show()
        self.mic_slider.show()
        self.mic_slider_2.show()

    def hide_setting(self):
        self.text3.hide()
        self.text4.hide()
        self.text5.hide()
        self.is_sound_01.hide()
        self.is_sound_02.hide()
        self.is_sound_03.hide()
        self.is_sound_04.hide()
        self.is_sound_05.hide()
        self.sta_enter.hide()
        self.background.hide()
        self.background_2.hide()
        self.background_3.hide()
        self.mic_slider.hide()
        self.mic_slider_2.hide()

    def statistics_click(self):
        if self.statistics.isChecked():
            self.statistics_screen.show()
            self.animation2 = QPropertyAnimation(self.statistics_screen, b"geometry")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(QRect(0, 50, 230, 0))
            self.animation2.setEndValue(QRect(0, 50, 230, 770))
            self.animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation2.start()
        else:
            self.animation2 = QPropertyAnimation(self.statistics_screen, b"geometry")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(QRect(0, 50, 230, 770))
            self.animation2.setEndValue(QRect(0, 50, 230, 0))
            self.animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation2.start()

    
    def camera_signal(self, frame):
        desired_width = 900
        desired_height = 600
        frame = cv2.resize(frame, (desired_width, desired_height))
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        qlmg = QtGui.QImage(img.data, w,h, w*c, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qlmg)
        self.camera_screen.setPixmap(pixmap)
        QtWidgets.QApplication.processEvents()
        
    def camera_click(self):
        if self.camera_on.isChecked():
            self.is_camera = True
            self.camera_thread = CameraProcessingThread(self)
            self.camera_thread.detected_class_signal.connect(self.show_alarm)
            self.camera_thread.start()
            self.camera_screen.show()
            self.camera_thread.frame_signal.connect(self.camera_signal)
        else:
            self.camera_screen.hide()
            if self.is_camera:
                self.is_camera = False
            if self.camera_thread:
                self.camera_thread.stop()  # 스레드 종료 메서드 호출 


    def updatedB(self, value):
        if value == 60:
            self.text3.setText(f"마이크 민감도 조정 : {str(value)}dB (기본)")

        else:
            self.text3.setText(f"마이크 민감도 조정 : {str(value)}dB")

    def updateAcc(self, value):
        if value == 1:
            self.text5.setText(f"인식 정확도 조정 : 매우 둔감")

        elif value == 2:
            self.text5.setText(f"인식 정확도 조정 : 둔감")
        elif value == 3:
            self.text5.setText(f"인식 정확도 조정 : 보통")
        elif value == 4:
            self.text5.setText(f"인식 정확도 조정 : 예민")
        elif value == 5:
            self.text5.setText(f"인식 정확도 조정 : 매우 예민")


class CameraProcessingThread(QThread):
    detected_class_signal = pyqtSignal(str)  # 감지된 클래스를 메인 윈도우에 전달할 시그널
    frame_signal = pyqtSignal(object)
    finished = pyqtSignal()  # 스레드가 종료될 때 발생하는 시그널
    global send
    send = 30
      
    def signal_send(self):
        global send
        if send == 30:
            send = 0
            self.detected_class_signal.emit("car_")
        else :
            send += 1
        

    def run(self):
        cap = cv2.VideoCapture("test10.MOV")  # 기본 카메라 사용 (필요에 따라 인덱스를 변경)
        prev_boxes = {}
        direction_vectors = {}  # 각 추적된 객체에 대한 방향 벡터 저장
        line_length_factor = 30  # 이 값을 높이면 선이 더 길어집니다
        smoothing_factor = 0.1  # 부드러운 모션 선을 얻으려면 이 값을 조절합니다
        self.is_camera = True
        self.camera_thread = None 
        while self.is_camera:
            ret, frame = cap.read()
            if not ret:
                break

            results = model_camera.track(frame, persist=True)

            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            clss = results[0].boxes
            ids = results[0].boxes.id.cpu().numpy().astype(int)

            for box, clsq, id in zip(boxes, clss, ids):
                class_index = int(clsq.cls.cpu().detach().numpy())

                if class_index < len(model_camera.names):
                    class_label = model_camera.names[class_index]
                    x1, y1, x2, y2 = box
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)

                    if class_label in ["person", "bicycle", "motorcycle", "car", "bus", "truck"]:
                        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

                        # 이전 프레임에서 ID가 존재하는 경우 방향 벡터 계산
                        if id in prev_boxes:
                            prev_center_x, prev_center_y, label = prev_boxes[id]
                            direction_vector = (center_x - prev_center_x, center_y - prev_center_y)

                            # 방향 벡터의 길이를 조절
                            direction_vector = (
                                int(direction_vector[0] * line_length_factor),
                                int(direction_vector[1] * line_length_factor)
                            )

                            # 방향 벡터에 부드러움 적용
                            if id in direction_vectors:
                                prev_direction = direction_vectors[id]
                                direction_vector = (
                                    int(smoothing_factor * direction_vector[0] + (1 - smoothing_factor) * prev_direction[0]),
                                    int(smoothing_factor * direction_vector[1] + (1 - smoothing_factor) * prev_direction[1])
                                )

                            # 차량의 중심에서 시작하는 선분을 그립니다
                            if class_label in ["bicycle", "motorcycle", "car", "bus", "truck"]:
                                # 운동 방향으로 중앙에서부터 선 그리기
                                line_end_x = center_x + direction_vector[0]
                                line_end_y = center_y + direction_vector[1]
                                cv2.line(frame, (center_x, center_y), (line_end_x, line_end_y), (255, 0, 0), 2)
                                
                                for person_id, person_center in prev_boxes.items():
                                    person_x, person_y, p_label = person_center
                                    if (p_label == "person"):
                                        if (
                                            
                                            line_end_x >= person_x - ((x2 - x1)/2) and line_end_x <= person_x + ((x2 - x1)/2) and
                                            line_end_y >= person_y - ((y2 - y1)/2) and line_end_y <= person_y + ((y2 - y1)/2)
                                        ):
                                            self.signal_send()
                                            #self.detected_class_signal.emit("car_")
                                            cv2.putText(
                                                frame,
                                                f"Warning!",
                                                (x1, y1 - 10),
                                                cv2.FONT_HERSHEY_SIMPLEX,
                                                3,
                                                (0, 0, 255),
                                                2,
                                            )
                                            
                                        else:
                                            # 다음 프레임을 위해 현재 방향 벡터 저장
                                            direction_vectors[id] = direction_vector
                                    else :
                                        direction_vectors[id] = direction_vector

                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"ID {id}",
                        (box[0], box[1]),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2,
                    )
                    
                    prev_boxes[id] = (center_x, center_y, class_label)
            self.frame_signal.emit(frame)      

        cap.release()

        
    def stop(self):
        self.is_camera = False  # 스레드를 종료하기 위해 플래그 설정
        self.finished.emit()  # 스레드 종료 시그널 발생





if __name__ == "__main__":
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./resource/GmarketSansTTFBold.ttf')
    app.setFont(QFont('GmarketSansTTFBold'))
    myWindow = MainClass()
    myWindow.show()
    sys.exit(app.exec_())
