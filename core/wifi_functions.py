""" This file defines the basic functions used to calculate the phy throughput for a particular configuration
for the standards 802.11 a/g/n
"""

from wifi_variables import *
import sys
from math import ceil


def set_qos_params(band, qos_value) :
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
        if qos_value < 0 or qos_value > 4 :
            raise ValueError
        if band < 0 or band > 1 :
            raise ValueError
        if band == 0 :
            sifs_time = sifs_time_50
            slot_time = slot_time_50[0]
            pifs_time = sifs_time + slot_time
        else :
            sifs_time = sifs_time_24
            slot_time = slot_time_24[0]
            pifs_time = sifs_time + slot_time

        if qos_value == 0 : # Legacy
            cwmin = 15
            aifsn = 2
            difs_time = sifs_time + aifsn * slot_time
            backoff_time = (cwmin / 2) * slot_time
            retrans = 6
            qos_error = 0
            txop_limit = 8106*10**-6
        elif qos_value == 1 : # BK
            cwmin = 15
            aifsn = 7
            difs_time = sifs_time + aifsn * slot_time
            backoff_time = (cwmin / 2) * slot_time
            retrans = 6
            qos_error = 0
            #txop = 2.528*10^-3
            txop_limit = 8106*10**-6
        elif qos_value == 2 : #BE
            cwmin = 15
            aifsn = 3
            difs_time = sifs_time + aifsn * slot_time
            backoff_time = (cwmin / 2) * slot_time
            retrans = 6
            qos_error = 0
            #txop = 2.528 * 10 ^ -3
            txop_limit = 8106*10**-6
        elif qos_value == 3 : # Vi
            cwmin = 7
            aifsn = 2
            difs_time = sifs_time + aifsn * slot_time
            backoff_time = (cwmin / 2) * slot_time
            retrans = 1
            qos_error = 0
            #txop = 4.096 * 10 ^ -3
            txop_limit = 4600 * 10**-6
        elif qos_value == 4 : # Vo
            cwmin = 3
            aifsn = 2
            difs_time = sifs_time + aifsn * slot_time
            backoff_time = (cwmin / 2) * slot_time
            retrans = 1
            qos_error = 0
            txop_limit = 2080 * 10**-6
        return qos_error, difs_time, sifs_time, pifs_time, cwmin, backoff_time, retrans, txop_limit

    except ValueError :
        print("define_qos function entry error ! Invalid parameters !")
        print("the considered qos configuration is legacy for 5 GHz.")
        difs_time = sifs_time_50 + 2*slot_time_50[0]
        cwmin = 15
        backoff_time = cwmin*slot_time_50[0]/2
        retrans = 6
        qos_error = 1
        return qos_error, difs_time, cwmin, backoff_time, retrans

############################## 802.11ag calculation functions ##############################

def ag_phy_throughput(modulation) :
    """ This function return the phy rate and the ndbps
        of the 802.11a standard, for a specified modulation
        modulation :    0 =< integer <= 7
        returns phy rate and ndbps
    """
    try:
        phy_rate = ag_code[modulation]*ag_sc*ag_symb_per_sec
        ndbps = ag_code[modulation]*48
        return phy_rate, ndbps
    except IndexError:
        print("a_phy_throughput function entry error ! The modulation value entered must be included between 0 and 7 !")
        print("Script is interrupted !")
        #sys.exit()



def ag_msdu_tx_time (band, modulation, msdu_length, encryption) :
    """ This function returns the msdu transmit time and the phy rate
            of the 802.11a standard
            band is 0 or 1 for 5000 et 2400 respectively
            modulation :    0 =< integer <= 7
            msdu_length: 1 to xxxx
            encryption mode: 0 = none, 1 = wep, 2 = wpa, 3 = wpa2
            Calls the ag_phy_throughput () function.
    """

    try:
        if modulation < 0 or modulation > 7 :
            raise ValueError
        if msdu_length < 1 :
            raise ValueError
        if band < 0 or band > 1 :
            raise ValueError
        if encryption < 0 or encryption > 3 :
            raise ValueError
        phy_thr, ndbps = ag_phy_throughput (modulation)
        if band == 0:
            signal_ext = 0
        elif band == 1:
            signal_ext = 6*10**-6 #6*10**-6
        msdu_t = ag_preamble_time + ag_plcp_header_time + 4*10**-6*ceil((l_service_bits + a_tail_bits + 8*(mac_header_bytes + mac_tail_bytes + msdu_length + encryption_bytes[encryption]))/ndbps)+signal_ext
        return phy_thr, msdu_t
    except IndexError:
        print("ag_msdu_tx_time function entry error ! Please check the index value of modulation or encryption")
        # sys.exit()
    except ValueError:
        print("ag_msdu_tx_time function entry error ! modulation or msdu entry error !")
        # sys.exit()

