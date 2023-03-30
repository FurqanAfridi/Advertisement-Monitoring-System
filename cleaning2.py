import traceback
import os
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton, QGridLayout, QMainWindow, QStatusBar, \
    QTabWidget, QFileDialog, QSizePolicy, QToolButton, QStackedWidget, QCalendarWidget, QScrollArea
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon, QCursor, QPixmap, QImage, QMovie, QFont
import sys
import cv2
import datetime
import time
import pafy
import main
import threading
import multiprocessing

style = """
    * {
        font-family: Arial;
    }
    #main_name_label {
        font-family: Castellar;
    }
    QPushButton {
        background-color: #040F16;
        color: #E3E3E3;
        border: 2px solid #E3E3E3;
        font-size: 22px;
        
        padding: 20px 10px;
    }
    QPushButton:hover {
        background-color: #E3E3E3;
        border: 2px solid #040F16;
        color: #040F16;
    }
    #windows {
        background-color: #040F16;
        background-image: url('images/back.jpg');
        color: #E3E3E3;
    }
    QWidget#tabs_av {
        background-color: #040F16;
    }
    QTabWidget::pane {
        border: 3px solid #8F9AFF;
    }
    QTabWidget::tab-bar {
        left: 10px;
    }
    QTabBar::tab {
        width: 100%;
        background-color: #E3E3E3;
        padding: 14px 9px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-top: 20px;
        font-size: 14px;
    }
    QTabBar::tab:selected {
        background-color: #8F9AFF;
    }
    QStatusBar, QLabel, QToolButton {
        color: #E3E3E3;
    }
    QToolButton {
        
        background-color: #E3E3E3;
        color: #040F16;
        border: 2px solid #040F16;
        font-weight: 900;
        font-size: 14px;
    }

    QToolButton:checked {
        background-color: #8F9AFF;
    }
    QPushButton:disabled {
        color: grey;
        border: 2px solid grey;
    }
    #hist {
        background-color: #E3E3E3;
        color: #040F16;
        border-radius: 8px;
        padding: 8px;
        font-size: 16px;
    }
    QScrollArea, #f_n {
        background-color: transparent;

    }
    QScrollArea {
        border: 2px solid #E3E3E3;
        border-radius: 5px;
    }
    #menu_options, #monitor_ad_archive_broadcast_btns {
        border-width: 0px;
        padding-top: 25px; 
        padding-bottom: 25px; 
    }
"""


def grids():
    g = QGridLayout()
    for i in range(9):
        for x in range(9):
            la = QLabel()
            g.addWidget(la, i, x, QtCore.Qt.AlignCenter)
    return g


date = None
name_ad = ""
selected_ads = []
brs = [{"image": "images/geo_logo.png", "name": "GEO News", "url": "https://www.youtube.com/watch?v=q130lTDaua0"},
       {"image": "images/samaa_logo.png", "name": "Samaa News", "url": "https://www.youtube.com/watch?v=VGm487f2R5k"},
       {"image": "images/bol_logo.png", "name": "BOL", "url": "https://www.youtube.com/watch?v=i5FK1tMNMnE"},
       {"image": "images/ary_logo.png", "name": "ARY News", "url": "https://www.youtube.com/watch?v=sUKwTVAc0Vo"}]

url = ""
local = False


class Main(QApplication):
    def __init__(self):
        super(Main, self).__init__([])
        self.setStyleSheet(style)
        self.window = QMainWindow()
        self.menu = self.window.menuBar().addMenu("&Menu")
        self.tabs = QTabWidget()
        self.setup()

    def setup(self):
        self.window.setObjectName("windows")
        self.window.setWindowTitle("Advertisement Monitoring System")
        self.window.setWindowIcon(QIcon("images/logo.ico"))
        self.menu.addAction("&Close", self.window.close)
        st = QStatusBar()
        st.showMessage("Welcome! Thanks for using the app.")
        self.window.setStatusBar(st)
        self.tabs.tabBar().setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.tabs.setMinimumSize(1024, 720)
        self.window.setCentralWidget(self.tabs)


class Layout(QWidget):
    def __init__(self):
        super(Layout, self).__init__()
        self.setObjectName("tabs_av")
        self.layout = grids()
        self.setLayout(self.layout)


