from PySide6.QtWidgets import QPushButton, QGroupBox
from core import *
from core.additional_functions import *
from ui_file import *
from ui_functions import *


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """Initialize the main window"""
        super(Main, self).__init__()
        self.setupUi(self)
        self.show()
        # ui functions
        self.connectFunction()
        self.hideTab()

    # ui functions

    def connectFunction(self):
        """Connect all the functions to the buttons"""
        # intercepter le changement du standard
        self.comboBox_standard_selection.currentTextChanged.connect(self.changeGroupbox)
        self.comboBox_frequency_band.removeItem(0)  # supprimer "choose …" dans le comboBox_frequency_band
        self.comboBox_bandwidth.removeItem(0)  # supprimer "choose …" dans dans le comboBox_frequency_band

        # intercepter signal quand slide sur les boutons slider
        self.mu_slider.valueChanged.connect(self.mu_slider_value_changed)
        self.su_slider.valueChanged.connect(self.su_slider_value_changed)
        # intercepter signal quand on change les valeurs de lineEdit_affichage_mu et lineEdit_affichage_su
        self.lineEdit_affichage_mu.textChanged.connect(self.mu_lineEdit_value_changed)
        self.lineEdit_affichage_su.textChanged.connect(self.su_lineEdit_value_changed)

        # intercepter le changement du standard dans le cas ou on doit cacher le spacer
        self.comboBox_standard_selection.currentTextChanged.connect(self.hide_spacer)

        for button in self.findChildren(QPushButton):
            button.clicked.connect(self.showSGI)

        for button in self.findChildren(QPushButton):
            button.clicked.connect(self.showCSI)

    def hideTab(self):
        """Hide or show the tabWidget and groupbox depending on the standard"""
        # Quand on change de tab (phy/mac) on cache/montre les groupbox correspondants
        self.tabWidget.currentChanged.connect(self.changeTab)
        self.tabWidget.currentChanged.connect(self.changeGroupbox)

        for groupbox in self.findChildren(QGroupBox):
            if groupbox.objectName() != "Header":
                groupbox.hide()
            else:
                groupbox.show()

        # pour chaque pushbutton on associe le fonctionnement (ON/OFF)
        for button in self.findChildren(QPushButton):
            button.clicked.connect(self.btn_txt)

    def changeTab(self):
        """Hide or show the tabWidget depending on the standard"""
        if self.comboBox_standard_selection.currentText() == "Choose a standard":
            for groupbox in self.findChildren(QGroupBox):
                if groupbox.objectName() != "Header":
                    groupbox.hide()

        if self.tabWidget.currentIndex() == 0:
            self.calculate_phy_btn.setText("Calculate physical throughput")

        elif self.tabWidget.currentIndex() == 1:
            self.calculate_phy_btn.setText("Calculate MAC throughput")

    def getStandardSelection(self):
        """Get the standard selection and return it for groupbox show/hide management depending on the standard"""
        list_of_standard = []
        for i in range(self.comboBox_standard_selection.count()):
            list_of_standard.append(self.comboBox_standard_selection.itemText(i))
        text = self.comboBox_standard_selection.currentText()
        return text, list_of_standard

    def getTroughputAB(self):
        """Get the throughput value and return it for Wi-Fi A/B standard"""
        self.calculate_phy_btn.clicked.connect(self.WiFi2_TroughputCalculationFunction)

    def getTroughputG(self):
        """Get the throughput value and return it for Wi-Fi G standard"""
        self.calculate_phy_btn.clicked.connect(self.WiFi3_TroughputCalculationFunction)

    def getTrougthputN(self):
        """Get the throughput value and return it for Wi-Fi N standard"""
        self.calculate_phy_btn.clicked.connect(self.WiFi4_TroughputCalculationFunction)

    def showPhy80211a(self):
        """Show the physical groupbox menu for 802.11a"""
        for groupbox in self.findChildren(QGroupBox):

            self.groupbox_modulation.show()
            if groupbox.objectName() != "Header" and "groupbox_modulation":
                groupbox.hide()
                self.comboBox_frequency_band.setCurrentText("5 GHz")
                self.comboBox_frequency_band.setEnabled(False)
                self.comboBox_bandwidth.setCurrentText("20 MHz")
                self.comboBox_bandwidth.setEnabled(False)

    def showMac80211a(self):
        """Show the MAC groupbox menu for 802.11a"""
        for _ in self.findChildren(QGroupBox):
            self.groupBox_mac_param.show()
            for groupBox_mac_param in self.groupBox_mac_param.findChildren(QGroupBox):
                list_show = ["groupBox_qos", "groupBox_rts", "groupBox_enc_protocol", "groupBox_tcp_eff"]
                for i in list_show:
                    if groupBox_mac_param.objectName() == i:
                        groupBox_mac_param.show()

            # parcourir groupBox_mac_result et afficher ses fils
            self.groupBox_mac_result.show()
            for groupBox_mac_result in self.groupBox_mac_result.findChildren(QGroupBox):
                groupBox_mac_result.show()

    def showPhy80211b(self):
        """Show the physical groupbox menu for 802.11b"""
        for groupbox in self.findChildren(QGroupBox):
            self.Header.show()
            self.groupbox_modulation.show()
            if groupbox.objectName() != "Header" and "groupbox_modulation":
                groupbox.hide()
                self.comboBox_frequency_band.setCurrentText("2.4 GHz")
                self.comboBox_frequency_band.setEnabled(False)
                self.comboBox_bandwidth.setCurrentText("20 MHz")
                self.comboBox_bandwidth.setEnabled(False)

    def showPhy80211g(self):
        """Show the physical groupbox menu for 802.11g"""
        self.showPhy80211b()

    def showPhy80211n(self):
        """Show the physical groupbox menu for 802.11n"""
        self.comboBox_frequency_band.removeItem(2)

        self.comboBox_bandwidth.removeItem(3)
        self.comboBox_bandwidth.removeItem(2)

        self.comboBox_frequency_band.setEnabled(True)
        self.comboBox_bandwidth.setEnabled(True)

        for groupbox in self.findChildren(QGroupBox):
            self.Header.show()
            self.groupbox_modulation.show()
            self.groupbox_ctrl_modulation.show()
            self.groupbox_sgi.show()
            self.groupbox_wifi_n.show()

            for groupbox_wifi_n in self.groupbox_wifi_n.findChildren(QGroupBox):
                groupbox_wifi_n.show()

            if groupbox.objectName() != "Header" and "groupbox_modulation" and "groupbox_ctrl_modulation" and "groupBox_sgi_btn" and "groupbox_wifi_n":
                groupbox.hide()

            self.groupBox_sgi_dl.hide()
            self.groupBox_sgi_ul.hide()

    def showMac80211n(self):
        """Show the MAC groupbox menu for 802.11n"""
        for _ in self.findChildren(QGroupBox):
            self.groupBox_mac_param.show()
            for groupBox_mac_param in self.groupBox_mac_param.findChildren(QGroupBox):
                groupBox_mac_param.show()

            self.groupBox_mac_result.show()
            for groupBox_mac_result in self.groupBox_mac_result.findChildren(QGroupBox):
                groupBox_mac_result.show()

        self.horizontalGroupBox.show()
        self.comboBox_mpdu.hide()
        self.comboBox_msdu.hide()
        self.GroupBox_msdu_nb.hide()
        self.groupBox_package_size.hide()

    def showPhy80211ac(self):
        """Show the physical groupbox menu for 802.11ac"""
        QMessageBox.about(self, "Information", "This standard is not yet implemented")
        for groupbox in self.findChildren(QGroupBox):
            if groupbox.objectName() != "Header":
                groupbox.hide()

        self.comboBox_frequency_band.removeItem(3)
        self.comboBox_frequency_band.setEnabled(True)
        self.comboBox_bandwidth.setEnabled(True)

        self.comboBox_frequency_band.setCurrentText("5 GHz")
        self.comboBox_frequency_band.setEnabled(False)

        self.comboBox_bandwidth.removeItem(3)

        if self.comboBox_bandwidth.findText("80 MHz") == -1:
            self.comboBox_bandwidth.addItem("80 MHz")
        pass

    def showPhy80211ax(self):
        QMessageBox.about(self, "Information", "This standard is not yet implemented")
        QMessageBox.about(self, "Information",
                          "revoir ou vérifier les variables Ldata, LdataTCP, mcs, bf, udp, tcp")
        QMessageBox.about(self, "Information", "adapter le mcs au ax")

        self.pushButton_sgi.setText("OFF")

        self.comboBox_frequency_band.setEnabled(True)
        self.comboBox_bandwidth.setEnabled(True)

        for groupbox in self.findChildren(QGroupBox):
            groupbox.show()

        self.groupBox_sgi_dl.hide()
        self.groupBox_sgi_ul.hide()

        self.groupBox_number_of_csi.hide()
        self.groupBox_number_of_ss_for_CSI.hide()
        self.groupBox_antennas_for_csi.hide()

        if self.comboBox_frequency_band.findText("6 GHz") == -1:
            self.comboBox_frequency_band.addItem("6 GHz")

        if self.comboBox_bandwidth.findText("80 MHz") == -1:
            self.comboBox_bandwidth.addItem("80 MHz")
        if self.comboBox_bandwidth.findText("160 MHz") == -1:
            self.comboBox_bandwidth.addItem("160 MHz")
        else:
            print("donner la techno")

    def changeGroupbox(self):
        """Hide or show the groupbox depending on the standard selected"""
        text, list_of_standard = self.getStandardSelection()
        #Choose wifi standard
        if text == list_of_standard[0]:
            #hide all groupbox except header
            for groupbox in self.findChildren(QGroupBox):
                if groupbox.objectName() != "Header":
                    groupbox.hide()
        # Wi-Fi a
        if text == list_of_standard[1]:
            self.getTroughputAB()
            if self.tabWidget.currentIndex() == 0:
                self.showPhy80211a()
            elif self.tabWidget.currentIndex() == 1:
                self.showMac80211a()
        # Wi-Fi b
        elif text == list_of_standard[2]:
            self.getTroughputAB()
            self.showPhy80211b()
        # Wi-Fi g
        elif text == list_of_standard[3]:
            self.getTroughputG()
            self.showPhy80211g()
        # Wi-Fi n
        elif text == list_of_standard[4]:
            self.getTrougthputN()
            if self.tabWidget.currentIndex() == 0:
                self.showPhy80211n()
            elif self.tabWidget.currentIndex() == 1:
                self.showMac80211n()
        # Wi-Fi ac
        elif text == list_of_standard[5]:
            self.showPhy80211ac()
        # Wi-Fi ax
        elif text == list_of_standard[6]:
            self.showPhy80211ax()

    def showSGI(self):
        """Show the SGI menu when standard is wifi ax"""
        if self.pushButton_sgi.isChecked():
            self.groupBox_sgi_dl.show()
            self.groupBox_sgi_ul.show()
        else:
            self.groupBox_sgi_dl.hide()
            self.groupBox_sgi_ul.hide()

    def showCSI(self):
        """Show the CSI menu when standard is wifi ax"""
        if self.pushButton_csi.isChecked():
            self.groupBox_number_of_csi.show()
            self.groupBox_number_of_ss_for_CSI.show()
            self.groupBox_antennas_for_csi.show()
        else:
            self.groupBox_number_of_csi.hide()
            self.groupBox_number_of_ss_for_CSI.hide()
            self.groupBox_antennas_for_csi.hide()

    def mu_slider_value_changed(self):
        """Get the value of the slider and display it in the label"""
        mu_value = self.mu_slider.value()
        mu_value = mu_value
        self.lineEdit_affichage_mu.setText(str(mu_value))

    def su_slider_value_changed(self):
        """Get the value of the slider and display it in the label"""
        su_value = self.su_slider.value()
        su_value = su_value
        self.lineEdit_affichage_su.setText(str(su_value))

    def mu_lineEdit_value_changed(self):
        """Get the value of the lineEdit and display it in the slider"""
        mu_value = self.lineEdit_affichage_mu.text()
        mu_value = int(mu_value)
        self.mu_slider.setValue(mu_value)

    def su_lineEdit_value_changed(self):
        """Get the value of the lineEdit and display it in the slider"""
        su_value = self.lineEdit_affichage_su.text()
        su_value = int(su_value)
        self.su_slider.setValue(su_value)

    def hide_spacer(self):
        """Hide or show spacer depending """
        text, list_of_standard = self.getStandardSelection()
        for i in range(1, 3):
            if text == list_of_standard[i]:
                self.vertical_left.addItem(self.verticalSpacer)
        for i in range(4, 6):
            if text == list_of_standard[i]:
                self.vertical_left.removeItem(self.verticalSpacer)

    def btn_txt(self):
        """Change the text of the button to ON or OFF"""
        if self.sender() != self.calculate_phy_btn:
            if self.sender().text() == "ON":
                self.sender().setText("OFF")
            else:
                self.sender().setText("ON")

    # wifi functions

    def WiFi2_TroughputCalculationFunction(self):
        """Calculate the throughput of the wifi 2"""
        WiFiagObject = WiFiag()
        p = reading_parameters(self)
        for cle, valeur in p.items():
            print("'"' {} '"' contient {}.".format(cle, valeur))

        # calculer le throughput

        debit, ndbps = WiFiagObject.ag_phy_throughput(p["data_modulation"])
        affichage_debit_phy = str(debit / 10 ** 6) + " Mbps"

        if self.tabWidget.currentIndex() == 0:
            self.show_phy_le.setText(affichage_debit_phy)

        elif self.tabWidget.currentIndex() == 1:
            self.show_phy_le.setText("")

        PG_phy_tpt = WiFiagObject.ag_phy_throughput(p["data_modulation"])
        print("PG_a : ", PG_phy_tpt)

        # calculer le debit mac

        tx_exchange_time = WiFiagObject.ag_msdu_exchange_time(p["bf"], p["data_modulation"], p["ctrl_modulation"],
                                                              p["qos"], p["msdu_length"], p["rts"], p["encryption"])
        ack_tcp_time = WiFiagObject.ag_msdu_exchange_time(p["bf"], p["data_modulation"], p["ctrl_modulation"], p["qos"],
                                                          WiFiagObject.tcp_ack_pckt_bytes_msdu, p["rts"],
                                                          p["encryption"])  # ??
        ack_tcp_time = WiFiagObject.ag_msdu_exchange_time(p["bf"], p["data_modulation"], p["ctrl_modulation"], p["qos"],
                                                          p["msdu_length"], p["rts"], p["encryption"])

        [MAC_throughput, UDP_throughput, TCP_throughput] = WiFiagObject.ag_throughput(tx_exchange_time, ack_tcp_time,
                                                                                      p["tcp_efficiency"],
                                                                                      p["msdu_length"])
        affichage_debit_mac = str(round(MAC_throughput, 2)) + " Mbps"
        if MAC_throughput < 0:
            affichage_debit_mac = " le debit mac n'est pas calculé "
        self.lineEdit_udp.setText(str(round(UDP_throughput, 2)) + " Mbps")
        self.lineEdit_tcp.setText(str(round(TCP_throughput, 2)) + " Mbps")
        self.lineEdit_mac.setText(affichage_debit_mac)
        print("PG_a : ",
              WiFiagObject.ag_throughput(tx_exchange_time, ack_tcp_time, p["tcp_efficiency"], p["msdu_length"]))

        # tx_exchange_time = WiFiagObject.ag_msdu_exchange_time(bf, data_modulation, ctrl_modulation, qos, msdu_length, rts, encryption)
        # ack_tcp_time = WiFiagObject.ag_msdu_exchange_time(bf, data_modulation, ctrl_modulation, qos, WiFiagObject.tcp_ack_pckt_bytes_msdu, rts, encryption)

        PG_phy_tpt, nbs = WiFiagObject.ag_phy_throughput(p["data_modulation"])
        mac_tpt, udp_tpt, tcp_tpt = WiFiagObject.ag_throughput(tx_exchange_time, ack_tcp_time, p["tcp_efficiency"],
                                                               p["msdu_length"])
        writing_validation_file(self, p, debit, PG_phy_tpt, MAC_throughput, mac_tpt, UDP_throughput, udp_tpt,
                                TCP_throughput, tcp_tpt)

    def WiFi3_TroughputCalculationFunction(self):
        """Calculate the throughput of the wifi 3"""
        WiFiagObject = WiFiag()
        p = reading_parameters(self)
        for cle, valeur in p.items():
            print("'"' {} '"' contient {}.".format(cle, valeur))
        print('fonction WiFi3_TroughputCalculationFunction')

        # calcul débit phy
        debit, ndbps = WiFiagObject.ag_phy_throughput(p["data_modulation"])
        affichage_debit_phy = str(debit / 10 ** 6) + " Mbps"

        if self.tabWidget.currentIndex() == 0:
            self.show_phy_le.setText(affichage_debit_phy)

        elif self.tabWidget.currentIndex() == 1:
            self.show_phy_le.setText("")

        print("PG_g :", WiFiagObject.ag_phy_throughput(p["data_modulation"]))
        self.show_phy_le.setText(affichage_debit_phy)
        affichage_2 = str(ndbps) + " ndbps"

        # calcul débit mac
        tx_exchange_time = WiFiagObject.ag_msdu_exchange_time(p["bf"], p["data_modulation"], p["ctrl_modulation"],
                                                              p["qos"], p["msdu_length"], p["rts"], p["encryption"])
        ack_tcp_time = WiFiagObject.ag_msdu_exchange_time(p["bf"], p["data_modulation"], p["ctrl_modulation"], p["qos"],
                                                          WiFiagObject.tcp_ack_pckt_bytes_msdu, p["rts"],
                                                          p["encryption"])  # ??
        ack_tcp_time = WiFiagObject.ag_msdu_exchange_time(p["bf"], p["data_modulation"], p["ctrl_modulation"], p["qos"],
                                                          p["msdu_length"], p["rts"], p["encryption"])

        [MAC_throughput, UDP_throughput, TCP_throughput] = WiFiagObject.ag_throughput(tx_exchange_time, ack_tcp_time,
                                                                                      p["tcp_efficiency"],
                                                                                      p["msdu_length"])
        affichage_debit_mac = str(round(MAC_throughput, 2)) + " Mbps"
        if MAC_throughput < 0:
            affichage_debit_mac = " le debit mac n'est pas calculé "
        self.lineEdit_udp.setText(str(round(UDP_throughput, 2)) + " Mbps")
        self.lineEdit_tcp.setText(str(round(TCP_throughput, 2)) + " Mbps")
        self.lineEdit_mac.setText(affichage_debit_mac)
        print("PG_g :",
              WiFiagObject.ag_throughput(tx_exchange_time, ack_tcp_time, p["tcp_efficiency"], p["msdu_length"]))

        PG_phy_tpt, nbs = WiFiagObject.ag_phy_throughput(p["data_modulation"])
        mac_tpt, udp_tpt, tcp_tpt = WiFiagObject.ag_throughput(tx_exchange_time, ack_tcp_time, p["tcp_efficiency"],
                                                               p["msdu_length"])
        writing_validation_file(self, p, debit, PG_phy_tpt, MAC_throughput, mac_tpt, UDP_throughput, udp_tpt,
                                TCP_throughput, tcp_tpt)

    def WiFi4_TroughputCalculationFunction(self):
        """Calculate the throughput of the wifi 4"""
        WiFinObject = WiFin()
        p = reading_parameters(self)
        for cle, valeur in p.items():
            print("'"' {} '"' contient {}.".format(cle, valeur))
        print('fonction WiFi4_TroughputCalculationFunction')
        n_sc_value = p["bw"]  # à vérifier
        PG_n, n_ndbps, nes = WiFinObject.n_phy_throughput(p["data_modulation"], n_sc_value, p["ss_nb"], p["sgi"])
        PG_n = str(round((PG_n / 10 ** 6), 2))
        print("PG_n:", PG_n)
        n_phy_rate, n_ndbps, nes = WiFinObject.n_phy_throughput(p["data_modulation"], n_sc_value, p["ss_nb"], p["sgi"])
        affichage_debit_phy = str(round((n_phy_rate / 10 ** 6), 2)) + " Mbps"

        if self.tabWidget.currentIndex() == 0:
            self.show_phy_le.setText(affichage_debit_phy)

        elif self.tabWidget.currentIndex() == 1:
            self.show_phy_le.setText("")

        # calcul débit mac
        [errors_data, errors_tcp_ack, mpdu_nb, msdu_nb, mpdu_nb_tcp_ack, msdu_nb_tcp_ack, data_tx_exchange_time,
         tcp_ack_exchange_time] = WiFinObject.n_msdu_exchange_time(p["bf"],
                                                                   p["bw"], p["data_modulation"], p["ss_nb"], p["sgi"],
                                                                   p["ldpc"], p["stbc"], p["greenfield"],
                                                                   p["control_preamble"], p["ctrl_modulation"],
                                                                   p["qos"], p["txop"],
                                                                   p["msdu_length"], p["msdu_nb"], p["msdu_limit"],
                                                                   p["mpdu_nb"], p["rts"], p["encryption"],
                                                                   p["tcp_efficiency"])

        if p["msdu_nb"] != msdu_nb:
            print("msdu limited to " + str(msdu_nb))
            QMessageBox.about(self, "Warning", "msdu limited to " + str(msdu_nb))
            p["msdu_nb"] = msdu_nb

        if p["mpdu_nb"] != mpdu_nb:
            print("mpdu limited to " + str(mpdu_nb))
            QMessageBox.about(self, "Warning", "mpdu limited to " + str(mpdu_nb))
            p["mpdu_nb"] = mpdu_nb

        [MAC_throughput, UDP_throughput, TCP_throughput] = WiFinObject.n_throughput(data_tx_exchange_time,
                                                                                    tcp_ack_exchange_time,
                                                                                    p["msdu_length"], p["msdu_nb"],
                                                                                    p["mpdu_nb"])
        if MAC_throughput < 0:
            affichage_debit_mac = " le debit mac n'est pas calculé "
        print("PG_n : ",
              WiFinObject.n_throughput(data_tx_exchange_time, tcp_ack_exchange_time, p["msdu_length"], p["msdu_nb"],
                                       p["mpdu_nb"]))
        self.lineEdit_mac.setText(str(round(MAC_throughput, 2)) + " Mbps")
        self.lineEdit_udp.setText(str(round(UDP_throughput, 2)) + " Mbps")
        self.lineEdit_tcp.setText(str(round(TCP_throughput, 2)) + " Mbps")

        [PG_phy_tpt, n_ndbps, nes] = WiFinObject.n_phy_throughput(p["data_modulation"], n_sc_value, p["ss_nb"],
                                                                  p["sgi"])
        mac_tpt, udp_tpt, tcp_tpt = WiFinObject.n_throughput(data_tx_exchange_time, tcp_ack_exchange_time,
                                                             p["msdu_length"], p["msdu_nb"], p["mpdu_nb"])
        writing_validation_file(self, p, n_phy_rate, PG_phy_tpt, MAC_throughput, mac_tpt, UDP_throughput, udp_tpt,
                                TCP_throughput, tcp_tpt)

    def WiFi6_TroughputCalculationFunction(self):
        """Calculate the throughput of the wifi 6"""
        p = reading_parameters(self)
        for cle, valeur in p.items():
            print("'"' {} '"' contient {}.".format(cle, valeur))

        """
            B, Bandwith utilisé [20,40,80,160]
            Msta, Nombre d'antenne station
            Map, Nombre d'antenne AP
            S, Nombre d'utilisateur dans la configuration
            AggMPDU, Nombre de paquets MPDU aggrégés dans une A-MPDU
            AggMSDU, Nombre de paquets MSDU aggrégés dans une MPDU
            GiDL, Interval de garde en DL en microsecondes
            GiUL,  Interval de garde en UL en microsecondes
            a, Taux d'utilisation SU et MU en pourcentage ( a= 0.2 => 20% SU et 80% en MU )
            b, Taux d'utilisation MU DL et MU UL en pourcentage ( b= 0.6 => 60% MU DL et 40% en MU UL)
            QoS, Classe de QOS :
                        'legacy', Legacy
                        'AX_VO' Voix,
                        'AX_VI' Video,
                        'AX_BE' Best Effort,
                        'AX_BK' Background
            LambdaCSI, Nombre de tentatives CSI  par seconde
            NSS, Nombre de flux spatiaux utilisé pour le csi
            NRX, Nombre d'antenne de transmission utilisé pour le csi
            AngleQuantif,  (AngleQuantif = 1)
            Grpmt,      (Grpmt = 1)
            DCM, Utilisation des mcs DCM (DCM = 1) ou pas (DCM = 0).
        """

        Msta = p["Msta"]
        b = p["bw"]
        B = p["B"]  # B, Bandwith utilisé [20,40,80,160]

        Map = p["Map"]
        S = p["S"]
        AggMPDU = p["AggMPDU"]
        AggMSDU = p["AggMSDU"]
        GiDL = p["GiDL"]
        GiUL = p["GiUL"]
        a = p["su_percentage"]
        b = p["mu_percentage"]
        # QoS = p["qos"]

        list_qos_values = [0, 1, 2, 3, 4]
        list_qos_code = ["legacy", "AX_BK", "AX_BE", "AX_VI", "AX_VO"]
        QoS = list_qos_code[list_qos_values.index(p["qos"])]

        LambdaCSI = p["nb_csi"]
        NSS = p["nb_ss"]
        NRX = p["nb_rx_csi"]
        AngleQuantif = p["angle_quantif"]
        Grpmt = p["grpmt"]

        DCM = p["DCM"]
        mcs = p["data_modulation"]
        Ldata = p["package_size"]

        ofdma = p["OFDMA_use"]
        nru = p["nru"]
        mumimo = p["mumimo"]
        RTSCTS = p["rts"]
        #  à regarder de près
        udp = 1
        tcp = 1
        LdataTCP = 0
        bf = 0

        QMessageBox.about(self, "Warning", "revoir ou vérifier les variables Ldata, LdataTCP, mcs, bf, udp, tcp")
        QMessageBox.about(self, "Warning", "adapter le mcs au ax")
        WiFiaxObject = IEEE80211ax(B, Msta, Map, S, AggMPDU, AggMSDU, GiDL, GiUL, a, b, QoS, LambdaCSI, NSS, NRX,
                                   AngleQuantif,
                                   Grpmt, DCM)
        WiFiaxObject.setup(Ldata, LdataTCP, mcs, bf, ofdma, nru, mumimo, RTSCTS, udp, tcp)
        WiFiaxObject.QoS_Config()
        RatePerOfdm = WiFiaxObject.Phy_DataRate_Full_MIMO()

        phy_rate = WiFiaxObject.Get_Phy_Datarate()

        affichage_debit_phy = str(round((phy_rate / 10 ** 6), 2)) + " Mbps"
        # affichage_debit_phy = " en cour d'implémentation"
        self.show_phy_le.setText(affichage_debit_phy)

        QMessageBox.about(self, "Warning", "802.11ax is not implemented yet")
        print("802.11ax is not implemented")

        # afficher le pourcentage mu et su


if __name__ == '__main__':
    app = QApplication()
    window = Main()
    app.exec()
