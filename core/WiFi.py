from math import ceil

from core import *
class WiFi():
    def __init__(self):
        ########## General variables ##########
        # Security variables
        self.encryption_bytes = [0, 8, 20, 16]  # [none, wep, wpa, wpa2] in bytes
        # mac variables
        self.mac_header_bytes = 30
        self.mac_tail_bytes = 4
        self.ack_length_bytes = 14
        self.compressed_block_ack_length_bytes = 32
        self.block_ack_length_bytes=152
        self.rts_length_bytes = 20
        self.cts_length_bytes = 14
        self.l_service_bits = 16
        self.a_tail_bits = 6

        ########## 802.11ag variables definition ##########
        # 802.11a standard variables (phy level)
        self.ag_sc = 48  # sc means sub_carrier
        self.ag_code = [0.5, 0.75, 1, 1.5, 2, 3, 4, 4.5]
        self.ag_symb_per_sec = 250 * 10 ** 3

        self.ag_preamble_time = 16 * 10 ** (-6)
        self.ag_plcp_header_time = 4 * 10 ** (-6)

        # 802.11a standard variables (mac level)
        self.rifs_time_50 = 2 * 10 ** (-6)
        self.slot_time_50 = [9 * 10 ** (-6), 9 * 10 ** (-6)]
        self.sifs_time_50 = 16 * 10 ** (-6)
        self.extension_time_50 = 0

        ########## 802.11g variables definition ##########
        # 802.11g standard variables
        self.rifs_time_24 = 2 * 10 ** (-6)
        self.slot_time_24 = [9 * 10 ** -6, 20 * 10 ** (-6)]
        self.sifs_time_24 = 10 * 10 ** (-6)
        self.extension_time_24 = 6 * 10 ** (-6)

        self.g_sc = 48  # sc means sub_carrier
        self.g_code = [0.5, 0.75, 1, 1.5, 2, 3, 4, 4.5]
        self.g_symb_per_sec = 250 * 10 ** 3

        # 802.11n/ac standard variables
        self.n_sc = [52, 108, 234, 468]
        self.n_code = [0.5, 1, 1.5, 2, 3, 4, 4.5, 5, 6, 8 * 5 / 6]
        self.n_symb_per_sec = [(1 / (4 * 10 ** -6)), (1 / (3.6 * 10 ** (-6)))]
        self.n_nb_ss = [1, 2, 3, 4]
        self.n_ac_mac_header_bytes = 36

        self.l_stf_time = 8*10**-6
        self.l_ltf_time = 8*10**-6
        self.l_sig_time = 4*10**-6
        self.ht_sig_1_time = 4*10**-6
        self.ht_sig_2_time = 4*10**-6
        self.ht_ltf_time = 4*10**-6
        self.ht_stf_time = 4*10**-6
        # mode greenfield
        self.gf_ht_stf_time = 8*10**-6
        self.ht_ltf1_time = 8*10**-6
        self.tsym_1 = 4*10**-6
        self.tsym_2 = 3.6*10**-6
        ############## Variables related to a_mpdu ###################
        self.mpdu_delimiter_bytes = 4
        self.n_mpdu_max_aggregate = 64
        self.n_max_msdu_length_in_ampdu_bytes = 4095 # for msdu or amsdu
        self.n_max_msdu_length_in_amsdu_bytes = 2304
        self.n_max_msdu_length_bytes = 7955 # length if no ampdu agg is used.
        
        ############### Vairables related to a_msdu ##################
        self.n_msdu_hdr_bytes = 14
        self.n_msdu_max_length_without_amsdu = 7955
        self.n_amsdu_max_bytes_1 = 3889
        self.n_amsdu_max_bytes_2 = 7935 # if ampdu cannot exceed 4095
        self.n_amsdu_max_bytes_3 = 4095
        ################ PSDU limit ################
        self.n_max_psdu_bytes = 65535
        ########## LLC / SNAP ##########
        self.llc_bytes = 3
        self.snap_bytes = 5

        ########## IP ##########
        self.ip_header_bytes = 20
        self.ip_header_with_option_bytes = 24

        ########## udp ##########
        self.udp_header_bytes = 8

        ########## TCP ##########
        self.tcp_header_bytes = 20
        self.tcp_ack_pckt_bytes = 20
        self.tcp_ack_pckt_bytes_msdu = self.tcp_ack_pckt_bytes + self.llc_bytes + self.snap_bytes + self.ip_header_bytes

    def set_qos_params(self, band, qos_value):
        """ This function return the values for the following parameteres:
            difs
            cwmin
            backoff_time
            The qos value must be 0, 1, 2, 3 or 4 for Legacy, BK, BE, VI or VO respectively
            The band value must be 0 or 1 for 5000 and 2400 respectively.
            If the qos value is out of range the default qos is Legacy with values of 5000
            If band is out of range the default qos is Legacy with values of 5000
            If qos value or band is out of range, the qos_error flag = 1
            If qos value or band is correct, their is no error and qos_error flag = 0
            Can be used for testing
        """
        try:
            if qos_value < 0 or qos_value > 4:
                raise ValueError
            if band < 0 or band > 1:
                raise ValueError
            if band == 0:
                sifs_time = self.sifs_time_50
                slot_time = self.slot_time_50[0]
                pifs_time = sifs_time + slot_time
            else:
                sifs_time = self.sifs_time_24
                slot_time = self.slot_time_24[0]
                pifs_time = sifs_time + slot_time

            if qos_value == 0:  # Legacy
                cwmin = 15
                aifsn = 2
                difs_time = sifs_time + aifsn * slot_time
                backoff_time = (cwmin / 2) * slot_time
                retrans = 6
                qos_error = 0
                txop_limit = 8106 * 10 ** -6
            elif qos_value == 1:  # BK
                cwmin = 15
                aifsn = 7
                difs_time = sifs_time + aifsn * slot_time
                backoff_time = (cwmin / 2) * slot_time
                retrans = 6
                qos_error = 0
                txop_limit = 8106 * 10 ** -6
            elif qos_value == 2:  # BE
                cwmin = 15
                aifsn = 3
                difs_time = sifs_time + aifsn * slot_time
                backoff_time = (cwmin / 2) * slot_time
                retrans = 6
                qos_error = 0
                txop_limit = 8106 * 10 ** -6
            elif qos_value == 3:  # Vi
                cwmin = 7
                aifsn = 2
                difs_time = sifs_time + aifsn * slot_time
                backoff_time = (cwmin / 2) * slot_time
                retrans = 1
                qos_error = 0
                txop_limit = 4600 * 10 ** -6
            elif qos_value == 4:  # Vo
                cwmin = 3
                aifsn = 2
                difs_time = sifs_time + aifsn * slot_time
                backoff_time = (cwmin / 2) * slot_time
                retrans = 1
                qos_error = 0
                txop_limit = 2080 * 10 ** -6
            return qos_error, difs_time, sifs_time, pifs_time, cwmin, backoff_time, retrans, txop_limit

        except ValueError:
            print("define_qos function entry error ! Invalid parameters !")
            print("the considered qos configuration is legacy for 5 GHz.")
            difs_time = self.sifs_time_50 + 2 * self.slot_time_50[0]
            cwmin = 15
            backoff_time = cwmin * self.slot_time_50[0] / 2
            retrans = 6
            qos_error = 1
            return qos_error, difs_time, cwmin, backoff_time, retrans
