""" Main programm for calculating the telecommunication throughput """


from wifi_variables import *
from wifi_functions import *


# n = list(range(8))
#
#
# print("physical rates of the 802.11a:")
# for i in n:
#     debit, ndbps = ag_phy_throughput(i)
#     print(debit/10**6, "Mbps")
#     print(ndbps)
#
# print("Test de la fonction qos")
# qos =set_qos_params(0, 0)
# print (qos)
# print("a standard msdu_tx_time calculation")
# phy_rate, msdu_tx_time = ag_msdu_tx_time (0, 0, 1500, 0)
# print(msdu_tx_time)



# Utilisation (data_modulation, ctrl_modulation, encryption, msdu_length, rts, qos)
msdu = 1500
leg = 0
bk = 1
be = 2
vi = 3
vo = 4
no_enc = 0
wep = 1
wpa = 2
wpa2 = 3
tcp_eff = 2
rts_off = 0
rts_on = 1
band = 0
mcs = 7
ctrl_mod = 2

# Old: def ag_msdu_exchange_time(data_modulation, ctrl_modulation, msdu_length, encryption, rts, qos, band):
#time = ag_msdu_exchange_time(7, 2, msdu, 0, 0, 2, 0)

# New: def ag_msdu_exchange_time(band, data_modulation, ctrl_modulation, qos, msdu_length, rts, encryption):

data_time = ag_msdu_exchange_time(band, mcs, ctrl_mod, be, msdu, rts_on, wep)
ack_tcp_time = ag_msdu_exchange_time(band, mcs, ctrl_mod, be, tcp_ack_pckt_msdu_bytes, rts_on, wep)
#d = (8*msdu/data_time)/10**6
#print("Débit (Mbps): ", d)
mac, udp, tcp = ag_throughput(data_time, ack_tcp_time, tcp_eff, msdu)
print(mac, udp, tcp)









modulation = 0
nb_ss = 1
bw = 0
sgi = 0


phy_rate, ndbps, nes = n_phy_throughput(modulation, bw, nb_ss, sgi)
print("phy_rate 802.11nac: ", phy_rate)
print("Bonjour")


#for modulation in range(8):
#        for bw in range(2):
#            for sgi in range(2):
#                print (n_phy_throughput(modulation, bw, nb_ss, sgi)/10**6)

for bw in range(2):
    for sgi in range(2):
        for modulation in range(8):
            thr, ndbps, nes = (n_phy_throughput(modulation, bw, nb_ss, sgi))
            thr = thr / 10 ** 6
            thr = round(thr,1)
            print(ndbps)

print('Affichage des ndbps \n')
for bw in range(2):
    for nb_ss in n_nb_ss:
        for modulation in range(8):
            thr, ndbps, nes = (n_phy_throughput(modulation, bw, nb_ss, sgi))
            thr = thr / 10 ** 6
            thr = round(thr, 1)
            print(ndbps)

#ag_throughput(0.0005, -2,)





#help(a_msdu_tx_time)

#print("physical rates of the 802.11g:")

#for i in n:
#    [debit, ndbps] = g_phy_throughput(i)
#    print(debit/10**6, "Mbps")
#    print(ndbps)






#sc = [n_sc_20, n_sc_40]

#for ss in n_ss:
#    for n_sc in sc:
#        print("Phy rates du 802.11n pour {0} ss et {1} sous-porteuse".format(ss, n_sc))
#        for i in n:
#            print(i)
#            print(ss)
#            print(n_sc)
#            debit = n_phy_throughput(i, ss, n_sc, 1)
#            print(debit/10**6, "Mbps")


#n_phy_throughput (modulation, nb_ss, n_sc, sgi)

#print("\n Test de la fonction n_phy_throughput:")
#debit_n = 0
#debit_n, ndbps = n_phy_throughput(0, 1, 0, 1)
#print("Le débit 80.11n vaut {0} Mbps. Ndbps = {1}".format(debit_n/10**6, ndbps))
#help(n_phy_throughput)