def ag_ctrl_frame_tx_time (modulation, pckt_length):
    """ This function returns the control frame transmit time and the phy rate
            of the 802.11ag standard
            modulation :    0 =< integer <= 7
            pckt_length: 1 to xxxx is the control packet length
            Calls the ag_phy_throughput () function.
            No signal extension considered for this kind of packet
    """

    try:
        if modulation < 0 or modulation > 7 :
            raise ValueError
        if pckt_length < 1:
            raise ValueError
        phy_thr, ndbps = ag_phy_throughput (modulation)
        ctrl_pckt_t = ag_preamble_time + ag_plcp_header_time + 4*10**-6*ceil((l_service_bits + a_tail_bits + 8*(pckt_length))/ndbps)
        return phy_thr, ctrl_pckt_t
    except IndexError:
        print("ag_ctrl_frame_tx_time function entry error ! Please check the index value of modulation or encryption")
        # sys.exit()
    except ValueError:
        print("ag_ctrl_frame_tx_time function entry error ! modulation or msdu entry error !")
        # sys.exit()


def ag_msdu_exchange_time(band, data_modulation, ctrl_modulation, qos, msdu_length, rts, encryption):
    """ This function returns the msdu transmit exchange time including mac control frames exchanges
        including rts, cts, ack
        modulation :    0 =< integer <= 7
        msdu_length: 1 to xxxx
        rts/cts : 0 or 1
        qos : 0, 1, 2 or 3 for BK, BE, VI or VO respectively
        utilisation: a_msdu_exchange_time(band, data_modulation, control_modulation, qos, msdu_length, rts, encryption)
        Calls the a_msdu_tx_time() function.
    """
    #band = 0 # 5000

    try:
        if data_modulation < 0 or data_modulation > 7 :
            raise ValueError
        elif ctrl_modulation < 0 or ctrl_modulation > 7 :
            raise ValueError
        elif msdu_length < 1 :
            raise ValueError
        elif rts < 0 or rts > 1 :
            raise ValueError
        elif qos < 0 or qos > 4 :
            raise ValueError
        elif encryption < 0 or encryption > 3 :
            raise ValueError
        # difs time calculation time
        qos_error, difs_time, sifs_time, pifs_time, cwmin, backoff_time, retrans, txop = set_qos_params(band, qos)

        # Get MSDU tx time for the given configuration
        # ack
        ack_phy_thr, ack_msdu_tx_time = ag_ctrl_frame_tx_time (ctrl_modulation, ack_length_bytes)

        # data frame
        data_phy_thr, data_msdu_tx_time =  ag_msdu_tx_time (band, data_modulation, msdu_length, encryption)

        if rts == 0 :
            exchange_time = backoff_time + data_msdu_tx_time + sifs_time + ack_msdu_tx_time + difs_time
        else :
            # rts tx time
            rts_phy_thr, rts_msdu_tx_time = ag_ctrl_frame_tx_time(ctrl_modulation, rts_length_bytes)
            # cts tx time
            cts_msdu_tx_time = ack_msdu_tx_time
            exchange_time = backoff_time + rts_msdu_tx_time + 3*sifs_time + cts_msdu_tx_time + data_msdu_tx_time + ack_msdu_tx_time + difs_time
        print("ack tx time: ", ack_msdu_tx_time)
        print("data tx time: ", data_msdu_tx_time)
        return exchange_time

    except ValueError:
        print("a_msdu_exchange_time function entry error: modulation, msdu, rts or qos entry error !")
        #sys.exit()



def ag_throughput(tx_exchange_time, ack_tcp_time, tcp_eff, msdu_size) :
    """ This function returns the throughput calculated for the following layers:
    MAC, UDP and TCP.
    tx_exchange_time is the time taken to send an MSDU, calculated by the
    ag_msdu_exchange_time function.
    tcp_eff is the TCP efficiency and describes the data segment over tcp ack segments ratio
    msdu_size is the size of the msdu.
    """
    try:
        if tx_exchange_time < 0 :
            raise ValueError
        elif tcp_eff < 0 :
            raise ValueError
        elif msdu_size < 0 :
            raise ValueError
        elif ack_tcp_time < 0 :
            raise ValueError
        mac_throughput = (8*msdu_size/tx_exchange_time)/10**6
        udp_throughput = (8*(msdu_size - llc_bytes - snap_bytes- ip_header_bytes - udp_header_bytes)/tx_exchange_time)/10**6
        tcp_exchange_time = ack_tcp_time + tcp_eff*tx_exchange_time
        tcp_throughput = (tcp_eff*8*(msdu_size- llc_bytes - snap_bytes- ip_header_bytes - tcp_header_bytes)/tcp_exchange_time)/10**6
        return mac_throughput, udp_throughput, tcp_throughput
    except ValueError :
        print("ag_throughput entry error: tx_exchange_time or tcp_eff entry error")



###########################################################################################
############################## 802.11n calculation functions ##############################
###########################################################################################