#Frame show on screen using thread
class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QImage)

    def run(self):
        if selected_ads:
            if local:
                vid = cv2.VideoCapture(url)
            else:
                video = pafy.new(url, ydl_opts={'nocheckcertificate': True})
                best = video.streams[2]
                assert best is not None
                vid = cv2.VideoCapture(best.url)
            while vid.isOpened():
                ret, frame = vid.read()
                if ret:
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bpl = ch * w
                    in_qt_format = QImage(rgb_image.data, w, h, bpl, QImage.Format_RGB888)
                    p = in_qt_format.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)
                    time.sleep(0.01)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
            vid.release()


#simple Buttons
class Button(QPushButton):
    def __init__(self, btn_text):
        super(Button, self).__init__(btn_text)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setMinimumWidth(200)
        self.adjustSize()


#Image Buttons Reuse Layout
class ToolButton(QToolButton):
    ResizeSignal = QtCore.pyqtSignal(int)

    def __init__(self, image, name):
        super().__init__()
        self.setIcon(QIcon(image))
        self.setIconSize(QtCore.QSize(320, 250))
        self.setText(name)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setCheckable(True)
        self.setAutoRaise(True)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    def resizeEvent(self, event):
        self.setIconSize(QtCore.QSize(self.width() - 30, self.height() - 50))

#Player Layout
class VideoPlayer(QLabel):
    ResizeSignal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setLineWidth(3)
        self.pix = None
        self.th = Thread(self)
        self.setText("<h3>Please Wait.....</h3>")
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.th.changePixmap.connect(self.change_image)

    def change_image(self, image):
        self.setText("")
        self.pix = QPixmap.fromImage(image)
        self.setPixmap(self.pix.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio))

#Same button
class Stack(QStackedWidget):
    def __init__(self):
        super(Stack, self).__init__()

    def next_button(self, layout, opt, disabled=True, add_func=lambda: None):
        next_btn = Button("Next")
        next_btn.setDisabled(disabled)
        next_btn.clicked.connect(lambda: self.setCurrentIndex(self.currentIndex() + 1) or add_func())
        layout.addWidget(next_btn, *opt)
        return next_btn

    def back_button(self, layout, opt, add_func=lambda: None):
        back_btn = Button("Back")
        back_btn.clicked.connect(lambda: self.setCurrentIndex(self.currentIndex() - 1) or add_func())
        layout.addWidget(back_btn, *opt)
        return back_btn

    def check(self, se, button, others=None, url_f=False, set_name=False):
        global url
        if url_f:
            for b in brs:
                if se.text() == b.get("name"):
                    url = b.get("url")
        if others is not None:
            for x in others:
                if x != se:
                    x.setChecked(False)
        if se.isChecked():
            button.setDisabled(False)
        else:
            button.setDisabled(True)

        if set_name:
            global name_ad
            name_ad = se.text()

#Main Menu Layout
class MainMenu(Layout):
    def __init__(self):
        super(MainMenu, self).__init__()

        f_btn = Button("Feed Ad")
        m_btn = Button("Monitor Ad")
        h_btn = Button("History")
        q_btn = Button("Quit")
        f_btn.setObjectName("menu_options")
        m_btn.setObjectName("menu_options")
        h_btn.setObjectName("menu_options")
        q_btn.setObjectName("menu_options")
        label = QLabel("<h1>Advertisement Monitoring System</h1>")
        label.setFont(QFont('Castellar', 16))
        label.setObjectName("main_name_label")
        f_btn.clicked.connect(lambda: app.tabs.setCurrentIndex(1))
        m_btn.clicked.connect(lambda: app.tabs.setCurrentIndex(2))
        h_btn.clicked.connect(lambda: app.tabs.setCurrentIndex(3))
        q_btn.clicked.connect(lambda: app.tabs.setCurrentIndex(4))
        self.layout.addWidget(label, 0, 0, 3, 10, QtCore.Qt.AlignCenter)
        self.layout.addWidget(f_btn, 3, 3, 1, 4)
        self.layout.addWidget(m_btn, 4, 3, 1, 4)
        self.layout.addWidget(h_btn, 5, 3, 1, 4)
        self.layout.addWidget(q_btn, 6, 3, 1, 4)
        self.layout.setVerticalSpacing(0)


