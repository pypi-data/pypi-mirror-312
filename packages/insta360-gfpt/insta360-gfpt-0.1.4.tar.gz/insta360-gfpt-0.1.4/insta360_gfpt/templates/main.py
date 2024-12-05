import sys
#
from src.test_project import TestProject

from PySide6.QtGui import QGuiApplication, QImageReader
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl
if __name__ == '__main__':
    app = QGuiApplication()
    engine = QQmlApplicationEngine()
    QImageReader.setAllocationLimit(0)
    # 初始化项目
    logical_lock = {"enable": False, "pwd": "123456"}
    # proj = TestProject(version="1.1.0", logical_lock=logical_lock, project='IAC2')
    proj = TestProject(version="1.2.9_build4_VB", logical_lock=logical_lock, project='VB')
    if not proj.proj_init():
        raise ("init proj fail!")

    root_context = engine.rootContext()
    root_context.setContextProperty("Proj", proj)
    engine.load(QUrl("res/qml/main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    # proj.set_module_index(proj.group_index, proj.module_index)
    app.aboutToQuit.connect(proj.teardown)
    sys.exit(app.exec())