def n_phy_throughput (modulation, n_sc_value, nb_ss, sgi) :
    """ This function aims to calculate de phy rate
    of the 802.11n standard
    modulation :    0 =< integer <= 7
    nb_ss :         1 =< integer <= 4
    n_sc :          is 0 or 1 (Defines the number of subcarriers
                    and, hence, the bandwidth: 0 = 20, 1 = 40 MHz
    sgi :           is 0 or 1
    """
    try:
        # if modulation <0 or modulation > 7 :
        #     raise ValueError("MCS")
        if nb_ss < 1 or nb_ss > 4 :
            raise ValueError("SpatialStreamError")
        if sgi < 0 or sgi > 1 :
            raise ValueError("SGIError")
        if n_sc_value != 0 and n_sc_value != 1 :
            raise ValueError("SubCarrierError")
        n_phy_rate = n_code[modulation] * nb_ss * n_sc[n_sc_value] * n_symb_per_sec[sgi]
        n_ndbps = n_code[modulation] * nb_ss * n_sc[n_sc_value]
        if n_phy_rate > 300000000:
            nes = 2
        else:
            nes = 1
        return n_phy_rate, n_ndbps, nes
    except IndexError :
        print("The modulation value must be included between 0 et 7 !")
    except ValueError :
        print("n_phy_throughput entry error !")



def n_amsdu_config_check (msdu_length_bytes, msdu_nb, amsdu_length_limit_bytes):
    """# Test of the MSDU length with regard to the configuration
        # We consider in this case that the amsdu_length_limit_bytes is correctly entered with regard to the mpdu_nb,
        # which is not analysed in this function
        # amsdu analysis: it must be padded if it is not a 32 bits word boundary
        # msdu_length_bytes is the msdu length in bytes
        # msdu_nb is the msdu number demanded for a a-msdu
        # amsdu_length_limit_bytes is the max length:
        # 3889 or 7935 according to capabilities of the station and if no a-mpdu is used
        # 3889 or 4095 according to capabilities of the station and if a-mpdu is used
        # The function returns:
        # error_msdu = 1 if the size of the msdu has been modified, 0 if no entry error is destected
        # error_msdu_nb = 1 if the number of msdu in amsdu has been modified, 0 if no error is detected
        # msdu value is modified only if an error occurs. The padding is not considered in the msdu value returned.
        # To take padding into consideration in the throughput calculation you must add it to the msdu value.
        # msdu_nb possible to place in the a-msdu (if the demanded number is too high, it is reduced)
        # amsdu_length_bytes: The length of the a-msdu
        # The amsdu contains the payload + headers + padding bytes
        # It has to be considered to calculate the mpdu tx time.
        # msdu_padding_bytes: the number of padding bytes for each msdu
        # all = 0 means msdu too high or msdu number entered lower than 1 (see message returned)
    """


    if msdu_nb >= 1:
        error_msdu = 0
        error_msdu_nb = 0
        if msdu_nb == 1:
            # If no msdu aggregation, the msdu must not exceed 7955 bytes
            # When no a-msdu used, there is no padding
            if msdu_length_bytes > n_msdu_max_length_without_amsdu:
                msdu_length_bytes = n_msdu_max_length_without_amsdu
                error_msdu = 1
            amsdu_length_bytes = msdu_length_bytes
            msdu_padding_bytes = 0
        else:
            org_msdu_length_bytes = msdu_length_bytes  # used in case a-msdu cannot be used because a-msdu it too long
            #  If msdu aggregation, the msdu must not exceed 2034 bytes
            if msdu_length_bytes > n_max_msdu_length_in_amsdu_bytes:
                msdu_length_bytes = n_max_msdu_length_in_amsdu_bytes
                error_msdu = 1
                print("Beware, the MSDU is greater the 2304. It will be truncated to 2304 !")
            # an msdu_block is one msdu + msdu_hdr + padding
            #Test of faster method
            msdu_block_bytes = ceil((n_msdu_hdr_bytes + msdu_length_bytes) / 4) * 4
            msdu_padding_bytes = msdu_block_bytes - (n_msdu_hdr_bytes + msdu_length_bytes)
            # The amsdu contains the payload + headers + padding bytes
            # It has to be considered to calculate the mpdu tx time.
            amsdu_length_bytes = msdu_nb * msdu_block_bytes
            excess = amsdu_length_bytes - amsdu_length_limit_bytes
            if excess > 0:
                # We remove enough msdu_blocks to match with the a_msdu_limit_bytes
                # a_msdu is hence modified
                # if the msdu is too high (greater than amsdu_length_limit_bytes), the returned msdu_nb is = 0
                msdu_nb = msdu_nb - ceil(excess / msdu_block_bytes)
                amsdu_length_bytes = msdu_nb * msdu_block_bytes
                # the condition bellow is not used any more ... due to truncature at 2304
                error_msdu_nb = 1
                if msdu_nb == 0:
                    msdu_padding_bytes = 0
                    print("msdu length is too high !")
                    error_msdu_nb = 1
                    msdu_lenth_bytes = 0
                # If only one msdu can be transmitted due a too high msdu length, we consider the msdu without padding as
                # if it was a trans without amsdu.
                if msdu_nb == 1:
                    # In this case we are back to the case for which there is no agg msdu
                    # If no msdu aggregation, the msdu must not exceed 7955 bytes
                    # When no a-msdu used, there is no padding
                    # msdu_length_bytes = n_msdu_max_length_without_amsdu if msdu_length_bytes > n_msdu_max_length_without_amsdu else msdu_length_bytes
                    error_msdu = 0
                    msdu_length_bytes = org_msdu_length_bytes
                    if msdu_length_bytes > n_msdu_max_length_without_amsdu:
                        msdu_length_bytes = n_msdu_max_length_without_amsdu
                        error_msdu = 1
                    amsdu_length_bytes = msdu_length_bytes
                    msdu_padding_bytes = 0
                    error_msdu_nb = 1
    else:
        print("msdu number must be higher than > 0 !")
        error_msdu = 1
        error_msdu_nb = 1
        msdu_nb = 0
        msdu_length_bytes = 0
        amsdu_length_bytes = 0
        msdu_padding_bytes = 0
    return error_msdu, error_msdu_nb, msdu_nb, msdu_length_bytes, amsdu_length_bytes, msdu_padding_bytes