#Feed Ad Layout
class FeedAd(Stack):
    def __init__(self):
        super(FeedAd, self).__init__()

        self.vid_l = QGridLayout()
        self.vid_l.rowMinimumHeight(300)
        self.vid_l.setDefaultPositioning(3, QtCore.Qt.Horizontal)
        self.addWidget(self.set_layout())
        self.addWidget(self.loading_screen())

    def set_layout(self):
        main_wid = QWidget()
        layout = grids()
        wid = QWidget()
        wid.setLayout(self.vid_l)
        wid.setObjectName("f_n")
        scroll = QScrollArea()
        scroll.setWidget(wid)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll, 0, 0, 6, 9)
        feed_btn = Button("Browse Ad!")
        feed_btn.clicked.connect(self.get_file)
        layout.addWidget(feed_btn, 7, 4)
        for file in os.listdir("ad_thumbs"):
            self.add_button(file.split(".")[0])
        main_wid.setLayout(layout)
        return main_wid

    def add_button(self, name):
        btn = ToolButton(f"ad_thumbs/{name}.jpg", name)
        btn.setMinimumSize(200, 150)
        btn.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        btn_selectable = ToolButton(f"ad_thumbs/{name}.jpg", name)
        btn_selectable.setMinimumSize(200, 150)
        btn_selectable.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        btn_selectable.clicked.connect(lambda: monitor_ad.check(btn_selectable.sender(), monitor_ad.btn_next,
                                                                selected_ads, set_name=True))
        selected_ads.append(btn_selectable)
        monitor_ad.vid_l.addWidget(btn_selectable)
        btn.setCheckable(False)
        btn.setAutoRaise(False)
        btn.setCursor(QCursor(QtCore.Qt.ArrowCursor))
        self.vid_l.addWidget(btn)

    def loading_screen(self):
        main_widget = QWidget()
        loading_layout = grids()
        widget = QLabel()
        movie = QMovie("loading.gif")
        widget.setMovie(movie)
        loading_layout.addWidget(widget, 0, 0, 9, 9, QtCore.Qt.AlignCenter)
        movie.start()
        main_widget.setLayout(loading_layout)
        return main_widget

    def get_file(self):
        dialog = QFileDialog()
        file_opened = dialog.getOpenFileName(caption="Open Video", filter="Videos (*.mp4)")
        if file_opened[0] != '':
            ad_name = file_opened[0].split("/")[-1].split(".")[0]

            self.setCurrentIndex(1)
            if os.listdir("ad_thumbs").__contains__(f"{ad_name}.jpg"):
                print("Already added!")
                self.setCurrentIndex(0)
                return False
            vidcap = cv2.VideoCapture(file_opened[0])
            success, image = vidcap.read()
            cv2.imwrite(f"ad_thumbs/{ad_name}.jpg", image)
            try:
                a = threading.Thread(target=main.feed_ad, args=(file_opened[0], ad_name))
                a.start()
                while a.is_alive():
                    QApplication.processEvents()

                self.add_button(ad_name)
                self.setCurrentIndex(0)
            except:
                traceback.print_exc()


#Counter Layout
class ThreadCounter(QtCore.QThread):
    Signal = QtCore.pyqtSignal(list)

    def __init__(self):
        super(ThreadCounter, self).__init__()

    def run(self):
        t = datetime.datetime.now()
        while True:
            elapsed_time = datetime.datetime.now() - t
            time.sleep(1)
            self.Signal.emit([str(elapsed_time).split(".")[0], main.history_text])

#Monitor Ad Layout
class MonitorAd(Stack):
    def __init__(self):
        super(MonitorAd, self).__init__()
        self.btn_next = None
        self.ad_sel = None
        self.name = None
        self.vid_l = QGridLayout()
        self.vid_l.rowMinimumHeight(300)
        self.vid_l.setDefaultPositioning(3, QtCore.Qt.Horizontal)
        # Third page
        self.broadcast = VideoPlayer()
        self.text = QLabel()
        self.time_mon = QLabel()
        self.th = ThreadCounter()
        self.ad_name = QLabel()
        self.ad_time = QLabel()
        self.currentChanged.connect(self.check_c)
        app.tabs.currentChanged.connect(self.check_c)
        self.th.Signal.connect(self.change_val)
        self.addWidget(self.first_page())
        self.addWidget(self.second_page())
        self.addWidget(self.get_broadcast())
        self.addWidget(self.third_page())
        self.file = ""
        self.mon_start = None

    def change_val(self, vals):
        self.time_mon.setText(vals[0])
        self.text.setText(f"<h3>Report</h3><hr>{'<br>'.join(vals[1].split('<br>'))}")
