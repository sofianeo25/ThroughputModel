# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDial, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1344, 983)
        self.frame = QWidget(MainWindow)
        self.frame.setObjectName(u"frame")
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.calculate_phy_btn = QPushButton(self.frame)
        self.calculate_phy_btn.setObjectName(u"calculate_phy_btn")
        self.calculate_phy_btn.setStyleSheet(u"background-color: rgb(255, 147, 0)")

        self.gridLayout.addWidget(self.calculate_phy_btn, 2, 0, 1, 1)

        self.show_phy_le = QLineEdit(self.frame)
        self.show_phy_le.setObjectName(u"show_phy_le")
        self.show_phy_le.setAlignment(Qt.AlignCenter)
        self.show_phy_le.setReadOnly(True)

        self.gridLayout.addWidget(self.show_phy_le, 3, 0, 1, 1)

        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_phy = QWidget()
        self.tab_phy.setObjectName(u"tab_phy")
        self.horizontalLayout = QHBoxLayout(self.tab_phy)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_left = QFrame(self.tab_phy)
        self.frame_left.setObjectName(u"frame_left")
        self.frame_left.setStyleSheet(u"")
        self.frame_left.setFrameShape(QFrame.StyledPanel)
        self.frame_left.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_left)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(6, 6, 6, 6)
        self.Header = QGroupBox(self.frame_left)
        self.Header.setObjectName(u"Header")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Header.sizePolicy().hasHeightForWidth())
        self.Header.setSizePolicy(sizePolicy)
        self.Header.setMinimumSize(QSize(1220, 85))
        self.horizontalLayout_6 = QHBoxLayout(self.Header)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(6, 6, 6, 6)
        self.layout_menu_principal = QHBoxLayout()
        self.layout_menu_principal.setObjectName(u"layout_menu_principal")
        self.layout_menu_principal.setContentsMargins(6, 6, 6, 6)
        self.standard_selection = QHBoxLayout()
        self.standard_selection.setObjectName(u"standard_selection")
        self.standard_selection.setContentsMargins(6, 6, 6, 6)
        self.standard_selection_label = QLabel(self.Header)
        self.standard_selection_label.setObjectName(u"standard_selection_label")
        self.standard_selection_label.setAlignment(Qt.AlignCenter)

        self.standard_selection.addWidget(self.standard_selection_label, 0, Qt.AlignHCenter)

        self.comboBox_standard_selection = QComboBox(self.Header)
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.setObjectName(u"comboBox_standard_selection")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_standard_selection.sizePolicy().hasHeightForWidth())
        self.comboBox_standard_selection.setSizePolicy(sizePolicy1)

        self.standard_selection.addWidget(self.comboBox_standard_selection, 0, Qt.AlignHCenter)


        self.layout_menu_principal.addLayout(self.standard_selection)

        self.frequency_band = QHBoxLayout()
        self.frequency_band.setObjectName(u"frequency_band")
        self.frequency_band.setContentsMargins(6, 6, 6, 6)
        self.label_frequency_band = QLabel(self.Header)
        self.label_frequency_band.setObjectName(u"label_frequency_band")
        self.label_frequency_band.setAlignment(Qt.AlignCenter)

        self.frequency_band.addWidget(self.label_frequency_band, 0, Qt.AlignHCenter)

        self.comboBox_frequency_band = QComboBox(self.Header)
        self.comboBox_frequency_band.addItem("")
        self.comboBox_frequency_band.addItem("")
        self.comboBox_frequency_band.addItem("")
        self.comboBox_frequency_band.addItem("")
        self.comboBox_frequency_band.setObjectName(u"comboBox_frequency_band")
        sizePolicy1.setHeightForWidth(self.comboBox_frequency_band.sizePolicy().hasHeightForWidth())
        self.comboBox_frequency_band.setSizePolicy(sizePolicy1)

        self.frequency_band.addWidget(self.comboBox_frequency_band, 0, Qt.AlignHCenter)


        self.layout_menu_principal.addLayout(self.frequency_band)

        self.bandwidth = QHBoxLayout()
        self.bandwidth.setObjectName(u"bandwidth")
        self.bandwidth.setContentsMargins(6, 6, 6, 6)
        self.bandwidth_label = QLabel(self.Header)
        self.bandwidth_label.setObjectName(u"bandwidth_label")
        self.bandwidth_label.setAlignment(Qt.AlignCenter)

        self.bandwidth.addWidget(self.bandwidth_label, 0, Qt.AlignHCenter)

        self.comboBox_bandwidth = QComboBox(self.Header)
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.setObjectName(u"comboBox_bandwidth")
        sizePolicy1.setHeightForWidth(self.comboBox_bandwidth.sizePolicy().hasHeightForWidth())
        self.comboBox_bandwidth.setSizePolicy(sizePolicy1)

        self.bandwidth.addWidget(self.comboBox_bandwidth, 0, Qt.AlignHCenter)


        self.layout_menu_principal.addLayout(self.bandwidth)


        self.horizontalLayout_6.addLayout(self.layout_menu_principal)


        self.gridLayout_4.addWidget(self.Header, 1, 0, 1, 3)

        self.vertical_right = QVBoxLayout()
        self.vertical_right.setObjectName(u"vertical_right")
        self.vertical_right.setContentsMargins(6, 6, 6, 6)
        self.vertical_3 = QGroupBox(self.frame_left)
        self.vertical_3.setObjectName(u"vertical_3")
        self.vertical_trois = QVBoxLayout(self.vertical_3)
        self.vertical_trois.setObjectName(u"vertical_trois")
        self.vertical_trois.setContentsMargins(0, 0, 0, 0)
        self.groupbox_dcm = QGroupBox(self.vertical_3)
        self.groupbox_dcm.setObjectName(u"groupbox_dcm")
        self.groupbox_dcm.setMaximumSize(QSize(16777215, 50))
        self.groupbox_dcm.setFlat(False)
        self.DCM = QHBoxLayout(self.groupbox_dcm)
        self.DCM.setObjectName(u"DCM")
        self.DCM.setContentsMargins(6, 6, 6, 6)
        self.label_dcm = QLabel(self.groupbox_dcm)
        self.label_dcm.setObjectName(u"label_dcm")

        self.DCM.addWidget(self.label_dcm)

        self.pushButton_dcm = QPushButton(self.groupbox_dcm)
        self.pushButton_dcm.setObjectName(u"pushButton_dcm")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_dcm.sizePolicy().hasHeightForWidth())
        self.pushButton_dcm.setSizePolicy(sizePolicy2)
        self.pushButton_dcm.setMinimumSize(QSize(70, 0))
        self.pushButton_dcm.setMaximumSize(QSize(70, 16777215))
        self.pushButton_dcm.setCheckable(True)
        self.pushButton_dcm.setFlat(False)

        self.DCM.addWidget(self.pushButton_dcm)


        self.vertical_trois.addWidget(self.groupbox_dcm)

        self.groupbox_nru = QGroupBox(self.vertical_3)
        self.groupbox_nru.setObjectName(u"groupbox_nru")
        self.groupbox_nru.setMaximumSize(QSize(16777215, 50))
        self.NRU = QHBoxLayout(self.groupbox_nru)
        self.NRU.setObjectName(u"NRU")
        self.NRU.setContentsMargins(6, 6, 6, 6)
        self.label_nru = QLabel(self.groupbox_nru)
        self.label_nru.setObjectName(u"label_nru")

        self.NRU.addWidget(self.label_nru)

        self.comboBox_nru = QComboBox(self.groupbox_nru)
        self.comboBox_nru.addItem("")
        self.comboBox_nru.addItem("")
        self.comboBox_nru.setObjectName(u"comboBox_nru")
        self.comboBox_nru.setMinimumSize(QSize(80, 0))
        self.comboBox_nru.setMaximumSize(QSize(70, 16777215))

        self.NRU.addWidget(self.comboBox_nru)


        self.vertical_trois.addWidget(self.groupbox_nru)

        self.groupbox_mu_mimo = QGroupBox(self.vertical_3)
        self.groupbox_mu_mimo.setObjectName(u"groupbox_mu_mimo")
        self.groupbox_mu_mimo.setMaximumSize(QSize(16777215, 50))
        self.MU_MIMO = QHBoxLayout(self.groupbox_mu_mimo)
        self.MU_MIMO.setObjectName(u"MU_MIMO")
        self.MU_MIMO.setContentsMargins(6, 6, 6, 6)
        self.label_mu_mimo = QLabel(self.groupbox_mu_mimo)
        self.label_mu_mimo.setObjectName(u"label_mu_mimo")

        self.MU_MIMO.addWidget(self.label_mu_mimo)

        self.pushButton_mu_mimo = QPushButton(self.groupbox_mu_mimo)
        self.pushButton_mu_mimo.setObjectName(u"pushButton_mu_mimo")
        sizePolicy2.setHeightForWidth(self.pushButton_mu_mimo.sizePolicy().hasHeightForWidth())
        self.pushButton_mu_mimo.setSizePolicy(sizePolicy2)
        self.pushButton_mu_mimo.setMinimumSize(QSize(70, 0))
        self.pushButton_mu_mimo.setMaximumSize(QSize(70, 16777215))
        self.pushButton_mu_mimo.setCheckable(True)
        self.pushButton_mu_mimo.setFlat(False)

        self.MU_MIMO.addWidget(self.pushButton_mu_mimo)


        self.vertical_trois.addWidget(self.groupbox_mu_mimo)

        self.groupbox_ofdma = QGroupBox(self.vertical_3)
        self.groupbox_ofdma.setObjectName(u"groupbox_ofdma")
        self.groupbox_ofdma.setMaximumSize(QSize(16777215, 50))
        self.OFDMA = QHBoxLayout(self.groupbox_ofdma)
        self.OFDMA.setObjectName(u"OFDMA")
        self.OFDMA.setContentsMargins(6, 6, 6, 6)
        self.ofdma_label = QLabel(self.groupbox_ofdma)
        self.ofdma_label.setObjectName(u"ofdma_label")

        self.OFDMA.addWidget(self.ofdma_label)

        self.pushButton_ofdma = QPushButton(self.groupbox_ofdma)
        self.pushButton_ofdma.setObjectName(u"pushButton_ofdma")
        sizePolicy2.setHeightForWidth(self.pushButton_ofdma.sizePolicy().hasHeightForWidth())
        self.pushButton_ofdma.setSizePolicy(sizePolicy2)
        self.pushButton_ofdma.setMinimumSize(QSize(70, 0))
        self.pushButton_ofdma.setMaximumSize(QSize(70, 16777215))
        self.pushButton_ofdma.setCheckable(True)
        self.pushButton_ofdma.setFlat(False)

        self.OFDMA.addWidget(self.pushButton_ofdma)


        self.vertical_trois.addWidget(self.groupbox_ofdma)

        self.groupbox_angle_quantif = QGroupBox(self.vertical_3)
        self.groupbox_angle_quantif.setObjectName(u"groupbox_angle_quantif")
        self.groupbox_angle_quantif.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.groupbox_angle_quantif)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.angle_quantif_label = QLabel(self.groupbox_angle_quantif)
        self.angle_quantif_label.setObjectName(u"angle_quantif_label")

        self.horizontalLayout_2.addWidget(self.angle_quantif_label)

        self.spinBox_angle_quantif = QSpinBox(self.groupbox_angle_quantif)
        self.spinBox_angle_quantif.setObjectName(u"spinBox_angle_quantif")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.spinBox_angle_quantif.sizePolicy().hasHeightForWidth())
        self.spinBox_angle_quantif.setSizePolicy(sizePolicy3)
        self.spinBox_angle_quantif.setMinimumSize(QSize(70, 0))
        self.spinBox_angle_quantif.setMaximumSize(QSize(62, 16777215))
        self.spinBox_angle_quantif.setMinimum(1)
        self.spinBox_angle_quantif.setMaximum(360)

        self.horizontalLayout_2.addWidget(self.spinBox_angle_quantif)


        self.vertical_trois.addWidget(self.groupbox_angle_quantif)


        self.vertical_right.addWidget(self.vertical_3)


        self.gridLayout_4.addLayout(self.vertical_right, 2, 2, 2, 1)

        self.vertical_left = QVBoxLayout()
        self.vertical_left.setObjectName(u"vertical_left")
        self.vertical_left.setContentsMargins(6, 6, 6, 6)
        self.groupbox_modulation = QGroupBox(self.frame_left)
        self.groupbox_modulation.setObjectName(u"groupbox_modulation")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.groupbox_modulation.sizePolicy().hasHeightForWidth())
        self.groupbox_modulation.setSizePolicy(sizePolicy4)
        self.groupbox_modulation.setMinimumSize(QSize(0, 0))
        self.groupbox_modulation.setMaximumSize(QSize(16777215, 50))
        self.choice_modulation_2 = QHBoxLayout(self.groupbox_modulation)
        self.choice_modulation_2.setObjectName(u"choice_modulation_2")
        self.choice_modulation_2.setContentsMargins(6, 6, 6, 6)
        self.choice_of_modulation_label = QLabel(self.groupbox_modulation)
        self.choice_of_modulation_label.setObjectName(u"choice_of_modulation_label")

        self.choice_modulation_2.addWidget(self.choice_of_modulation_label)

        self.combobox_choice_modulation = QComboBox(self.groupbox_modulation)
        self.combobox_choice_modulation.addItem("")
        self.combobox_choice_modulation.addItem("")
        self.combobox_choice_modulation.addItem("")
        self.combobox_choice_modulation.addItem("")
        self.combobox_choice_modulation.addItem("")
        self.combobox_choice_modulation.addItem("")
        self.combobox_choice_modulation.addItem("")
        self.combobox_choice_modulation.addItem("")
        self.combobox_choice_modulation.setObjectName(u"combobox_choice_modulation")
        self.combobox_choice_modulation.setMinimumSize(QSize(80, 0))
        self.combobox_choice_modulation.setMaximumSize(QSize(70, 16777215))

        self.choice_modulation_2.addWidget(self.combobox_choice_modulation)


        self.vertical_left.addWidget(self.groupbox_modulation)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vertical_left.addItem(self.verticalSpacer)

        self.groupbox_ctrl_modulation = QGroupBox(self.frame_left)
        self.groupbox_ctrl_modulation.setObjectName(u"groupbox_ctrl_modulation")
        self.groupbox_ctrl_modulation.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_3 = QHBoxLayout(self.groupbox_ctrl_modulation)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.label_ctrl_modulation = QLabel(self.groupbox_ctrl_modulation)
        self.label_ctrl_modulation.setObjectName(u"label_ctrl_modulation")

        self.horizontalLayout_3.addWidget(self.label_ctrl_modulation)

        self.comboBox_ctrl_modulation = QComboBox(self.groupbox_ctrl_modulation)
        self.comboBox_ctrl_modulation.addItem("")
        self.comboBox_ctrl_modulation.addItem("")
        self.comboBox_ctrl_modulation.addItem("")
        self.comboBox_ctrl_modulation.addItem("")
        self.comboBox_ctrl_modulation.addItem("")
        self.comboBox_ctrl_modulation.addItem("")
        self.comboBox_ctrl_modulation.addItem("")
        self.comboBox_ctrl_modulation.addItem("")
        self.comboBox_ctrl_modulation.setObjectName(u"comboBox_ctrl_modulation")
        self.comboBox_ctrl_modulation.setMinimumSize(QSize(80, 0))
        self.comboBox_ctrl_modulation.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_3.addWidget(self.comboBox_ctrl_modulation)


        self.vertical_left.addWidget(self.groupbox_ctrl_modulation)

        self.groupbox_wifi_n = QGroupBox(self.frame_left)
        self.groupbox_wifi_n.setObjectName(u"groupbox_wifi_n")
        self.gridLayout_3 = QGridLayout(self.groupbox_wifi_n)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.groupBox_greenfield = QGroupBox(self.groupbox_wifi_n)
        self.groupBox_greenfield.setObjectName(u"groupBox_greenfield")
        self.groupBox_greenfield.setMaximumSize(QSize(16777215, 50))
        self.groupBox_greenfield.setFlat(False)
        self.greenfield = QHBoxLayout(self.groupBox_greenfield)
        self.greenfield.setObjectName(u"greenfield")
        self.greenfield.setSizeConstraint(QLayout.SetMinimumSize)
        self.greenfield.setContentsMargins(6, 6, 6, 6)
        self.label_greenfield = QLabel(self.groupBox_greenfield)
        self.label_greenfield.setObjectName(u"label_greenfield")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.label_greenfield.sizePolicy().hasHeightForWidth())
        self.label_greenfield.setSizePolicy(sizePolicy5)

        self.greenfield.addWidget(self.label_greenfield)

        self.pushButton_greenfield = QPushButton(self.groupBox_greenfield)
        self.pushButton_greenfield.setObjectName(u"pushButton_greenfield")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.pushButton_greenfield.sizePolicy().hasHeightForWidth())
        self.pushButton_greenfield.setSizePolicy(sizePolicy6)
        self.pushButton_greenfield.setMinimumSize(QSize(70, 0))
        self.pushButton_greenfield.setMaximumSize(QSize(70, 16777215))
        self.pushButton_greenfield.setCheckable(True)
        self.pushButton_greenfield.setChecked(False)

        self.greenfield.addWidget(self.pushButton_greenfield)


        self.gridLayout_3.addWidget(self.groupBox_greenfield, 3, 0, 1, 1)

        self.groupBox_control_preamble = QGroupBox(self.groupbox_wifi_n)
        self.groupBox_control_preamble.setObjectName(u"groupBox_control_preamble")
        self.groupBox_control_preamble.setMaximumSize(QSize(16777215, 50))
        self.groupBox_control_preamble.setFlat(False)
        self.control_preamble = QHBoxLayout(self.groupBox_control_preamble)
        self.control_preamble.setObjectName(u"control_preamble")
        self.control_preamble.setSizeConstraint(QLayout.SetMinimumSize)
        self.control_preamble.setContentsMargins(6, 6, 6, 6)
        self.label_control_preamble = QLabel(self.groupBox_control_preamble)
        self.label_control_preamble.setObjectName(u"label_control_preamble")

        self.control_preamble.addWidget(self.label_control_preamble)

        self.pushButton_control_preamble = QPushButton(self.groupBox_control_preamble)
        self.pushButton_control_preamble.setObjectName(u"pushButton_control_preamble")
        sizePolicy6.setHeightForWidth(self.pushButton_control_preamble.sizePolicy().hasHeightForWidth())
        self.pushButton_control_preamble.setSizePolicy(sizePolicy6)
        self.pushButton_control_preamble.setMinimumSize(QSize(70, 0))
        self.pushButton_control_preamble.setMaximumSize(QSize(70, 16777215))
        self.pushButton_control_preamble.setCheckable(True)
        self.pushButton_control_preamble.setChecked(False)

        self.control_preamble.addWidget(self.pushButton_control_preamble)


        self.gridLayout_3.addWidget(self.groupBox_control_preamble, 4, 0, 1, 1)

        self.groupBox_txop = QGroupBox(self.groupbox_wifi_n)
        self.groupBox_txop.setObjectName(u"groupBox_txop")
        self.groupBox_txop.setMaximumSize(QSize(16777215, 50))
        self.groupBox_txop.setFlat(False)
        self.txop = QHBoxLayout(self.groupBox_txop)
        self.txop.setObjectName(u"txop")
        self.txop.setSizeConstraint(QLayout.SetMinimumSize)
        self.txop.setContentsMargins(6, 6, 6, 6)
        self.label_txop = QLabel(self.groupBox_txop)
        self.label_txop.setObjectName(u"label_txop")

        self.txop.addWidget(self.label_txop)

        self.pushButton_txop = QPushButton(self.groupBox_txop)
        self.pushButton_txop.setObjectName(u"pushButton_txop")
        sizePolicy6.setHeightForWidth(self.pushButton_txop.sizePolicy().hasHeightForWidth())
        self.pushButton_txop.setSizePolicy(sizePolicy6)
        self.pushButton_txop.setMinimumSize(QSize(70, 0))
        self.pushButton_txop.setMaximumSize(QSize(70, 16777215))
        self.pushButton_txop.setCheckable(True)
        self.pushButton_txop.setChecked(False)

        self.txop.addWidget(self.pushButton_txop)


        self.gridLayout_3.addWidget(self.groupBox_txop, 5, 0, 1, 1)

        self.groupBox_sgi_ul = QGroupBox(self.groupbox_wifi_n)
        self.groupBox_sgi_ul.setObjectName(u"groupBox_sgi_ul")
        self.groupBox_sgi_ul.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_sgi_ul.setFlat(False)
        self.groupBox = QHBoxLayout(self.groupBox_sgi_ul)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setContentsMargins(6, 6, 6, 6)
        self.label_sgi_ul = QLabel(self.groupBox_sgi_ul)
        self.label_sgi_ul.setObjectName(u"label_sgi_ul")

        self.groupBox.addWidget(self.label_sgi_ul)

        self.comboBox_sgi_ul = QComboBox(self.groupBox_sgi_ul)
        self.comboBox_sgi_ul.addItem("")
        self.comboBox_sgi_ul.addItem("")
        self.comboBox_sgi_ul.addItem("")
        self.comboBox_sgi_ul.setObjectName(u"comboBox_sgi_ul")
        self.comboBox_sgi_ul.setMinimumSize(QSize(80, 0))
        self.comboBox_sgi_ul.setMaximumSize(QSize(70, 16777215))

        self.groupBox.addWidget(self.comboBox_sgi_ul)


        self.gridLayout_3.addWidget(self.groupBox_sgi_ul, 8, 0, 1, 1)

        self.groupBox_sgi_dl = QGroupBox(self.groupbox_wifi_n)
        self.groupBox_sgi_dl.setObjectName(u"groupBox_sgi_dl")
        self.groupBox_sgi_dl.setMaximumSize(QSize(16777215, 16777215))
        self.groupBox_sgi_dl.setFlat(False)
        self.SGI_DL_2 = QHBoxLayout(self.groupBox_sgi_dl)
        self.SGI_DL_2.setObjectName(u"SGI_DL_2")
        self.SGI_DL_2.setContentsMargins(6, 6, 6, 6)
        self.label_sgi_dl = QLabel(self.groupBox_sgi_dl)
        self.label_sgi_dl.setObjectName(u"label_sgi_dl")

        self.SGI_DL_2.addWidget(self.label_sgi_dl)

        self.comboBox_sgi_dl = QComboBox(self.groupBox_sgi_dl)
        self.comboBox_sgi_dl.addItem("")
        self.comboBox_sgi_dl.addItem("")
        self.comboBox_sgi_dl.addItem("")
        self.comboBox_sgi_dl.setObjectName(u"comboBox_sgi_dl")
        self.comboBox_sgi_dl.setMinimumSize(QSize(80, 0))
        self.comboBox_sgi_dl.setMaximumSize(QSize(70, 16777215))

        self.SGI_DL_2.addWidget(self.comboBox_sgi_dl)


        self.gridLayout_3.addWidget(self.groupBox_sgi_dl, 7, 0, 1, 1)

        self.groupBox_ldpc = QGroupBox(self.groupbox_wifi_n)
        self.groupBox_ldpc.setObjectName(u"groupBox_ldpc")
        self.groupBox_ldpc.setMaximumSize(QSize(16777215, 50))
        self.groupBox_ldpc.setFlat(False)
        self.LDPC = QHBoxLayout(self.groupBox_ldpc)
        self.LDPC.setObjectName(u"LDPC")
        self.LDPC.setContentsMargins(6, 6, 6, 6)
        self.label_ldpc = QLabel(self.groupBox_ldpc)
        self.label_ldpc.setObjectName(u"label_ldpc")

        self.LDPC.addWidget(self.label_ldpc)

        self.pushButton_ldpc = QPushButton(self.groupBox_ldpc)
        self.pushButton_ldpc.setObjectName(u"pushButton_ldpc")
        sizePolicy2.setHeightForWidth(self.pushButton_ldpc.sizePolicy().hasHeightForWidth())
        self.pushButton_ldpc.setSizePolicy(sizePolicy2)
        self.pushButton_ldpc.setMinimumSize(QSize(70, 0))
        self.pushButton_ldpc.setMaximumSize(QSize(70, 16777215))
        self.pushButton_ldpc.setCheckable(True)
        self.pushButton_ldpc.setChecked(False)

        self.LDPC.addWidget(self.pushButton_ldpc)


        self.gridLayout_3.addWidget(self.groupBox_ldpc, 0, 0, 1, 1)

        self.groupBox_nb_of_ss = QGroupBox(self.groupbox_wifi_n)
        self.groupBox_nb_of_ss.setObjectName(u"groupBox_nb_of_ss")
        self.groupBox_nb_of_ss.setMaximumSize(QSize(16777215, 50))
        self.groupBox_nb_of_ss.setFlat(False)
        self.groupBox_nb_ss = QHBoxLayout(self.groupBox_nb_of_ss)
        self.groupBox_nb_ss.setObjectName(u"groupBox_nb_ss")
        self.groupBox_nb_ss.setContentsMargins(6, 6, 6, 6)
        self.label_nb_ss = QLabel(self.groupBox_nb_of_ss)
        self.label_nb_ss.setObjectName(u"label_nb_ss")

        self.groupBox_nb_ss.addWidget(self.label_nb_ss)

        self.comboBox_number_spatial_stream = QComboBox(self.groupBox_nb_of_ss)
        self.comboBox_number_spatial_stream.addItem("")
        self.comboBox_number_spatial_stream.addItem("")
        self.comboBox_number_spatial_stream.addItem("")
        self.comboBox_number_spatial_stream.addItem("")
        self.comboBox_number_spatial_stream.setObjectName(u"comboBox_number_spatial_stream")
        sizePolicy2.setHeightForWidth(self.comboBox_number_spatial_stream.sizePolicy().hasHeightForWidth())
        self.comboBox_number_spatial_stream.setSizePolicy(sizePolicy2)
        self.comboBox_number_spatial_stream.setMinimumSize(QSize(80, 0))
        self.comboBox_number_spatial_stream.setMaximumSize(QSize(70, 16777215))

        self.groupBox_nb_ss.addWidget(self.comboBox_number_spatial_stream)


        self.gridLayout_3.addWidget(self.groupBox_nb_of_ss, 1, 0, 1, 1)

        self.groupBox_stbc = QGroupBox(self.groupbox_wifi_n)
        self.groupBox_stbc.setObjectName(u"groupBox_stbc")
        self.groupBox_stbc.setMaximumSize(QSize(16777215, 50))
        self.groupBox_stbc.setFlat(False)
        self.STBC = QHBoxLayout(self.groupBox_stbc)
        self.STBC.setObjectName(u"STBC")
        self.STBC.setContentsMargins(6, 6, 6, 6)
        self.label_stbc = QLabel(self.groupBox_stbc)
        self.label_stbc.setObjectName(u"label_stbc")

        self.STBC.addWidget(self.label_stbc)

        self.pushButton_stbc = QPushButton(self.groupBox_stbc)
        self.pushButton_stbc.setObjectName(u"pushButton_stbc")
        sizePolicy2.setHeightForWidth(self.pushButton_stbc.sizePolicy().hasHeightForWidth())
        self.pushButton_stbc.setSizePolicy(sizePolicy2)
        self.pushButton_stbc.setMinimumSize(QSize(70, 0))
        self.pushButton_stbc.setMaximumSize(QSize(70, 16777215))
        self.pushButton_stbc.setCheckable(True)
        self.pushButton_stbc.setChecked(False)

        self.STBC.addWidget(self.pushButton_stbc)


        self.gridLayout_3.addWidget(self.groupBox_stbc, 2, 0, 1, 1)

        self.sgi = QHBoxLayout()
        self.sgi.setObjectName(u"sgi")
        self.sgi.setContentsMargins(6, 6, 6, 6)
        self.label_sgi = QLabel(self.groupbox_wifi_n)
        self.label_sgi.setObjectName(u"label_sgi")
        sizePolicy5.setHeightForWidth(self.label_sgi.sizePolicy().hasHeightForWidth())
        self.label_sgi.setSizePolicy(sizePolicy5)
        self.label_sgi.setAlignment(Qt.AlignCenter)

        self.sgi.addWidget(self.label_sgi, 0, Qt.AlignLeft)

        self.pushButton_sgi = QPushButton(self.groupbox_wifi_n)
        self.pushButton_sgi.setObjectName(u"pushButton_sgi")
        self.pushButton_sgi.setMinimumSize(QSize(70, 0))
        self.pushButton_sgi.setMaximumSize(QSize(70, 16777215))
        self.pushButton_sgi.setCheckable(True)
        self.pushButton_sgi.setChecked(False)

        self.sgi.addWidget(self.pushButton_sgi)


        self.gridLayout_3.addLayout(self.sgi, 6, 0, 1, 1)


        self.vertical_left.addWidget(self.groupbox_wifi_n)


        self.gridLayout_4.addLayout(self.vertical_left, 2, 0, 2, 1)

        self.vertical_center = QVBoxLayout()
        self.vertical_center.setObjectName(u"vertical_center")
        self.vertical_center.setContentsMargins(6, 6, 6, 6)
        self.other_parameters_802_11_n_2 = QVBoxLayout()
        self.other_parameters_802_11_n_2.setObjectName(u"other_parameters_802_11_n_2")
        self.other_parameters_802_11_n_2.setContentsMargins(6, 6, 6, 6)
        self.groupbox_antennas = QGroupBox(self.frame_left)
        self.groupbox_antennas.setObjectName(u"groupbox_antennas")
        self.verticalLayout_3 = QVBoxLayout(self.groupbox_antennas)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.antennas = QGridLayout()
        self.antennas.setObjectName(u"antennas")
        self.antennas.setContentsMargins(0, 0, 0, 0)
        self.label_title_antennas = QLabel(self.groupbox_antennas)
        self.label_title_antennas.setObjectName(u"label_title_antennas")
        sizePolicy5.setHeightForWidth(self.label_title_antennas.sizePolicy().hasHeightForWidth())
        self.label_title_antennas.setSizePolicy(sizePolicy5)
        self.label_title_antennas.setAlignment(Qt.AlignCenter)

        self.antennas.addWidget(self.label_title_antennas, 0, 0, 1, 1)

        self.groupBox_ap_nb = QGroupBox(self.groupbox_antennas)
        self.groupBox_ap_nb.setObjectName(u"groupBox_ap_nb")
        self.groupBox_ap_nb.setMaximumSize(QSize(16777215, 50))
        self.groupBox_ap_nb.setFlat(True)
        self.ap_number_2 = QHBoxLayout(self.groupBox_ap_nb)
        self.ap_number_2.setObjectName(u"ap_number_2")
        self.ap_number_2.setContentsMargins(6, 6, 6, 6)
        self.label_antennas_ap_number = QLabel(self.groupBox_ap_nb)
        self.label_antennas_ap_number.setObjectName(u"label_antennas_ap_number")

        self.ap_number_2.addWidget(self.label_antennas_ap_number)

        self.comboBox_ap_number = QComboBox(self.groupBox_ap_nb)
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.setObjectName(u"comboBox_ap_number")
        self.comboBox_ap_number.setMinimumSize(QSize(80, 0))
        self.comboBox_ap_number.setMaximumSize(QSize(70, 16777215))

        self.ap_number_2.addWidget(self.comboBox_ap_number)


        self.antennas.addWidget(self.groupBox_ap_nb, 1, 0, 1, 1)

        self.groupBox_station_number = QGroupBox(self.groupbox_antennas)
        self.groupBox_station_number.setObjectName(u"groupBox_station_number")
        self.groupBox_station_number.setMaximumSize(QSize(16777215, 50))
        self.groupBox_station_number.setFlat(True)
        self.station_number_2 = QHBoxLayout(self.groupBox_station_number)
        self.station_number_2.setObjectName(u"station_number_2")
        self.station_number_2.setContentsMargins(6, 6, 6, 6)
        self.label_antennas_station_number = QLabel(self.groupBox_station_number)
        self.label_antennas_station_number.setObjectName(u"label_antennas_station_number")

        self.station_number_2.addWidget(self.label_antennas_station_number)

        self.comboBox_station_number = QComboBox(self.groupBox_station_number)
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.setObjectName(u"comboBox_station_number")
        self.comboBox_station_number.setMinimumSize(QSize(80, 0))
        self.comboBox_station_number.setMaximumSize(QSize(70, 16777215))

        self.station_number_2.addWidget(self.comboBox_station_number)


        self.antennas.addWidget(self.groupBox_station_number, 2, 0, 1, 1)

        self.groupBox_users_nb = QGroupBox(self.groupbox_antennas)
        self.groupBox_users_nb.setObjectName(u"groupBox_users_nb")
        self.groupBox_users_nb.setMaximumSize(QSize(16777215, 50))
        self.groupBox_users_nb.setFlat(True)
        self.users_number_2 = QHBoxLayout(self.groupBox_users_nb)
        self.users_number_2.setObjectName(u"users_number_2")
        self.users_number_2.setContentsMargins(6, 6, 6, 6)
        self.label_antennas_users_number = QLabel(self.groupBox_users_nb)
        self.label_antennas_users_number.setObjectName(u"label_antennas_users_number")

        self.users_number_2.addWidget(self.label_antennas_users_number)

        self.comboBox_users_number = QComboBox(self.groupBox_users_nb)
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.setObjectName(u"comboBox_users_number")
        self.comboBox_users_number.setMinimumSize(QSize(80, 0))
        self.comboBox_users_number.setMaximumSize(QSize(70, 16777215))

        self.users_number_2.addWidget(self.comboBox_users_number)


        self.antennas.addWidget(self.groupBox_users_nb, 3, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.antennas)


        self.other_parameters_802_11_n_2.addWidget(self.groupbox_antennas)

        self.groupbox_mu_su = QGroupBox(self.frame_left)
        self.groupbox_mu_su.setObjectName(u"groupbox_mu_su")
        self.grid_su = QGridLayout(self.groupbox_mu_su)
        self.grid_su.setObjectName(u"grid_su")
        self.grid_su.setContentsMargins(6, 6, 6, 6)
        self.groupBox_mu_slider = QGroupBox(self.groupbox_mu_su)
        self.groupBox_mu_slider.setObjectName(u"groupBox_mu_slider")
        self.groupBox_mu_slider.setFlat(True)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_mu_slider)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(6, 6, 6, 6)
        self.label_mu = QLabel(self.groupBox_mu_slider)
        self.label_mu.setObjectName(u"label_mu")
        sizePolicy6.setHeightForWidth(self.label_mu.sizePolicy().hasHeightForWidth())
        self.label_mu.setSizePolicy(sizePolicy6)

        self.verticalLayout_8.addWidget(self.label_mu, 0, Qt.AlignHCenter)

        self.mu_slider = QDial(self.groupBox_mu_slider)
        self.mu_slider.setObjectName(u"mu_slider")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.mu_slider.sizePolicy().hasHeightForWidth())
        self.mu_slider.setSizePolicy(sizePolicy7)
        self.mu_slider.setMaximum(100)

        self.verticalLayout_8.addWidget(self.mu_slider, 0, Qt.AlignHCenter)

        self.lineEdit_affichage_mu = QLineEdit(self.groupBox_mu_slider)
        self.lineEdit_affichage_mu.setObjectName(u"lineEdit_affichage_mu")
        self.lineEdit_affichage_mu.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.lineEdit_affichage_mu, 0, Qt.AlignHCenter)


        self.grid_su.addWidget(self.groupBox_mu_slider, 0, 0, 1, 1)

        self.groupBox_su_slider = QGroupBox(self.groupbox_mu_su)
        self.groupBox_su_slider.setObjectName(u"groupBox_su_slider")
        self.groupBox_su_slider.setFlat(True)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_su_slider)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(6, 6, 6, 6)
        self.label_su = QLabel(self.groupBox_su_slider)
        self.label_su.setObjectName(u"label_su")
        sizePolicy6.setHeightForWidth(self.label_su.sizePolicy().hasHeightForWidth())
        self.label_su.setSizePolicy(sizePolicy6)

        self.verticalLayout_9.addWidget(self.label_su, 0, Qt.AlignHCenter)

        self.su_slider = QDial(self.groupBox_su_slider)
        self.su_slider.setObjectName(u"su_slider")
        sizePolicy7.setHeightForWidth(self.su_slider.sizePolicy().hasHeightForWidth())
        self.su_slider.setSizePolicy(sizePolicy7)
        self.su_slider.setMaximum(100)
        self.su_slider.setNotchTarget(3.700000000000000)

        self.verticalLayout_9.addWidget(self.su_slider, 0, Qt.AlignHCenter)

        self.lineEdit_affichage_su = QLineEdit(self.groupBox_su_slider)
        self.lineEdit_affichage_su.setObjectName(u"lineEdit_affichage_su")
        self.lineEdit_affichage_su.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.lineEdit_affichage_su, 0, Qt.AlignHCenter)


        self.grid_su.addWidget(self.groupBox_su_slider, 0, 1, 1, 1)


        self.other_parameters_802_11_n_2.addWidget(self.groupbox_mu_su)

        self.groupbox_csi = QGroupBox(self.frame_left)
        self.groupbox_csi.setObjectName(u"groupbox_csi")
        self.groupbox_csi.setMaximumSize(QSize(16777215, 200))
        self.CSI = QVBoxLayout(self.groupbox_csi)
        self.CSI.setObjectName(u"CSI")
        self.CSI.setContentsMargins(6, 6, 6, 6)
        self.csi = QHBoxLayout()
        self.csi.setObjectName(u"csi")
        self.csi.setContentsMargins(6, 6, 6, 6)
        self.label_csi_title = QLabel(self.groupbox_csi)
        self.label_csi_title.setObjectName(u"label_csi_title")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.label_csi_title.sizePolicy().hasHeightForWidth())
        self.label_csi_title.setSizePolicy(sizePolicy8)
        self.label_csi_title.setAlignment(Qt.AlignCenter)

        self.csi.addWidget(self.label_csi_title)

        self.pushButton_csi = QPushButton(self.groupbox_csi)
        self.pushButton_csi.setObjectName(u"pushButton_csi")
        self.pushButton_csi.setMinimumSize(QSize(70, 0))
        self.pushButton_csi.setMaximumSize(QSize(70, 16777215))
        self.pushButton_csi.setCheckable(True)

        self.csi.addWidget(self.pushButton_csi)


        self.CSI.addLayout(self.csi)

        self.groupBox_number_of_csi = QGroupBox(self.groupbox_csi)
        self.groupBox_number_of_csi.setObjectName(u"groupBox_number_of_csi")
        self.groupBox_number_of_csi.setMaximumSize(QSize(16777215, 50))
        self.groupBox_number_of_csi.setFlat(True)
        self.number_of_csi = QHBoxLayout(self.groupBox_number_of_csi)
        self.number_of_csi.setObjectName(u"number_of_csi")
        self.number_of_csi.setContentsMargins(6, 6, 6, 6)
        self.label_number_of_csi = QLabel(self.groupBox_number_of_csi)
        self.label_number_of_csi.setObjectName(u"label_number_of_csi")

        self.number_of_csi.addWidget(self.label_number_of_csi)

        self.comboBox_nb_csi = QComboBox(self.groupBox_number_of_csi)
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.addItem("")
        self.comboBox_nb_csi.setObjectName(u"comboBox_nb_csi")
        sizePolicy9 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.comboBox_nb_csi.sizePolicy().hasHeightForWidth())
        self.comboBox_nb_csi.setSizePolicy(sizePolicy9)
        self.comboBox_nb_csi.setMinimumSize(QSize(80, 0))
        self.comboBox_nb_csi.setMaximumSize(QSize(70, 16777215))

        self.number_of_csi.addWidget(self.comboBox_nb_csi)


        self.CSI.addWidget(self.groupBox_number_of_csi)

        self.groupBox_number_of_ss_for_CSI = QGroupBox(self.groupbox_csi)
        self.groupBox_number_of_ss_for_CSI.setObjectName(u"groupBox_number_of_ss_for_CSI")
        self.groupBox_number_of_ss_for_CSI.setMaximumSize(QSize(16777215, 50))
        self.groupBox_number_of_ss_for_CSI.setFlat(True)
        self.number_of_ss_for_CSI = QHBoxLayout(self.groupBox_number_of_ss_for_CSI)
        self.number_of_ss_for_CSI.setObjectName(u"number_of_ss_for_CSI")
        self.number_of_ss_for_CSI.setContentsMargins(6, 6, 6, 6)
        self.label_number_of_ss_for_csi = QLabel(self.groupBox_number_of_ss_for_CSI)
        self.label_number_of_ss_for_csi.setObjectName(u"label_number_of_ss_for_csi")

        self.number_of_ss_for_CSI.addWidget(self.label_number_of_ss_for_csi)

        self.comboBox_nb_of_ss_csi = QComboBox(self.groupBox_number_of_ss_for_CSI)
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.setObjectName(u"comboBox_nb_of_ss_csi")
        sizePolicy9.setHeightForWidth(self.comboBox_nb_of_ss_csi.sizePolicy().hasHeightForWidth())
        self.comboBox_nb_of_ss_csi.setSizePolicy(sizePolicy9)
        self.comboBox_nb_of_ss_csi.setMinimumSize(QSize(80, 0))
        self.comboBox_nb_of_ss_csi.setMaximumSize(QSize(70, 16777215))

        self.number_of_ss_for_CSI.addWidget(self.comboBox_nb_of_ss_csi)


        self.CSI.addWidget(self.groupBox_number_of_ss_for_CSI)

        self.groupBox_antennas_for_csi = QGroupBox(self.groupbox_csi)
        self.groupBox_antennas_for_csi.setObjectName(u"groupBox_antennas_for_csi")
        self.groupBox_antennas_for_csi.setMaximumSize(QSize(16777215, 50))
        self.groupBox_antennas_for_csi.setFlat(True)
        self.antennas_for_csi = QHBoxLayout(self.groupBox_antennas_for_csi)
        self.antennas_for_csi.setObjectName(u"antennas_for_csi")
        self.antennas_for_csi.setContentsMargins(6, 6, 6, 6)
        self.label_antennas_for_csi = QLabel(self.groupBox_antennas_for_csi)
        self.label_antennas_for_csi.setObjectName(u"label_antennas_for_csi")

        self.antennas_for_csi.addWidget(self.label_antennas_for_csi)

        self.comboBox_antennas_csi = QComboBox(self.groupBox_antennas_for_csi)
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.setObjectName(u"comboBox_antennas_csi")
        self.comboBox_antennas_csi.setMinimumSize(QSize(80, 0))
        self.comboBox_antennas_csi.setMaximumSize(QSize(70, 16777215))

        self.antennas_for_csi.addWidget(self.comboBox_antennas_csi)


        self.CSI.addWidget(self.groupBox_antennas_for_csi)


        self.other_parameters_802_11_n_2.addWidget(self.groupbox_csi)


        self.vertical_center.addLayout(self.other_parameters_802_11_n_2)


        self.gridLayout_4.addLayout(self.vertical_center, 2, 1, 2, 1)


        self.horizontalLayout.addWidget(self.frame_left)

        self.tabWidget.addTab(self.tab_phy, "")
        self.tab_mac = QWidget()
        self.tab_mac.setObjectName(u"tab_mac")
        self.gridLayout_5 = QGridLayout(self.tab_mac)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.groupBox_mac_result = QGroupBox(self.tab_mac)
        self.groupBox_mac_result.setObjectName(u"groupBox_mac_result")
        self.horizontalLayout_12 = QHBoxLayout(self.groupBox_mac_result)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_mac = QLabel(self.groupBox_mac_result)
        self.label_mac.setObjectName(u"label_mac")
        sizePolicy10 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.label_mac.sizePolicy().hasHeightForWidth())
        self.label_mac.setSizePolicy(sizePolicy10)
        self.label_mac.setLayoutDirection(Qt.LeftToRight)
        self.label_mac.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_mac)

        self.lineEdit_mac = QLineEdit(self.groupBox_mac_result)
        self.lineEdit_mac.setObjectName(u"lineEdit_mac")
        sizePolicy6.setHeightForWidth(self.lineEdit_mac.sizePolicy().hasHeightForWidth())
        self.lineEdit_mac.setSizePolicy(sizePolicy6)
        self.lineEdit_mac.setMinimumSize(QSize(100, 0))
        self.lineEdit_mac.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_12.addWidget(self.lineEdit_mac)

        self.label_udp = QLabel(self.groupBox_mac_result)
        self.label_udp.setObjectName(u"label_udp")
        sizePolicy10.setHeightForWidth(self.label_udp.sizePolicy().hasHeightForWidth())
        self.label_udp.setSizePolicy(sizePolicy10)
        self.label_udp.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_udp)

        self.lineEdit_udp = QLineEdit(self.groupBox_mac_result)
        self.lineEdit_udp.setObjectName(u"lineEdit_udp")
        sizePolicy6.setHeightForWidth(self.lineEdit_udp.sizePolicy().hasHeightForWidth())
        self.lineEdit_udp.setSizePolicy(sizePolicy6)
        self.lineEdit_udp.setMinimumSize(QSize(100, 0))
        self.lineEdit_udp.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_12.addWidget(self.lineEdit_udp)

        self.label_tcp = QLabel(self.groupBox_mac_result)
        self.label_tcp.setObjectName(u"label_tcp")
        sizePolicy10.setHeightForWidth(self.label_tcp.sizePolicy().hasHeightForWidth())
        self.label_tcp.setSizePolicy(sizePolicy10)
        self.label_tcp.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_tcp)

        self.lineEdit_tcp = QLineEdit(self.groupBox_mac_result)
        self.lineEdit_tcp.setObjectName(u"lineEdit_tcp")
        self.lineEdit_tcp.setMinimumSize(QSize(100, 0))
        self.lineEdit_tcp.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_12.addWidget(self.lineEdit_tcp)


        self.gridLayout_5.addWidget(self.groupBox_mac_result, 1, 0, 1, 1)

        self.groupBox_mac_param = QGroupBox(self.tab_mac)
        self.groupBox_mac_param.setObjectName(u"groupBox_mac_param")
        sizePolicy11 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.groupBox_mac_param.sizePolicy().hasHeightForWidth())
        self.groupBox_mac_param.setSizePolicy(sizePolicy11)
        self.groupBox_mac_param.setMaximumSize(QSize(16777215, 250))
        self.frame_right = QGridLayout(self.groupBox_mac_param)
        self.frame_right.setObjectName(u"frame_right")
        self.groupBox_rts = QGroupBox(self.groupBox_mac_param)
        self.groupBox_rts.setObjectName(u"groupBox_rts")
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox_rts)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_rts = QLabel(self.groupBox_rts)
        self.label_rts.setObjectName(u"label_rts")

        self.horizontalLayout_8.addWidget(self.label_rts)

        self.pushButton_rts = QPushButton(self.groupBox_rts)
        self.pushButton_rts.setObjectName(u"pushButton_rts")
        self.pushButton_rts.setCheckable(True)

        self.horizontalLayout_8.addWidget(self.pushButton_rts)


        self.frame_right.addWidget(self.groupBox_rts, 0, 1, 1, 1)

        self.groupBox_enc_protocol = QGroupBox(self.groupBox_mac_param)
        self.groupBox_enc_protocol.setObjectName(u"groupBox_enc_protocol")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_enc_protocol)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.comboBox_enc_protocol = QComboBox(self.groupBox_enc_protocol)
        self.comboBox_enc_protocol.addItem("")
        self.comboBox_enc_protocol.addItem("")
        self.comboBox_enc_protocol.addItem("")
        self.comboBox_enc_protocol.addItem("")
        self.comboBox_enc_protocol.setObjectName(u"comboBox_enc_protocol")

        self.horizontalLayout_7.addWidget(self.comboBox_enc_protocol)


        self.frame_right.addWidget(self.groupBox_enc_protocol, 0, 2, 1, 1)

        self.groupBox_qos = QGroupBox(self.groupBox_mac_param)
        self.groupBox_qos.setObjectName(u"groupBox_qos")
        sizePolicy12 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.groupBox_qos.sizePolicy().hasHeightForWidth())
        self.groupBox_qos.setSizePolicy(sizePolicy12)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_qos)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.comboBox_qos = QComboBox(self.groupBox_qos)
        self.comboBox_qos.addItem("")
        self.comboBox_qos.addItem("")
        self.comboBox_qos.addItem("")
        self.comboBox_qos.addItem("")
        self.comboBox_qos.addItem("")
        self.comboBox_qos.setObjectName(u"comboBox_qos")

        self.verticalLayout_5.addWidget(self.comboBox_qos)


        self.frame_right.addWidget(self.groupBox_qos, 0, 0, 1, 1)

        self.groupBox_tcp_eff = QGroupBox(self.groupBox_mac_param)
        self.groupBox_tcp_eff.setObjectName(u"groupBox_tcp_eff")
        self.verticalLayout = QVBoxLayout(self.groupBox_tcp_eff)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit_tcp_eff = QLineEdit(self.groupBox_tcp_eff)
        self.lineEdit_tcp_eff.setObjectName(u"lineEdit_tcp_eff")
        self.lineEdit_tcp_eff.setMaximumSize(QSize(40, 16777215))

        self.verticalLayout.addWidget(self.lineEdit_tcp_eff, 0, Qt.AlignHCenter)


        self.frame_right.addWidget(self.groupBox_tcp_eff, 0, 3, 1, 1)

        self.groupBox_msdu = QGroupBox(self.groupBox_mac_param)
        self.groupBox_msdu.setObjectName(u"groupBox_msdu")
        self.gridLayout_2 = QGridLayout(self.groupBox_msdu)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.GroupBox_MSDU_value = QGroupBox(self.groupBox_msdu)
        self.GroupBox_MSDU_value.setObjectName(u"GroupBox_MSDU_value")
        self.Layout_msdu = QHBoxLayout(self.GroupBox_MSDU_value)
        self.Layout_msdu.setObjectName(u"Layout_msdu")
        self.Layout_msdu.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_msdu = QLabel(self.GroupBox_MSDU_value)
        self.label_msdu.setObjectName(u"label_msdu")
        sizePolicy5.setHeightForWidth(self.label_msdu.sizePolicy().hasHeightForWidth())
        self.label_msdu.setSizePolicy(sizePolicy5)

        self.Layout_msdu.addWidget(self.label_msdu)

        self.lineEdit_msdu = QLineEdit(self.GroupBox_MSDU_value)
        self.lineEdit_msdu.setObjectName(u"lineEdit_msdu")
        self.lineEdit_msdu.setMinimumSize(QSize(40, 0))

        self.Layout_msdu.addWidget(self.lineEdit_msdu)


        self.gridLayout_2.addWidget(self.GroupBox_MSDU_value, 1, 0, 1, 1)

        self.GroupBox_msdu_nb = QGroupBox(self.groupBox_msdu)
        self.GroupBox_msdu_nb.setObjectName(u"GroupBox_msdu_nb")
        self.horizontalLayout_4 = QHBoxLayout(self.GroupBox_msdu_nb)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_msdu_nb = QLabel(self.GroupBox_msdu_nb)
        self.label_msdu_nb.setObjectName(u"label_msdu_nb")

        self.horizontalLayout_4.addWidget(self.label_msdu_nb)

        self.lineEdit_msdu_nb = QLineEdit(self.GroupBox_msdu_nb)
        self.lineEdit_msdu_nb.setObjectName(u"lineEdit_msdu_nb")
        self.lineEdit_msdu_nb.setMinimumSize(QSize(30, 0))

        self.horizontalLayout_4.addWidget(self.lineEdit_msdu_nb)


        self.gridLayout_2.addWidget(self.GroupBox_msdu_nb, 1, 1, 1, 1)

        self.comboBox_msdu = QComboBox(self.groupBox_msdu)
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.setObjectName(u"comboBox_msdu")

        self.gridLayout_2.addWidget(self.comboBox_msdu, 0, 0, 1, 2)

        self.GroupBox_msdu_limit = QGroupBox(self.groupBox_msdu)
        self.GroupBox_msdu_limit.setObjectName(u"GroupBox_msdu_limit")
        self.horizontalLayout_5 = QHBoxLayout(self.GroupBox_msdu_limit)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_msdu_limit = QLabel(self.GroupBox_msdu_limit)
        self.label_msdu_limit.setObjectName(u"label_msdu_limit")

        self.horizontalLayout_5.addWidget(self.label_msdu_limit)

        self.comboBox_msdu_limit = QComboBox(self.GroupBox_msdu_limit)
        self.comboBox_msdu_limit.addItem("")
        self.comboBox_msdu_limit.addItem("")
        self.comboBox_msdu_limit.setObjectName(u"comboBox_msdu_limit")

        self.horizontalLayout_5.addWidget(self.comboBox_msdu_limit)


        self.gridLayout_2.addWidget(self.GroupBox_msdu_limit, 3, 0, 1, 2)


        self.frame_right.addWidget(self.groupBox_msdu, 0, 5, 1, 1)

        self.groupBox_package_size = QGroupBox(self.groupBox_mac_param)
        self.groupBox_package_size.setObjectName(u"groupBox_package_size")
        self.horizontalLayout_11 = QHBoxLayout(self.groupBox_package_size)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.comboBox_package_size = QComboBox(self.groupBox_package_size)
        self.comboBox_package_size.addItem("")
        self.comboBox_package_size.addItem("")
        self.comboBox_package_size.setObjectName(u"comboBox_package_size")

        self.horizontalLayout_11.addWidget(self.comboBox_package_size)


        self.frame_right.addWidget(self.groupBox_package_size, 0, 6, 1, 1)

        self.groupBox_mpdu = QGroupBox(self.groupBox_mac_param)
        self.groupBox_mpdu.setObjectName(u"groupBox_mpdu")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_mpdu)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.comboBox_mpdu = QComboBox(self.groupBox_mpdu)
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.addItem("")
        self.comboBox_mpdu.setObjectName(u"comboBox_mpdu")

        self.verticalLayout_7.addWidget(self.comboBox_mpdu)

        self.horizontalGroupBox = QGroupBox(self.groupBox_mpdu)
        self.horizontalGroupBox.setObjectName(u"horizontalGroupBox")
        self.Layout_MPDU = QHBoxLayout(self.horizontalGroupBox)
        self.Layout_MPDU.setObjectName(u"Layout_MPDU")
        self.label_MPDU = QLabel(self.horizontalGroupBox)
        self.label_MPDU.setObjectName(u"label_MPDU")

        self.Layout_MPDU.addWidget(self.label_MPDU)

        self.lineEdit_MPDU = QLineEdit(self.horizontalGroupBox)
        self.lineEdit_MPDU.setObjectName(u"lineEdit_MPDU")
        self.lineEdit_MPDU.setMinimumSize(QSize(30, 0))

        self.Layout_MPDU.addWidget(self.lineEdit_MPDU)


        self.verticalLayout_7.addWidget(self.horizontalGroupBox)


        self.frame_right.addWidget(self.groupBox_mpdu, 0, 4, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_mac_param, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_mac, "")
        self.tab_help = QWidget()
        self.tab_help.setObjectName(u"tab_help")
        self.tabWidget.addTab(self.tab_help, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.frame)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.comboBox_nru.setCurrentIndex(1)
        self.combobox_choice_modulation.setCurrentIndex(7)
        self.comboBox_ctrl_modulation.setCurrentIndex(4)
        self.comboBox_number_spatial_stream.setCurrentIndex(1)
        self.comboBox_ap_number.setCurrentIndex(1)
        self.comboBox_station_number.setCurrentIndex(1)
        self.comboBox_users_number.setCurrentIndex(0)
        self.comboBox_nb_csi.setCurrentIndex(20)
        self.comboBox_nb_of_ss_csi.setCurrentIndex(4)
        self.comboBox_enc_protocol.setCurrentIndex(2)
        self.comboBox_qos.setCurrentIndex(1)
        self.comboBox_msdu.setCurrentIndex(6)
        self.comboBox_msdu_limit.setCurrentIndex(1)
        self.comboBox_mpdu.setCurrentIndex(10)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Wi-Fi Throughtput calculator", None))
        self.calculate_phy_btn.setText(QCoreApplication.translate("MainWindow", u"Calculate the physical throughput", None))
        self.show_phy_le.setPlaceholderText(QCoreApplication.translate("MainWindow", u"d\u00e9bit physique", None))
        self.Header.setTitle("")
        self.standard_selection_label.setText(QCoreApplication.translate("MainWindow", u"Standard selection", None))
        self.comboBox_standard_selection.setItemText(0, QCoreApplication.translate("MainWindow", u"Choose your standard", None))
        self.comboBox_standard_selection.setItemText(1, QCoreApplication.translate("MainWindow", u"802.11a", None))
        self.comboBox_standard_selection.setItemText(2, QCoreApplication.translate("MainWindow", u"802.11b", None))
        self.comboBox_standard_selection.setItemText(3, QCoreApplication.translate("MainWindow", u"802.11g", None))
        self.comboBox_standard_selection.setItemText(4, QCoreApplication.translate("MainWindow", u"802.11n", None))
        self.comboBox_standard_selection.setItemText(5, QCoreApplication.translate("MainWindow", u"802.11ac", None))
        self.comboBox_standard_selection.setItemText(6, QCoreApplication.translate("MainWindow", u"802.11ax", None))

        self.label_frequency_band.setText(QCoreApplication.translate("MainWindow", u"Frequency band", None))
        self.comboBox_frequency_band.setItemText(0, QCoreApplication.translate("MainWindow", u"Choose your frequency band", None))
        self.comboBox_frequency_band.setItemText(1, QCoreApplication.translate("MainWindow", u"2.4 GHz", None))
        self.comboBox_frequency_band.setItemText(2, QCoreApplication.translate("MainWindow", u"5 GHz", None))
        self.comboBox_frequency_band.setItemText(3, QCoreApplication.translate("MainWindow", u"6 GHz", None))

        self.bandwidth_label.setText(QCoreApplication.translate("MainWindow", u"Bandwidth", None))
        self.comboBox_bandwidth.setItemText(0, QCoreApplication.translate("MainWindow", u"Choose your bandwidth", None))
        self.comboBox_bandwidth.setItemText(1, QCoreApplication.translate("MainWindow", u"20 MHz", None))
        self.comboBox_bandwidth.setItemText(2, QCoreApplication.translate("MainWindow", u"40 MHz", None))
        self.comboBox_bandwidth.setItemText(3, QCoreApplication.translate("MainWindow", u"80 MHz", None))
        self.comboBox_bandwidth.setItemText(4, QCoreApplication.translate("MainWindow", u"160 MHz", None))

        self.label_dcm.setText(QCoreApplication.translate("MainWindow", u"DCM (Dual Carrier Modulation)", None))
        self.pushButton_dcm.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_nru.setText(QCoreApplication.translate("MainWindow", u"NRU", None))
        self.comboBox_nru.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_nru.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))

        self.label_mu_mimo.setText(QCoreApplication.translate("MainWindow", u"MU-MIMO", None))
        self.pushButton_mu_mimo.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.ofdma_label.setText(QCoreApplication.translate("MainWindow", u"OFDMA", None))
        self.pushButton_ofdma.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.angle_quantif_label.setText(QCoreApplication.translate("MainWindow", u"Angle quantif", None))
        self.choice_of_modulation_label.setText(QCoreApplication.translate("MainWindow", u"Choice of modulation", None))
        self.combobox_choice_modulation.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.combobox_choice_modulation.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.combobox_choice_modulation.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.combobox_choice_modulation.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))
        self.combobox_choice_modulation.setItemText(4, QCoreApplication.translate("MainWindow", u"4", None))
        self.combobox_choice_modulation.setItemText(5, QCoreApplication.translate("MainWindow", u"5", None))
        self.combobox_choice_modulation.setItemText(6, QCoreApplication.translate("MainWindow", u"6", None))
        self.combobox_choice_modulation.setItemText(7, QCoreApplication.translate("MainWindow", u"7", None))

        self.label_ctrl_modulation.setText(QCoreApplication.translate("MainWindow", u"Control modulation", None))
        self.comboBox_ctrl_modulation.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.comboBox_ctrl_modulation.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_ctrl_modulation.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_ctrl_modulation.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_ctrl_modulation.setItemText(4, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_ctrl_modulation.setItemText(5, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_ctrl_modulation.setItemText(6, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_ctrl_modulation.setItemText(7, QCoreApplication.translate("MainWindow", u"7", None))

        self.label_greenfield.setText(QCoreApplication.translate("MainWindow", u"Greenfield", None))
        self.pushButton_greenfield.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_control_preamble.setText(QCoreApplication.translate("MainWindow", u"Control preamble", None))
        self.pushButton_control_preamble.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_txop.setText(QCoreApplication.translate("MainWindow", u"txop", None))
        self.pushButton_txop.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_sgi_ul.setText(QCoreApplication.translate("MainWindow", u"SGI in UL :", None))
        self.comboBox_sgi_ul.setItemText(0, QCoreApplication.translate("MainWindow", u"0.8", None))
        self.comboBox_sgi_ul.setItemText(1, QCoreApplication.translate("MainWindow", u"1.6", None))
        self.comboBox_sgi_ul.setItemText(2, QCoreApplication.translate("MainWindow", u"3.2", None))

        self.label_sgi_dl.setText(QCoreApplication.translate("MainWindow", u"SGI in DL :", None))
        self.comboBox_sgi_dl.setItemText(0, QCoreApplication.translate("MainWindow", u"0.8", None))
        self.comboBox_sgi_dl.setItemText(1, QCoreApplication.translate("MainWindow", u"1.6", None))
        self.comboBox_sgi_dl.setItemText(2, QCoreApplication.translate("MainWindow", u"3.2", None))

        self.label_ldpc.setText(QCoreApplication.translate("MainWindow", u"LDPC (Low Density Parity Check)", None))
        self.pushButton_ldpc.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_nb_ss.setText(QCoreApplication.translate("MainWindow", u"Number of spatial stream", None))
        self.comboBox_number_spatial_stream.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_number_spatial_stream.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_number_spatial_stream.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_number_spatial_stream.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))

        self.label_stbc.setText(QCoreApplication.translate("MainWindow", u"STBC (Space Time Bloc Code)", None))
        self.pushButton_stbc.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_sgi.setText(QCoreApplication.translate("MainWindow", u"SGI (short guard interval)", None))
        self.pushButton_sgi.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.groupbox_antennas.setTitle("")
        self.label_title_antennas.setText(QCoreApplication.translate("MainWindow", u"Antennas", None))
        self.label_antennas_ap_number.setText(QCoreApplication.translate("MainWindow", u"AP number", None))
        self.comboBox_ap_number.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_ap_number.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_ap_number.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_ap_number.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_ap_number.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_ap_number.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_ap_number.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.comboBox_ap_number.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))

        self.label_antennas_station_number.setText(QCoreApplication.translate("MainWindow", u"Station number", None))
        self.comboBox_station_number.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_station_number.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_station_number.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_station_number.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_station_number.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_station_number.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_station_number.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.comboBox_station_number.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))

        self.label_antennas_users_number.setText(QCoreApplication.translate("MainWindow", u"Users number", None))
        self.comboBox_users_number.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_users_number.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_users_number.setItemText(2, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_users_number.setItemText(3, QCoreApplication.translate("MainWindow", u"8", None))
        self.comboBox_users_number.setItemText(4, QCoreApplication.translate("MainWindow", u"16", None))
        self.comboBox_users_number.setItemText(5, QCoreApplication.translate("MainWindow", u"32", None))
        self.comboBox_users_number.setItemText(6, QCoreApplication.translate("MainWindow", u"64", None))

        self.label_mu.setText(QCoreApplication.translate("MainWindow", u"mu %", None))
        self.lineEdit_affichage_mu.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_su.setText(QCoreApplication.translate("MainWindow", u"su %", None))
        self.lineEdit_affichage_su.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_csi_title.setText(QCoreApplication.translate("MainWindow", u"CSI (Channel State Information)", None))
        self.pushButton_csi.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_number_of_csi.setText(QCoreApplication.translate("MainWindow", u"Number of CSI", None))
        self.comboBox_nb_csi.setItemText(0, QCoreApplication.translate("MainWindow", u"0", None))
        self.comboBox_nb_csi.setItemText(1, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_nb_csi.setItemText(2, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_nb_csi.setItemText(3, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_nb_csi.setItemText(4, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_nb_csi.setItemText(5, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_nb_csi.setItemText(6, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_nb_csi.setItemText(7, QCoreApplication.translate("MainWindow", u"7", None))
        self.comboBox_nb_csi.setItemText(8, QCoreApplication.translate("MainWindow", u"8", None))
        self.comboBox_nb_csi.setItemText(9, QCoreApplication.translate("MainWindow", u"9", None))
        self.comboBox_nb_csi.setItemText(10, QCoreApplication.translate("MainWindow", u"10", None))
        self.comboBox_nb_csi.setItemText(11, QCoreApplication.translate("MainWindow", u"11", None))
        self.comboBox_nb_csi.setItemText(12, QCoreApplication.translate("MainWindow", u"12", None))
        self.comboBox_nb_csi.setItemText(13, QCoreApplication.translate("MainWindow", u"13", None))
        self.comboBox_nb_csi.setItemText(14, QCoreApplication.translate("MainWindow", u"14", None))
        self.comboBox_nb_csi.setItemText(15, QCoreApplication.translate("MainWindow", u"15", None))
        self.comboBox_nb_csi.setItemText(16, QCoreApplication.translate("MainWindow", u"16", None))
        self.comboBox_nb_csi.setItemText(17, QCoreApplication.translate("MainWindow", u"17", None))
        self.comboBox_nb_csi.setItemText(18, QCoreApplication.translate("MainWindow", u"18", None))
        self.comboBox_nb_csi.setItemText(19, QCoreApplication.translate("MainWindow", u"19", None))
        self.comboBox_nb_csi.setItemText(20, QCoreApplication.translate("MainWindow", u"20", None))

        self.label_number_of_ss_for_csi.setText(QCoreApplication.translate("MainWindow", u"Number of ss for CSI", None))
        self.comboBox_nb_of_ss_csi.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_nb_of_ss_csi.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_nb_of_ss_csi.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_nb_of_ss_csi.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_nb_of_ss_csi.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_nb_of_ss_csi.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_nb_of_ss_csi.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.comboBox_nb_of_ss_csi.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))

        self.label_antennas_for_csi.setText(QCoreApplication.translate("MainWindow", u"Antennas for CSI", None))
        self.comboBox_antennas_csi.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_antennas_csi.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_antennas_csi.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_antennas_csi.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_antennas_csi.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_antennas_csi.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_antennas_csi.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.comboBox_antennas_csi.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_phy), QCoreApplication.translate("MainWindow", u"Physical layer", None))
        self.groupBox_mac_result.setTitle(QCoreApplication.translate("MainWindow", u"Results", None))
        self.label_mac.setText(QCoreApplication.translate("MainWindow", u"MAC throughput", None))
        self.label_udp.setText(QCoreApplication.translate("MainWindow", u"UDP throughput", None))
        self.label_tcp.setText(QCoreApplication.translate("MainWindow", u"TCP throughput", None))
        self.groupBox_rts.setTitle(QCoreApplication.translate("MainWindow", u"Request to send (RTS)", None))
        self.label_rts.setText(QCoreApplication.translate("MainWindow", u"RTS", None))
        self.pushButton_rts.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.groupBox_enc_protocol.setTitle(QCoreApplication.translate("MainWindow", u"Encryption protocols", None))
        self.comboBox_enc_protocol.setItemText(0, QCoreApplication.translate("MainWindow", u"none", None))
        self.comboBox_enc_protocol.setItemText(1, QCoreApplication.translate("MainWindow", u"WEP", None))
        self.comboBox_enc_protocol.setItemText(2, QCoreApplication.translate("MainWindow", u"WPA", None))
        self.comboBox_enc_protocol.setItemText(3, QCoreApplication.translate("MainWindow", u"WPA2", None))

        self.groupBox_qos.setTitle(QCoreApplication.translate("MainWindow", u"Quality of service (QoS)", None))
        self.comboBox_qos.setItemText(0, QCoreApplication.translate("MainWindow", u"Legacy", None))
        self.comboBox_qos.setItemText(1, QCoreApplication.translate("MainWindow", u"BK (Background)", None))
        self.comboBox_qos.setItemText(2, QCoreApplication.translate("MainWindow", u"BE (Best Effort)", None))
        self.comboBox_qos.setItemText(3, QCoreApplication.translate("MainWindow", u"VI (Video)", None))
        self.comboBox_qos.setItemText(4, QCoreApplication.translate("MainWindow", u"VO (Voice)", None))

        self.groupBox_tcp_eff.setTitle(QCoreApplication.translate("MainWindow", u"TCP efficiency", None))
        self.lineEdit_tcp_eff.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.groupBox_msdu.setTitle(QCoreApplication.translate("MainWindow", u"Agg MSDU", None))
        self.label_msdu.setText(QCoreApplication.translate("MainWindow", u"MSDU", None))
        self.lineEdit_msdu.setText(QCoreApplication.translate("MainWindow", u"1500", None))
        self.label_msdu_nb.setText(QCoreApplication.translate("MainWindow", u"MSDU nb", None))
        self.lineEdit_msdu_nb.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_msdu.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_msdu.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_msdu.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_msdu.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_msdu.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_msdu.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_msdu.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))

        self.label_msdu_limit.setText(QCoreApplication.translate("MainWindow", u"MSDU limit", None))
        self.comboBox_msdu_limit.setItemText(0, QCoreApplication.translate("MainWindow", u"3889", None))
        self.comboBox_msdu_limit.setItemText(1, QCoreApplication.translate("MainWindow", u"7936", None))

        self.groupBox_package_size.setTitle(QCoreApplication.translate("MainWindow", u"Package size", None))
        self.comboBox_package_size.setItemText(0, QCoreApplication.translate("MainWindow", u"1350", None))
        self.comboBox_package_size.setItemText(1, QCoreApplication.translate("MainWindow", u"1460", None))

        self.groupBox_mpdu.setTitle(QCoreApplication.translate("MainWindow", u"Agg MPDU ", None))
        self.comboBox_mpdu.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_mpdu.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_mpdu.setItemText(2, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_mpdu.setItemText(3, QCoreApplication.translate("MainWindow", u"8", None))
        self.comboBox_mpdu.setItemText(4, QCoreApplication.translate("MainWindow", u"16", None))
        self.comboBox_mpdu.setItemText(5, QCoreApplication.translate("MainWindow", u"32", None))
        self.comboBox_mpdu.setItemText(6, QCoreApplication.translate("MainWindow", u"64", None))
        self.comboBox_mpdu.setItemText(7, QCoreApplication.translate("MainWindow", u"128", None))
        self.comboBox_mpdu.setItemText(8, QCoreApplication.translate("MainWindow", u"256", None))
        self.comboBox_mpdu.setItemText(9, QCoreApplication.translate("MainWindow", u"512", None))
        self.comboBox_mpdu.setItemText(10, QCoreApplication.translate("MainWindow", u"1024", None))

        self.label_MPDU.setText(QCoreApplication.translate("MainWindow", u"MPDU nb", None))
        self.lineEdit_MPDU.setText(QCoreApplication.translate("MainWindow", u"20", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mac), QCoreApplication.translate("MainWindow", u"MAC and Transport layer", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_help), QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