def n_ampdu_config_check(mpdu_nb, msdu_nb, msdu_length_bytes, amsdu_length_limit_bytes, encryption_bytes):
    """This function is used to check if the A-MPDU configuration is correct
    It accepts three arguments:
    - mpdu_nb: The number of MPDU in the A-MPDU aggregation
    - msdu: 0 if no A-MSDU, 1 if A-MSDU
    - msdu_length: length of the MSDU. Must not exceed 4095 bytes if no A-MPDU is used,
      7935 bytes if A-MSDU ios used (this is tested in the amsdu_config_check function.
      For 802.11n .........
    - psdu max length is 65535
    Contrary to the previous function n_ampdu_config_check the test of the amsdu nb in not done,amsdu_length_limit_bytes
    this test is left to the n_amsdu_config_check
      """
    error_mpdu = 0
    error_mpdu_nb = 0
    error_msdu = 0
    error_msdu_nb = 0
    error_max_amsdu_nb = 0
    amsdu_length_bytes = 0
    mpdu_padding_bytes = 0
    msdu_padding_bytes = 0
    if mpdu_nb == 1: # No mpdu aggregation
        # The test of the msdu_length byte is done in the n_amsdu_config_check function
        #msdu_length_bytes = n_max_msdu_length_in_amsdu_bytes if msdu_length_bytes > n_max_msdu_length_in_amsdu_bytes else msdu_length_bytes
        error_msdu, error_msdu_nb, msdu_nb, msdu_length_bytes, amsdu_length_bytes, msdu_padding_bytes = n_amsdu_config_check(msdu_length_bytes, msdu_nb, amsdu_length_limit_bytes)
        mpdu_length_bytes = n_ac_mac_header_bytes + msdu_length_bytes + mac_tail_bytes + encryption_bytes
    else:
        #mpdu_nb = n_mpdu_max_aggregate if mpdu_nb > n_mpdu_max_aggregate else mpdu_nb
        if mpdu_nb > n_mpdu_max_aggregate:
            mpdu_nb = n_mpdu_max_aggregate
            error_mpdu_nb = 1
        # For information
        # n_max_msdu_length_in_ampdu_bytes = 4095
        # n_amsdu_max_bytes_1 = 3839
        # n_amsdu_max_bytes_2 = 7935

        # In the case of the mpdu aggregation, the maximum MSDU or a-MSDU length is 4095
        # If A-MSDU is used, we must calibrate the A-MSDU to make sure it does not exceed 4095 ( n_max_msdu_length_in_ampdu_bytes)

        # In this case the MSDU max size in the A-MSDU is n_max_msdu_length_in_amsdu_bytes = 2304
        # And the A-MSDU must not exceed 4095 which is the mas limit of the MPDU payload.

        # We limit the MSDU size to n_max_msdu_length_in_amsdu_bytes = 2304
        #msdu_length_bytes = n_max_msdu_length_in_amsdu_bytes if msdu_length_bytes > n_max_msdu_length_in_amsdu_bytes else msdu_length_bytes

        # We call the n_amsdu_config_check function to check if the number of MSDU in A-MSDU demanded is conform to the standard.
        # If not we reduce the number of MSDU in the A-MSDU.
        # If a-mpdu, the maximum length of the msdu / a-msdu is 4095 (n_max_msdu_length_in_ampdu_bytes)
        if amsdu_length_limit_bytes > n_max_msdu_length_in_ampdu_bytes:
            amsdu_length_limit_bytes = n_max_msdu_length_in_ampdu_bytes
            error_max_amsdu_nb = 1

        error_msdu, error_msdu_nb, msdu_nb, msdu_length_bytes, amsdu_length_bytes, msdu_padding_bytes = n_amsdu_config_check(msdu_length_bytes, msdu_nb, amsdu_length_limit_bytes)
        #mpdu_padding_bytes = 4 - ((mpdu_delimiter_bytes + n_ac_mac_header_bytes + msdu_length_bytes + mac_tail_bytes + encryption_bytes) % 4) if ((mpdu_delimiter_bytes + n_ac_mac_header_bytes + msdu_length_bytes + mac_tail_bytes + encryption_bytes) % 4) != 0 else 0
        #mpdu_block_bytes = mpdu_delimiter_bytes + n_ac_mac_header_bytes + amsdu_length_bytes + mac_tail_bytes + encryption_bytes + mpdu_padding_bytes
        mpdu_block_bytes = ceil((mpdu_delimiter_bytes + n_ac_mac_header_bytes + amsdu_length_bytes + mac_tail_bytes + encryption_bytes) / 4) * 4
        mpdu_padding_byte = mpdu_block_bytes - (mpdu_delimiter_bytes + n_ac_mac_header_bytes + msdu_length_bytes + mac_tail_bytes + encryption_bytes)
        max_mpdu_blocks_nb = int(n_max_psdu_bytes / mpdu_block_bytes)
        mpdu_nb = max_mpdu_blocks_nb if mpdu_nb > max_mpdu_blocks_nb else mpdu_nb
        if mpdu_nb > max_mpdu_blocks_nb:
            mpdu_nb = max_mpdu_blocks_nb
            error_mpdu_nb = 1
        ampdu_length_bytes = mpdu_nb * mpdu_block_bytes

        mpdu_length_bytes = ampdu_length_bytes

    return error_mpdu, error_mpdu_nb, error_msdu, error_msdu_nb, error_max_amsdu_nb, msdu_nb, mpdu_nb, msdu_length_bytes, amsdu_length_bytes, mpdu_length_bytes, msdu_padding_bytes, mpdu_padding_bytes