#//tabs changing
    def check_c(self):
        if self.currentIndex() == 3 and app.tabs.currentIndex() == 2:
            self.ad_name.setText(name_ad)
            self.th.start()
            try:
                self.broadcast.th.start()
                features = main.load_ad_features(f'{name_ad}.npy')
                main.monitoring_start = True
                if local:
                    archeive_video_name =  url.split("/")[-1].split(".")[0]
                    self.mon_start = threading.Thread(target=main.monitor_archeive, args = (features,url, archeive_video_name))
                    self.mon_start.start()
                else:
                    self.mon_start = threading.Thread(target=main.live_broadcast_frames_extraction, args=(features, url))
                    self.mon_start.start()
            except:
                traceback.print_exc()
        else:
            if self.th.isRunning():
                if app.tabs.currentIndex() != 2:
                    self.setCurrentIndex(0)
                self.th.terminate()
                history_local = "archive" if local else "broadcast"
                if self.mon_start is not None:
                    main.monitoring_start = False
                with open(f"history/{date_today}/{name_ad} in {history_local}", "a") as history_file:
                    main.history_text = main.history_text.replace("<h3>Report</h3><hr>", "")
                    main.history_text = main.history_text.replace("<br>", "\n")
                    history_file.write(main.history_text)
                main.history_text = ""
                self.text.setText("<h3>Report</h3><hr>")
                self.set_local(False)
                self.time_mon.setText("")
                self.broadcast.th.terminate()
                self.broadcast.setPixmap(QPixmap())
                self.broadcast.setText("<h3>Please Wait....</h3>")
#layouts
    def first_page(self):
        wid = QWidget()
        wid.setLayout(self.vid_l)
        wid.setObjectName("f_n")
        scroll = QScrollArea()
        scroll.setWidget(wid)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setWidgetResizable(True)
        first_layout = Layout()
        self.btn_next = self.next_button(first_layout.layout, [8, 8])
        first_layout.layout.addWidget(scroll, 0, 0, 7, 9)
        first_layout.layout.addWidget(self.ad_sel, 1, 2, 5, 5)
        return first_layout

    def second_page(self):
        sec_layout = Layout()
        btn_browse_local = Button("Select from Local Videos")
        btn_browse_local.clicked.connect(self.get_local_video)
        btn_broadcast = Button("Select from Live Broadcasts")
        btn_browse_local.setObjectName("monitor_ad_archive_broadcast_btns")
        btn_broadcast.setObjectName("monitor_ad_archive_broadcast_btns")
        btn_broadcast.clicked.connect(lambda: self.setCurrentIndex(2))
        sec_layout.layout.addWidget(btn_browse_local, 3, 2, 1, 5)
        sec_layout.layout.addWidget(btn_broadcast, 4, 2, 1, 5)
        sec_layout.layout.setVerticalSpacing(0)
        self.back_button(sec_layout.layout, [8, 8])
        return sec_layout

    def get_local_video(self):
        global url
        dialog = QFileDialog()
        url = dialog.getOpenFileName(caption="Select from local videos", filter="Videos (*.mp4)")[0]
        if url != "":
            self.set_local(True)
            self.setCurrentIndex(3)

        main.monitor_frames()

    @staticmethod
    def set_local(val):
        global local
        local = val
#broadcast layout
    def get_broadcast(self):
        global brs
        second_layout = Layout()
        added = []
        btn_next_1 = self.next_button(second_layout.layout, [8, 8], add_func=lambda: self.set_local(False))
        btn_back = self.back_button(second_layout.layout, [8, 6])
        for br in brs:
            added.append(ToolButton(br["image"], br["name"]))
        al = [[1, 1], [1, 5], [4, 1], [4, 5]]
        for i in range(4):
            added[i].clicked.connect(lambda: self.check(added[i].sender(), btn_next_1, added, True))
            added[i].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            second_layout.layout.addWidget(added[i], al[i][0], al[i][1], 3, 3)
        coming_soon = QLabel("<h3>More Channels will be coming soon!</h3>")
        second_layout.layout.addWidget(coming_soon, 8, 1, 1, 3, QtCore.Qt.AlignCenter)
        return second_layout
