# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'wifi.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
        MainWindow.resize(1316, 983)
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
        self.frame_left.setFrameShape(QFrame.StyledPanel)
        self.frame_left.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_left)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.separateur_3 = QFrame(self.frame_left)
        self.separateur_3.setObjectName(u"separateur_3")
        self.separateur_3.setFrameShape(QFrame.VLine)
        self.separateur_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.separateur_3, 2, 3, 1, 1)

        self.vertical_deux = QVBoxLayout()
        self.vertical_deux.setObjectName(u"vertical_deux")
        self.other_parameters_802_11_n_2 = QVBoxLayout()
        self.other_parameters_802_11_n_2.setObjectName(u"other_parameters_802_11_n_2")
        self.groupbox_wifi_n_2 = QGroupBox(self.frame_left)
        self.groupbox_wifi_n_2.setObjectName(u"groupbox_wifi_n_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupbox_wifi_n_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.greenfield = QHBoxLayout()
        self.greenfield.setObjectName(u"greenfield")
        self.greenfield.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_greenfield = QLabel(self.groupbox_wifi_n_2)
        self.label_greenfield.setObjectName(u"label_greenfield")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_greenfield.sizePolicy().hasHeightForWidth())
        self.label_greenfield.setSizePolicy(sizePolicy)

        self.greenfield.addWidget(self.label_greenfield)

        self.pushButton_greenfield = QPushButton(self.groupbox_wifi_n_2)
        self.pushButton_greenfield.setObjectName(u"pushButton_greenfield")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pushButton_greenfield.sizePolicy().hasHeightForWidth())
        self.pushButton_greenfield.setSizePolicy(sizePolicy1)
        self.pushButton_greenfield.setCheckable(True)

        self.greenfield.addWidget(self.pushButton_greenfield)


        self.verticalLayout_2.addLayout(self.greenfield)

        self.control_preamble = QHBoxLayout()
        self.control_preamble.setObjectName(u"control_preamble")
        self.control_preamble.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_control_preamble = QLabel(self.groupbox_wifi_n_2)
        self.label_control_preamble.setObjectName(u"label_control_preamble")

        self.control_preamble.addWidget(self.label_control_preamble)

        self.pushButton_control_preamble = QPushButton(self.groupbox_wifi_n_2)
        self.pushButton_control_preamble.setObjectName(u"pushButton_control_preamble")
        sizePolicy1.setHeightForWidth(self.pushButton_control_preamble.sizePolicy().hasHeightForWidth())
        self.pushButton_control_preamble.setSizePolicy(sizePolicy1)
        self.pushButton_control_preamble.setCheckable(True)

        self.control_preamble.addWidget(self.pushButton_control_preamble)


        self.verticalLayout_2.addLayout(self.control_preamble)

        self.txop = QHBoxLayout()
        self.txop.setObjectName(u"txop")
        self.txop.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_txop = QLabel(self.groupbox_wifi_n_2)
        self.label_txop.setObjectName(u"label_txop")

        self.txop.addWidget(self.label_txop)

        self.pushButton_txop = QPushButton(self.groupbox_wifi_n_2)
        self.pushButton_txop.setObjectName(u"pushButton_txop")
        sizePolicy1.setHeightForWidth(self.pushButton_txop.sizePolicy().hasHeightForWidth())
        self.pushButton_txop.setSizePolicy(sizePolicy1)
        self.pushButton_txop.setCheckable(True)

        self.txop.addWidget(self.pushButton_txop)


        self.verticalLayout_2.addLayout(self.txop)


        self.other_parameters_802_11_n_2.addWidget(self.groupbox_wifi_n_2)

        self.groupbox_mu_su = QGroupBox(self.frame_left)
        self.groupbox_mu_su.setObjectName(u"groupbox_mu_su")
        self.grid_su = QGridLayout(self.groupbox_mu_su)
        self.grid_su.setObjectName(u"grid_su")
        self.su_2 = QHBoxLayout()
        self.su_2.setObjectName(u"su_2")
        self.label_mu = QLabel(self.groupbox_mu_su)
        self.label_mu.setObjectName(u"label_mu")
        sizePolicy1.setHeightForWidth(self.label_mu.sizePolicy().hasHeightForWidth())
        self.label_mu.setSizePolicy(sizePolicy1)

        self.su_2.addWidget(self.label_mu)

        self.mu_slider = QDial(self.groupbox_mu_su)
        self.mu_slider.setObjectName(u"mu_slider")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.mu_slider.sizePolicy().hasHeightForWidth())
        self.mu_slider.setSizePolicy(sizePolicy2)

        self.su_2.addWidget(self.mu_slider)


        self.grid_su.addLayout(self.su_2, 0, 0, 1, 1)

        self.su = QHBoxLayout()
        self.su.setObjectName(u"su")
        self.label_su = QLabel(self.groupbox_mu_su)
        self.label_su.setObjectName(u"label_su")
        sizePolicy1.setHeightForWidth(self.label_su.sizePolicy().hasHeightForWidth())
        self.label_su.setSizePolicy(sizePolicy1)

        self.su.addWidget(self.label_su)

        self.su_slider = QDial(self.groupbox_mu_su)
        self.su_slider.setObjectName(u"su_slider")
        sizePolicy2.setHeightForWidth(self.su_slider.sizePolicy().hasHeightForWidth())
        self.su_slider.setSizePolicy(sizePolicy2)

        self.su.addWidget(self.su_slider)


        self.grid_su.addLayout(self.su, 0, 1, 1, 1)


        self.other_parameters_802_11_n_2.addWidget(self.groupbox_mu_su)

        self.groupbox_csi = QGroupBox(self.frame_left)
        self.groupbox_csi.setObjectName(u"groupbox_csi")
        self.CSI = QVBoxLayout(self.groupbox_csi)
        self.CSI.setObjectName(u"CSI")
        self.csi = QHBoxLayout()
        self.csi.setObjectName(u"csi")
        self.label_csi_title = QLabel(self.groupbox_csi)
        self.label_csi_title.setObjectName(u"label_csi_title")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_csi_title.sizePolicy().hasHeightForWidth())
        self.label_csi_title.setSizePolicy(sizePolicy3)
        self.label_csi_title.setAlignment(Qt.AlignCenter)

        self.csi.addWidget(self.label_csi_title)


        self.CSI.addLayout(self.csi)

        self.pushButton_csi = QPushButton(self.groupbox_csi)
        self.pushButton_csi.setObjectName(u"pushButton_csi")
        self.pushButton_csi.setCheckable(True)

        self.CSI.addWidget(self.pushButton_csi)

        self.number_of_csi = QHBoxLayout()
        self.number_of_csi.setObjectName(u"number_of_csi")
        self.label_number_of_csi = QLabel(self.groupbox_csi)
        self.label_number_of_csi.setObjectName(u"label_number_of_csi")

        self.number_of_csi.addWidget(self.label_number_of_csi)

        self.comboBox_nb_csi = QComboBox(self.groupbox_csi)
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
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comboBox_nb_csi.sizePolicy().hasHeightForWidth())
        self.comboBox_nb_csi.setSizePolicy(sizePolicy4)

        self.number_of_csi.addWidget(self.comboBox_nb_csi)


        self.CSI.addLayout(self.number_of_csi)

        self.number_of_ss_for_CSI = QHBoxLayout()
        self.number_of_ss_for_CSI.setObjectName(u"number_of_ss_for_CSI")
        self.label_number_of_ss_for_csi = QLabel(self.groupbox_csi)
        self.label_number_of_ss_for_csi.setObjectName(u"label_number_of_ss_for_csi")

        self.number_of_ss_for_CSI.addWidget(self.label_number_of_ss_for_csi)

        self.comboBox_nb_of_ss_csi = QComboBox(self.groupbox_csi)
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.addItem("")
        self.comboBox_nb_of_ss_csi.setObjectName(u"comboBox_nb_of_ss_csi")
        sizePolicy4.setHeightForWidth(self.comboBox_nb_of_ss_csi.sizePolicy().hasHeightForWidth())
        self.comboBox_nb_of_ss_csi.setSizePolicy(sizePolicy4)

        self.number_of_ss_for_CSI.addWidget(self.comboBox_nb_of_ss_csi)


        self.CSI.addLayout(self.number_of_ss_for_CSI)

        self.antennas_for_csi = QHBoxLayout()
        self.antennas_for_csi.setObjectName(u"antennas_for_csi")
        self.label_antennas_for_csi = QLabel(self.groupbox_csi)
        self.label_antennas_for_csi.setObjectName(u"label_antennas_for_csi")

        self.antennas_for_csi.addWidget(self.label_antennas_for_csi)

        self.comboBox_antennas_csi = QComboBox(self.groupbox_csi)
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.addItem("")
        self.comboBox_antennas_csi.setObjectName(u"comboBox_antennas_csi")

        self.antennas_for_csi.addWidget(self.comboBox_antennas_csi)


        self.CSI.addLayout(self.antennas_for_csi)


        self.other_parameters_802_11_n_2.addWidget(self.groupbox_csi)


        self.vertical_deux.addLayout(self.other_parameters_802_11_n_2)


        self.gridLayout_4.addLayout(self.vertical_deux, 2, 2, 1, 1)

        self.vertical_trois = QVBoxLayout()
        self.vertical_trois.setObjectName(u"vertical_trois")
        self.groupbox_dcm = QGroupBox(self.frame_left)
        self.groupbox_dcm.setObjectName(u"groupbox_dcm")
        self.DCM = QHBoxLayout(self.groupbox_dcm)
        self.DCM.setObjectName(u"DCM")
        self.label_dcm = QLabel(self.groupbox_dcm)
        self.label_dcm.setObjectName(u"label_dcm")

        self.DCM.addWidget(self.label_dcm)

        self.pushButton_dcm = QPushButton(self.groupbox_dcm)
        self.pushButton_dcm.setObjectName(u"pushButton_dcm")
        sizePolicy5 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.pushButton_dcm.sizePolicy().hasHeightForWidth())
        self.pushButton_dcm.setSizePolicy(sizePolicy5)
        self.pushButton_dcm.setCheckable(True)
        self.pushButton_dcm.setFlat(False)

        self.DCM.addWidget(self.pushButton_dcm)


        self.vertical_trois.addWidget(self.groupbox_dcm)

        self.groupbox_nru = QGroupBox(self.frame_left)
        self.groupbox_nru.setObjectName(u"groupbox_nru")
        self.NRU = QHBoxLayout(self.groupbox_nru)
        self.NRU.setObjectName(u"NRU")
        self.label_nru = QLabel(self.groupbox_nru)
        self.label_nru.setObjectName(u"label_nru")

        self.NRU.addWidget(self.label_nru)

        self.comboBox_nru = QComboBox(self.groupbox_nru)
        self.comboBox_nru.addItem("")
        self.comboBox_nru.addItem("")
        self.comboBox_nru.setObjectName(u"comboBox_nru")

        self.NRU.addWidget(self.comboBox_nru)


        self.vertical_trois.addWidget(self.groupbox_nru)

        self.groupbox_mu_mimo = QGroupBox(self.frame_left)
        self.groupbox_mu_mimo.setObjectName(u"groupbox_mu_mimo")
        self.MU_MIMO = QHBoxLayout(self.groupbox_mu_mimo)
        self.MU_MIMO.setObjectName(u"MU_MIMO")
        self.label_mu_mimo = QLabel(self.groupbox_mu_mimo)
        self.label_mu_mimo.setObjectName(u"label_mu_mimo")

        self.MU_MIMO.addWidget(self.label_mu_mimo)

        self.pushButton_mu_mimo = QPushButton(self.groupbox_mu_mimo)
        self.pushButton_mu_mimo.setObjectName(u"pushButton_mu_mimo")
        sizePolicy5.setHeightForWidth(self.pushButton_mu_mimo.sizePolicy().hasHeightForWidth())
        self.pushButton_mu_mimo.setSizePolicy(sizePolicy5)
        self.pushButton_mu_mimo.setCheckable(True)
        self.pushButton_mu_mimo.setFlat(False)

        self.MU_MIMO.addWidget(self.pushButton_mu_mimo)


        self.vertical_trois.addWidget(self.groupbox_mu_mimo)

        self.groupbox_ofdma = QGroupBox(self.frame_left)
        self.groupbox_ofdma.setObjectName(u"groupbox_ofdma")
        self.OFDMA = QHBoxLayout(self.groupbox_ofdma)
        self.OFDMA.setObjectName(u"OFDMA")
        self.ofdma_label = QLabel(self.groupbox_ofdma)
        self.ofdma_label.setObjectName(u"ofdma_label")

        self.OFDMA.addWidget(self.ofdma_label)

        self.pushButton_ofdma = QPushButton(self.groupbox_ofdma)
        self.pushButton_ofdma.setObjectName(u"pushButton_ofdma")
        sizePolicy5.setHeightForWidth(self.pushButton_ofdma.sizePolicy().hasHeightForWidth())
        self.pushButton_ofdma.setSizePolicy(sizePolicy5)
        self.pushButton_ofdma.setCheckable(True)
        self.pushButton_ofdma.setFlat(False)

        self.OFDMA.addWidget(self.pushButton_ofdma)


        self.vertical_trois.addWidget(self.groupbox_ofdma)

        self.groupbox_angle_quantif = QGroupBox(self.frame_left)
        self.groupbox_angle_quantif.setObjectName(u"groupbox_angle_quantif")
        self.horizontalLayout_2 = QHBoxLayout(self.groupbox_angle_quantif)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.angle_quantif_label = QLabel(self.groupbox_angle_quantif)
        self.angle_quantif_label.setObjectName(u"angle_quantif_label")

        self.horizontalLayout_2.addWidget(self.angle_quantif_label)

        self.spinBox_angle_quantif = QSpinBox(self.groupbox_angle_quantif)
        self.spinBox_angle_quantif.setObjectName(u"spinBox_angle_quantif")
        sizePolicy6 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.spinBox_angle_quantif.sizePolicy().hasHeightForWidth())
        self.spinBox_angle_quantif.setSizePolicy(sizePolicy6)
        self.spinBox_angle_quantif.setMinimum(1)
        self.spinBox_angle_quantif.setMaximum(360)

        self.horizontalLayout_2.addWidget(self.spinBox_angle_quantif)


        self.vertical_trois.addWidget(self.groupbox_angle_quantif)


        self.gridLayout_4.addLayout(self.vertical_trois, 2, 4, 1, 1)

        self.vertical_un = QVBoxLayout()
        self.vertical_un.setObjectName(u"vertical_un")
        self.groupbox_modulation = QGroupBox(self.frame_left)
        self.groupbox_modulation.setObjectName(u"groupbox_modulation")
        self.choice_modulation_2 = QHBoxLayout(self.groupbox_modulation)
        self.choice_modulation_2.setObjectName(u"choice_modulation_2")
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

        self.choice_modulation_2.addWidget(self.combobox_choice_modulation)


        self.vertical_un.addWidget(self.groupbox_modulation)

        self.groupBox_sgi_btn = QGroupBox(self.frame_left)
        self.groupBox_sgi_btn.setObjectName(u"groupBox_sgi_btn")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_sgi_btn)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_sgi = QLabel(self.groupBox_sgi_btn)
        self.label_sgi.setObjectName(u"label_sgi")
        sizePolicy.setHeightForWidth(self.label_sgi.sizePolicy().hasHeightForWidth())
        self.label_sgi.setSizePolicy(sizePolicy)
        self.label_sgi.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_sgi)

        self.pushButton_sgi = QPushButton(self.groupBox_sgi_btn)
        self.pushButton_sgi.setObjectName(u"pushButton_sgi")
        self.pushButton_sgi.setCheckable(True)
        self.pushButton_sgi.setChecked(False)

        self.verticalLayout_4.addWidget(self.pushButton_sgi)


        self.vertical_un.addWidget(self.groupBox_sgi_btn)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.vertical_un.addItem(self.verticalSpacer_2)

        self.groupbox_sgi_dl_ul = QGroupBox(self.frame_left)
        self.groupbox_sgi_dl_ul.setObjectName(u"groupbox_sgi_dl_ul")
        self.SGI_2 = QGridLayout(self.groupbox_sgi_dl_ul)
        self.SGI_2.setObjectName(u"SGI_2")
        self.SGI_UL_2 = QHBoxLayout()
        self.SGI_UL_2.setObjectName(u"SGI_UL_2")
        self.label_18 = QLabel(self.groupbox_sgi_dl_ul)
        self.label_18.setObjectName(u"label_18")

        self.SGI_UL_2.addWidget(self.label_18)

        self.comboBox_sgi_ul = QComboBox(self.groupbox_sgi_dl_ul)
        self.comboBox_sgi_ul.addItem("")
        self.comboBox_sgi_ul.addItem("")
        self.comboBox_sgi_ul.addItem("")
        self.comboBox_sgi_ul.setObjectName(u"comboBox_sgi_ul")

        self.SGI_UL_2.addWidget(self.comboBox_sgi_ul)


        self.SGI_2.addLayout(self.SGI_UL_2, 3, 0, 1, 1)

        self.SGI_DL_2 = QHBoxLayout()
        self.SGI_DL_2.setObjectName(u"SGI_DL_2")
        self.label_16 = QLabel(self.groupbox_sgi_dl_ul)
        self.label_16.setObjectName(u"label_16")

        self.SGI_DL_2.addWidget(self.label_16)

        self.comboBox_sgi_dl = QComboBox(self.groupbox_sgi_dl_ul)
        self.comboBox_sgi_dl.addItem("")
        self.comboBox_sgi_dl.addItem("")
        self.comboBox_sgi_dl.addItem("")
        self.comboBox_sgi_dl.setObjectName(u"comboBox_sgi_dl")

        self.SGI_DL_2.addWidget(self.comboBox_sgi_dl)


        self.SGI_2.addLayout(self.SGI_DL_2, 2, 0, 1, 1)


        self.vertical_un.addWidget(self.groupbox_sgi_dl_ul)

        self.groupbox_wifi_n = QGroupBox(self.frame_left)
        self.groupbox_wifi_n.setObjectName(u"groupbox_wifi_n")
        self.gridLayout_3 = QGridLayout(self.groupbox_wifi_n)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.STBC = QHBoxLayout()
        self.STBC.setObjectName(u"STBC")
        self.label_stbc = QLabel(self.groupbox_wifi_n)
        self.label_stbc.setObjectName(u"label_stbc")

        self.STBC.addWidget(self.label_stbc)

        self.pushButton_stbc = QPushButton(self.groupbox_wifi_n)
        self.pushButton_stbc.setObjectName(u"pushButton_stbc")
        sizePolicy5.setHeightForWidth(self.pushButton_stbc.sizePolicy().hasHeightForWidth())
        self.pushButton_stbc.setSizePolicy(sizePolicy5)
        self.pushButton_stbc.setCheckable(True)

        self.STBC.addWidget(self.pushButton_stbc)


        self.gridLayout_3.addLayout(self.STBC, 1, 0, 1, 1)

        self.LDPC = QHBoxLayout()
        self.LDPC.setObjectName(u"LDPC")
        self.label_ldpc = QLabel(self.groupbox_wifi_n)
        self.label_ldpc.setObjectName(u"label_ldpc")

        self.LDPC.addWidget(self.label_ldpc)

        self.pushButton_ldpc = QPushButton(self.groupbox_wifi_n)
        self.pushButton_ldpc.setObjectName(u"pushButton_ldpc")
        sizePolicy5.setHeightForWidth(self.pushButton_ldpc.sizePolicy().hasHeightForWidth())
        self.pushButton_ldpc.setSizePolicy(sizePolicy5)
        self.pushButton_ldpc.setCheckable(True)

        self.LDPC.addWidget(self.pushButton_ldpc)


        self.gridLayout_3.addLayout(self.LDPC, 0, 0, 1, 1)

        self.number_spacial_stream = QHBoxLayout()
        self.number_spacial_stream.setObjectName(u"number_spacial_stream")
        self.label_nb_ss = QLabel(self.groupbox_wifi_n)
        self.label_nb_ss.setObjectName(u"label_nb_ss")

        self.number_spacial_stream.addWidget(self.label_nb_ss)

        self.comboBox_number_spatial_stream = QComboBox(self.groupbox_wifi_n)
        self.comboBox_number_spatial_stream.addItem("")
        self.comboBox_number_spatial_stream.addItem("")
        self.comboBox_number_spatial_stream.addItem("")
        self.comboBox_number_spatial_stream.addItem("")
        self.comboBox_number_spatial_stream.setObjectName(u"comboBox_number_spatial_stream")
        sizePolicy5.setHeightForWidth(self.comboBox_number_spatial_stream.sizePolicy().hasHeightForWidth())
        self.comboBox_number_spatial_stream.setSizePolicy(sizePolicy5)

        self.number_spacial_stream.addWidget(self.comboBox_number_spatial_stream)


        self.gridLayout_3.addLayout(self.number_spacial_stream, 2, 0, 1, 1)


        self.vertical_un.addWidget(self.groupbox_wifi_n)

        self.groupbox_antennas = QGroupBox(self.frame_left)
        self.groupbox_antennas.setObjectName(u"groupbox_antennas")
        self.verticalLayout_3 = QVBoxLayout(self.groupbox_antennas)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.antennas = QGridLayout()
        self.antennas.setObjectName(u"antennas")
        self.ap_number_2 = QHBoxLayout()
        self.ap_number_2.setObjectName(u"ap_number_2")
        self.label_antennas_ap_number = QLabel(self.groupbox_antennas)
        self.label_antennas_ap_number.setObjectName(u"label_antennas_ap_number")

        self.ap_number_2.addWidget(self.label_antennas_ap_number)

        self.comboBox_ap_number = QComboBox(self.groupbox_antennas)
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.addItem("")
        self.comboBox_ap_number.setObjectName(u"comboBox_ap_number")

        self.ap_number_2.addWidget(self.comboBox_ap_number)


        self.antennas.addLayout(self.ap_number_2, 1, 0, 1, 1)

        self.label_title_antennas = QLabel(self.groupbox_antennas)
        self.label_title_antennas.setObjectName(u"label_title_antennas")
        sizePolicy.setHeightForWidth(self.label_title_antennas.sizePolicy().hasHeightForWidth())
        self.label_title_antennas.setSizePolicy(sizePolicy)
        self.label_title_antennas.setAlignment(Qt.AlignCenter)

        self.antennas.addWidget(self.label_title_antennas, 0, 0, 1, 1)

        self.station_number_2 = QHBoxLayout()
        self.station_number_2.setObjectName(u"station_number_2")
        self.label_antennas_station_number = QLabel(self.groupbox_antennas)
        self.label_antennas_station_number.setObjectName(u"label_antennas_station_number")

        self.station_number_2.addWidget(self.label_antennas_station_number)

        self.comboBox_station_number = QComboBox(self.groupbox_antennas)
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.addItem("")
        self.comboBox_station_number.setObjectName(u"comboBox_station_number")

        self.station_number_2.addWidget(self.comboBox_station_number)


        self.antennas.addLayout(self.station_number_2, 2, 0, 1, 1)

        self.users_number_2 = QHBoxLayout()
        self.users_number_2.setObjectName(u"users_number_2")
        self.label_antennas_users_number = QLabel(self.groupbox_antennas)
        self.label_antennas_users_number.setObjectName(u"label_antennas_users_number")

        self.users_number_2.addWidget(self.label_antennas_users_number)

        self.comboBox_users_number = QComboBox(self.groupbox_antennas)
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.addItem("")
        self.comboBox_users_number.setObjectName(u"comboBox_users_number")

        self.users_number_2.addWidget(self.comboBox_users_number)


        self.antennas.addLayout(self.users_number_2, 3, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.antennas)


        self.vertical_un.addWidget(self.groupbox_antennas)


        self.gridLayout_4.addLayout(self.vertical_un, 2, 0, 1, 1)

        self.separateur_2 = QFrame(self.frame_left)
        self.separateur_2.setObjectName(u"separateur_2")
        self.separateur_2.setFrameShape(QFrame.VLine)
        self.separateur_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_4.addWidget(self.separateur_2, 2, 1, 1, 1)

        self.Header = QGroupBox(self.frame_left)
        self.Header.setObjectName(u"Header")
        sizePolicy7 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.Header.sizePolicy().hasHeightForWidth())
        self.Header.setSizePolicy(sizePolicy7)
        self.Header.setMinimumSize(QSize(1220, 85))
        self.horizontalLayout_6 = QHBoxLayout(self.Header)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 12, -1, -1)
        self.layout_menu_principal = QHBoxLayout()
        self.layout_menu_principal.setObjectName(u"layout_menu_principal")
        self.standard_selection = QHBoxLayout()
        self.standard_selection.setObjectName(u"standard_selection")
        self.standard_selection_label = QLabel(self.Header)
        self.standard_selection_label.setObjectName(u"standard_selection_label")
        self.standard_selection_label.setAlignment(Qt.AlignCenter)

        self.standard_selection.addWidget(self.standard_selection_label)

        self.comboBox_standard_selection = QComboBox(self.Header)
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.addItem("")
        self.comboBox_standard_selection.setObjectName(u"comboBox_standard_selection")
        sizePolicy8 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.comboBox_standard_selection.sizePolicy().hasHeightForWidth())
        self.comboBox_standard_selection.setSizePolicy(sizePolicy8)

        self.standard_selection.addWidget(self.comboBox_standard_selection)


        self.layout_menu_principal.addLayout(self.standard_selection)

        self.frequency_band = QHBoxLayout()
        self.frequency_band.setObjectName(u"frequency_band")
        self.label_frequency_band = QLabel(self.Header)
        self.label_frequency_band.setObjectName(u"label_frequency_band")
        self.label_frequency_band.setAlignment(Qt.AlignCenter)

        self.frequency_band.addWidget(self.label_frequency_band)

        self.comboBox_frequency_band = QComboBox(self.Header)
        self.comboBox_frequency_band.addItem("")
        self.comboBox_frequency_band.addItem("")
        self.comboBox_frequency_band.addItem("")
        self.comboBox_frequency_band.addItem("")
        self.comboBox_frequency_band.setObjectName(u"comboBox_frequency_band")
        sizePolicy8.setHeightForWidth(self.comboBox_frequency_band.sizePolicy().hasHeightForWidth())
        self.comboBox_frequency_band.setSizePolicy(sizePolicy8)

        self.frequency_band.addWidget(self.comboBox_frequency_band)


        self.layout_menu_principal.addLayout(self.frequency_band)

        self.bandwidth = QHBoxLayout()
        self.bandwidth.setObjectName(u"bandwidth")
        self.bandwidth_label = QLabel(self.Header)
        self.bandwidth_label.setObjectName(u"bandwidth_label")
        self.bandwidth_label.setAlignment(Qt.AlignCenter)

        self.bandwidth.addWidget(self.bandwidth_label)

        self.comboBox_bandwidth = QComboBox(self.Header)
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.addItem("")
        self.comboBox_bandwidth.setObjectName(u"comboBox_bandwidth")
        sizePolicy8.setHeightForWidth(self.comboBox_bandwidth.sizePolicy().hasHeightForWidth())
        self.comboBox_bandwidth.setSizePolicy(sizePolicy8)

        self.bandwidth.addWidget(self.comboBox_bandwidth)


        self.layout_menu_principal.addLayout(self.bandwidth)


        self.horizontalLayout_6.addLayout(self.layout_menu_principal)


        self.gridLayout_4.addWidget(self.Header, 1, 0, 1, 5)


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
        sizePolicy9 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_mac.sizePolicy().hasHeightForWidth())
        self.label_mac.setSizePolicy(sizePolicy9)
        self.label_mac.setLayoutDirection(Qt.LeftToRight)
        self.label_mac.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_mac)

        self.lineEdit_mac = QLineEdit(self.groupBox_mac_result)
        self.lineEdit_mac.setObjectName(u"lineEdit_mac")
        sizePolicy1.setHeightForWidth(self.lineEdit_mac.sizePolicy().hasHeightForWidth())
        self.lineEdit_mac.setSizePolicy(sizePolicy1)
        self.lineEdit_mac.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_12.addWidget(self.lineEdit_mac)

        self.label_udp = QLabel(self.groupBox_mac_result)
        self.label_udp.setObjectName(u"label_udp")
        sizePolicy9.setHeightForWidth(self.label_udp.sizePolicy().hasHeightForWidth())
        self.label_udp.setSizePolicy(sizePolicy9)
        self.label_udp.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_udp)

        self.lineEdit_udp = QLineEdit(self.groupBox_mac_result)
        self.lineEdit_udp.setObjectName(u"lineEdit_udp")
        sizePolicy1.setHeightForWidth(self.lineEdit_udp.sizePolicy().hasHeightForWidth())
        self.lineEdit_udp.setSizePolicy(sizePolicy1)
        self.lineEdit_udp.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_12.addWidget(self.lineEdit_udp)

        self.label_tcp = QLabel(self.groupBox_mac_result)
        self.label_tcp.setObjectName(u"label_tcp")
        sizePolicy9.setHeightForWidth(self.label_tcp.sizePolicy().hasHeightForWidth())
        self.label_tcp.setSizePolicy(sizePolicy9)
        self.label_tcp.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.label_tcp)

        self.lineEdit_tcp = QLineEdit(self.groupBox_mac_result)
        self.lineEdit_tcp.setObjectName(u"lineEdit_tcp")
        self.lineEdit_tcp.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_12.addWidget(self.lineEdit_tcp)


        self.gridLayout_5.addWidget(self.groupBox_mac_result, 1, 0, 1, 1)

        self.groupBox_mac_param = QGroupBox(self.tab_mac)
        self.groupBox_mac_param.setObjectName(u"groupBox_mac_param")
        sizePolicy10 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.groupBox_mac_param.sizePolicy().hasHeightForWidth())
        self.groupBox_mac_param.setSizePolicy(sizePolicy10)
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
        sizePolicy11 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.groupBox_qos.sizePolicy().hasHeightForWidth())
        self.groupBox_qos.setSizePolicy(sizePolicy11)
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

        self.verticalLayout.addWidget(self.lineEdit_tcp_eff)


        self.frame_right.addWidget(self.groupBox_tcp_eff, 0, 3, 1, 1)

        self.groupBox_msdu = QGroupBox(self.groupBox_mac_param)
        self.groupBox_msdu.setObjectName(u"groupBox_msdu")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_msdu)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.comboBox_msdu = QComboBox(self.groupBox_msdu)
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.addItem("")
        self.comboBox_msdu.setObjectName(u"comboBox_msdu")

        self.verticalLayout_6.addWidget(self.comboBox_msdu)

        self.Layout_msdu = QHBoxLayout()
        self.Layout_msdu.setObjectName(u"Layout_msdu")
        self.Layout_msdu.setSizeConstraint(QLayout.SetMinimumSize)
        self.label_msdu = QLabel(self.groupBox_msdu)
        self.label_msdu.setObjectName(u"label_msdu")
        sizePolicy.setHeightForWidth(self.label_msdu.sizePolicy().hasHeightForWidth())
        self.label_msdu.setSizePolicy(sizePolicy)

        self.Layout_msdu.addWidget(self.label_msdu)

        self.lineEdit_msdu = QLineEdit(self.groupBox_msdu)
        self.lineEdit_msdu.setObjectName(u"lineEdit_msdu")

        self.Layout_msdu.addWidget(self.lineEdit_msdu)


        self.verticalLayout_6.addLayout(self.Layout_msdu)


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

        self.Layout_MPDU = QHBoxLayout()
        self.Layout_MPDU.setObjectName(u"Layout_MPDU")
        self.label_MPDU = QLabel(self.groupBox_mpdu)
        self.label_MPDU.setObjectName(u"label_MPDU")

        self.Layout_MPDU.addWidget(self.label_MPDU)

        self.lineEdit_MPDU = QLineEdit(self.groupBox_mpdu)
        self.lineEdit_MPDU.setObjectName(u"lineEdit_MPDU")

        self.Layout_MPDU.addWidget(self.lineEdit_MPDU)


        self.verticalLayout_7.addLayout(self.Layout_MPDU)


        self.frame_right.addWidget(self.groupBox_mpdu, 0, 4, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_mac_param, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_mac, "")

        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.frame)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Wi-Fi Throughtput calculator", None))
        self.calculate_phy_btn.setText(QCoreApplication.translate("MainWindow", u"Calculate the physical throughput", None))
        self.show_phy_le.setPlaceholderText(QCoreApplication.translate("MainWindow", u"d\u00e9bit physique", None))
        self.label_greenfield.setText(QCoreApplication.translate("MainWindow", u"Greenfield", None))
        self.pushButton_greenfield.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_control_preamble.setText(QCoreApplication.translate("MainWindow", u"Control preamble", None))
        self.pushButton_control_preamble.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_txop.setText(QCoreApplication.translate("MainWindow", u"txop", None))
        self.pushButton_txop.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_mu.setText(QCoreApplication.translate("MainWindow", u"mu %", None))
        self.label_su.setText(QCoreApplication.translate("MainWindow", u"su %", None))
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

        self.groupBox_sgi_btn.setTitle("")
        self.label_sgi.setText(QCoreApplication.translate("MainWindow", u"SGI (short guard interval)", None))
        self.pushButton_sgi.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"SGI in UL :", None))
        self.comboBox_sgi_ul.setItemText(0, QCoreApplication.translate("MainWindow", u"0.8", None))
        self.comboBox_sgi_ul.setItemText(1, QCoreApplication.translate("MainWindow", u"1.6", None))
        self.comboBox_sgi_ul.setItemText(2, QCoreApplication.translate("MainWindow", u"3.2", None))

        self.label_16.setText(QCoreApplication.translate("MainWindow", u"SGI in DL :", None))
        self.comboBox_sgi_dl.setItemText(0, QCoreApplication.translate("MainWindow", u"0.8", None))
        self.comboBox_sgi_dl.setItemText(1, QCoreApplication.translate("MainWindow", u"1.6", None))
        self.comboBox_sgi_dl.setItemText(2, QCoreApplication.translate("MainWindow", u"3.2", None))

        self.label_stbc.setText(QCoreApplication.translate("MainWindow", u"STBC (Space Time Bloc Code)", None))
        self.pushButton_stbc.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_ldpc.setText(QCoreApplication.translate("MainWindow", u"LDPC (Low Density Parity Check)", None))
        self.pushButton_ldpc.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_nb_ss.setText(QCoreApplication.translate("MainWindow", u"Number of spatial stream", None))
        self.comboBox_number_spatial_stream.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_number_spatial_stream.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_number_spatial_stream.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_number_spatial_stream.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))

        self.groupbox_antennas.setTitle("")
        self.label_antennas_ap_number.setText(QCoreApplication.translate("MainWindow", u"AP number", None))
        self.comboBox_ap_number.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_ap_number.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_ap_number.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_ap_number.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_ap_number.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_ap_number.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_ap_number.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.comboBox_ap_number.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))

        self.label_title_antennas.setText(QCoreApplication.translate("MainWindow", u"Antennas", None))
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
        self.comboBox_qos.setItemText(1, QCoreApplication.translate("MainWindow", u"BK", None))
        self.comboBox_qos.setItemText(2, QCoreApplication.translate("MainWindow", u"BE", None))
        self.comboBox_qos.setItemText(3, QCoreApplication.translate("MainWindow", u"VI", None))
        self.comboBox_qos.setItemText(4, QCoreApplication.translate("MainWindow", u"VO", None))

        self.groupBox_tcp_eff.setTitle(QCoreApplication.translate("MainWindow", u"TCP efficiency", None))
        self.lineEdit_tcp_eff.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.groupBox_msdu.setTitle(QCoreApplication.translate("MainWindow", u"Agg MSDU", None))
        self.comboBox_msdu.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.comboBox_msdu.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.comboBox_msdu.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.comboBox_msdu.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.comboBox_msdu.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.comboBox_msdu.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.comboBox_msdu.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))

        self.label_msdu.setText(QCoreApplication.translate("MainWindow", u"MSDU", None))
        self.lineEdit_msdu.setText(QCoreApplication.translate("MainWindow", u"1500", None))
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
    # retranslateUi