def n_ctrl_frame_tx_time (plcp_header_mode, n_plcp_header_time, sgi, modulation, pckt_length):
    """ This function returns the control frame transmit time and the phy rate
            of the 802.11n standard
            modulation :    0 =< integer <= 7
            pckt_length: 1 to xxxx is the control packet length
            Calls the ag_phy_throughput () function.
            No signal extension considered for this kind of packet
            Greenfield can take three values: 0 for lagacy premable, 1 for mixed mode and 2 for greenfield mode
    """

    try:
        if modulation < 0 or modulation > 7 :
            raise ValueError
        if pckt_length < 1:
            raise ValueError
        phy_thr, ndbps = ag_phy_throughput (modulation)

        if plcp_header_mode == 0:
            plcp_header_time = ag_preamble_time + ag_plcp_header_time
        elif plcp_header_mode == 1:
            plcp_header_time = n_plcp_header_time
        else:
            plcp_header_time = ag_preamble_time + ag_plcp_header_time
        #elif greenfield == 2:
        #    n_plcp_header_time = gf_ht_stf_time + ht_ltf1_time + ht_sig_1_time + ht_sig_2_time + ht_ltf_time
        tsym = tsym_1
        tsyms = tsym_1 if sgi == 0 else tsym_2
        # Padding at symbole evel and at sgi level.
        ctrl_pckt_t = plcp_header_time + tsym * ceil((tsym / tsyms) * ceil((l_service_bits + a_tail_bits + 8 * (pckt_length)) / ndbps))
        return phy_thr, ctrl_pckt_t
    except IndexError:
        print("ag_ctrl_frame_tx_time function entry error ! Please check the index value of modulation or encryption")
        # sys.exit()
    except ValueError:
        print("ag_ctrl_frame_tx_time function entry error ! modulation or msdu entry error !")
        # sys.exit()