#Monitoring Page layout
    def third_page(self):
        third_layout = Layout()

        self.text.setObjectName("hist")
        self.text.setText("<h3>Report</h3><hr>")
        self.text.setAlignment(QtCore.Qt.AlignTop)
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.text)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(True)
        self.time_mon.setText("")
        self.time_mon.setObjectName("hist")
        self.time_mon.setAlignment(QtCore.Qt.AlignCenter)
        self.ad_name.setText("")
        self.ad_name.setObjectName("hist")
        self.ad_name.setAlignment(QtCore.Qt.AlignCenter)
        self.ad_time.setText("")
        self.ad_time.setObjectName("hist")
        self.ad_time.setAlignment(QtCore.Qt.AlignCenter)
        btn_back = self.back_button(third_layout.layout, [8, 8],
                                    add_func=lambda: self.setCurrentIndex(1) if local else self.setCurrentIndex(2))
        third_layout.layout.addWidget(self.broadcast, 0, 0, 6, 6)
        third_layout.layout.addWidget(scroll_area, 0, 6, 6, 3)
        third_layout.layout.addWidget(self.time_mon, 8, 0)
        third_layout.layout.addWidget(self.ad_name, 8, 2)
        third_layout.layout.addWidget(self.ad_time, 8, 4)
        return third_layout

#History Tab
class History(Stack):
    def __init__(self):
        super(History, self).__init__()
        self.lab = QLabel("\n\nHELLO HISTORY")
        self.lab.setObjectName("hist")
        self.addWidget(self.first_page())
        self.addWidget(self.second_page())
        self.lab.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

    def first_page(self):
        first_layout = Layout()
        ca = QCalendarWidget()
        first_layout.layout.addWidget(ca, 1, 1, 6, 7)
        btn = self.next_button(first_layout.layout, [8, 8], False)
        btn.clicked.connect(lambda: self.get_date(ca))
        return first_layout

    def second_page(self):
        second_layout = Layout()
        download_btn = Button("Download")
        second_layout.layout.addWidget(download_btn, 8, 8)
        second_layout.layout.addWidget(self.lab, 1, 1, 6, 7)
        self.back_button(second_layout.layout, [8, 6])
        return second_layout

    def get_date(self, cal):
        global date
        self.setCurrentIndex(self.currentIndex() + 1)
        date = cal.selectedDate()
        self.lab.setText(f"<h3>Report for {date.toString()}</h3><hr>")


#Quit Tab
class Quit(Layout):
    def __init__(self):
        super(Quit, self).__init__()
        self.set_layout()

    def set_layout(self):
        quit_label = QLabel("<h1>Are you sure, you want to quit!</h1>")
        quit_label.setFont(QFont('Arial', 14))
        self.layout.addWidget(quit_label, 0, 2, 9, 5, QtCore.Qt.AlignCenter)

        yes_btn = Button("Yes")
        yes_btn.clicked.connect(app.window.close)
        self.layout.addWidget(yes_btn, 8, 6)
        no_btn = Button("No")
        no_btn.clicked.connect(app.tabs.tabBar().setCurrentIndex)
        self.layout.addWidget(no_btn, 8, 8)


if __name__ == '__main__':
    if not os.path.exists("ad_thumbs"):
        os.mkdir("ad_thumbs")
    if not os.path.exists("history"):
        os.mkdir("history")
    date_today = datetime.datetime.now().strftime("%d-%m-%Y")
    if not os.path.exists(f"history/{date_today}"):
        os.mkdir(f"history/{date_today}")
    app = Main()
    main_menu = MainMenu()
    monitor_ad = MonitorAd()
    feed_ad = FeedAd()
    history = History()
    quit_tab = Quit()
    app.tabs.addTab(main_menu, "Main Menu")
    app.tabs.addTab(feed_ad, "Feed Ad")
    app.tabs.addTab(monitor_ad, "Monitor Ad")
    app.tabs.addTab(history, "History")
    app.tabs.addTab(quit_tab, "Quit")
    app.window.show()
    sys.exit(app.exec())
