""" This file defines the variables used for the different 802.11 throughput models
   for the 802.11 a/g/n standards
"""


########## General variables ##########
# Security variables
encryption_bytes = [0, 8, 20, 16] # [none, wep, wpa, wpa2] in bytes
# mac varioables
mac_header_bytes = 30
n_ac_mac_header_bytes = 36
mac_tail_bytes = 4
ack_length_bytes = 14
compressed_block_ack_length_bytes = 32
block_ack_length_bytes = 152
rts_length_bytes = 20
cts_length_bytes = 14


l_service_bits = 16
a_tail_bits = 6


########## 802.11ag variables definition ##########
# 802.11a standard variables (phy level)
ag_sc = 48 #sc means sub_carrier
ag_code = [0.5, 0.75, 1, 1.5, 2, 3, 4, 4.5]
ag_symb_per_sec = 250*10**3

ag_preamble_time = 16*10**-6
ag_plcp_header_time = 4*10**-6

# 802.11a standard variables (mac level)
rifs_time_50 = 2*10**-6
slot_time_50 = [9*10**-6, 9*10**-6]
sifs_time_50 = 16*10**-6
#pifs_time_50 = sifs_time_50 + slot_time_50[0] # Time used before sending a beacon
extension_time_50 = 0



########## 802.11g variables definition ##########
# 802.11g standard variables
rifs_time_24 = 2*10**-6
slot_time_24 = [9*10**-6,20*10**-6]
sifs_time_24 = 10*10**-6
#pifs_time_24 = sifs_time_24 + slot_time_24 # Time used before sending a beacon
extension_time_24 = 6*10**-6


g_sc = 48 #sc means sub_carrier
g_code = [0.5, 0.75, 1, 1.5, 2, 3, 4, 4.5]
g_symb_per_sec = 250*10**3


###############################################
########## 802.11n standard variables #########
###############################################
n_sc = [52, 108, 234, 468] # le nombre de porteuses dépend de la largeur de bande (20, 40, 80, 160).
n_code = [0.5, 1, 1.5, 2, 3, 4, 4.5, 5, 6, 8*5/6]
n_symb_per_sec = [(1/(4*10**-6)),(1/(3.6*10**-6))]
n_nb_ss = [1, 2, 3, 4]
bw = [0, 1]
# 802.11n standard variables (mac level)
# rifs, slot_time, sifs et extension time sont les mêmes que pour le 802.11a
#rifs_time_50 = 2*10**-6
#slot_time_50 = [9*10**-6, 9*10**-6]
#sifs_time_50 = 16*10**-6
#extension_time_50 = 0
l_stf_time = 8*10**-6
l_ltf_time = 8*10**-6
l_sig_time = 4*10**-6
ht_sig_1_time = 4*10**-6
ht_sig_2_time = 4*10**-6
ht_ltf_time = 4*10**-6
ht_stf_time = 4*10**-6
# mode greenfield
gf_ht_stf_time = 8*10**-6
ht_ltf1_time = 8*10**-6
tsym_1 = 4*10**-6
tsym_2 = 3.6*10**-6


############## Variables related to a_mpdu ###################
mpdu_delimiter_bytes = 4
n_mpdu_max_aggregate = 64
n_max_msdu_length_in_ampdu_bytes = 4095 # for msdu or amsdu
n_max_msdu_length_in_amsdu_bytes = 2304
n_max_msdu_length_bytes = 7955 # length if no ampdu agg is used.

############### Vairables related to a_msdu ##################
n_msdu_hdr_bytes = 14
n_msdu_max_length_without_amsdu = 7955
n_amsdu_max_bytes_1 = 3889
n_amsdu_max_bytes_2 = 7935 # if ampdu cannot exceed 4095
n_amsdu_max_bytes_3 = 4095
################ PSDU limit ################
n_max_psdu_bytes = 65535



########## LLC / SNAP ##########
llc_bytes = 3
snap_bytes = 5

########## IP ##########
ip_header_bytes = 20
ip_header_with_option_bytes = 24
# for more info: https://www.frameip.com/entete-ip/
########## udp ##########
udp_header_bytes = 8

########## TCP ##########
tcp_header_bytes = 20 # 32 with options field (not used under Matlab) We leave it this way for the comparison.
tcp_ack_pckt_bytes = 20 # # 32 with options field (not used under Matlab)  We leave it this way for the comparison.
tcp_ack_pckt_msdu_bytes = tcp_ack_pckt_bytes + llc_bytes + snap_bytes + ip_header_bytes