def n_msdu_tx_time (band, bw, modulation, nb_ss, sgi, ldpc, stbc, greenfield, control_modulation,
                    msdu_length_bytes, msdu_nb, amsdu_limit_bytes, mpdu_nb, encryption):
    """ Comment to be updated
            This function returns the msdu transmit time and the phy rate
            of the 802.11n standard
            band is 0 or 1 for 5000 et 2400 respectively
            bw is the bandwidth considered: 0 or 1 for 20 and 40 MHz respectively
            modulation :    0 =< integer <= 7
            nb_ss: number of spatial streams
            sgi: 0 or 1 (0=sgi off, 1=sgi on)
            ldpc: 0 or 1
            stbc: 0 or 1
            msdu_length: 1 to xxxx: depends on the txop
            msdu_nb: indicate the number of aggregate msdu in an a-msdu
            msdu_limit_nb_bytes: Maximum limit of bytes in a amsdu
            mpdu_nb: indicate the number of aggregate mpdu in an a-mpdu
            mpdu_limit_nb_bytes: Maximum limit of bytes in a amsdu
            The standard defines two possible value: 3839 or 7935, depending on the client station capabilities
            greenfield: 0 or 1 according to the option setting
            encryption mode: 0 = none, 1 = wep, 2 = wpa, 3 = wpa2
            Calls the ag_phy_throughput () function.
    """
    try:
        if band < 0 or band > 1:
            raise ValueError
        if bw < 0 or bw > 1:
            raise ValueError
        if modulation < 0 or modulation > 7:
            raise ValueError
        if nb_ss < 0 or nb_ss > 4:
            raise ValueError
        if sgi < 0 or sgi > 1:
            raise ValueError
        if ldpc < 0 or ldpc > 1:
            raise ValueError
        if stbc < 0 or stbc > 1:
            raise ValueError
        if greenfield < 0 or greenfield > 1:
            raise ValueError
        if control_modulation < 0 or control_modulation > 7:
            raise ValueError
        if msdu_length_bytes < 1:
            raise ValueError
        if encryption < 0 or encryption > 3:
            raise ValueError

        # Phy rate, ndbps and nes computation
        #phy_rate, ndbps, nes = n_phy_throughput (modulation)
        n_sc_value = bw
        n_phy_rate, n_ndbps, nes = n_phy_throughput(modulation, n_sc_value, nb_ss, sgi)

        if band == 0:
            signal_ext = 6*10**-6 #6*10**-6
        elif band == 1:
            signal_ext = 0

        # if stbc = 0 then mstbc = 1
        # if stbc = 1 then mstbc = 2
        mstbc = stbc + 1

        # PLCP header building: depends on the following parameters
        # - HT GF or HT MF
        # - Number of spatial Stream(s)
        # plcp header time computation
        if nb_ss == 3:
            total_ht_ltf_time = 4 * ht_ltf_time
        else:
            total_ht_ltf_time = nb_ss * ht_ltf_time

        if greenfield == 0:
            n_plcp_header_time = l_stf_time + l_ltf_time + l_sig_time + ht_sig_1_time + ht_sig_2_time + ht_stf_time + total_ht_ltf_time
        else:
            n_plcp_header_time = gf_ht_stf_time + ht_ltf1_time + ht_sig_1_time + ht_sig_2_time + total_ht_ltf_time

        tsym = tsym_1
        tsyms = tsym_1 if sgi == 0 else tsym_2

        # Ancienne version avant modif du traitement de l'encrypt au niveau mpdu
        #error_mpdu, msdu_nb, mpdu_nb, msdu_length_bytes, amsdu_length_bytes, mpdu_length_bytes, msdu_padding_bytes, mpdu_padding_bytes = n_ampdu_config_check(
        #    mpdu_nb, msdu_nb, msdu_length_bytes, amsdu_limit_bytes)
        error_mpdu, error_mpdu_nb, error_msdu, error_msdu_nb,  error_max_amsdu_nb, msdu_nb, mpdu_nb, msdu_length_bytes, amsdu_length_bytes, mpdu_length_bytes, msdu_padding_bytes, mpdu_padding_bytes = n_ampdu_config_check(
            mpdu_nb, msdu_nb, msdu_length_bytes, amsdu_limit_bytes, encryption_bytes[encryption])
        errors = [error_mpdu, error_mpdu_nb, error_msdu, error_msdu_nb,  error_max_amsdu_nb]
        msdu_t = 0

        # Ancienne version avant modif du traitement de l'encrypt au niveau mpdu
        #symbols_nb = mstbc * ceil((8 * (mpdu_length_bytes + encryption_bytes[encryption] + 16 + 6 * nes)) / (mstbc * n_ndbps))
        symbols_nb = mstbc * ceil((8 * (mpdu_length_bytes) + 16 + 6 * nes) / (mstbc * n_ndbps))
        mpdu_tx_time = n_plcp_header_time + tsym * ceil(symbols_nb * tsyms / tsym)
        return errors, mpdu_nb, msdu_nb, n_plcp_header_time, n_phy_rate,  mpdu_tx_time
    except IndexError:
        print("ag_msdu_tx_time function entry error ! Please check the index value of modulation or encryption")
        # sys.exit()
    except ValueError:
        print("ag_msdu_tx_time function entry error ! modulation or msdu entry error !")
        # sys.exit()



