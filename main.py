from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMenuBar,
    QMenu,
    QMessageBox,
    QListWidget,
    QTabWidget,
    QFileDialog,
    QCheckBox,
    QStyle,
    QScrollArea,
)
from PySide6.QtCore import Qt, Signal, QTime
from PySide6.QtGui import QFont, QAction, QPixmap, QActionGroup, QIcon
import qdarkstyle
import os
import sys
import script

desktop = os.path.join(os.path.expanduser("~"), "Desktop")


def get_resource_path(relative_path):
    """获取资源文件的绝对路径，适用于开发环境和打包后的环境"""
    try:
        # PyInstaller 创建临时文件夹并将路径存储在 _MEIPASS 中
        base_path = sys._MEIPASS
    except Exception:
        # 如果没有 _MEIPASS，说明是在开发环境中运行
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.load_ui()
        self.bind()
        self.center()
        self.automatic_theme_switching()

    def load_ui(self):
        # 设置窗口大小
        self.resize(800, 600)
        self.setWindowTitle("做着玩的")
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        )
        self.mainLayout = QVBoxLayout()
        # 一 菜单栏
        self.menuBar = QMenuBar()
        self.menuBar.setFont(QFont("微软雅黑", 15))
        # 1. 打开文件菜单
        self.fileMenu = QMenu("📁文件 ", self)
        self.openFile = QAction("打开文件", self)
        self.openFile.setShortcut("Ctrl+O")
        self.openFile.setFont(QFont("微软雅黑", 15))
        self.openFile.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)
        )
        self.fileMenu.addAction(self.openFile)
        self.menuBar.addMenu(self.fileMenu)
        # 2. 设置菜单
        self.settingsMenu = QMenu("⚙️设置 ", self)
        self.settingsMenu.setFont(QFont("微软雅黑", 15))
        # 主题菜单
        self.themeMenu = QMenu("🌈主题", self)
        self.themeMenu.setFont(QFont("微软雅黑", 15))
        self.themeGroup = QActionGroup(self)
        self.lightMode = QAction("☀️浅色模式", self)
        self.lightMode.setChecked(True)
        self.lightMode.setCheckable(True)
        self.darkMode = QAction("🌙深色模式", self)
        self.darkMode.setCheckable(True)
        self.themeGroup.addAction(self.lightMode)
        self.themeGroup.addAction(self.darkMode)
        self.themeMenu.addAction(self.lightMode)
        self.themeMenu.addAction(self.darkMode)

        self.windowMenu = QMenu("🪟窗口", self)
        self.windowMenu.setFont(QFont("微软雅黑", 15))
        self.stayOnTop = QAction("窗口置顶", self)
        self.stayOnTop.setShortcut("Ctrl+T")

        self.stayOnTop.setCheckable(True)
        self.windowMenu.addAction(self.stayOnTop)

        self.settingsMenu.addMenu(self.themeMenu)
        self.settingsMenu.addMenu(self.windowMenu)
        self.menuBar.addMenu(self.settingsMenu)

        # 二 选项卡 qidong
        self.tab1 = QWidget()
        self.tab1Layout = QVBoxLayout()

        self.checkAll = QCheckBox("选择所有")
        self.checkAll.setFont(QFont("微软雅黑", 12))
        self.checkAll.setChecked(True)

        self.namesList = QListWidget()
        self.namesList.setFont(QFont("微软雅黑", 15))
        # 可以多选
        self.namesList.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.contents = self.load_app_list()
        self.namesList.addItems(self.contents)

        # 添加一个右键菜单用于删除数据
        self.namesList.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.namesListAction = QAction("删除", self)
        self.namesListAction.setFont(QFont("微软雅黑", 12))
        self.namesList.addAction(self.namesListAction)

        # 设置所有元素能够被checked
        for i in range(self.namesList.count()):
            item = self.namesList.item(i)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)

        self.addBtn = QPushButton("请添加你要启动的软件")
        self.addBtn.setFont(QFont("微软雅黑", 12))
        self.addBtn.setFixedHeight(40)

        self.startBtn = QPushButton("一键启动")
        self.startBtn.setFont(QFont("微软雅黑", 12))
        self.startBtn.setFixedHeight(40)

        self.tab1Layout.addWidget(self.checkAll)
        self.tab1Layout.addWidget(self.namesList)
        self.tab1Layout.addWidget(self.addBtn)
        self.tab1Layout.addWidget(self.startBtn)

        self.tab1.setLayout(self.tab1Layout)

        self.tab2 = QWidget()

        # 图片
        self.tab3 = QWidget()
        self.tab3Layout = QVBoxLayout()

        # 设置右键菜单
        self.tab3.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.changeImageAction = QAction("📷更换图片", self)
        self.changeImageAction.setFont(QFont("微软雅黑", 12))
        self.tab3.addAction(self.changeImageAction)

        # 创建滚动区域来显示图片
        self.scrollArea = QScrollArea()
        self.imageLabel = QLabel()

        # 如果要显示图片，保持原始宽高比
        image_path = get_resource_path("image1.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # 直接显示原图，保持完美的宽高比
            self.imageLabel.setPixmap(pixmap)
            # 设置图片标签的大小为图片的实际大小
            self.imageLabel.resize(pixmap.size())

        # 让图片在标签中居中显示
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 将图片标签放入滚动区域
        self.scrollArea.setWidget(self.imageLabel)
        # 让滚动区域内容居中
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 设置滚动区域的策略，让它能够自适应窗口大小
        self.scrollArea.setWidgetResizable(True)
        # 设置滚动区域的最小尺寸
        self.scrollArea.setMinimumSize(400, 400)

        # 让滚动区域填充整个选项卡空间，而不是居中显示
        self.tab3Layout.addWidget(self.scrollArea)
        self.tab3.setLayout(self.tab3Layout)

        self.tab = QTabWidget()
        self.tab.setFont(QFont("微软雅黑", 12))
        self.tab.addTab(self.tab1, "启动启动")
        self.tab.addTab(self.tab2, "选项卡2")
        self.tab.addTab(self.tab3, "图片")

        self.mainLayout.addWidget(self.tab)
        self.mainLayout.setMenuBar(self.menuBar)
        self.setLayout(self.mainLayout)

    def center(self):
        # 添加窗口居中显示的代码
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_size = self.size()
        self.move(
            (screen_geometry.width() - window_size.width()) // 2,
            (screen_geometry.height() - window_size.height()) // 2,
        )

    # 信号
    def bind(self):
        self.openFile.triggered.connect(self.open_file)
        self.lightMode.triggered.connect(self.set_light_mode)
        self.darkMode.triggered.connect(self.set_dark_mode)
        self.stayOnTop.triggered.connect(self.set_stay_on_top)
        self.addBtn.clicked.connect(self.on_addBtn_click)
        self.startBtn.clicked.connect(self.on_startBtn_click)
        self.namesList.doubleClicked.connect(self.on_namesList_doubleClicked)
        self.namesList.itemChanged.connect(self.on_namesList_itemChanged)
        self.checkAll.stateChanged.connect(self.on_checkAll_stateChanged)
        self.namesListAction.triggered.connect(self.on_namesListAction_triggered)
        self.changeImageAction.triggered.connect(self.on_changeImageAction_triggered)

    def on_namesListAction_triggered(self):
        """当右键菜单项被触发时，删除选中的应用"""
        # 删除namesList、contents和本地文件
        for item in self.namesList.selectedItems():
            self.namesList.takeItem(self.namesList.row(item))
            self.contents.remove(item.text())
            # 从文件中删除对应的行
            self.delete_names(item)

    def delete_names(self, item):
        """从文件中删除对应的行"""
        if not os.path.exists("names.txt"):
            return
        with open("names.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open("names.txt", "w", encoding="utf-8") as f:
            for line in lines:
                if line.strip() != item.text():
                    f.write(line)

    def on_namesList_itemChanged(self, item):
        """当列表项状态改变时，更新全选复选框状态"""
        self.update_checkAll_state()

    def update_checkAll_state(self):
        """根据列表项状态更新全选复选框"""
        total_count = self.namesList.count()
        if total_count == 0:
            return

        checked_count = 0
        for i in range(total_count):
            item = self.namesList.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                checked_count += 1

        # 临时断开信号连接，避免递归调用
        self.checkAll.stateChanged.disconnect()

        # 只有全选或全不选两种状态
        if checked_count == total_count:
            # 全部选中
            self.checkAll.setChecked(True)
        else:
            # 部分选中或全部未选中都显示为未选中
            self.checkAll.setChecked(False)

        # 重新连接信号
        self.checkAll.stateChanged.connect(self.on_checkAll_stateChanged)

    def on_checkAll_stateChanged(self):
        """全选复选框状态改变时，更新所有列表项"""
        new_state = (
            Qt.CheckState.Checked
            if self.checkAll.isChecked()
            else Qt.CheckState.Unchecked
        )

        for i in range(self.namesList.count()):
            item = self.namesList.item(i)
            item.setCheckState(new_state)

    def on_namesList_doubleClicked(self, index):
        item = self.namesList.item(index.row())
        new_state = (
            Qt.CheckState.Checked
            if item.checkState() == Qt.CheckState.Unchecked
            else Qt.CheckState.Unchecked
        )
        item.setCheckState(new_state)

    def load_app_list(self):
        if not os.path.exists("names.txt"):
            return []
        with open("names.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    def on_addBtn_click(self):
        result = QFileDialog.getOpenFileNames(
            self, "打开文件", desktop, "可执行文件 (*.exe *.lnk)"
        )
        # 去除重复项
        if result[0] not in self.contents:
            if result[0]:
                with open("names.txt", "a", encoding="utf-8") as f:
                    f.write(result[0] + "\n")
                # 重新读取文件，刷新self.contents和QListWidget
                self.contents = self.load_app_list()
                self.namesList.clear()
                self.namesList.addItems(self.contents)
                # 为新添加的所有元素设置复选框
                for i in range(self.namesList.count()):
                    item = self.namesList.item(i)
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(Qt.CheckState.Checked)

            # 更新全选复选框状态
            self.update_checkAll_state()
        else:
            # 如果已存在相同项，则不添加
            QMessageBox.warning(self, "警告", "该项已存在！")

    def on_startBtn_click(self):
        # 启动被勾选的软件
        selected = []
        for i in range(self.namesList.count()):
            item = self.namesList.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected.append(item.text())

        if selected:
            script.open_applications(selected)
        else:
            # 如果没有勾选任何项目，启动所有软件
            script.open_applications(self.contents)

    # 设置窗口置顶
    def set_stay_on_top(self, checked):
        # 保存当前窗口状态
        was_visible = self.isVisible()
        current_pos = self.pos()
        current_size = self.size()

        # 设置窗口标志
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, checked)

        # 如果窗口之前是可见的，重新显示并恢复位置和大小
        if was_visible:
            self.show()
            self.move(current_pos)
            self.resize(current_size)

    def open_file(self):
        QFileDialog.getOpenFileNames(self, "打开文件", "", "所有文件 (*)")

    def set_light_mode(self):
        app.setStyleSheet(
            qdarkstyle.load_stylesheet(
                qt_api="pyside6", palette=qdarkstyle.LightPalette
            )
        )

    def set_dark_mode(self):
        app.setStyleSheet(
            qdarkstyle.load_stylesheet(qt_api="pyside6", palette=qdarkstyle.DarkPalette)
        )

    def automatic_theme_switching(self):
        # 自动主题切换
        current_hour = QTime.currentTime().hour()
        if 6 <= current_hour < 18:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def on_changeImageAction_triggered(self):
        """当右键菜单更换图片被触发时"""
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.jpg *.jpeg *.png *.bmp *.gif)"
        )

        if image_path:
            # 加载新图片
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.imageLabel.setPixmap(pixmap)
                self.imageLabel.resize(pixmap.size())
            else:
                QMessageBox.warning(self, "错误", "无法加载选中的图片文件！")


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
# pyinstaller -F -w main.py --add-data "image1.jpg;." --distpath release --workpath build_temp
