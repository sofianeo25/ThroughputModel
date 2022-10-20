from core import *
from math import ceil

class WiFiag(WiFi):
    def __init__(self):
        WiFi.__init__(self)

    ############################## 802.11ag calculation functions ##############################
    def ag_phy_throughput(self, modulation):
        """ This function return the phy rate and the ndbps
            of the 802.11a standard, for a specified modulation
            modulation :    0 =< integer <= 7
            returns phy rate and ndbps
        """
        try:
            phy_rate = self.ag_code[modulation] * self.ag_sc * self.ag_symb_per_sec
            ndbps = self.ag_code[modulation] * 48
            return phy_rate, ndbps
        except IndexError:
            print(
                "a_phy_throughput function entry error ! "
                "The modulation value entered must be included between 0 and 7 !")
            print("Script is interrupted !")
            # sys.exit()

    def ag_msdu_tx_time(self, band, modulation, msdu_length, encryption):
        """ This function returns the msdu transmit time and the phy rate
                of the 802.11a standard
                band is 0 or 1 for 5000 et 2400 respectively
                modulation :    0 =< integer <= 7
                msdu_length: 1 to xxxx
                encryption mode: 0 = none, 1 = wep, 2 = wpa, 3 = wpa2
                Calls the ag_phy_throughput () function.
        """
        global signal_ext
        try:
            if modulation < 0 or modulation > 7:
                raise ValueError
            if msdu_length < 1:
                raise ValueError
            if band < 0 or band > 1:
                raise ValueError
            if encryption < 0 or encryption > 3:
                raise ValueError
            phy_thr, ndbps = self.ag_phy_throughput(modulation)
            if band == 0:
                signal_ext = 0
            elif band == 1:
                signal_ext = 6 * 10 ** (-6)
            msdu_t = self.ag_preamble_time + \
                     self.ag_plcp_header_time + 4 * 10 ** (-6) * ceil((self.l_service_bits +
                                                                       self.a_tail_bits + 8 * (
                                                                               self.mac_header_bytes
                                                                               + self.mac_tail_bytes
                                                                               + msdu_length +
                                                                               self.encryption_bytes[
                                                                                   encryption])) / ndbps) + signal_ext
            return phy_thr, msdu_t
        except IndexError:
            print("ag_msdu_tx_time function entry error ! Please check the index value of modulation or encryption")
            # sys.exit()
        except ValueError:
            print("ag_msdu_tx_time function entry error ! modulation or msdu entry error !")
            # sys.exit()

    def ag_ctrl_frame_tx_time(self, modulation, pckt_length):
        """ This function returns the control frame transmit time and the phy rate
                of the 802.11ag standard
                modulation :    0 =< integer <= 7
                pckt_length: 1 to xxxx is the control packet length
                Calls the ag_phy_throughput () function.
                No signal extension considered for this kind of packet
        """

        try:
            if modulation < 0 or modulation > 7:
                raise ValueError
            if pckt_length < 1:
                raise ValueError
            phy_thr, ndbps = self.ag_phy_throughput(modulation)
            ctrl_pckt_t = self.ag_preamble_time + self.ag_plcp_header_time + 4 * 10 ** -6 * ceil(
                (self.l_service_bits + self.a_tail_bits + 8 * (pckt_length)) / ndbps)
            return phy_thr, ctrl_pckt_t
        except IndexError:
            print("ag_ctrl_frame_tx_time function entry error ! Please check the index value of modulation or encryption")
            # sys.exit()
        except ValueError:
            print("ag_ctrl_frame_tx_time function entry error ! modulation or msdu entry error !")
            # sys.exit()

    def ag_msdu_exchange_time(self, band, data_modulation, ctrl_modulation, qos, msdu_length, rts, encryption):
        """ This function returns the msdu transmit exchange time including mac control frames exchanges
            including rts, cts, ack
            modulation :    0 =< integer <= 7
            msdu_length: 1 to xxxx
            rts/cts : 0 or 1
            qos : 0, 1, 2 or 3 for BK, BE, VI or VO respectively
            utilisation: a_msdu_exchange_time(band, data_modulation, control_modulation, qos, msdu_length, rts, encryption)
            Calls the a_msdu_tx_time() function.
        """
        # band = 0 # 5000

        try:
            if data_modulation < 0 or data_modulation > 7:
                raise ValueError
            elif ctrl_modulation < 0 or ctrl_modulation > 7:
                raise ValueError
            elif msdu_length < 1:
                raise ValueError
            elif rts < 0 or rts > 1:
                raise ValueError
            elif qos < 0 or qos > 4:
                raise ValueError
            elif encryption < 0 or encryption > 3:
                raise ValueError
            # difs time calculation time
            qos_error, difs_time, sifs_time, pifs_time, cwmin, backoff_time, retrans, txop = self.set_qos_params(band, qos)

            # Get MSDU tx time for the given configuration
            # ack
            ack_phy_thr, ack_msdu_tx_time = self.ag_ctrl_frame_tx_time(ctrl_modulation, self.ack_length_bytes)

            # data frame
            data_phy_thr, data_msdu_tx_time = self.ag_msdu_tx_time(band, data_modulation, msdu_length, encryption)

            if rts == 0:
                exchange_time = backoff_time + data_msdu_tx_time + sifs_time + ack_msdu_tx_time + difs_time
            else:
                # rts tx time
                rts_phy_thr, rts_msdu_tx_time = self.ag_ctrl_frame_tx_time(ctrl_modulation, self.rts_length_bytes)
                # cts tx time
                cts_msdu_tx_time = ack_msdu_tx_time
                exchange_time = backoff_time + rts_msdu_tx_time + 3 * sifs_time + cts_msdu_tx_time + data_msdu_tx_time + ack_msdu_tx_time + difs_time
            #print("ack tx time: ", ack_msdu_tx_time)
            #print("data tx time: ", data_msdu_tx_time)
            return exchange_time

        except ValueError:
            print("a_msdu_exchange_time function entry error: modulation, msdu, rts or qos entry error !")
            # sys.exit()

    def ag_throughput(self, tx_exchange_time, ack_tcp_time, tcp_eff, msdu_size):
        """ This function returns the throughput calculated for the following layers:
        MAC, UDP and TCP.
        tx_exchange_time is the time taken to send an MSDU, calculated by the
        ag_msdu_exchange_time function.
        tcp_eff is the TCP efficiency and describes the data segment over tcp ack segments ratio
        msdu_size is the size of the msdu.
        """
        try:
            if tx_exchange_time < 0:
                raise ValueError
            elif tcp_eff < 0:
                raise ValueError
            elif msdu_size < 0:
                raise ValueError
            elif ack_tcp_time < 0:
                raise ValueError
            mac_throughput = (8 * msdu_size / tx_exchange_time) / 10 ** 6
            udp_throughput = (8 * (
                    msdu_size - self.llc_bytes - self.snap_bytes - self.ip_header_bytes - self.udp_header_bytes) / tx_exchange_time) / 10 ** 6
            tcp_exchange_time = ack_tcp_time + tcp_eff * tx_exchange_time
            tcp_throughput = (tcp_eff * 8 * (
                    msdu_size - self.llc_bytes - self.snap_bytes - self.ip_header_bytes - self.tcp_header_bytes) / tcp_exchange_time) / 10 ** 6
            return mac_throughput, udp_throughput, tcp_throughput
        except ValueError:
            print("ag_throughput entry error: tx_exchange_time or tcp_eff entry error")