def n_msdu_exchange_time (band, bw, modulation, nb_ss, sgi, ldpc, stbc, greenfield, control_preamble, control_modulation, QoS, txop,
                    msdu_length_bytes, msdu_nb, msdu_limit_nb_bytes, mpdu_nb,  rts, encryption, tcp_efficiency):
    """ This function returns the msdu transmit time and the phy rate
            of the 802.11n standard
            band is 0 or 1 for 5000 et 2400 respectively
            bw is the bandwidth considered: 0 or 1 for 20 and 40 MHz respectively
            modulation :    0 =< integer <= 7
            nb_ss: number of spatial streams
            sgi: 0 or 1 (0=sgi off, 1=sgi on)
            msdu_length: 1 to xxxx: depends on the txop
            msdu_nb: indicate the number of aggregate msdu in an a-msdu
            msdu_limit_nb_bytes: Maximum limit of bytes in a amsdu
            mpdu_nb: indicate the number of aggregate mpdu in an a-mpdu
            The standard defines two possible value: 3839 or 7935, depending on the client station capabilities
            greenfield: 0 or 1 according to the option setting
            encryption mode: 0 = none, 1 = wep, 2 = wpa, 3 = wpa2
            Calls the ag_phy_throughput () function.
            tcp_efficiency: data frame number / ack frame number: if 2 date frames for one ack frame: 2/1 = 2
    """
    ########################################## Time definition ####################################################

    # Test of the used band
    if band == 0:
        # We consider the 5000 times constants
        rifs_time = rifs_time_50
        extension_time = extension_time_50

    elif band == 1:
        # We consider the 2400 time constants
        rifs_time = rifs_time_24
        extension_time = extension_time_24
    else:
        # We consider the 5000 time constants
        rifs_time = rifs_time_50
        extension_time = extension_time_50

    qos_error, difs_time, sifs_time, pifs_time, cwmin, backoff_time, retrans, txop_limit = set_qos_params(band, QoS)

    # Is amsdu configured ?
    amsdu_configured = 1 if msdu_nb > 1 else 0

    txop_optimization = 0
    while txop_optimization == 0:

        ################################ Data frame time computation ##############################################
        errors_data, mpdu_nb, msdu_nb, plcp_hdr_time, phy_rate, msdu_tx_time = n_msdu_tx_time(band, bw, modulation, nb_ss, sgi, ldpc, stbc, greenfield, control_modulation, msdu_length_bytes, msdu_nb, msdu_limit_nb_bytes, mpdu_nb, encryption)

        ################################ TCP ack number of frame computation ######################################
        # Computed from the ampdu and amsdu point of view.
        # Depdends on the size of the msdu ack TCP which remains constant and does not depend on the data MSDU
        # Hence we must use the value of msdu_limit_nb_bytes (3889, 7925 or 4095)
        # A-MSDU = MAC hdr + n*(MSDU hdr + TCP_Ack data) + MAC FCS
        # We will have at least as many TCP ack frames as TCP data frames
        ################################ TCP ack time computation ################################################

        # We consider that if A-MSDU is demanded, the ack tcp frames must be sent with a-msdu.
        # We favour the a-msdu because the over head is lower, hence the channel capacity higher
        # The number of tcp ack segment is determined by mdu_nb * msdu_nb, whatever the the configuration:
        tcp_ack_frame_number = ceil(mpdu_nb * msdu_nb / tcp_efficiency)

        # Then we calculate the time used to send these tcp_ack_frame_number
        # Two cases are possible:
        # If amsdu is configured, we send tcp_ack_frame_number msdu and only one mpdu
        # If not, we send tcp_ack_frame_number mpdu containing only one msdu
        if amsdu_configured == 0:
            errors_tcp_ack, mpdu_nb_tcp_ack, msdu_nb_tcp_ack, tcp_ack_plcp_hdr_time, tcp_ack_phy_rate, tcp_ack_pckt_bytes_tx_time = n_msdu_tx_time(band, bw, modulation, nb_ss, sgi, ldpc, stbc, greenfield, control_modulation, tcp_ack_pckt_msdu_bytes,  msdu_nb, msdu_limit_nb_bytes, tcp_ack_frame_number, encryption)
        else:
            errors_tcp_ack, mpdu_nb_tcp_ack, msdu_nb_tcp_ack, tcp_ack_plcp_hdr_time, tcp_ack_phy_rate, tcp_ack_pckt_bytes_tx_time = n_msdu_tx_time(band, bw, modulation, nb_ss, sgi, ldpc, stbc, greenfield, control_modulation, tcp_ack_pckt_msdu_bytes, tcp_ack_frame_number, msdu_limit_nb_bytes, 1, encryption)

        ################################# Ctrl frame time computation #############################################
        compressed_block_ack_phy_rate, compressed_block_ack_tx_time = n_ctrl_frame_tx_time(control_preamble, plcp_hdr_time, sgi, control_modulation, compressed_block_ack_length_bytes)
        rts_phy_rate, rts_tx_time = n_ctrl_frame_tx_time(control_preamble, plcp_hdr_time, sgi,control_modulation, rts_length_bytes)
        cts_phy_rate, cts_tx_time = n_ctrl_frame_tx_time(control_preamble, plcp_hdr_time, sgi, control_modulation, cts_length_bytes)

        # This version seeks to take into account of the txop limit

        if rts == 0:
            txop_msdu_exchange_time = msdu_tx_time + extension_time + sifs_time + compressed_block_ack_tx_time + extension_time
            msdu_exchange_time = difs_time + backoff_time + msdu_tx_time + extension_time + sifs_time + compressed_block_ack_tx_time + extension_time
            tcp_ack_exchange_time = difs_time + backoff_time + tcp_ack_pckt_bytes_tx_time + extension_time + sifs_time + compressed_block_ack_tx_time + extension_time
        elif rts == 1:
            txop_msdu_exchange_time = msdu_tx_time + extension_time + 3 * sifs_time + compressed_block_ack_tx_time + extension_time + rts_tx_time + extension_time + cts_tx_time + extension_time
            msdu_exchange_time = difs_time + backoff_time + msdu_tx_time + extension_time + 3 * sifs_time + compressed_block_ack_tx_time + extension_time + rts_tx_time + extension_time + cts_tx_time + extension_time
            tcp_ack_exchange_time = difs_time + backoff_time + tcp_ack_pckt_bytes_tx_time + extension_time + 3 * sifs_time + compressed_block_ack_tx_time + extension_time + rts_tx_time + extension_time + cts_tx_time + extension_time
        else:
            # We consider that rts = 0
            txop_msdu_exchange_time = msdu_tx_time + extension_time + sifs_time + compressed_block_ack_tx_time + extension_time
            msdu_exchange_time = difs_time + backoff_time + msdu_tx_time + extension_time + sifs_time + compressed_block_ack_tx_time + extension_time
            tcp_ack_exchange_time = difs_time + backoff_time + tcp_ack_pckt_bytes_tx_time + extension_time + sifs_time + compressed_block_ack_tx_time + extension_time

        print("test")

        if txop == 1:
            if txop_msdu_exchange_time > txop_limit:
                print ("a_mpdu / a_msdu must be adjsted")
                # Soit j'enlève un mpdu, soit j'enlève un msdu par mpdu

                if mpdu_nb >= msdu_nb:
                    if mpdu_nb > 2:
                        mpdu_nb -= 1
                else:
                    if msdu_nb > 2:
                        msdu_nb -= 1

                if mpdu_nb == 1 and msdu_nb == 1 and msdu_length_bytes > 1:
                    msdu_length_bytes -= 1
            else:
                txop_optimization = 1
        else:
            txop_optimization = 1
        print ("txop test")
    print ("mpdu_nb recalculé")
    print(mpdu_nb)
    return errors_data, errors_tcp_ack, mpdu_nb, msdu_nb, mpdu_nb_tcp_ack, msdu_nb_tcp_ack, msdu_exchange_time, tcp_ack_exchange_time



