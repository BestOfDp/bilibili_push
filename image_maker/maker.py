import sys
import os
import shutil
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from image_maker import ImageMaker


class filedialogdemo(QWidget):

    def __init__(self):
        self.GUI_init()
        self.offset_h = 0
        self.font_size = 0
        self.pre = None
        # self.center()
        self.setWindowIcon(QIcon('head.jpg'))

    def center(self):
        self.setGeometry(100, 100, 100, 100)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _add_label(self):
        self.text = QLabel('内容')
        self.textEdit = QLineEdit()
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.text, 1, 0)
        grid.addWidget(self.textEdit, 1, 1)
        return grid

    def _add_op_btn(self):
        self.btn_up = QPushButton()
        self.btn_up.clicked.connect(self.up)
        self.btn_up.setText("上移")
        self.btn_down = QPushButton()
        self.btn_down.clicked.connect(self.down)
        self.btn_down.setText("下移")

        self.btn_add = QPushButton()
        self.btn_add.clicked.connect(self.add)
        self.btn_add.setText("增大字体")
        self.btn_desc = QPushButton()
        self.btn_desc.clicked.connect(self.desc)
        self.btn_desc.setText("缩小字体")

        op_box = QHBoxLayout()
        op_box.addStretch(1)
        op_box.addWidget(self.btn_add)
        op_box.addWidget(self.btn_desc)
        op_box.addWidget(self.btn_up)
        op_box.addWidget(self.btn_down)
        return op_box

    def _add_io_btn(self):
        self.btn.clicked.connect(self.loadFile)
        self.btn.setText("从文件中获取照片")

        self.btn_save = QPushButton()
        self.btn_save.clicked.connect(self.save_file)
        self.btn_save.setText("保存")

        self.btn_add_word = QPushButton()
        self.btn_add_word.clicked.connect(self.add_word)
        self.btn_add_word.setText("查看效果")

        io_box = QHBoxLayout()
        io_box.addStretch(1)
        io_box.addWidget(self.btn)
        io_box.addWidget(self.btn_add_word)
        io_box.addWidget(self.btn_save)
        return io_box

    def GUI_init(self):
        layout = QVBoxLayout()
        super(filedialogdemo, self).__init__()
        self.btn = QPushButton()
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(self._add_io_btn())
        vbox.addLayout(self._add_op_btn())
        layout.addLayout(self._add_label())
        layout.addLayout(vbox)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setWindowTitle("表情包生成器")

        self.setLayout(layout)

    def add(self):
        self.font_size += 5
        self.add_word()

    def desc(self):
        self.font_size -= 5
        self.add_word()

    def up(self):
        self.offset_h -= 1
        self.add_word()

    def down(self):
        self.offset_h += 1
        self.add_word()

    def loadFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', "./",
                                               'Image files(*.jpg *.gif *.png)')
        setattr(self, 'path', fname)
        self.label.setPixmap(QPixmap(fname))

    def save_file(self):
        if self.pre is None:
            QMessageBox.information(self, "错误", "没有生成表情包！",
                                    QMessageBox.Yes)
            return
        fileName2, ok2 = QFileDialog.getSaveFileName(self,
                                                     "文件保存",
                                                     "c://{}".format(self.textEdit.text()),
                                                     "Image Files (*.jpg)",
                                                     )
        if fileName2:
            shutil.copyfile(self.get_image_name(self.pre), fileName2)
            QMessageBox.information(self, "成功", "生成表情包成功！",
                                    QMessageBox.Yes)
            os.remove(self.get_image_name(self.pre))

    def add_word(self):
        if not self._judge():
            QMessageBox.information(self, "错误", "添加文字不能为空！",
                                    QMessageBox.Yes)
            return
        try:
            image_maker = ImageMaker(self.path, self.textEdit.text(), self.offset_h, self.font_size)
            path = image_maker.run()
            self.label.setPixmap(QPixmap(path))

            if self.pre and os.path.exists(self.get_image_name(self.pre)):
                os.remove(self.get_image_name(self.pre))
            self.pre = path
        except Exception as e:
            QMessageBox.information(self, "错误", "先上传图片！",
                                    QMessageBox.Yes)

    def _judge(self):
        return True if self.textEdit.text() else False

    @staticmethod
    def get_image_name(name):
        return '{}.jpg'.format(name)

    def closeEvent(self, event):
        if self.pre and os.path.exists(self.get_image_name(self.pre)):
            os.remove(self.get_image_name(self.pre))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileload = filedialogdemo()
    fileload.show()
    sys.exit(app.exec_())
