import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QFontDatabase, QColor, QIcon
from pathlib import Path
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
##############################
detect_fire = resource_path("./resource/image/firesiren.jpg")
detect_boom = resource_path("./resource/image/boom.png")
detect_gun = resource_path("./resource/image/gun.png")
detect_emer = resource_path("./resource/image/emer.jpg")
detect_siren = resource_path("./resource/image/siren.jpg")
############## Main 윈도우 ###########################
form_main = resource_path("./resource/ui/main.ui")
form_main_class = uic.loadUiType(form_main)[0]
########### Calendar 클래스 ##################
class MainClass(QDialog, QWidget, form_main_class):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setupUi(self)
        self.setWindowIcon(QIcon(icon_path))

        self.setWindowTitle('실시간 소리인식 서비스')
        self.program_name.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        self.text1.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 18))
        self.text2.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 10))

        self.statistics.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 11))
        self.setting.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 11))

        self.text3.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        self.text4.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        self.text5.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        #self.text6.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 12))
        self.is_sound_01.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_02.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_03.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_04.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_05.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_06.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_07.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_08.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_09.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_10.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_11.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_12.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_13.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_14.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_15.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.is_sound_16.setFont(QtGui.QFont("G마켓 산스 TTF Medium", 10))
        self.sta_enter.setFont(QtGui.QFont("G마켓 산스 TTF Bold", 11))

        self.hide_setting()

        self.alarm.hide()
       
        self.sample_hide()
        self.sample_hide_1()
        self.sample_hide_2()
        self.sample_hide_3()
        self.sample_hide_4()
        
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
        
######################################################################

        self.is_play=False
        self.progressBar.hide()
        self.text2.hide()
        print(logo_path)
        print(f''' border-image: url("{logo_path}");
                 background : transparent;''')
        self.center()
        self.show()

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

    def keyPressEvent(self, e):
        if e.key()== Qt.Key_A:
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

            QTimer.singleShot(1000, self.down_alarm)

        if e.key()== Qt.Key_S:
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

            QTimer.singleShot(1000, self.down_alarm_1)
        
        if e.key()== Qt.Key_D:
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

            QTimer.singleShot(1000, self.down_alarm_2)
        
        if e.key()== Qt.Key_F:
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

            QTimer.singleShot(1000, self.down_alarm_3)
        
        if e.key()== Qt.Key_G:
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

            QTimer.singleShot(1000, self.down_alarm_4)
        
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
        
    def hide_siren_text(self):
        self.siren_label.hide()
        
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

    def setStopMode(self):
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
        self.is_sound_06.show()
        self.is_sound_07.show()
        self.is_sound_08.show()
        self.is_sound_09.show()
        self.is_sound_10.show()
        self.is_sound_11.show()
        self.is_sound_12.show()
        self.is_sound_13.show()
        self.is_sound_14.show()
        self.is_sound_15.show()
        self.is_sound_16.show()
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
        self.is_sound_06.hide()
        self.is_sound_07.hide()
        self.is_sound_08.hide()
        self.is_sound_09.hide()
        self.is_sound_10.hide()
        self.is_sound_11.hide()
        self.is_sound_12.hide()
        self.is_sound_13.hide()
        self.is_sound_14.hide()
        self.is_sound_15.hide()
        self.is_sound_16.hide()
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
            self.animation2.setStartValue(QRect(-10, 50, 401, 0))
            self.animation2.setEndValue(QRect(-10, 50, 401, 731))
            self.animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation2.start()
        else:
            self.animation2 = QPropertyAnimation(self.statistics_screen, b"geometry")
            self.animation2.setDuration(500)
            self.animation2.setStartValue(QRect(-10, 50, 401, 731))
            self.animation2.setEndValue(QRect(-10, 50, 401, 0))
            self.animation2.setEasingCurve(QEasingCurve.InOutQuad)
            self.animation2.start()

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./resource/GmarketSansTTFBold.ttf')
    app.setFont(QFont('GmarketSansTTFBold'))
    myWindow = MainClass()
    myWindow.show()
    sys.exit(app.exec_())