def n_throughput(tx_exchange_time, tcp_ack_exchange_time, msdu_size, msdu_nb, mpdu_nb):
    """ This function returns the throughput calculated for the following layers:
    MAC, UDP and TCP.
    tx_exchange_time is the time taken to send an MSDU, calculated by the
    ag_msdu_exchange_time function.
    tcp_eff is the TCP efficiency and describes the data segment over tcp ack segments ratio
    msdu_size is the size of the msdu.
    """
    try:
        if tx_exchange_time < 0 :
            raise ValueError
        elif msdu_size < 0 :
            raise ValueError
        elif msdu_nb < 1:
            raise ValueError
        elif mpdu_nb < 1:
            raise ValueError



        tcp_exchange_time = tx_exchange_time + tcp_ack_exchange_time
        mac_throughput = (8*mpdu_nb*msdu_nb*msdu_size/tx_exchange_time)/10**6
        udp_throughput = (8*mpdu_nb*msdu_nb*(msdu_size - llc_bytes - snap_bytes- ip_header_bytes - udp_header_bytes)/tx_exchange_time)/10**6
        tcp_throughput = (8*mpdu_nb*msdu_nb*(msdu_size - llc_bytes - snap_bytes- ip_header_bytes - tcp_header_bytes)/(tx_exchange_time + tcp_ack_exchange_time))/10**6
        tcp_throughput_2 = (8 * mpdu_nb * msdu_nb * (msdu_size - llc_bytes - snap_bytes - ip_header_bytes - tcp_header_bytes) / (tcp_exchange_time)) / 10 ** 6
        #tcp_throughput = (tcp_eff*8*(msdu_size- llc_bytes - snap_bytes- ip_header_bytes - tcp_header_bytes)/tcp_exchange_time)/10**6
        return mac_throughput, udp_throughput, tcp_throughput
    except ValueError :
        print("ag_throughput entry error: tx_exchange_time or tcp_eff entry error")

def addition (a, b):
    a=10
    return (a+b)