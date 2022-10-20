from PySide6.QtWidgets import QMessageBox

import csv # Le module csv implémente des classes pour lire et ecrire des données tabulaires au format CSV.


def reading_parameters(self):

    """ functions for reading input parameters """
    bf_code = "5 GHz"  # pour 802.11a
    param_dictionary ={}

    #récuperer la techno dans comboBox_standard_selection
    techno = self.comboBox_standard_selection.currentText()
    print(techno+" additionnal_functions")
    param_dictionary["techno"]= techno

    # # lecture des informations
    ################################

    #récuperer la frequency band dans comboBox_frequency_band  

    frequency_band_code = self.comboBox_frequency_band.currentText()  # récupère le texte de la case bw           
    list_frequency_band_values = [0, 1]
    list_frequency_band_code = ["5 GHz", "2.4 GHz"]
    bf_value = list_frequency_band_values[list_frequency_band_code.index(frequency_band_code)]
    param_dictionary["bf"]= bf_value

    #récuperer la bandwidth dans comboBox_bandwidth
    bw_code = self.comboBox_bandwidth.currentText()   
    list_bw_code = ["20 MHz", "40 MHz", "80 MHz", "160 MHz"]       
    list_bw_values = [0, 1, 2, 3 ]    
    bw_value = list_bw_values[list_bw_code.index(bw_code)]
    param_dictionary["bw"] = bw_value # bw bandwith pour a, g, n

    list_B_values = [20, 40, 80, 160 ] # pour le ax
    B_value = list_B_values[list_bw_code.index(bw_code)] # pour le ax
    param_dictionary["B"] = int(B_value) # B bandwith pour ax
    if techno != "802.11ax" and B_value == 160 :
        QMessageBox.about(self, "Error", "160 MHz bandwidth is only allowed for 802.11ax")
    
    if ( techno == "802.11n" ) and B_value == 80 :
        QMessageBox.about(self, "Error", "80 MHz bandwidth is only allowed for 802.11ac and 802.11ax")
    
    #récuperer la modulation dans combobox_choice_modulation
    data_modulation_code = self.combobox_choice_modulation.currentText()  # récupère le texte de la case modulation
    data_modulation_value = int(data_modulation_code)
    param_dictionary["data_modulation"]= data_modulation_value

    #récuperer le ctrl modulation dans comboBox_ctrl_modulation
    ctrl_modulation_code = self.comboBox_ctrl_modulation.currentText()  # récupère le texte de la case ctrl_modulation
    ctrl_modulation_value = int(ctrl_modulation_code)
    param_dictionary["ctrl_modulation"]= ctrl_modulation_value

    # récupération de la valeur du bouton SGI :
    if self.pushButton_sgi.isChecked():
        sgi_code = "ON"
    else:
        sgi_code = "OFF"
 
    list_sgi_values = [0, 1]
    list_sgi_code = ["OFF", "ON"]
    sgi_value = list_sgi_values[list_sgi_code.index(sgi_code)]  # affecte la valeur de SGI
    param_dictionary["sgi"]= sgi_value

    sgi_dl_code = self. comboBox_sgi_dl.currentText()  # récupère le texte de la case Short Guard Interval en DL
    sgi_dl_value = float(sgi_dl_code)
    param_dictionary["GiDL"]= sgi_dl_value

    sgi_ul_code = self. comboBox_sgi_ul.currentText()  # récupère le texte de la case Short Guard Interval en UL
    sgi_ul_value = float(sgi_ul_code)
    param_dictionary["GiUL"]= sgi_ul_value

    # récupération de la valeur de ldpc ;
    if self.pushButton_ldpc.isChecked():
        ldpc_code = "ON"
    else:
        ldpc_code = "OFF" 

    list_ldpc_values = [0, 1]
    list_ldpc_number = ["OFF", "ON"]
    ldpc_value = list_ldpc_values[list_ldpc_number.index(ldpc_code)]  # affecte la valeur de stbc
    param_dictionary["ldpc"]= ldpc_value  
        
    # récupération de la valeur de stbc ;
    if self.pushButton_stbc.isChecked():
        stbc_code = "ON"
    else:
        stbc_code = "OFF"

    list_stbc_values = [0, 1]
    list_stbc_number = ["OFF", "ON"]
    stbc_value = list_stbc_values[list_stbc_number.index(stbc_code)]  # affecte la valeur de stbc
    param_dictionary["stbc"]= stbc_value

    # récupération de la valeur de number of spatial streams ; ; 
    ss_nb_code = self.comboBox_number_spatial_stream.currentText()  # récupère le texte de la case ss_number   
    list_ss_nb_values = [1, 2, 3, 4]
    list_ss_number_code = ["1", "2", "3", "4"]
    ss_nb_value = list_ss_nb_values[list_ss_number_code.index(ss_nb_code)]  # affecte la valeur de ss_number
    param_dictionary["ss_nb"]= ss_nb_value  
    
    # récuperation de la valeur de comboBox_ap_number
    ap_nb_code = self.comboBox_ap_number.currentText()  # récupère le texte de la case ap_number
    list_ap_nb_values = [1, 2, 3, 4, 5, 6, 7, 8]
    list_ap_number_code = ["1", "2", "3", "4", "5", "6", "7", "8"]
    ap_nb_value = list_ap_nb_values[list_ap_number_code.index(ap_nb_code)]  # affecte la valeur de ap_number
    param_dictionary["Map"]= ap_nb_value

    # récuperation de la valeur de comboBox_station_number
    station_nb_code = self.comboBox_station_number.currentText()  # récupère le texte de la case station_number
    list_station_nb_values = [1, 2, 3, 4, 5, 6, 7, 8]
    list_station_number_code = ["1", "2", "3", "4", "5", "6", "7", "8"]
    station_nb_value = list_station_nb_values[list_station_number_code.index(station_nb_code)]  # affecte la valeur de station_number
    param_dictionary["Msta"]= station_nb_value

    # récuperation de la valeur de comboBox_users_number
    users_nb_code = self.comboBox_users_number.currentText()  # récupère le texte de la case users_number
    list_users_nb_values = [1, 2, 4, 8, 16, 32, 64]
    list_users_number_code = ["1", "2", "4", "8", "16", "32", "64"]
    users_nb_value = list_users_nb_values[list_users_number_code.index(users_nb_code)]  # affecte la valeur de users_number
    param_dictionary["S"]= users_nb_value

    # récupération de la valeur de greenfield
    if self.pushButton_greenfield.isChecked():
        greenfield_code = "ON"
    else:
        greenfield_code = "OFF"
 
    list_greenfield_values = [0, 1]
    list_greenfield_number = ["OFF", "ON"]
    greenfield_value = list_greenfield_values[list_greenfield_number.index(greenfield_code)]  # affecte la valeur de greenfield
    param_dictionary["greenfield"]= greenfield_value

    # récupération de la valeur case  du control_preamble
    if self.pushButton_control_preamble.isChecked():
        control_preamble_code = "ON"
    else:
        control_preamble_code = "OFF"

    list_control_preamble_values = [0, 1]
    list_control_preamble_number = ["OFF", "ON"]
    control_preamble_value = list_control_preamble_values[list_control_preamble_number.index(control_preamble_code)]  # affecte la valeur de control_preamble
    param_dictionary["control_preamble"]= control_preamble_value

    # récupération de la valeur de txop ;
    if self.pushButton_txop.isChecked():
        txop_code = "ON"
    else:
        txop_code = "OFF"

    list_txop_values = [0, 1]
    list_txop_number = ["OFF", "ON"]
    txop_value = list_txop_values[list_txop_number.index(txop_code)]  # affecte la valeur de txop
    param_dictionary["txop"]= txop_value

    #récuperation du slider mu
    mu_percentage_value = self. mu_slider.value()  # récupère le texte de la case MU utilization percentage    
    param_dictionary["mu_percentage"]= mu_percentage_value 

    #récuperation du slider su
    su_percentage_value = self. su_slider.value()  # récupère le texte de la case SU utilization percentage
    param_dictionary["su_percentage"]= su_percentage_value

    #récuperer l'état du bouton CSI (Channel State Information)
    if self.pushButton_csi.isChecked():
        csi_code = "ON"
    else:
        csi_code = "OFF"
    list_csi_values = [0, 1]
    list_csi_code = ["OFF", "ON"]
    csi_value = list_csi_values[list_csi_code.index(csi_code)]  # affecte la valeur de csi
    param_dictionary["CSI_use"]= csi_value

    # récupération de la valeur du combobox comboBox_nb_csi
    nb_csi_code = self.comboBox_nb_csi.currentText()  # récupère le texte de la case nb_csi
    nb_csi_value = int(nb_csi_code)
    param_dictionary["nb_csi"]= nb_csi_value

    # récupération de la valeur du combobox comboBox_nb_of_ss_csi
    nb_ss_code = self.comboBox_nb_of_ss_csi.currentText()  # récupère le texte de la case Number of spatial flows used for the csi
    nb_ss_value = int(nb_ss_code)
    param_dictionary["nb_ss"]= nb_ss_value

    # récupération de la valeur du combobox comboBox_antennas_csi
    nb_rx_csi_code = self.comboBox_antennas_csi.currentText()  # récupère le texte de la case Number of RX antennas used for the csi ?????
    nb_rx_csi_value = int(nb_rx_csi_code)
    param_dictionary["nb_rx_csi"]= nb_rx_csi_value

    # récupération de la valeur du pushbutton dcm
    if self.pushButton_dcm.isChecked():
        DCM_code = "ON"
    else:
        DCM_code = "OFF"
    
    list_DCM_values = [0, 1]
    list_DCM_number = ["OFF", "ON"]
    DCM_value = list_DCM_values[list_DCM_number.index(DCM_code)]  # affecte la valeur de DCM
    param_dictionary["DCM"]= DCM_value

    # récupération de la valeur du combobox NRU
    nru_code = self.comboBox_nru.currentText()  # récupération de le texte de la case nru   
    list_nru_values = [1, 2]
    list_nru_number = [ "1", "2"]
    nru_value = list_nru_values[list_nru_number.index(nru_code)]  # affecte la valeur de nru
    param_dictionary["nru"]= nru_value

    # récupération de la valeur du pushbutton mu_mimo
    if self.pushButton_mu_mimo.isChecked():
        mumimo_code = "ON"
    else:
        mumimo_code = "OFF"
    
    list_mumimo_values = [0, 1]
    list_mumimo_code = ["OFF", "ON"]
    mumimo_value = list_mumimo_values[list_mumimo_code.index(mumimo_code)]  # affecte la valeur de mumimo
    param_dictionary["mumimo"]= mumimo_value

    # récupération de la valeur du pushbutton OFDMA
    if self.pushButton_ofdma.isChecked():
        OFDMA_use_code = "ON"
    else:
        OFDMA_use_code = "OFF"
    
    list_OFDMA_use_values = [0, 1]
    list_OFDMA_use_number = ["OFF", "ON"]
    OFDMA_use_value = list_OFDMA_use_values[list_OFDMA_use_number.index(OFDMA_use_code)]  # affecte la valeur de OFDMA_use
    param_dictionary["OFDMA_use"]= OFDMA_use_value

    # récupération de la valeur du spinbox angle_quantif
    angle_quantif_value = self. spinBox_angle_quantif.text()  # récupère le texte de la case angle_quantif_box
    param_dictionary["angle_quantif"]= angle_quantif_value

    #récuperer le qos de la comboBox_qos
    qos_code = self.comboBox_qos.currentText()  # récupère le texte de la case qos
    list_qos_values = [0, 1, 2, 3, 4]
    list_qos_code = ["Legacy", "BK (Background)", "BE (Best Effort)", "VI (Video)", "VO (Voice)"]
    qos_value = list_qos_values[list_qos_code.index(qos_code)]
    param_dictionary["qos"]= qos_value

    #vérifier si le bouton pushButton_rts est coché
    if self.pushButton_rts.isChecked():
        rts_code = "ON"
    else:
        rts_code = "OFF"
    list_rts_values = [0, 1]
    list_rts_code = ["OFF", "ON"]
    rts_value = list_rts_values[list_rts_code.index(rts_code)]  # affecte la valeur de rts
    param_dictionary["rts"]= rts_value

    #récuperer le encryption mode de la comboBox_encryption_protocol
    encryption_code = self.comboBox_enc_protocol.currentText()  # récupère le texte de la  encryption    
    list_encryption_values = [0, 1, 2, 3]  # encryption mode: 0 = none, 1 = wep, 2 = wpa, 3 = wpa2
    list_encryption_codes = ["none", "WEP", "WPA", "WPA2"]
    encryption_value = list_encryption_values[list_encryption_codes.index(encryption_code)]
    param_dictionary["encryption"]= encryption_value
    
  
    # récupération de la valeur de tcp_efficiency_code
    if self.lineEdit_tcp_eff.text() != "":
        tcp_efficiency_value = int(self.lineEdit_tcp_eff.text())
    else:
        tcp_efficiency_value = 0         
    param_dictionary["tcp_efficiency"]= tcp_efficiency_value

    # récupération de la valeur de agg_mpdu
    agg_mpdu_code = self.comboBox_mpdu.currentText()  # récupère le texte de la case agg_mpdu
    list_agg_mpdu_values = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    list_agg_mpdu_codes = ["1", "2", "4", "8", "16", "32", "64", "128", "256", "512", "1024"]
    agg_mpdu_value = list_agg_mpdu_values[list_agg_mpdu_codes.index(agg_mpdu_code)]
    param_dictionary["AggMPDU"]= agg_mpdu_value

    # récupération de la valeur de mpdu_nb
    if self.lineEdit_MPDU.text() != "":
        mpdu_nb_value = int(self.lineEdit_MPDU.text())
    else:
        mpdu_nb_value = 20 
    param_dictionary["mpdu_nb"]= mpdu_nb_value

    #récuperation de la valeur de agg_msdu
    agg_msdu_code = self.comboBox_msdu.currentText()  # récupère le texte de la case agg_msdu
    list_agg_msdu_values = [1, 2, 3, 4, 5, 6, 7]
    list_agg_msdu_codes = ["1", "2", "3", "4", "5", "6", "7"]
    agg_msdu_value = list_agg_msdu_values[list_agg_msdu_codes.index(agg_msdu_code)]
    param_dictionary["AggMSDU"]= agg_msdu_value

    #si le lineEdit_msdu n'est pas vide, récupérer la valeur
    if self.lineEdit_msdu.text() != "":
        msdu_length_value = int(self.lineEdit_msdu.text())
    else:
        msdu_length_value = 0
    param_dictionary["msdu_length"]= msdu_length_value

    # récupération de la valeur de MSDU_nb
    if self.lineEdit_msdu_nb.text() != "":
        msdu_nb_value = int(self.lineEdit_msdu_nb.text())
    else:
        msdu_nb_value = 2
    param_dictionary["msdu_nb"]= msdu_nb_value 

    #récupération de la valeur de msdu_limit ; 
    msdu_limit_code = self.comboBox_msdu_limit.currentText()  # récupère le texte de la case msdu_limit   
    # list_msdu_limit_values = [3889, 7925, 4095]
    # list_msdu_limit = ["3889", "7925", "4095"]
    # msdu_limit_value = list_msdu_limit_values[list_msdu_limit.index(msdu_limit_code)]  # affecte la valeur de msdu_limit_number
    msdu_limit_value = int(msdu_limit_code)
    param_dictionary["msdu_limit"]= msdu_limit_value

    #récupération de la valeur du combo box package_size
    package_size_code = self.comboBox_package_size.currentText()  # récupère le texte de la case package_size
    list_package_size_values = [1350, 1460]
    list_package_size_codes = ["1350", "1460"]
    package_size_value = list_package_size_values[list_package_size_codes.index(package_size_code)]
    param_dictionary["package_size"]= package_size_value

    return param_dictionary