# #################################################################################################################
# ########### Test de l'ageégation A-MSDU ##################
# ################################################################################################################
#
# print("Tests de l'adaptation du MSDU:")
# # a_msdu_limit_bytes peut prendre deux valeurs selon la station client
# amsdu_nb_limit_bytes_1 = n_amsdu_max_bytes_1 # 3889
# amsdu_nb_limit_bytes_2 = n_amsdu_max_bytes_3 # 4095
# amsdu_nb_limit_bytes_3 = n_amsdu_max_bytes_2 # 7935
#
# msdu_length = 1500
# mpdu_nb = 32
# msdu_nb = 1
# amsdu_limit_bytes = amsdu_nb_limit_bytes_3
# encrypt = encryption_bytes [0]
# print ('Information msdu pour la configuration un longueur de msdu de {} octets et un nombre de msdu(s) agrégé(s) demandés de {}. Limite max de {}'.format(msdu_length, msdu_nb, amsdu_nb_limit_bytes_1))
# error_msdu, error_msdu_nb, nbre_msdu_aggreges, msdu_length_bytes, a_msdu_length, pad = n_amsdu_config_check (msdu_length, msdu_nb, amsdu_limit_bytes)
# print ('Le nombre de MSDU agrégés est de {}, la longueur de la trame agrégée est de {} et le nombre d''octets de padding est de {}.\n'.format (nbre_msdu_aggreges, a_msdu_length, pad))
#
#
# #amsdu_length_limit_bytes = n_amsdu_max_bytes_1
#
# error_mpdu, error_mpdu_nb, error_msdu2, error_msdu_nb_2, error_max_amsdu_nb, msdu_nb, mpdu_nb, msdu_length_bytes, amsdu_length_bytes, mpdu_length_bytes, msdu_paddin_bytes, mpdu_padding_bytes = n_ampdu_config_check (mpdu_nb, msdu_nb, msdu_length, amsdu_limit_bytes, encrypt)
# #print (error_mpdu1, error_mpdu2, error_mpdu3, error_mpdu4, msdu_nb, mpdu_nb, msdu_length_bytes, amsdu_length_bytes, mpdu_length_bytes, msdu_paddin_bytes, mpdu_padding_bytes)
# print('test')
#
# #################################################################################################################
# ########### Fin Test de l'ageégation A-MSDU ##################
# ################################################################################################################





#####################################################################################################################
########################## Test du calcul de débit ##################################################################
#####################################################################################################################

band = 1
bw = 0
modulation = 1
nb_ss = 2
sgi = 0
ldpc = 0
stbc = 0
greenfield = 0
control_preamble = 1
control_modulation = 1
QoS = 2
txop =  1
msdu_length_bytes = 1500
amsdu_limit_bytes = n_amsdu_max_bytes_2
mpdu_nb = 8
msdu_nb = 2
encryption = encryption_bytes [0]
rts = 0
tcp_eff = 2

# Test de la fonction n_msdu_tx_time

#plcp_hdr_time, phy_rate, msdu_tx_time = n_msdu_tx_time (band, bw, modulation, nb_ss, sgi, ldpc, stbc, greenfield, control_modulation, msdu_length_bytes, msdu_nb, amsdu_limit_bytes, mpdu_nb, encryption)


print('test!!!')

#####################################################################################################################
# # Test de la fonction de calcul du temps d'émission d'un paquet de contrôle
#
# # Def de la longueur des paquets
# compressed_ba_pkt = compressed_block_ack_length_bytes
# ba_pkt = block_ack_length_bytes
# rts_pkt = rts_length_bytes
# cts_pkt = cts_length_bytes
#
#
# # Def du type de preamble
# greenfield = 1
# # Modulation de contrôle
# ctrl_mod = 7
#
# ctrl_pkt_phy_thr_2, ctrl_pckt_t_2 = n_ctrl_frame_tx_time (greenfield, ctrl_mod, ba_pkt)
# ctrl_pkt_phy_thr_1, ctrl_pckt_t_1 = n_ctrl_frame_tx_time (greenfield, ctrl_mod, compressed_ba_pkt)
# ctrl_pkt_phy_thr_3, ctrl_pckt_t_3 = n_ctrl_frame_tx_time (greenfield, ctrl_mod, rts_pkt)
# ctrl_pkt_phy_thr_4, ctrl_pckt_t_4 = n_ctrl_frame_tx_time (greenfield, ctrl_mod, cts_pkt)
#
# print ("test")
######################################################################################################################
# # Fin test de la fonction de calcul du temps d'émission d'un paquet de contrôle
#####################################################################################################################

# Afin de comparer les deux versions Matlab / Python il faut se mettre dans les mêmes conditions sachant que sur le
# script Matlab, la configuration utilisée est la suivante:
# Preamble HT_MF et ctrl mod = 24 Mbps

#ack_tcp_time = ag_msdu_exchange_time(0, 7, 2, be, tcp_ack_pckt_bytes_msdu, rts_on, wep)

#n_ack_tcp_tx_time = n_msdu_tx_time (band, bw, modulation, nb_ss, sgi, ldpc, stbc, greenfield, control_modulation,
#                                msdu_length_bytes, tcp_ack_pckt_bytes_msdu, amsdu_limit_bytes, mpdu_nb, encryption)



errors_data, errors_tcp_ack, mpdu_nb, msdu_nb, mpdu_nb_tcp_ack, msdu_nb_tcp_ack, data_tx_exchange_time, tcp_ack_exchange_time = n_msdu_exchange_time (band, bw, modulation, nb_ss, sgi, ldpc, stbc, greenfield, control_preamble, control_modulation, QoS, txop,
                    msdu_length_bytes, msdu_nb, amsdu_limit_bytes, mpdu_nb, rts, encryption, tcp_eff)

tcp_exchange_time = data_tx_exchange_time + tcp_ack_exchange_time
mac, udp, tcp = n_throughput(data_tx_exchange_time, tcp_ack_exchange_time, msdu_length_bytes, msdu_nb, mpdu_nb)


print (mac, udp, tcp)
print ("Fin du programme \n")

#####################################################################################################################
########################## Fin Test du calcul de débit ##################################################################
####################################################################################################################