def writing_validation_file(self, dict, debit ,PG_phy_tpt , MAC_throughput , mac_tpt, UDP_throughput, udp_tpt, TCP_throughput, tcp_tpt) :
    file_name = "validations.csv"

    dict["phy_throughput"] = str(debit)
    dict["PG_phy_throughput"] = str(PG_phy_tpt)
    dict["MAC_throughput"] = str(round(MAC_throughput,2))
    dict["PG_MAC_throughput"] = str(round(mac_tpt,2))
    dict["UDP_throughput"] = str(round(UDP_throughput,2))
    dict["PG_UDP_throughput"] = str(round(udp_tpt,2))
    dict["TCP_throughput"] = str(round(TCP_throughput,2))
    dict["PG_TCP_throughput"] = str(round(tcp_tpt,2))

    keys_list = []  # liste des clés
    for cle, valeur in dict.items():
        keys_list.append(cle)
        print("'"' {} '"' contient {}.".format(cle, valeur))
    
    """
    # écriture dans un fichier csv pour les validations:
    print("entrez le nom de fichier")
    name = input()
    file_name = name +".csv"
    with open(file_name, "a",newline='') as file :
        # Création de l'''écrivain'' CSV.
        writer = csv.DictWriter(file,delimiter = ';',fieldnames=keys_list)
        writer.writeheader()            
        writer.writerow(dict)
        file.close()
        #quit()
    return None

    """