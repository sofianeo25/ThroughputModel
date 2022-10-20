# -------------------------------------------------------------------------------
# Name:        IEEE80211ax
# Purpose:
#
# Author:      FTSN7840
#
# Created:     18/10/2018
# Copyright:   (c) FTSN7840 2018
# Licence:     <your licence>
# -------------------------------------------------------------------------------

import cProfile
import csv
import datetime
import io
import math
import pstats
from pstats import SortKey

import numpy as np
import scipy.io as sio
from scipy.interpolate import interp1d
from core import *


class IEEE80211ax:

    def __init__(self, B, Msta, Map, S, AggMPDU, AggMSDU, GiDL, GiUL, a, b, QoS, LambdaCSI, NSS, NRX, AngleQuantif,
                 Grpmt, DCM):
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
        self.BW = B
        self.Map = Map
        self.Msta = Msta
        self.S = S
        self.AggMPDU = AggMPDU
        self.AggMSDU = AggMSDU
        self.GiDL = GiDL
        self.GiUL = GiUL
        self.a = a
        self.b = b
        self.QoS = QoS
        self.LambdaCSI = LambdaCSI
        self.QoS_Config()
        self.NSS = NSS
        self.NRX = NRX
        self.AngleQuantif = AngleQuantif
        self.Grpmt = Grpmt
        self.DCM = DCM

    def setup(self, Ldata, LdataTCP, mcs, bf, ofdma, nru, mumimo, RTSCTS, udp, tcp):
        """
           Configuration du modèle:
           Ldata, Taille des paquets (si Ldata = 1350, la taille des paquets en TCP sera 1460 par defaut)
           mcs,  MCS choisi
           bf, Utiliser CSI (tcsi = 1) ou pas (tcsi = 0)
           ofdma, Utiliser OFDMA (ofdma = 1) ou pas (ofdma = 0)
           nru,   Choisir le nombre de répartition de la bande en OFDMA (Utilisation de toute la bande : nru = 1, Utilisation de la moitié la bande : nru = 2 )
           mumimo, Utiliser MU-MIMO (mumimo = 1) ou pas (mumimo = 0)
           RTSCTS, Utiliser RTSCTS (RTSCTS = 1) ou pas (RTSCTS = 0)
           udp,    Calculer UDP (udp = 1) ou pas (udp = 0)
           tcp    Calculer TCP (tcp = 1) ou pas (tcp = 0)
        """
        self.Ldata = Ldata
        self.LdataTCP = LdataTCP
        self.tcsi = bf
        self.RTSCTS = RTSCTS
        self.ofdma = ofdma
        self.mumimo = mumimo
        self.udp = udp
        self.tcp = tcp
        self.mcs = mcs
        self.nru = nru
        self.UDP_Throughput_UL = self.Th_UL()
        self.UDP_Throughput_DL = self.Th_DL()
        self.UDP_Throughput_DL_UL = self.Th_DL_UL()
        if tcp == 1:
            self.TCP_Throughput = self.Th_TCP()
            self.TCP_OP_Throughput = self.Th_TCP_OP()

        # self.RunConfig()

    def QoS_Config(self):
        """
            Choix de la classe de QoS:
            'legacy', Legacy
            'AX_VO' Voix,
            'AX_VI' Video,
            'AX_BE' Best Effort,
            'AX_BK' Background
        """
        if self.QoS == 'legacy':
            self.CWmin = 16
            self.CWmax = 1024
            self.MaxPPDU = 5.4884 * 10 ** (-3)
            self.TXOP = 8160 * 10 ** (-6)
            self.AIFSN = 2
        elif self.QoS == 'AX_VO':
            self.CWmin = 8
            self.CWmax = 16
            self.MaxPPDU = 5.4884 * 10 ** (-3)
            self.TXOP = 2080 * 10 ** (-6)
            self.AIFSN = 2
        elif self.QoS == 'AX_VI':
            self.CWmin = 16
            self.CWmax = 32
            self.MaxPPDU = 5.4884 * 10 ** (-3)
            self.TXOP = 4006 * 10 ** (-6)
            self.AIFSN = 2
        elif self.QoS == 'AX_BE':
            self.CWmin = 32
            self.CWmax = 1024
            self.MaxPPDU = 5.4884 * 10 ** (-3)
            self.TXOP = 8160 * 10 ** (-6)
            self.AIFSN = 3
        elif self.QoS == 'AX_BK':
            self.CWmin = 32
            self.CWmax = 1024
            self.MaxPPDU = 5.4884 * 10 ** (-3)
            self.TXOP = 8160 * 10 ** (-6)
            self.AIFSN = 7

    def RunConfig(self, mcs1, mcs2):
        """
            Calcul des Débits UDP et TCP pour la configuration donnée
            mcs1 pour le DL, TCP, TCP OP et DL_UL
            mcs2 pour le UL
        """

        # Scénario DL seul
        self.Setmcs(mcs1)
        self.TCP_Throughput = self.Th_TCP()
        self.TCP_OP_Throughput = self.Th_TCP_OP()
        self.UDP_Throughput_DL = self.Th_DL()

        # Scénario DL_UL UDP (Article Boris) Cascading transmission
        if self.S >= 64 and self.mumimo == 1 and self.ofdma == 1 and (mcs1 == 10 or mcs1 == 11):
            self.Setmcs(9)
        self.UDP_Throughput_DL_UL = self.Th_DL_UL()

        # Scénario UL seul
        self.Setmcs(mcs2)
        self.UDP_Throughput_UL = self.Th_UL()

    ##    def Get_User_UDP_Throughput_DL_UL(self, QoS) :
    ##    #          UDP_Throughput_DL_UL [0]  DL
    ##    #          UDP_Throughput_DL_UL [1]  UL
    ##        """
    ##            Calcul du Débit UDP DL/UL utilisateur de la configuration donnée pour une classe de QoS
    ##        """
    ##        self.QoS = QoS
    ##        self.QoS_Config()
    ##        self.RunConfig()
    ##        (DL,UL ) = self.UDP_Throughput_DL_UL
    ##        return (   round ( DL /self.S , 2 )  ,  round ( UL/self.S, 2 )  )
    ##
    ##    def Get_User_UDP_Throughput_DL (self, QoS) :
    ##        """
    ##            Calcul du Débit UDP DL utilisateur de la configuration donnée pour une classe de QoS
    ##        """
    ##        self.QoS = QoS
    ##        self.QoS_Config()
    ##        self.RunConfig()
    ##        DL = self.UDP_Throughput_DL
    ##        return round (DL /self.S , 2 )
    ##
    ##
    ##    def Get_User_UDP_Throughput_UL  (self, QoS) :
    ##        """
    ##            Calcul du Débit UDP UL utilisateur de la configuration donnée pour une classe de QoS
    ##        """
    ##        self.QoS = QoS
    ##        self.QoS_Config()
    ##        self.RunConfig()
    ##        UL = self.UDP_Throughput_UL
    ##        return round (UL /self.S , 2 )
    ##
    ##    def Get_User_TCP_Throughput (self, QoS) :
    ##        """
    ##            Calcul du Débit TCP utilisateur de la configuration donnée pour une classe de QoS
    ##        """
    ##        self.QoS = QoS
    ##        self.QoS_Config()
    ##        self.RunConfig()
    ##        TCP = self.TCP_Throughput
    ##        return round (TCP /self.S , 2 )

    def Get_AP_UDP_Throughput_DL_UL(self):
        #          UDP_Throughput_DL_UL [0]  DL
        #          UDP_Throughput_DL_UL [1]  UL
        """
            Calcul du Débit UDP DL/UL TOTAL de la configuration donnée
        """
        T = self.UDP_Throughput_DL_UL
        return (round(T[0], 2), round(T[1], 2))

    def Get_AP_UDP_Throughput_DL(self):
        """
            Calcul du Débit UDP DL TOTAL de la configuration donnée
        """
        T = self.UDP_Throughput_DL
        return (round(T[0], 2), round(T[1], 2), round(T[2], 20))

    def Get_AP_UDP_Throughput_UL(self):
        """
            Calcul du Débit UDP UL TOTAL de la configuration donnée
        """
        T = self.UDP_Throughput_UL
        return (round(T[0], 2), round(T[1], 2), round(T[2], 20))

    def Get_AP_TCP_Throughput(self):
        """
            Calcul du Débit TCP TOTAL de la configuration donnée
        """
        T = self.TCP_Throughput
        return (round(T[0], 2), round(T[1], 2))

    def Get_AP_TCP_OP_Throughput(self):
        """
            Calcul du Débit TCP Optimisé TOTAL de la configuration donnée
        """
        T = self.TCP_OP_Throughput
        return (round(T[0], 2), round(T[1], 2))

    def Collision_Config(self, Nuser):
        """
            Extraction des valeurs de Tau et P ( paramètres de collision) en fonction du nombre d'utilisateur
            Les fichier .mat sont dans le répertoire courrant.  Utilisée dans le modèle DL_UL
        """
        if self.CWmin == 8:
            TauETP = sio.loadmat('Collisions\TauEtP8.mat')
            TauEtP = TauETP['TauEtP8']
        elif self.CWmin == 16:
            TauETP = sio.loadmat('Collisions\TauEtP16.mat')
            TauEtP = TauETP['TauEtP16'];
        elif self.CWmin == 32:
            TauETP = sio.loadmat('Collisions\TauEtP32.mat')
            TauEtP = TauETP['TauEtP32'];
        elif self.CWmin == 64:
            TauETP = sio.loadmat('Collisions\TauEtP64.mat')
            TauEtP = TauETP['TauEtP64'];
        elif self.CWmin == 128:
            TauETP = sio.loadmat('Collisions\TauEtP128.mat')
            TauEtP = TauETP['TauEtP128'];
        elif self.CWmin == 256:
            TauETP = sio.loadmat('Collisions\TauEtP256.mat')
            TauEtP = TauETP['TauEtP256'];
        elif self.CWmin == 512:
            TauETP = sio.loadmat('Collisions\TauEtP512.mat')
            TauEtP = TauETP['TauEtP512'];
        elif self.CWmin == 1024:
            TauETP = sio.loadmat('Collisions\TauEtP1024.mat')
            TauEtP = TauETP['TauEtP1024'];

        x = [1, 4, 16, 32, 64, 128, 256, 512, 1024]
        YToap = [2 / float(self.CWmin), TauEtP[0, 0], TauEtP[1, 0], TauEtP[2, 0], TauEtP[3, 0], TauEtP[4, 0],
                 TauEtP[5, 0], TauEtP[6, 0], TauEtP[7, 0]]
        YTosta = [2 / float(self.CWmin), TauEtP[0, 1], TauEtP[1, 1], TauEtP[2, 1], TauEtP[3, 1], TauEtP[4, 1],
                  TauEtP[5, 1], TauEtP[6, 1], TauEtP[7, 1]]
        Ypcap = [2 / float(self.CWmin), TauEtP[0, 2], TauEtP[1, 2], TauEtP[2, 2], TauEtP[3, 2], TauEtP[4, 2],
                 TauEtP[5, 2], TauEtP[6, 2], TauEtP[7, 2]]
        Ypcsta = [2 / float(self.CWmin), TauEtP[0, 3], TauEtP[1, 3], TauEtP[2, 3], TauEtP[3, 3], TauEtP[4, 3],
                  TauEtP[5, 3], TauEtP[6, 3], TauEtP[7, 3]]

        FToap = interp1d(x, YToap)
        FTosta = interp1d(x, YToap)
        Fpcap = interp1d(x, YToap)
        Fpcsta = interp1d(x, YToap)

        Toap = FToap(Nuser)
        Tosta = FTosta(Nuser)
        pcap = Fpcap(Nuser)
        pcsta = Fpcsta(Nuser)

        return (Toap, Tosta, pcap, pcsta)

    def Get_GiDL(self):

        if self.GiDL == 3.2:
            return 2
        elif self.GiDL == 1.6:
            return 1
        elif self.GiDL == 0.8:
            return 0

    def Get_GiUL(self):
        if self.GiUL == 3.2:
            return 2
        elif self.GiUL == 1.6:
            return 1
        elif self.GiUL == 0.8:
            return 0

    def Setmcs(self, m):
        """
           Modifier la valeur de la MCS
        """
        self.mcs = m

    def SetNRU(self, nru):
        """
           Modifier la valeur de nru
        """
        self.nru = nru

    def MCSConfig(self):
        ##    Ym,   NBPSCS voir tables de débit ax
        ##    Yc,   R, code rate,  voir tables de débit ax
        """
            En fonction du numéro de MCS, Obtenir le 'Coding rate' et 'Number of coded bits per subcarrier per spatial stream'
        """
        if self.mcs == 0:
            Ym = 1
            Yc = float(1) / float(2)
        elif self.mcs == 1:
            Ym = 2
            Yc = float(1) / float(2)
        elif self.mcs == 2:
            Ym = 2
            Yc = float(3) / float(4)
        elif self.mcs == 3:
            Ym = 4
            Yc = float(1) / float(2)
        elif self.mcs == 4:
            Ym = 4
            Yc = float(3) / float(4)
        elif self.mcs == 5:
            Ym = 6
            Yc = float(2) / float(3)
        elif self.mcs == 6:
            Ym = 6
            Yc = float(3) / float(4)
        elif self.mcs == 7:
            Ym = 6
            Yc = float(5) / float(6)
        elif self.mcs == 8:
            Ym = 8
            Yc = float(3) / float(4)
        elif self.mcs == 9:
            Ym = 8
            Yc = float(5) / float(6)
        elif self.mcs == 10:
            Ym = 10
            Yc = float(3) / float(4)
        elif self.mcs == 11:
            Ym = 10
            Yc = float(5) / float(6)
        else:
            return (0, 0)

        return (Ym * Yc)

    def Get_NSS(self):
        """
           Obtenir le nombre de flux spatiaux pour la configuration
           Retourne le Nombre de flux spataux par station
        """

        if self.S == 1 or self.mumimo == 0:
            Vs = self.Get_NSS_Full_MIMO()
        else:
            Vs = self.Get_NSS_MUMIMO_Table()

        return Vs

    def Get_NSS_MIMO(self):
        """
           Obtenir le nombre de flux spatiaux pour le Nombre d'antenne Tx et Rx utilisés
           Retourne le Nombre de flux spataux par station
           Version Article Boris
        """
        Nru = math.ceil(float(self.S) / float(self.Map))
        Vm = math.ceil(float(self.S) / float(Nru))
        Vs = min(self.Msta, math.ceil(self.Map / Vm))
        return Vs

    def Get_NSS_MUMIMO_Table(self):
        """
           Obtenir le nombre de flux spatiaux pour le Nombre d'antenne Tx et Rx utilisés
           Retourne le Nombre de flux spataux par station en servant le maximum de station qui peut être < S
        """
        if self.ofdma == 1:
            Nru = self.nru
        else:
            Nru = 1

        Vm = math.ceil(float(self.S) / float(Nru))
        Vs = min(self.Msta, math.ceil(self.Map / Vm))
        return Vs

    def Get_NSS_Full_MIMO(self):
        """
           Obtenir le nombre de flux spatiaux pour une configuration  Full MIMO
        """
        Vs = min(self.Msta, self.Map)
        return Vs

    def Get_Ysc(self):
        """
           Obtenir la taille des RUs en nombre de sous porteurses pour la configuration
        """

        if self.ofdma == 0:
            Ysc = self.Get_Ysc_Full_BAND()
        else:
            Ysc = self.Get_Ysc_BAND()

        return Ysc

    def Get_Ysc_BAND(self):
        """
           Obtenir la taille des RUs en nombre de sous porteurses en fonction de la configuration utilisée
        """

        (YscSU, YscMU) = self.Strategy()
        Ysc = YscMU
        return Ysc

    def Get_Ysc_Full_BAND(self):
        """
           Obtenir la taille des RUs en nombre de sous porteurses en FULL Band
        """

        (YscSU, YscMU) = self.Strategy_NO_OFDMA()
        return YscSU

    def BeamformingConfig(self):
        """
          Calculer la taille du report beamforming
        """

        (YscSU, YscMU) = self.Strategy()
        Ysc = YscSU
        balpha, bbeta = 0, 0
        NR = self.NSS;
        NC = min(self.NSS, self.NRX);

        if self.AngleQuantif == 0:
            balpha = 5
            bbeta = 7
        elif self.AngleQuantif == 1:
            balpha = 7
            bbeta = 9

        if NR == 2:
            Nang = 2
        elif NR == 3:
            if NC == 1:
                Nang = 4
            else:
                Nang = 6
        elif NR == 4:
            if NC == 1:
                Nang = 6
            elif NC == 2:
                Nang = 10
            else:
                Nang = 12
        elif NR == 5:
            if NC == 1:
                Nang = 8
            elif NC == 2:
                Nang = 14
            elif NC == 3:
                Nang = 18
            else:
                Nang = 20
        elif NR == 6:
            if NC == 1:
                Nang = 10
            elif NC == 2:
                Nang = 18
            elif NC == 3:
                Nang = 24
            elif NC == 4:
                Nang = 28
            else:
                Nang = 30
        elif NR == 7:
            if NC == 1:
                Nang = 12
            elif NC == 2:
                Nang = 22
            elif NC == 3:
                Nang = 30
            elif NC == 4:
                Nang = 36
            elif NC == 5:
                Nang = 40
            else:
                Nang = 42
        elif NR == 8:
            if NC == 1:
                Nang = 14
            elif NC == 2:
                Nang = 26
            elif NC == 3:
                Nang = 36
            elif NC == 4:
                Nang = 44
            elif NC == 5:
                Nang = 50
            elif NC == 6:
                Nang = 54
            else:
                Nang = 56

        if self.Grpmt == 0:
            Nsg = 4
        else:
            Nsg = 16

        return (NC * 8 + (Ysc * (Nang * (balpha + bbeta)) / (Nsg * 2)))

    def Strategy_NO_OFDMA(self):
        """
           Obtenir la taille des RUs quand OFDMA est désactivé
        """

        if self.BW == 160:  # MHz
            YscSU = 996 * 2;  # Nombre de sous porteuses full band en SU 160 MHz

        elif self.BW == 80:  # MHz
            YscSU = 996;  # Nombre de sous porteuses full band en SU 80 MHz

        elif self.BW == 40:  # MHz
            YscSU = 484;  # Nombre de sous porteuses full band en SU 40 MHz

        elif self.BW == 20:  # MHz
            YscSU = 242;  # Nombre de sous porteuses full band en SU 20 MHz

        else:
            print('mauvaise config, Bande non definie');
            return (0, 0)

        return (YscSU, YscSU)

    def Strategy_OFDMA_NO_MUMIMO(self):
        """
           Obtenir la taille des RUs quand OFDMA est activé et MU-MIMO est désactivé
        """

        Nru = self.nru
        if self.BW == 160:  # MHz
            YscMU = np.array([996 * 2, 996, 484, 242, 106, 52,
                              26]);  # Nombre de sous porteuses par RU 160 MHz 80 MHz 40 MHz 20 MHz 10 MHz 5 MHz 2 MHz : 1, 2, 4, 8, 16, 37, 74 RUs
            YscSU = 1960 / Nru;  # Nombre de sous porteuses full band en SU 160 MHz ??
            if Nru == 1:
                index = 1;
            elif Nru == 2:
                index = 2;
            elif Nru == 4:
                index = 3;
            elif Nru == 9:
                index = 4;
            elif Nru == 18:
                index = 5;
            elif Nru == 37:
                index = 6;
            elif Nru == 74:
                index = 7;
            else:
                print('mauvaise config, Nru non defini');
                return (0, 0)
        elif self.BW == 80:  # MHz
            YscMU = np.array([996, 484, 242, 106, 52,
                              26]);  # Nombre de sous porteuses par RU 80 MHz 40 MHz 20 MHz 10 MHz 5 MHz 2 MHz : 1, 2, 4, 8, 16, 37 RUs
            YscSU = 980 / Nru;  # Nombre de sous porteuses full band en SU 80 MHz ??
            if Nru == 1:
                index = 1;
            elif Nru == 2:
                index = 2;
            elif Nru == 4:
                index = 3;
            elif Nru == 9:
                index = 4;
            elif Nru == 18:
                index = 5;
            elif Nru == 37:
                index = 6;
            else:
                print('mauvaise config, Nru non defini');
                return (0, 0)
        elif self.BW == 40:  # MHz
            YscMU = np.array([484, 242, 106, 52,
                              26]);  # Nombre de sous porteuses par RU 40 MHz 20 MHz 10 MHz 5 MHz 2 MHz : 1, 2, 4, 8, 16  RUs
            YscSU = 468 / Nru;  # Nombre de sous porteuses full band en SU 40 MHz ??
            if Nru == 1:
                index = 1;
            elif Nru == 2:
                index = 2;
            elif Nru == 4:
                index = 3;
            elif Nru == 9:
                index = 4;
            elif Nru == 18:
                index = 5;
            else:
                print('mauvaise config, Nru non defini');
                return (0, 0)
        elif self.BW == 20:  # MHz
            YscMU = np.array(
                [242, 106, 52, 26]);  # Nombre de sous porteuses par RU 20 MHz 10 MHz 5 MHz 2 MHz : 1, 2, 4, 8 RUs
            YscSU = 234 / Nru;  # Nombre de sous porteuses full band en SU 20 MHz ??
            if Nru == 1:
                index = 1;
            elif Nru == 2:
                index = 2;
            elif Nru == 4:
                index = 3;
            elif Nru == 9:
                index = 4;
            else:
                print('mauvaise config, Nru non defini');
                return (0, 0)
        else:
            return (0, 0)

        return (YscSU, YscMU[index - 1])

    def Strategy_OFDMA_MUMIMO(self):
        """
           Obtenir la taille des RUs quand OFDMA et MU-MIMO sont activés
        """

        Nru = math.ceil(float(self.S) / float(self.Map))
        if self.BW == 160:  # MHz
            YscMU = np.array([996 * 2, 996, 484, 242,
                              106]);  # Nombre de sous porteuses par RU 160 MHz 80 MHz 40 MHz 20 MHz 10 MHz 5 MHz 2 MHz : 1, 2, 4, 8, 16, 37, 74 RUs
            YscSU = 1960;  # Nombre de sous porteuses full band en SU 160 MHz ??
            if Nru == 1:
                index = 1;
            elif Nru == 2:
                index = 2;
            elif Nru == 4:
                index = 3;
            elif Nru == 8:
                index = 4;
            elif Nru == 16:
                index = 5;
            else:
                print('mauvaise config, Nru non defini');
                return (0, 0)
        elif self.BW == 80:  # MHz
            YscMU = np.array([996, 484, 242,
                              106]);  # Nombre de sous porteuses par RU 80 MHz 40 MHz 20 MHz 10 MHz 5 MHz 2 MHz : 1, 2, 4, 8, 16, 37 RUs
            YscSU = 980;  # Nombre de sous porteuses full band en SU 80 MHz ??
            if Nru == 1:
                index = 1;
            elif Nru == 2:
                index = 2;
            elif Nru == 4:
                index = 3;
            elif Nru == 8:
                index = 4;
            else:
                print('mauvaise config, Nru non defini');
                return (0, 0)
        elif self.BW == 40:  # MHz
            YscMU = np.array([484, 242,
                              106]);  # Nombre de sous porteuses par RU 40 MHz 20 MHz 10 MHz 5 MHz 2 MHz : 1, 2, 4, 8, 16  RUs
            YscSU = 468;  # Nombre de sous porteuses full band en SU 40 MHz ??
            if Nru == 1:
                index = 1;
            elif Nru == 2:
                index = 2;
            elif Nru == 4:
                index = 3;
            else:
                print('mauvaise config, Nru non defini');
                return (0, 0)
        elif self.BW == 20:  # MHz
            YscMU = np.array([242, 106]);  # Nombre de sous porteuses par RU 20 MHz 10 MHz 5 MHz 2 MHz : 1, 2, 4, 8 RUs
            YscSU = 234;  # Nombre de sous porteuses full band en SU 20 MHz ??
            if Nru == 1:
                index = 1;
            elif Nru == 2:
                index = 2;
            else:
                print('mauvaise config, Nru non definiii');
                return (0, 0)
        else:
            return (0, 0)

        return (YscSU, YscMU[index - 1])

    def Strategy(self):
        """
           Obtenir la taille des RUs en fonction du choix de l'utilisateur
        """

        if self.ofdma == 0:
            return self.Strategy_NO_OFDMA()
        else:
            if self.mumimo == 0:
                return self.Strategy_OFDMA_NO_MUMIMO()
            else:
                return self.Strategy_OFDMA_MUMIMO()

    def Phy_DataRate_MIMO_OFDMA(self):
        """
           Calcul du débit Physique MU-MIMO + OFDMA  nombre de bit par symbol OFDM
        """
        mcsConfg = self.MCSConfig()
        Vs = self.Get_NSS()
        YscMU = self.Get_Ysc()
        YscSU = self.Get_Ysc_Full_BAND()
        GpeMUMIMO = (self.S * Vs / self.Map)
        GpeOFDMA = (self.S / self.nru)

        if self.S == 1:
            # Sur toute la bande
            RatePerOfdm = Vs * mcsConfg * YscSU
        else:
            if self.ofdma == 0:
                # MU-MIMO sur toute la bande
                RatePerOfdm = Vs * mcsConfg * YscSU  # / GpeMUMIMO
            else:
                ##                if   self.mumimo == 0  :
                ##                    if  (self.S * YscMU) > YscSU :
                ##                        RatePerOfdm = Vs*mcsConfg*YscMU  #/ GpeOFDMA
                ##                    else :
                ##                        RatePerOfdm = Vs*mcsConfg*YscMU
                ##                else:
                RatePerOfdm = Vs * mcsConfg * YscMU

        if Vs == 1 or Vs == 2:
            if self.DCM == 1:
                if self.mcs == 0 or self.mcs == 1 or self.mcs == 3 or self.mcs == 4:
                    return (RatePerOfdm / 2)

        return (RatePerOfdm)

    def Phy_DataRate_Full_MIMO(self):
        """
           Calcul du débit Physique Full MIMO avec le nombre maximum de flux spaciaux possible
        """

        mcsConf = self.MCSConfig()
        Yscc = self.Get_Ysc()
        Vs = self.Get_NSS_Full_MIMO()

        RatePerOfdm = Vs * mcsConf * Yscc

        if Vs == 1 or Vs == 2:
            if self.DCM == 1:
                if self.mcs == 0 or self.mcs == 1 or self.mcs == 3 or self.mcs == 4:
                    return (RatePerOfdm / 2)

        return (RatePerOfdm)

    def Phy_DataRate_Full_Band(self):
        """
           Calcul du débit Physique Full Band en utilisant toute la bande
        """

        mcsConf = self.MCSConfig()
        Yscc = self.Get_Ysc_Full_BAND()
        Vs = self.Get_NSS()

        RatePerOfdm = Vs * mcsConf * Yscc

        if Vs == 1 or Vs == 2:
            if self.DCM == 1:
                if self.mcs == 0 or self.mcs == 1 or self.mcs == 3 or self.mcs == 4:
                    return (RatePerOfdm / 2)

        return (RatePerOfdm)

    def Phy_DataRate_Full_MIMO_Full_Band(self):
        """
           Calcul du débit Physique Full MIMO Full OFDMA
        """

        mcsConf = self.MCSConfig()
        Yscc = self.Get_Ysc_Full_BAND()
        Vs = self.Get_NSS_Full_MIMO()

        RatePerOfdm = Vs * mcsConf * Yscc

        if Vs == 1 or Vs == 2:
            if self.DCM == 1:
                if self.mcs == 0 or self.mcs == 1 or self.mcs == 3 or self.mcs == 4:
                    return (RatePerOfdm / 2)

        return (RatePerOfdm)

    def Get_Phy_Datarate(self):
        """
           Obtenir le débit Physique MU-MIMO+OFDMA
        """

        return round(self.Phy_DataRate_MIMO_OFDMA(), 2)

    def Th_DL(self):
        """
           Calcul du débit UDP DL
        """

        Nuser = self.S
        # MUMIMO + OFDMA ou MUMIMO seul (nru = 1 )
        datarateMU = self.Phy_DataRate_MIMO_OFDMA()
        # SU sur toute la bande
        datarateSU = self.Phy_DataRate_Full_MIMO_Full_Band()
        # OFDMA seul pas forcément sur oute la bande
        datarateOFDMA = self.Phy_DataRate_Full_MIMO()
        # MU MIMO sur toute la bande
        datarateMIMO = self.Phy_DataRate_Full_Band()
        datarateLEG = 24;  # [bits / OFDM symbol ]( 1 * Ym * Yc * Ysc20 ) ;
        Vs = self.Get_NSS()
        Breport = self.BeamformingConfig()
        OFDMA_Duration = 12.8
        TsymUL = (OFDMA_Duration + self.GiUL) * 10 ** (-6);  # [s]
        TsymDL = (OFDMA_Duration + self.GiDL) * 10 ** (-6);  # [s]
        TsymLeg = (3.2 + 0.8) * 10 ** (-6);  # [s]
        TPHYLegacy = 20 * 10 ** (-6);

        if self.GiDL == 3.2:
            HELTFNDP = 12.8  # optional
            HELTFSU = 12.8
            HELTFMU = 12.8
            HELTFTB = 12.8

        elif self.GiDL == 1.6:
            HELTFNDP = 6.4
            HELTFSU = 6.4
            HELTFMU = 6.4
            HELTFTB = 6.4
        else:
            HELTFNDP = 0
            HELTFSU = 6.4
            HELTFMU = 6.4
            HELTFTB = 0

        TPHYSU = (36 + (HELTFSU + self.GiDL) * Vs) * 10 ** (-6);
        TPHYMU = (36 + (HELTFMU + self.GiDL) * Vs) * 10 ** (-6);
        TPHYTB = (40 + (HELTFTB + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        ## MAC Config
        MACHEADER = 28;
        FCS = 4;
        MPDUDel = 4;
        OM = MACHEADER + MPDUDel + FCS;

        Len = 4 * math.ceil((self.Ldata + 14) / 4);
        Ci = 8 * 4 * math.ceil((OM + self.AggMSDU * Len) / 4);

        Te = 9 * 10 ** (-6);  # [s]
        TSIFS = 16 * 10 ** (-6);  # [s]
        TDIFS = TSIFS + 2 * Te
        Tbo = float(self.CWmin) / 2 * Te;  # temps BO moyen, moyenne [0...15]
        TAIFS = TDIFS + self.AIFSN * Te  # 34        * 10**(-6) ; #[s]
        MAXPPDU = self.MaxPPDU

        ## Scenario Config
        alpha = self.a
        beta = self.b

        GpeMUMIMO = (self.S * self.Get_NSS() / self.Map)
        GpeOFDMA = (self.S / self.nru)

        if self.S == 1:
            nbgpe = 1
        else:
            if self.ofdma == 0:
                if GpeMUMIMO >= 2:
                    nbgpe = 2
                    # Nombre de users dans les 2 groupes
                    Nuser = self.S / (GpeMUMIMO / nbgpe)
                else:
                    nbgpe = 1
                    Nuser = self.S
            else:
                if self.mumimo == 0:
                    if GpeOFDMA >= 2:
                        nbgpe = 2
                        Nuser = self.S / (GpeOFDMA / nbgpe)
                    else:
                        nbgpe = 1
                        Nuser = self.S * self.nru / GpeMUMIMO
                else:
                    nbgpe = 1

        ######################################################
        # SU and MU Transmission Duration

        LTB = 18;
        LSF = 16;
        LMH = 320;
        LRTS = 160;
        LCTS = 112;
        LMURTS = 224 + 40 * Nuser;
        Ltrigger = 224 + 48 * Nuser;
        LBA = 256;
        LMSBACK = 176 + 288 * Nuser;  # [bits]
        TRTS = TPHYLegacy + math.ceil(float(LSF + LRTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMURTSVu = TPHYLegacy + math.ceil(float(LSF + LMURTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TCTS = TPHYLegacy + math.ceil(float(LSF + LCTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TBA = TPHYLegacy + math.ceil(float(LSF + LBA + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMSBACK = TPHYLegacy + math.ceil(float(LSF + LMSBACK + LTB) / datarateLEG) * TsymLeg;  # [s]
        TTBBACK = TPHYTB + math.ceil(float(LSF + LBA + LTB) / datarateOFDMA) * TsymUL;  # [s]
        TtriggerVu = TPHYLegacy + ((LSF + Ltrigger + LTB) / datarateLEG) * TsymLeg;  # [s]

        #########################################################################
        # B. Duration of the Channel Sounding Procedure

        LNDPA = 168 + 32 * Nuser;  # [bits]
        TNDP = (36 + (HELTFNDP + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        LBRB = 224 + 48 * Nuser;  # [bits]
        K = nbgpe;
        # LambdaCSI = 20; #[Attempts per seconds]
        LBREPORT = Breport;
        TNDPA = TPHYLegacy + math.ceil((LSF + LNDPA + LTB) / datarateLEG) * TsymLeg;  # [s]

        TBRPOLL = TPHYLegacy + math.ceil(LBRB / datarateLEG) * TsymLeg;  # [s]
        TBREPORT = TPHYTB + math.ceil((LSF + LMH + LBREPORT + LTB) / datarateOFDMA) * TsymDL;  # [s]

        Tcsi = self.tcsi * (TAIFS + TNDPA + TSIFS + TNDP + K * (TSIFS + TBRPOLL + TSIFS + TBREPORT));  # [s]

        Tdata = 1 / float(self.LambdaCSI) - Tcsi;  # [s]

        #########################################################################
        if self.RTSCTS == 0:
            RTSCTSMU = 0
            RTSCTSSU = 0
        elif self.RTSCTS == 1:
            RTSCTSMU = TMURTSVu + TSIFS + TCTS + TSIFS
            RTSCTSSU = TRTS + TSIFS + TCTS + TSIFS

        XSU = 1
        XMU = 1
        agg2SU = 1
        agg2MU = 1
        agg1SU = 1
        agg1MU = 1

        if self.S == 1:
            for na_su in range(self.AggMPDU, 0, -1):
                for Yi_su in range(self.AggMSDU, 0, -1):  # range(7, 0, -1):
                    Cisu = 8 * 4 * math.ceil((OM + Yi_su * Len) / 4);
                    TsuD = TPHYSU + math.ceil(float(na_su * (Cisu + 22)) / datarateSU) * TsymDL  # [s]
                    if TsuD < MAXPPDU:
                        if Yi_su * na_su > XSU:
                            agg2SU = Yi_su
                            agg1SU = na_su
                            XSU = Yi_su * na_su
            # print('DL: Yi SU: {} & NA SU: {}  --------- {}'.format( agg2SU, agg1SU , agg2SU* agg1SU ))
            Cisu = 8 * 4 * math.ceil((OM + agg2SU * Len) / 4);
            TsuD = TPHYSU + math.ceil(float(agg1SU * (Cisu + 22)) / datarateSU) * TsymDL  # [s]
            TsuDL = RTSCTSSU + TsuD + TSIFS + TBA + TAIFS;  # + Te ;  #[s]
            DL_SU = 10 ** (-6) * float(XSU * 8 * self.Ldata) / float(Tbo + TsuDL) * (Tdata / float(Tdata + Tcsi))

            SU = round(DL_SU, 1)
            return (SU, TsuDL, (XSU * 8 * self.Ldata))
        else:
            for na_mu in range(self.AggMPDU, -1, -1):
                for Yi_mu in range(self.AggMSDU, 0, -1):  # range(7, 0, -1):
                    Cimu = 8 * 4 * math.ceil((OM + Yi_mu * Len) / 4);
                    TmuD = TPHYMU + math.ceil(float(na_mu * (Cimu + 22 + (OM + 72) * 8)) / datarateMU) * TsymDL;  # [s]
                    TmuDL = RTSCTSMU + TmuD + TSIFS + TTBBACK + TAIFS;  # + Te ; #[s]
                    if Tbo + TmuD * nbgpe < self.TXOP:
                        if TmuD < MAXPPDU:
                            if Yi_mu * na_mu > XMU:
                                agg2MU = Yi_mu
                                agg1MU = na_mu
                                XMU = Yi_mu * na_mu
            # print('DL:  Yi MU: {} & NA MU: {}  --------- {}'.format( agg2MU, agg1MU , agg2MU* agg1MU ))
            Cimu = 8 * 4 * math.ceil((OM + agg2MU * Len) / 4);

            TmuD = TPHYMU + math.ceil(float(agg1MU * (Cimu + 22 + (OM + 72) * 8)) / datarateMU) * TsymDL;  # [s]
            TmuDL = RTSCTSMU + TmuD + TSIFS + TMSBACK + TAIFS;  # + Te ; #[s]

            DL_MU = 10 ** (-6) * (Tdata / float(Tdata + Tcsi)) * float(Nuser * XMU * 8 * self.Ldata) / float(
                Tbo + nbgpe * TmuDL)

            MU = round(DL_MU, 1)
            return (MU, Nuser, TmuD, XMU)

    def Th_UL(self):
        ## PHY Config
        """
           Calcul du débit UDP UL, en demande de l'AP (Trigger based)
        """

        Nuser = self.S
        # MUMIMO + OFDMA ou MUMIMO seul (nru = 1 )
        datarateMU = self.Phy_DataRate_MIMO_OFDMA()
        # SU sur toute la bande
        datarateSU = self.Phy_DataRate_Full_MIMO_Full_Band()
        # OFDMA seul pas forcément sur oute la bande
        datarateOFDMA = self.Phy_DataRate_Full_MIMO()
        # MU MIMO sur toute la bande
        datarateMIMO = self.Phy_DataRate_Full_Band()
        datarateLEG = 24;  # [bits / OFDM symbol ]( 1 * Ym * Yc * Ysc20 ) ;
        Vs = self.Get_NSS()
        Breport = self.BeamformingConfig()
        OFDMA_Duration = 12.8
        TsymUL = (OFDMA_Duration + self.GiUL) * 10 ** (-6);  # [s]
        TsymDL = (OFDMA_Duration + self.GiDL) * 10 ** (-6);  # [s]
        TsymLeg = 4 * 10 ** (-6);  # [s]
        TPHYLegacy = 20 * 10 ** (-6);

        if self.GiDL == 3.2:
            HELTFNDP = 12.8  # optional
            HELTFSU = 12.8
            HELTFMU = 12.8
            HELTFTB = 12.8

        elif self.GiDL == 1.6:
            HELTFNDP = 6.4
            HELTFSU = 6.4
            HELTFMU = 6.4
            HELTFTB = 6.4
        else:
            HELTFNDP = 0
            HELTFSU = 6.4
            HELTFMU = 6.4
            HELTFTB = 0

        TPHYSU = (36 + (HELTFSU + self.GiDL) * Vs) * 10 ** (-6);
        TPHYMU = (36 + (HELTFMU + self.GiDL) * Vs) * 10 ** (-6);
        TPHYTB = (40 + (HELTFTB + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        ## MAC Config
        MACHEADER = 28;
        FCS = 4;
        MPDUDel = 4;
        OM = MACHEADER + MPDUDel + FCS;

        Len = 4 * math.ceil((self.Ldata + 14) / 4);
        Ci = 8 * 4 * math.ceil((OM + self.AggMSDU * Len) / 4);

        Te = 9 * 10 ** (-6);  # [s]
        TSIFS = 16 * 10 ** (-6);  # [s]
        TDIFS = TSIFS + 2 * Te
        Tbo = float(self.CWmin) / 2 * Te;  # temps BO moyen, moyenne [0...15]
        TAIFS = TDIFS + self.AIFSN * Te  # 34        * 10**(-6) ; #[s]
        MAXPPDU = self.MaxPPDU

        ## Scenario Config
        alpha = self.a
        beta = self.b

        GpeMUMIMO = (self.S * self.Get_NSS() / self.Map)
        GpeOFDMA = (self.S / self.nru)
        if self.S == 1:
            nbgpe = 1
        else:
            if self.ofdma == 0:
                if GpeMUMIMO >= 2:
                    nbgpe = 2
                    # Nombre de users dans les 2 groupes
                    Nuser = self.S / (GpeMUMIMO / nbgpe)
                else:
                    nbgpe = 1
                    Nuser = self.S
            else:
                if self.mumimo == 0:
                    if GpeOFDMA >= 2:
                        nbgpe = 2
                        Nuser = self.S / (GpeOFDMA / nbgpe)
                    else:
                        nbgpe = 1
                        Nuser = self.S * self.nru / GpeMUMIMO
                else:
                    nbgpe = 1

        ######################################################
        # SU and MU Transmission Duration

        LTB = 18;
        LSF = 16;
        LMH = 320;
        LRTS = 160;
        LCTS = 112;
        LMURTS = 224 + 40 * Nuser;
        Ltrigger = 224 + 48 * Nuser;
        LBA = 256;
        LMSBACK = 176 + 288 * Nuser;  # [bits]
        TRTS = TPHYLegacy + math.ceil(float(LSF + LRTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMURTSVu = TPHYLegacy + math.ceil(float(LSF + LMURTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TCTS = TPHYLegacy + math.ceil(float(LSF + LCTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TBA = TPHYLegacy + math.ceil(float(LSF + LBA + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMSBACK = TPHYLegacy + math.ceil(float(LSF + LMSBACK + LTB) / datarateLEG) * TsymLeg;  # [s]
        TTBBACK = TPHYTB + math.ceil(float(LSF + LBA + LTB) / datarateMU) * TsymLeg;  # [s]
        TtriggerVu = TPHYLegacy + ((LSF + Ltrigger + LTB) / datarateLEG) * TsymLeg;  # [s]

        #########################################################################
        # B. Duration of the Channel Sounding Procedure

        LNDPA = 168 + 32 * Nuser;  # [bits]
        TNDP = (36 + (HELTFNDP + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        LBRB = 224 + 48 * Nuser;  # [bits]
        K = nbgpe;
        # LambdaCSI = 20; #[Attempts per seconds]
        LBREPORT = Breport;
        TNDPA = TPHYLegacy + math.ceil((LSF + LNDPA + LTB) / datarateLEG) * TsymLeg;  # [s]

        TBRPOLL = TPHYLegacy + math.ceil(LBRB / datarateLEG) * TsymLeg;  # [s]
        TBREPORT = TPHYTB + math.ceil((LSF + LMH + LBREPORT + LTB) / datarateOFDMA) * TsymDL;  # [s]

        Tcsi = self.tcsi * (TAIFS + TNDPA + TSIFS + TNDP + K * (TSIFS + TBRPOLL + TSIFS + TBREPORT));  # [s]

        Tdata = 1 / float(self.LambdaCSI) - Tcsi;  # [s]

        #########################################################################
        if self.RTSCTS == 0:
            RTSCTSMU = 0
            RTSCTSSU = 0
        elif self.RTSCTS == 1:
            RTSCTSMU = TMURTSVu + TSIFS + TCTS + TSIFS
            RTSCTSSU = TRTS + TSIFS + TCTS + TSIFS

        XSU = 1
        XMU = 1
        agg2SU = 1
        agg2MU = 1
        agg1SU = 1
        agg1MU = 1

        if self.S == 1:
            for na_su in range(self.AggMPDU, 0, -1):
                for Yi_su in range(self.AggMSDU, 0, -1):
                    Cisu = 8 * 4 * math.ceil((OM + Yi_su * Len) / 4);
                    TsuU = TPHYSU + math.ceil(float(na_su * (Cisu + 22)) / datarateSU) * TsymUL  # [s]
                    if TsuU < MAXPPDU:
                        if Yi_su * na_su > XSU:
                            agg2SU = Yi_su
                            agg1SU = na_su
                            XSU = agg2SU * agg1SU

            t = 8;
            TMultiback = TPHYTB + math.ceil(((22 + self.S * t) * 8 + 22) / datarateSU) * TsymDL;
            # print('UL: Yi SU: {} & NA SU: {}  --------- {}'.format( agg2SU, agg1SU , agg2SU* agg1SU ))
            Cisu = 8 * 4 * math.ceil((OM + agg2SU * Len) / 4);
            TsuU = TPHYSU + math.ceil(float(agg1SU * (Cisu + 22)) / datarateSU) * TsymUL  # [s]
            TsuUL = RTSCTSSU + TsuU + TSIFS + TBA + TAIFS;  # + Te ;  #[s]
            UL_SU = 10 ** (-6) * float(XSU * 8 * self.Ldata) / float(Tbo + TsuUL) * (Tdata / float(Tdata + Tcsi))

            SU = round(UL_SU, 1)
            return (SU, TsuUL)
        else:
            for na_mu in range(self.AggMPDU, 0, -1):
                for Yi_mu in range(self.AggMSDU, 0, -1):
                    Cimu = 8 * 4 * math.ceil((OM + Yi_mu * Len) / 4);
                    TmuU = TPHYMU + math.ceil(float(na_mu * (Cimu + 22 + (OM + 72) * 8)) / datarateMU) * TsymUL;  # [s]
                    TmuUL = RTSCTSMU + TtriggerVu + TmuU + TSIFS + TAIFS + TTBBACK;  # + Te ; #[s]
                    if TmuU * nbgpe + Tbo < self.TXOP:
                        if TmuU < MAXPPDU:
                            if Yi_mu * na_mu > XMU:
                                agg2MU = Yi_mu
                                agg1MU = na_mu
                                XMU = agg2MU * agg1MU
            if agg1MU == 256:
                t = 36;
                TMultiback = TPHYTB + math.ceil(((22 + self.S * t) * 8 + 22) / datarateMU) * TsymDL;
            elif agg1MU < 256:
                t = 12;
                TMultiback = TPHYTB + math.ceil(((22 + self.S * t) * 8 + 22) / datarateMU) * TsymDL;
            # print('UL: Yi MU: {} & NA MU: {}  --------- {}'.format( agg2MU, agg1MU , agg2MU* agg1MU ))
            Cimu = 8 * 4 * math.ceil((OM + agg2MU * Len) / 4);
            TmuU = TPHYMU + math.ceil(float(agg1MU * (Cimu + 22 + (OM + 72) * 8)) / datarateMU) * TsymUL;  # [s]

            TmuUL = RTSCTSMU + TtriggerVu + TmuU + TSIFS + TAIFS + TMSBACK;  # + Te ; #[s]

            UL_MU = 10 ** (-6) * float(Nuser * XMU * 8 * self.Ldata) / float(Tbo + TmuUL * nbgpe) * (
                    Tdata / float(Tdata + Tcsi))

            MU = round(UL_MU, 1)

            return (MU, Nuser, float(Tbo + nbgpe * TmuUL), XMU)

    def Th_TCP(self):
        """
           Calcul du débit TCP DL non Optimisé ( TCP ACK renvoyés séquentiellement )
        """

        ## PHY Config
        Nuser = self.S
        # MUMIMO + OFDMA ou MUMIMO seul (nru = 1 )
        datarateMU = self.Phy_DataRate_MIMO_OFDMA()
        # SU sur toute la bande
        datarateSU = self.Phy_DataRate_Full_MIMO_Full_Band()
        # OFDMA seul pas forcément sur oute la bande
        datarateOFDMA = self.Phy_DataRate_Full_MIMO()
        # MU MIMO sur toute la bande
        datarateMIMO = self.Phy_DataRate_Full_Band()
        datarateLEG = 24;  # [bits / OFDM symbol ]( 1 * Ym * Yc * Ysc20 ) ;
        Vs = self.Get_NSS()
        Breport = self.BeamformingConfig()
        OFDMA_Duration = 12.8
        TsymUL = (OFDMA_Duration + self.GiUL) * 10 ** (-6);  # [s]
        TsymDL = (OFDMA_Duration + self.GiDL) * 10 ** (-6);  # [s]
        TsymLeg = 4 * 10 ** (-6);  # [s]
        TPHYLegacy = 20 * 10 ** (-6);

        ## MAC Config
        LenD = self.LdataTCP;  # 464,208

        MACHEADER = 28;
        FCS = 4;
        MPDUDel = 4;
        OM = MACHEADER + MPDUDel + FCS;

        Len = 4 * math.ceil((LenD + 14) / 4);
        Ci = 8 * 4 * math.ceil((OM + self.AggMSDU * Len) / 4);

        Te = 9 * 10 ** (-6);  # [s]
        TSIFS = 16 * 10 ** (-6);  # [s]
        TDIFS = TSIFS + 2 * Te
        Tbo = float(self.CWmin) / 2 * Te;  # temps BO moyen, moyenne [0...15]
        TAIFS = TDIFS + self.AIFSN * Te  # 34        * 10**(-6) ; #[s]
        MAXPPDU = self.MaxPPDU

        ## Scenario Config
        alpha = self.a
        beta = self.b

        GpeMUMIMO = (self.S * self.Get_NSS() / self.Map)
        GpeOFDMA = (self.S / self.nru)
        if self.S == 1:
            nbgpe = 1
        else:
            if self.ofdma == 0:
                if GpeMUMIMO >= 2:
                    nbgpe = 2
                    # Nombre de users dans les 2 groupes
                    Nuser = self.S / (GpeMUMIMO / nbgpe)
                else:
                    nbgpe = 1
                    Nuser = self.S
            else:
                if self.mumimo == 0:
                    if GpeOFDMA >= 2:
                        nbgpe = 2
                        Nuser = self.S / (GpeOFDMA / nbgpe)
                    else:
                        nbgpe = 1
                        Nuser = self.S * self.nru / GpeMUMIMO
                else:
                    nbgpe = 1

        TCPack = 48;  # (20 of TCP header and 20 of IP header +8 of LLC SNAP)
        LenA = 64;

        if self.GiDL == 3.2:
            HELTFNDPD = 12.8  # optional
            HELTFSUD = 12.8
            HELTFMUD = 12.8
            HELTFTBD = 12.8

        elif self.GiDL == 1.6:
            HELTFNDPD = 6.4
            HELTFSUD = 6.4
            HELTFMUD = 6.4
            HELTFTBD = 6.4
        else:
            HELTFNDPD = 0
            HELTFSUD = 6.4
            HELTFMUD = 6.4
            HELTFTBD = 0

        TPHYSUD = (36 + (HELTFSUD + self.GiDL) * Vs) * 10 ** (-6);
        TPHYMUD = (36 + (HELTFMUD + self.GiDL) * Vs) * 10 ** (-6);
        TPHYTBD = (40 + (HELTFTBD + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        if self.GiUL == 3.2:
            HELTFNDPU = 12.8
            HELTFSUU = 12.8
            HELTFMUU = 12.8
            HELTFTBU = 12.8

        elif self.GiUL == 1.6:
            HELTFNDPU = 6.4
            HELTFSUU = 6.4
            HELTFMUU = 6.4
            HELTFTBU = 6.4
        else:
            HELTFNDPU = 0
            HELTFSUU = 6.4
            HELTFMUU = 6.4
            HELTFTBU = 0

        TPHYSUU = (36 + (HELTFSUU + self.GiUL) * Vs) * 10 ** (-6);
        TPHYMUU = (36 + (HELTFMUU + self.GiUL) * Vs) * 10 ** (-6);
        TPHYTBU = (36 + (HELTFTBU + self.GiUL) * Vs) * 10 ** (-6);  # [s]

        LTB = 18;
        LSF = 16;
        LRTS = 160;
        LCTS = 112;
        LMURTS = 224 + 40 * Nuser;
        Ltrigger = 224 + 48 * Nuser;
        LBA = 256;
        LMSBACK = 176 + 288 * Nuser;  # [bits]

        LMH = 320;

        TRTS = TPHYLegacy + math.ceil(float(LSF + LRTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMURTSVu = TPHYLegacy + math.ceil(float(LSF + LMURTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TCTS = TPHYLegacy + math.ceil(float(LSF + LCTS + LTB) / datarateLEG) * TsymLeg;  # [s]

        TBA = TPHYLegacy + math.ceil(float(LSF + LBA + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMSBACK = TPHYLegacy + math.ceil(float(LSF + LMSBACK + LTB) / datarateLEG) * TsymLeg;  # [s]
        TTBBACK = TPHYTBD + math.ceil(float(LSF + LBA + LTB) / datarateOFDMA) * TsymUL;  # [s]
        TtriggerVu = TPHYLegacy + ((LSF + Ltrigger + LTB) / datarateLEG) * TsymLeg;  # [s]

        if self.RTSCTS == 0:
            RTSCTSMU = 0
            RTSCTSSU = 0
        elif self.RTSCTS == 1:
            RTSCTSMU = TMURTSVu + TSIFS + TCTS + TSIFS
            RTSCTSSU = TRTS + TSIFS + TCTS + TSIFS

        #########################################################################
        # B. Duration of the Channel Sounding Procedure

        LNDPA = 168 + 32 * Nuser;  # [bits]
        TNDP = (36 + (HELTFNDPD + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        LBRB = 224 + 48 * Nuser;  # [bits]
        K = nbgpe;
        # LambdaCSI = 20; #[Attempts per seconds]
        LBREPORT = Breport;
        TNDPA = TPHYLegacy + math.ceil((LSF + LNDPA + LTB) / datarateLEG) * TsymLeg;  # [s]

        TBRPOLL = TPHYLegacy + math.ceil(LBRB / datarateLEG) * TsymLeg;  # [s]
        TBREPORT = TPHYTBD + math.ceil((LSF + LMH + LBREPORT + LTB) / datarateOFDMA) * TsymDL;  # [s]

        Tcsi = self.tcsi * (TAIFS + TNDPA + TSIFS + TNDP + K * (TSIFS + TBRPOLL + TSIFS + TBREPORT));  # [s]

        Tdata = 1 / float(self.LambdaCSI) - Tcsi;  # [s]

        #########################################################################

        ## duree de transmission SU et MU

        XSUD = 1
        XMUD = 1
        XSUU = 1
        XMUU = 1

        agg2MUD = 1
        agg1MUD = 1
        agg2SUU = 1
        agg1SUU = 1

        if self.S == 1:
            for na_suU in range(self.AggMPDU, 0, -1):
                for Yi_suU in range(self.AggMSDU, 0, -1):
                    Cisu = 8 * 4 * math.ceil((OM + Yi_suU * Len) / 4);
                    TDataCycle = TPHYSUD + math.ceil(float(na_suU * (Cisu + 22)) / datarateSU) * TsymDL  # [s]
                    TAckCycle = TPHYTBU + TsymUL * (
                            (Yi_suU * na_suU * LenA + na_suU * OM * 8 + 22) / datarateOFDMA) + TBA
                    #    TPHYTBU+TsymUL*(   (( Yi_suU*na_suU* LenA + na_suU  *OM)*8+22)/datarateOFDMA)+ Tback1+2*TSIFS;
                    if TDataCycle < MAXPPDU:
                        if Yi_suU * na_suU > XSUU:
                            agg2SUU = Yi_suU
                            agg1SUU = na_suU
                            XSUU = Yi_suU * na_suU
            # print(' TCP Yi SU: {} & NA SU: {}  --------- {}'.format( agg2SUU, agg1SUU , agg2SUU* agg1SUU ))
            TAckCycle = TPHYTBU + TsymUL * ((agg2SUU * agg1SUU * LenA + agg1SUU * (OM) * 8 + 22) / datarateOFDMA) + TBA
            # TPHYTBU+TsymUL*((( agg2SUU*agg1SUU* LenA + agg1SUU  *OM)*8+22)/datarateOFDMA) +Tback1+2*TSIFS;

            Cisu = 8 * 4 * math.ceil((OM + agg2SUU * Len) / 4);
            TDataCycle = TPHYSUD + math.ceil(float(agg1SUU * (Cisu + 22)) / datarateSU) * TsymDL  # [s]

            Tdata1 = RTSCTSSU + TAIFS + TDataCycle + TAckCycle + TBA + TSIFS;
            XXX = (Tdata / float(Tdata + Tcsi))

            GP1 = 10 ** (-6) * XXX * ((XSUU * LenD * 8) / (float(Tbo + nbgpe * Tdata1)));
            return (GP1, float(Tbo + nbgpe * Tdata1), (XSUU * LenD * 8))
        else:
            for na_muD in range(self.AggMPDU, 0, -1):  # range(self.AggMPDU, 0, -1):
                for Yi_muD in range(self.AggMSDU, 0,
                                    -1):  # range( int(math.floor((self.AggMPDU*2)/(na_muD*self.AggMSDU))), 0, -1):
                    Cimu = 8 * 4 * math.ceil((OM + Yi_muD * Len) / 4);
                    TDataCycleMU = TPHYMUD + math.ceil(
                        float(na_muD * (Cimu + 22 + (OM + 72) * 8)) / datarateMU) * TsymDL  # [s]
                    if TDataCycleMU * nbgpe + Tbo < self.TXOP:
                        if TDataCycleMU < MAXPPDU:

                            if Yi_muD * na_muD > XMUD:
                                agg2MUD = Yi_muD
                                agg1MUD = na_muD
                                XMUD = Yi_muD * na_muD
            # print('TCP Yi MU: {} & NA MU: {}  --------- {}'.format( agg2MUD, agg1MUD , agg2MUD* agg1MUD ))
            Cimu = 8 * 4 * math.ceil((OM + agg2MUD * Len) / 4);
            TDataCycleMU = TPHYMUD + math.ceil(
                float(agg1MUD * (Cimu + 22 + (OM + 72) * 8)) / datarateMU) * TsymDL  # [s]

            mMSDU = (agg1MUD * agg2MUD * nbgpe * LenA)
            agg1MUDp = math.ceil(mMSDU / (Len * agg2MUD))
            agg2MUDp = agg2MUD

            TAckCycleMU = (Nuser / nbgpe) * (TtriggerVu + (
                    TsymUL * (agg2MUD * agg1MUD * LenA + agg1MUDp * (OM + 72) * 8 + 22) / datarateOFDMA) + TTBBACK)

            Tdata2 = RTSCTSMU + TAIFS + TSIFS + TMSBACK + TDataCycleMU + TAckCycleMU;

            XXX = (Tdata / float(Tdata + Tcsi))
            GP2 = 10 ** (-6) * XXX * ((XMUD * LenD * 8 * Nuser) / (float(Tbo + nbgpe * Tdata2)));

            # print('TDataCycleMU = {} / TAckCycleMU = {} / nbgpe = {} / Nuser = {} / Tdata2 = {}   ' .format(TDataCycleMU,TAckCycleMU  ,nbgpe  ,Nuser   , Tdata2   ))
            # print('agg1MUD = {} / agg1MUDp = {} / agg2MUD = {} / agg2MUDp = {}   ' .format(agg1MUD,agg1MUDp  ,agg2MUD  ,agg2MUDp      ))
            return (GP2, TDataCycleMU, XMUD)

    def Th_TCP_OP(self):
        """
           Calcul du débit TCP DL Optimisé ( TCP ACK renvoyés en MU dans la même TXOP )
        """

        ## PHY Config
        Nuser = self.S
        # MUMIMO + OFDMA ou MUMIMO seul (nru = 1 )
        datarateMU = self.Phy_DataRate_MIMO_OFDMA()
        # SU sur toute la bande
        datarateSU = self.Phy_DataRate_Full_MIMO_Full_Band()
        # OFDMA seul pas forcément sur oute la bande
        datarateOFDMA = self.Phy_DataRate_Full_MIMO()
        # MU MIMO sur toute la bande
        datarateMIMO = self.Phy_DataRate_Full_Band()
        datarateLEG = 24;  # [bits / OFDM symbol ]( 1 * Ym * Yc * Ysc20 ) ;
        Vs = self.Get_NSS()
        Breport = self.BeamformingConfig()
        OFDMA_Duration = 12.8
        TsymUL = (OFDMA_Duration + self.GiUL) * 10 ** (-6);  # [s]
        TsymDL = (OFDMA_Duration + self.GiDL) * 10 ** (-6);  # [s]
        TsymLeg = 4 * 10 ** (-6);  # [s]
        TPHYLegacy = 20 * 10 ** (-6);

        ## MAC Config
        LenD = self.LdataTCP;  # 464,208

        MACHEADER = 28;
        FCS = 4;
        MPDUDel = 4
        OM = MACHEADER + MPDUDel + FCS;

        Len = 4 * math.ceil((LenD + 14) / 4);
        Ci = 8 * 4 * math.ceil((OM + self.AggMSDU * Len) / 4);

        Te = 9 * 10 ** (-6);  # [s]
        TSIFS = 16 * 10 ** (-6);  # [s]
        TDIFS = TSIFS + 2 * Te
        Tbo = float(self.CWmin) / 2 * Te;  # temps BO moyen, moyenne [0...15]
        TAIFS = TDIFS + self.AIFSN * Te  # 34        * 10**(-6) ; #[s]
        MAXPPDU = self.MaxPPDU

        ## Scenario Config
        alpha = self.a
        beta = self.b

        GpeMUMIMO = (self.S * self.Get_NSS() / self.Map)
        GpeOFDMA = (self.S / self.nru)
        if self.S == 1:
            nbgpe = 1
        else:
            if self.ofdma == 0:
                if GpeMUMIMO >= 2:
                    nbgpe = 2
                    # Nombre de users dans les 2 groupes
                    Nuser = self.S / (GpeMUMIMO / nbgpe)
                else:
                    nbgpe = 1
                    Nuser = self.S
            else:
                if self.mumimo == 0:
                    if GpeOFDMA >= 2:
                        nbgpe = 2
                        Nuser = self.S / (GpeOFDMA / nbgpe)
                    else:
                        nbgpe = 1
                        Nuser = self.S * self.nru / GpeMUMIMO
                else:
                    nbgpe = 1

        TCPack = 48;  # (20 of TCP header and 20 of IP header +8 of LLC SNAP)
        LenA = 64;

        if self.GiDL == 3.2:
            HELTFNDPD = 12.8  # optional
            HELTFSUD = 12.8
            HELTFMUD = 12.8
            HELTFTBD = 12.8

        elif self.GiDL == 1.6:
            HELTFNDPD = 6.4
            HELTFSUD = 6.4
            HELTFMUD = 6.4
            HELTFTBD = 6.4
        else:
            HELTFNDPD = 0
            HELTFSUD = 6.4
            HELTFMUD = 6.4
            HELTFTBD = 0

        TPHYSUD = (36 + (HELTFSUD + self.GiDL) * Vs) * 10 ** (-6);
        TPHYMUD = (36 + (HELTFMUD + self.GiDL) * Vs) * 10 ** (-6);
        TPHYTBD = (40 + (HELTFTBD + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        if self.GiUL == 3.2:
            HELTFNDPU = 12.8
            HELTFSUU = 12.8
            HELTFMUU = 12.8
            HELTFTBU = 12.8

        elif self.GiUL == 1.6:
            HELTFNDPU = 6.4
            HELTFSUU = 6.4
            HELTFMUU = 6.4
            HELTFTBU = 6.4
        else:
            HELTFNDPU = 0
            HELTFSUU = 6.4
            HELTFMUU = 6.4
            HELTFTBU = 0

        TPHYSUU = (36 + (HELTFSUU + self.GiUL) * Vs) * 10 ** (-6);
        TPHYMUU = (36 + (HELTFMUU + self.GiUL) * Vs) * 10 ** (-6);
        TPHYTBU = (36 + (HELTFTBU + self.GiUL) * Vs) * 10 ** (-6);  # [s]

        LTB = 18;
        LSF = 16;
        LRTS = 160;
        LCTS = 112;
        LMURTS = 224 + 40 * Nuser;
        Ltrigger = 224 + 48 * Nuser;
        LBA = 256;
        LMSBACK = 176 + 288 * Nuser;  # [bits]

        LMH = 320;

        TRTS = TPHYLegacy + math.ceil(float(LSF + LRTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMURTSVu = TPHYLegacy + math.ceil(float(LSF + LMURTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TCTS = TPHYLegacy + math.ceil(float(LSF + LCTS + LTB) / datarateLEG) * TsymLeg;  # [s]

        TBA = TPHYLegacy + math.ceil(float(LSF + LBA + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMSBACK = TPHYLegacy + math.ceil(float(LSF + LMSBACK + LTB) / datarateLEG) * TsymLeg;  # [s]
        TTBBACK = TPHYTBD + math.ceil(float(LSF + LBA + LTB) / datarateOFDMA) * TsymUL;  # [s]

        TtriggerVu = TPHYLegacy + ((LSF + Ltrigger + LTB) / datarateLEG) * TsymLeg;  # [s]

        if self.RTSCTS == 0:
            RTSCTSMU = 0
            RTSCTSSU = 0
        elif self.RTSCTS == 1:
            RTSCTSMU = TMURTSVu + TSIFS + TCTS + TSIFS
            RTSCTSSU = TRTS + TSIFS + TCTS + TSIFS

        #########################################################################
        # B. Duration of the Channel Sounding Procedure

        LNDPA = 168 + 32 * Nuser;  # [bits]
        TNDP = (36 + (HELTFNDPD + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        LBRB = 224 + 48 * Nuser;  # [bits]
        K = nbgpe;
        # LambdaCSI = 20; #[Attempts per seconds]
        LBREPORT = Breport;
        TNDPA = TPHYLegacy + math.ceil((LSF + LNDPA + LTB) / datarateLEG) * TsymLeg;  # [s]

        TBRPOLL = TPHYLegacy + math.ceil(LBRB / datarateLEG) * TsymLeg;  # [s]
        TBREPORT = TPHYTBD + math.ceil((LSF + LMH + LBREPORT + LTB) / datarateOFDMA) * TsymDL;  # [s]

        Tcsi = self.tcsi * (TAIFS + TNDPA + TSIFS + TNDP + K * (TSIFS + TBRPOLL + TSIFS + TBREPORT));  # [s]

        Tdata = 1 / float(self.LambdaCSI) - Tcsi;  # [s]

        #########################################################################
        ## duree de transmission SU et MU

        XSUD = 1
        XMUD = 1
        XSUU = 1
        XMUU = 1

        agg2MUD = 1
        agg1MUD = 1
        agg2SUU = 1
        agg1SUU = 1

        if self.S == 1:
            for na_suU in range(self.AggMPDU, 0, -1):
                for Yi_suU in range(self.AggMSDU, 0, -1):
                    Cisu = 8 * 4 * math.ceil((OM + Yi_suU * Len) / 4);
                    TDataCycle = TPHYSUD + math.ceil(float(na_suU * (Cisu + 22)) / datarateSU) * TsymDL  # [s]
                    TAckCycle = TPHYTBU + TsymUL * (
                            (Yi_suU * na_suU * LenA + na_suU * OM * 8 + 22) / datarateOFDMA) + TBA
                    # TPHYTBU+ TsymUL*(   (( Yi_suU*na_suU* LenA + na_suU  *OM)*8+22)/datarateSU)
                    if TDataCycle < MAXPPDU:
                        if Yi_suU * na_suU > XSUU:
                            agg2SUU = Yi_suU
                            agg1SUU = na_suU
                            XSUU = Yi_suU * na_suU
            # print(' TCP Yi SU: {} & NA SU: {}  --------- {}'.format( agg2SUU, agg1SUU , agg2SUU* agg1SUU ))
            TAckCycle = TPHYTBU + TsymUL * ((agg2SUU * agg1SUU * LenA + agg1SUU * (OM) * 8 + 22) / datarateOFDMA) + TBA
            # TPHYTBU+TsymUL*((( agg2SUU*agg1SUU* LenA + agg1SUU  *OM)*8+22)/datarateMU) +Tback1+2*TSIFS;
            Cisu = 8 * 4 * math.ceil((OM + agg2SUU * Len) / 4);
            TDataCycle = TPHYSUD + math.ceil(float(agg1SUU * (Cisu + 22)) / datarateSU) * TsymDL  # [s]
            Tdata1 = RTSCTSSU + TAIFS + TDataCycle + TAckCycle + TBA + TSIFS;
            XXX = (Tdata / float(Tdata + Tcsi))

            GP1 = 10 ** (-6) * XXX * ((XSUU * LenD * 8) / (float(Tbo + nbgpe * Tdata1)));
            return (GP1, float(Tbo + nbgpe * Tdata1), (XSUU * LenD * 8))
        else:
            for na_muD in range(self.AggMPDU, 0, -1):  # range(self.AggMPDU, 0, -1):
                for Yi_muD in range(self.AggMSDU, 0,
                                    -1):  # range( int(math.floor((self.AggMPDU*2)/(na_muD*self.AggMSDU))), 0, -1):

                    Cimu = 8 * 4 * math.ceil((OM + Yi_muD * Len) / 4);
                    TDataCycleMU = TPHYMUD + math.ceil(
                        float(na_muD * (Cimu + 22 + (OM + 72) * 8)) / datarateMU) * TsymDL  # [s]

                    mMSDU1 = (na_muD * Yi_muD * nbgpe * LenA)
                    na_muDp = math.ceil(mMSDU1 / (LenD * Yi_muD))
                    Yi_muDp = Yi_muD

                    TAckCycleMU = TtriggerVu + TsymUL * (
                            (Yi_muD * na_muDp * LenA + na_muDp * (OM + 72) * 8 + 22) / datarateOFDMA) + TTBBACK
                    # PrB+Ttf+PrD+TsymUL*((( na_muD*Yi_muD   *LenA +  na_muDp  *OM)*8+22)/datarateMU)+PrB+TMulback+2*TSIFS;
                    Tdata2 = RTSCTSMU + TAIFS + TSIFS + TMSBACK + TDataCycleMU + TAckCycleMU;
                    if TDataCycleMU * nbgpe + Tbo + TAckCycleMU < self.TXOP:
                        if TDataCycleMU < MAXPPDU:
                            if Yi_muD * na_muD > XMUD:
                                agg2MUD = Yi_muD
                                agg1MUD = na_muD
                                XMUD = Yi_muD * na_muD
            # print('TCP Yi MU: {} & NA MU: {}  --------- {}'.format( agg2MUD, agg1MUD , agg2MUD* agg1MUD ))
            Cimu = 8 * 4 * math.ceil((OM + agg2MUD * Len) / 4);
            TDataCycleMU = TPHYMUD + math.ceil(
                float(agg1MUD * (Cimu + 22 + (OM + 72) * 8)) / datarateMU) * TsymDL  # [s]

            mMSDU = (agg1MUD * agg2MUD * nbgpe * LenA)
            agg1MUDp = math.ceil(mMSDU / (Len * agg2MUD))
            agg2MUDp = agg2MUD

            TAckCycleMU = TtriggerVu + TsymUL * (
                    ((agg2MUD * agg1MUD * LenA + agg1MUDp * (OM + 72)) * 8 + 22) / datarateOFDMA) + TTBBACK
            Tdata2 = RTSCTSMU + TAIFS + TSIFS + TMSBACK + TDataCycleMU + TAckCycleMU;

            GP2 = 10 ** (-6) * (Tdata / float(Tdata + Tcsi)) * (
                    (XMUD * LenD * 8 * Nuser) / (float(Tbo + nbgpe * Tdata2)));
            return (GP2, TDataCycleMU, XMUD)  # /nbgpe

    def Th_DL_UL(self):
        """
           Calcul du débit UDP (DL,UL)en fct de a et b
        """

        ## PHY Config
        Nuser = self.S
        # MUMIMO + OFDMA ou MUMIMO seul (nru = 1 )
        datarateMU = self.Phy_DataRate_MIMO_OFDMA()
        # SU sur toute la bande
        datarateSU = self.Phy_DataRate_Full_MIMO_Full_Band()
        # OFDMA seul pas forcément sur oute la bande
        datarateOFDMA = self.Phy_DataRate_Full_MIMO()
        # MU MIMO sur toute la bande
        datarateMIMO = self.Phy_DataRate_Full_Band()
        datarateLEG = 24;  # [bits / OFDM symbol ]( 1 * Ym * Yc * Ysc20 ) ;
        Vs = self.Get_NSS()
        Breport = self.BeamformingConfig()
        OFDMA_Duration = 12.8
        TsymUL = (OFDMA_Duration + self.GiUL) * 10 ** (-6);  # [s]
        TsymDL = (OFDMA_Duration + self.GiDL) * 10 ** (-6);  # [s]
        TsymLeg = 4 * 10 ** (-6);  # [s]
        TPHYLegacy = 20 * 10 ** (-6);

        if self.GiDL == 3.2:
            HELTFNDP = 12.8  # optional
            HELTFSU = 12.8
            HELTFMU = 12.8
            HELTFTB = 12.8

        elif self.GiDL == 1.6:
            HELTFNDP = 6.4
            HELTFSU = 6.4
            HELTFMU = 6.4
            HELTFTB = 6.4
        else:
            HELTFNDP = 0
            HELTFSU = 6.4
            HELTFMU = 6.4
            HELTFTB = 0

        TPHYSU = (36 + (HELTFSU + self.GiDL) * Vs) * 10 ** (-6);
        TPHYMU = (36 + (HELTFMU + self.GiDL) * Vs) * 10 ** (-6);
        TPHYTB = (40 + (HELTFTB + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        ## MAC Config
        MACHEADER = 28;
        FCS = 4;
        MPDUDel = 4;
        OM = MACHEADER + MPDUDel + FCS;

        Len = 4 * math.ceil((self.Ldata + 14) / 4);
        Ci = 8 * 4 * math.ceil((OM + self.AggMSDU * Len) / 4);

        Te = 9 * 10 ** (-6);  # [s]
        TSIFS = 16 * 10 ** (-6);  # [s]
        TDIFS = TSIFS + 2 * Te
        Tbo = float(self.CWmin) / 2 * Te;  # temps BO moyen, moyenne [0...15]
        TAIFS = TDIFS + self.AIFSN * Te  # 34        * 10**(-6) ; #[s]
        MAXPPDU = self.MaxPPDU

        ## Scenario Config
        alpha = self.a
        beta = self.b

        GpeMUMIMO = (self.S * self.Get_NSS() / self.Map)
        GpeOFDMA = (self.S / self.nru)
        if self.S == 1:
            nbgpe = 1
        else:
            if self.ofdma == 0:
                if GpeMUMIMO >= 2:
                    nbgpe = 2
                    # Nombre de users dans les 2 groupes
                    Nuser = self.S / (GpeMUMIMO / nbgpe)
                else:
                    nbgpe = 1
                    Nuser = self.S
            else:
                if self.mumimo == 0:
                    if GpeOFDMA >= 2:
                        nbgpe = 2
                        Nuser = self.S / (GpeOFDMA / nbgpe)
                    else:
                        nbgpe = 1
                        Nuser = self.S * self.nru / GpeMUMIMO
                else:
                    nbgpe = 1

        ######################################################
        # SU and MU Transmission Duration

        LTB = 18;
        LSF = 16;
        LMH = 320;
        LRTS = 160;
        LCTS = 112;
        LMURTS = 224 + 40 * Nuser;
        Ltrigger = 224 + 48 * Nuser;
        LBA = 256;
        LMSBACK = 176 + 288 * Nuser;  # [bits]
        TRTS = TPHYLegacy + math.ceil(float(LSF + LRTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMURTSVu = TPHYLegacy + math.ceil(float(LSF + LMURTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TCTS = TPHYLegacy + math.ceil(float(LSF + LCTS + LTB) / datarateLEG) * TsymLeg;  # [s]
        TBA = TPHYLegacy + math.ceil(float(LSF + LBA + LTB) / datarateLEG) * TsymLeg;  # [s]
        TMSBACK = TPHYLegacy + math.ceil(float(LSF + LMSBACK + LTB) / datarateLEG) * TsymLeg;  # [s]
        TTBBACK = TPHYTB + math.ceil(float(LSF + LBA + LTB) / datarateOFDMA) * TsymUL;  # [s]
        TtriggerVu = TPHYLegacy + ((LSF + Ltrigger + LTB) / datarateLEG) * TsymLeg;  # [s]

        if self.RTSCTS == 0:
            RTSCTSMU = 0
            RTSCTSSU = 0
        elif self.RTSCTS == 1:
            RTSCTSMU = TMURTSVu + TSIFS + TCTS + TSIFS
            RTSCTSSU = TRTS + TSIFS + TCTS + TSIFS

        XSUD = 1
        XMUD = 1
        XSUU = 1
        XMUU = 1

        agg2SUU = 1
        agg1SUU = 1
        agg2SUD = 1
        agg1SUD = 1
        agg1MUU = 1
        agg2MUU = 1
        agg1MUD = 1
        agg2MUD = 1

        ##    if S==1:
        for na_suU in range(self.AggMPDU, 0, -1):
            for Yi_suU in range(self.AggMSDU, 0, -1):
                CisuU = 8 * 4 * math.ceil((OM + Yi_suU * Len) / 4);
                TsuU = TPHYSU + math.ceil(float(na_suU * (CisuU + 22)) / datarateSU) * TsymUL  # [s]
                if TsuU < MAXPPDU:
                    if Yi_suU * na_suU > XSUU:
                        agg2SUU = Yi_suU
                        agg1SUU = na_suU
                        XSUU = agg2SUU * agg1SUU

        ##        tU = 8;
        ##        TMultiback  = TPHYTB    + math.ceil( ((22 +  S * tU)* 8  +22 )  / ( rBru ) ) * TsymDL ;
        # print('DLUL: Yi SU: {} & NA SU: {}  --------- {}'.format( agg2SUU, agg1SUU , agg2SUU* agg1SUU ))
        CisuU = 8 * 4 * math.ceil((OM + agg2SUU * Len) / 4);
        TsuU = TPHYSU + math.ceil(float(agg1SUU * (CisuU + 22)) / datarateSU) * TsymUL  # [s]
        TsuUL = RTSCTSSU + TsuU + TSIFS + TBA + TAIFS;  # + Te ;  #[s]

        for na_suD in range(self.AggMPDU, 0, -1):
            for Yi_suD in range(self.AggMSDU, 0, -1):  # range(7, 0, -1):
                CisuD = 8 * 4 * math.ceil((OM + Yi_suD * Len) / 4);
                TsuD = TPHYSU + math.ceil(float(na_suD * (CisuD + 22)) / datarateSU) * TsymDL  # [s]
                if TsuD < MAXPPDU:
                    if Yi_suD * na_suD > XSUD:
                        agg2SUD = Yi_suD
                        agg1SUD = na_suD
                        XSUD = Yi_suD * na_suD
        # print('DLUL: Yi SU: {} & NA SU: {}  --------- {}'.format( agg2SUD, agg1SUD , agg2SUD* agg1SUD ))
        CisuD = 8 * 4 * math.ceil((OM + agg2SUD * Len) / 4);
        TsuD = TPHYSU + math.ceil(float(agg1SUD * (CisuD + 22)) / datarateSU) * TsymDL  # [s]
        TsuDL = RTSCTSSU + TsuD + TSIFS + TBA + TAIFS;  # + Te ;  #[s]

        ##    else:
        for na_muU in range(self.AggMPDU, 0, -1):
            for Yi_muU in range(self.AggMSDU, 0, -1):
                CimuU = 8 * 4 * math.ceil((OM + Yi_muU * Len) / 4);
                TmuU = TPHYMU + math.ceil(float(na_muU * (CimuU + 22 + (OM + 72) * 8)) / datarateMU) * TsymUL;  # [s]
                TmuUL = RTSCTSMU + TtriggerVu + TSIFS + + TmuU + TSIFS + TAIFS + TMSBACK;  # + Te ; #[s]
                if TmuU * nbgpe + Tbo < self.TXOP:
                    if TmuU < MAXPPDU:
                        if Yi_muU * na_muU > XMUU:
                            agg2MUU = Yi_muU
                            agg1MUU = na_muU
                            XMUU = agg2MUU * agg1MUU
        # print('DLUL: Yi MU: {} & NA MU: {}  --------- {}'.format( agg2MUU, agg1MUU , agg2MUU* agg1MUU ))
        CimuU = 8 * 4 * math.ceil((OM + agg2MUU * Len) / 4);
        TmuU = TPHYMU + math.ceil(float(agg1MUU * (CimuU + 22 + (OM + 72) * 8)) / datarateMU) * TsymUL;  # [s]
        TmuUL = RTSCTSMU + TtriggerVu + TSIFS + + TmuU + TSIFS + TAIFS + TMSBACK;  # + Te ; #[s]

        for na_muD in range(self.AggMPDU, -1, -1):
            for Yi_muD in range(self.AggMSDU, 0, -1):  # range(7, 0, -1):
                CimuD = 8 * 4 * math.ceil((OM + Yi_muD * Len) / 4);
                TmuD = TPHYMU + math.ceil(float(na_muD * (CimuD + 22 + (OM + 72) * 8)) / datarateMU) * TsymDL;  # [s]
                TmuDL = RTSCTSMU + TmuD + TSIFS + TTBBACK + TAIFS;  # + Te ; #[s]
                if TmuD * nbgpe + Tbo < self.TXOP:
                    if TmuD < MAXPPDU:
                        if Yi_muD * na_muD > XMUD:
                            agg2MUD = Yi_muD
                            agg1MUD = na_muD
                            XMUD = Yi_muD * na_muD
        # print('DLUL: Yi MU: {} & NA MU: {}  --------- {}'.format( agg2MUD, agg1MUD , agg2MUD* agg1MUD ))
        CimuD = 8 * 4 * math.ceil((OM + agg2MUD * Len) / 4);
        TmuD = TPHYMU + math.ceil(float(agg1MUD * (CimuD + 22 + (OM + 72) * 8)) / datarateMU) * TsymDL;  # [s]
        TmuDL = RTSCTSMU + TmuD + TSIFS + TMSBACK + TAIFS;  # + Te ; #[s]

        #########################################################################
        # B. Duration of the Channel Sounding Procedure

        LNDPA = 168 + 32 * Nuser;  # [bits]
        TNDP = (36 + (HELTFNDP + self.GiDL) * Vs) * 10 ** (-6);  # [s]

        LBRB = 224 + 48 * Nuser;  # [bits]
        K = nbgpe;
        # LambdaCSI = 20; #[Attempts per seconds]
        LBREPORT = Breport;
        TNDPA = TPHYLegacy + math.ceil((LSF + LNDPA + LTB) / datarateLEG) * TsymLeg;  # [s]

        TBRPOLL = TPHYLegacy + math.ceil(LBRB / datarateLEG) * TsymLeg;  # [s]
        TBREPORT = TPHYTB + math.ceil((LSF + LMH + LBREPORT + LTB) / datarateOFDMA) * TsymDL;  # [s]

        Tcsi = self.tcsi * (TAIFS + TNDPA + TSIFS + TNDP + K * (TSIFS + TBRPOLL + TSIFS + TBREPORT));  # [s]

        Tdata = 1 / float(self.LambdaCSI) - Tcsi;  # [s]

        #########################################################################
        # C. Probability of Successful Transmissions and Collisions

        (Toap, Tosta, pcap, pcsta) = self.Collision_Config(Nuser)  # Nuser or self.S ??
        Tacktimeout = TCTS + TAIFS;  # +Te; #[s]
        Tcsu = TRTS + TSIFS + Tacktimeout;  # [s]
        Tcmu = TMURTSVu + TSIFS + Tacktimeout;  # [s]

        a1 = float(alpha) * float(Toap) * ((1 - float(Tosta)) ** Nuser);
        a2 = Nuser * float(Tosta) * (1 - float(Toap)) * ((1 - float(Tosta)) ** (Nuser - 1));
        a3 = (1 - float(alpha)) * float(beta) * float(Toap) * (1 - float(Tosta)) ** Nuser;
        a4 = (1 - float(alpha)) * (1 - float(beta)) * float(Toap) * (1 - float(Tosta)) ** Nuser;
        b1 = (1 - float(Toap)) * (1 - float(Tosta)) ** Nuser;
        # No collision
        # c1 = 0;#  float(alpha)* float(Toap)*(1 - (1 - float(Tosta))^N);
        # c2 = 0;# (1-float(alpha))*float(beta)*float(Toap)*(1 - (1 - float(Tosta))^N);
        # c3 = 0;# (1-float(alpha))*(1-float(beta))*float(Toap)*(1 - (1 - float(Tosta))^N);
        # c4 = 0;# 1-a1-a2-a3-a4-b1-c1-c2-c3;
        c1 = float(alpha) * float(Toap) * (1 - (1 - float(Tosta)) ** Nuser);
        c2 = (1 - float(alpha)) * float(beta) * float(Toap) * (1 - (1 - float(Tosta)) ** Nuser);
        c3 = (1 - float(alpha)) * (1 - float(beta)) * float(Toap) * (1 - (1 - float(Tosta)) ** Nuser);
        c4 = 1 - a1 - a2 - a3 - a4 - b1 - c1 - c2 - c3;

        #######################################################
        # D. UL and DL Throughput
        Ta1 = TsuDL;
        Ta2 = TsuUL;
        Ta3 = TmuDL * nbgpe + Tbo;
        Ta4 = TmuUL * nbgpe + Tbo;  # [s]
        Tc1 = Tcsu;  # [s]Tbo ; #Tcsu ; #[s]
        Tc4 = Tcsu;  # [s]Tbo ; #Tcsu; #[s]
        Tc2 = Tcmu;  # [s] Tbo ; #Tcmu ; #[s]
        Tc3 = Tcmu;  # [s] Tbo ; #Tcmu ;  #[s]

        # Tcsi = 0; # channel sounding disabled
        ##[Mbits/s] Throughputs du Système

        Sd1 = XSUD * a1 * self.Ldata * 8 + XMUD * a3 * Nuser * self.Ldata * 8
        Sd2 = b1 * Te + a1 * (Ta1 + Te) + a2 * (Ta2 + Te) + a3 * (Ta3 + Te) + a4 * (Ta4 + Te) + c1 * (Tc1 + Te) + c2 * (
                Tc2 + Te) + c3 * (Tc3 + Te) + c4 * (Tc4 + Te)

        Su1 = XSUU * a2 * self.Ldata * 8 + XMUU * a4 * Nuser * self.Ldata * 8
        Su2 = b1 * Te + a1 * (Ta1 + Te) + a2 * (Ta2 + Te) + a3 * (Ta3 + Te) + a4 * (Ta4 + Te) + c1 * (Tc1 + Te) + c2 * (
                Tc2 + Te) + c3 * (Tc3 + Te) + c4 * (Tc4 + Te)

        Su = 10 ** (-6) * float(Su1 / Su2) * (Tdata / float(Tdata + Tcsi));
        Sd = 10 ** (-6) * float(Sd1 / Sd2) * (Tdata / float(Tdata + Tcsi));

        return (Sd, Su)


def Pathloss(d):
    # Received P
    PL = (23 - (38.66 + 10 * 4.2 * math.log10(d) + 6.87))
    return PL


def Calcul_Gain_MIMO(ntx, nrx, nss, bf, los, UL):
    # NLOS(gainP) %LOS(gainC)
    # nss 1                # nss 2                 # nss 3                # nss 4
    UL48RX = [[8.2333, 7.0614], [7.7040, 7.4471], [6.6303, 6.5047], [5.3276, 5.4586]]

    DL84RX = [[8.0385, 4.5464], [4.0490, 3.9115], [2.2869, 2.2659], [0, 0]]

    DL83RX = [[3.7345, 3.2471], [2.4397, 2.2903], [0.0132, 0.000096050], [0, 0]]

    DL82RX = [[1.8567, 1.4943], [0, 0], [0, 0], [0, 0]]

    DL44RX = [[5.9884, 4.4400], [3.8363, 3.6664], [4.2514, 1.9947], [0, 0]]

    DL43RX = [[3.6635, 3.1546], [2.1834, 2.0715], [0, 0], [0, 0]]

    DL42RX = [[1.7644, .3777], [0, 0], [0, 0], [0, 0]]

    DL84BF = [[3.8349, 4.0922], [4.0494, 3.9760], [4.0417, 3.8891], [3.8572, 3.7267]]

    DL83BF = [[4.2342, 4.3160], [4.5954, 4.3460], [4.8751, 4.6109], [0, 0]]

    DL82BF = [[4.8519, 4.6235], [5.7064, 5.3699], [0, 0], [0, 0]]

    DL81BF = [[6.6830, 5.9455], [0, 0], [0, 0], [0, 0]]

    DL44BF = [[2.6, 3], [2.5, 2.7], [1.8, 1.8], [0, 0]]

    DL43BF = [[3, 3.3], [2.9, 2.9], [2.2, 2.2], [0, 0]]

    DL42BF = [[3.4, 3.4], [3.7, 3.6], [0, 0], [0, 0]]

    DL41BF = [[4.8, 4.4], [0, 0], [0, 0], [0, 0]]

    DL33BF = [[2.4, 2.6], [1.9, 2], [0, 0], [0, 0]]

    DL32BF = [[2.7, 2.8], [2.5, 2.5], [0, 0], [0, 0]]

    DL31BF = [[3.9, 3.6], [0, 0], [0, 0], [0, 0]]

    DL22BF = [[1.5, 1.5], [0, 0], [0, 0], [0, 0]]

    DL21BF = [[2.3, 2], [0, 0], [0, 0], [0, 0]]

    Div_Gain = [0, 0, 0, 0]
    BF_Gain = [0, 0, 0, 0]
    if bf == 0:
        BF_Gain = [0, 0, 0, 0];
    elif ntx == 8:
        if nrx == 4:
            if los == 1:
                BF_Gain = [DL84BF[i][1] for i in range(len(DL84BF))]
            elif los == 0:
                BF_Gain = [DL84BF[i][0] for i in range(len(DL84BF))]

        elif nrx == 3:
            if los == 1:
                BF_Gain = [DL83BF[i][1] for i in range(len(DL83BF))]
            elif los == 0:
                BF_Gain = [DL83BF[i][0] for i in range(len(DL83BF))]

        elif nrx == 2:
            if los == 1:
                BF_Gain = [DL82BF[i][1] for i in range(len(DL82BF))]
            elif los == 0:
                BF_Gain = [DL82BF[i][0] for i in range(len(DL82BF))]

        elif nrx == 1:
            if los == 1:
                BF_Gain = [DL81BF[i][1] for i in range(len(DL81BF))]
            elif los == 0:
                BF_Gain = [DL81BF[i][0] for i in range(len(DL81BF))]

    elif ntx == 4:
        if nrx == 4:
            if los == 1:
                BF_Gain = [DL44BF[i][1] for i in range(len(DL44BF))]
            elif los == 0:
                BF_Gain = [DL44BF[i][0] for i in range(len(DL44BF))]

        elif nrx == 3:
            if los == 1:
                BF_Gain = [DL43BF[i][1] for i in range(len(DL43BF))]
            elif los == 0:
                BF_Gain = [DL43BF[i][0] for i in range(len(DL43BF))]

        elif nrx == 2:
            if los == 1:
                BF_Gain = [DL42BF[i][1] for i in range(len(DL42BF))]
            elif los == 0:
                BF_Gain = [DL42BF[i][0] for i in range(len(DL42BF))]

        elif nrx == 1:
            if los == 1:
                BF_Gain = [DL41BF[i][1] for i in range(len(DL41BF))]
            elif los == 0:
                BF_Gain = [DL41BF[i][0] for i in range(len(DL41BF))]

    elif ntx == 3:
        if nrx == 3:
            if los == 1:
                BF_Gain = [DL33BF[i][1] for i in range(len(DL33BF))]
            elif los == 0:
                BF_Gain = [DL33BF[i][0] for i in range(len(DL33BF))]

        elif nrx == 2:
            if los == 1:
                BF_Gain = [DL32BF[i][1] for i in range(len(DL32BF))]
            elif los == 0:
                BF_Gain = [DL32BF[i][0] for i in range(len(DL32BF))]

        elif nrx == 1:
            if los == 1:
                BF_Gain = [DL31BF[i][1] for i in range(len(DL31BF))]
            elif los == 0:
                BF_Gain = [DL31BF[i][0] for i in range(len(DL31BF))]

    elif ntx == 2:
        if nrx == 2:
            if los == 1:
                BF_Gain = [DL22BF[i][1] for i in range(len(DL22BF))]
            elif los == 0:
                BF_Gain = [DL22BF[i][0] for i in range(len(DL22BF))]

        elif nrx == 1:
            if los == 1:
                BF_Gain = [DL21BF[i][1] for i in range(len(DL21BF))]
            elif los == 0:
                BF_Gain = [DL21BF[i][0] for i in range(len(DL21BF))]

    if nss == 8:
        Div_Gain = [0, 0, 0, 0]
    else:
        if UL == 0:
            if ntx == 8:
                if nrx == 4:
                    if los == 1:
                        Div_Gain = [DL84RX[i][1] for i in range(len(DL84RX))]
                    elif los == 0:
                        Div_Gain = [DL84RX[i][0] for i in range(len(DL84RX))]

                elif nrx == 3:
                    if los == 1:
                        Div_Gain = [DL83RX[i][1] for i in range(len(DL83RX))]
                    elif los == 0:
                        Div_Gain = [DL83RX[i][0] for i in range(len(DL83RX))]

                elif nrx == 2:
                    if los == 1:
                        Div_Gain = [DL82RX[i][1] for i in range(len(DL82RX))]
                    elif los == 0:
                        Div_Gain = [DL82RX[i][0] for i in range(len(DL82RX))]

                else:
                    Div_Gain = [0, 0, 0, 0]

            elif ntx == 4:
                if nrx == 4:
                    if los == 1:
                        Div_Gain = [DL44RX[i][1] for i in range(len(DL44RX))]
                    elif los == 0:
                        Div_Gain = [DL44RX[i][0] for i in range(len(DL44RX))]

                elif nrx == 3:
                    if los == 1:
                        Div_Gain = [DL43RX[i][1] for i in range(len(DL43RX))]
                    elif los == 0:
                        Div_Gain = [DL43RX[i][0] for i in range(len(DL43RX))]

                elif nrx == 2:
                    if los == 1:
                        Div_Gain = [DL42RX[i][1] for i in range(len(DL42RX))]
                    elif los == 0:
                        Div_Gain = [DL42RX[i][0] for i in range(len(DL42RX))]

                else:
                    Div_Gain = [0, 0, 0, 0]


        elif UL == 1:
            if los == 1:
                Div_Gain = [UL48RX[i][1] for i in range(len(UL48RX))]
            elif los == 0:
                Div_Gain = [UL48RX[i][0] for i in range(len(UL48RX))]

    Gain = Div_Gain[nss - 1] + BF_Gain[nss - 1]
    return Gain


def SensTreshold(B, nss, dcm):
    # mcs 0 dcm   #mcs 0   # mcs 1 dcm    # mcs 1   # mcs 2   # mcs 3 dcm  # mcs 3   # mcs 4 dcm   # mcs 4   # mcs 5     # mcs 6    # mcs 7      # mcs 8   # mcs 9   # mcs 10      # mcs 11
    mcs = [[-82, -79, -76, -73], [-82, -79, -76, -73], [-82, -79, -76, -73], [-79, -76, -73, -70], [-77, -74, -71, -68],
           [-79, -76, -73, -70], [-74, -71, -68, -65], [-77, -74, -71, -68], [-70, -67, -64, -61], [-66, -63, -60, -57],
           [-65, -62, -59, -56], [-64, -61, -58, -55], [-59, -56, -53, -50], [-57, -54, -51, -48], [-54, -51, -48, -45],
           [-52, -49, -46, -43]]
    decrease = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [3, 3, 3, 3], [3, 3, 3, 3],
                [3, 3, 3, 3], [3, 3, 3, 3], [4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [5, 5, 5, 5], [5, 5, 5, 5],
                [6, 6, 6, 6], [6, 6, 6, 6]]
    nss_Gain = [0, 1.6, 3, 4, 5, 6, 7, 8]
    ST = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
          [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
          [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(len(mcs)):
        for j in range(len(mcs[i])):
            ST[i][j] = mcs[i][j] - decrease[i][j] + nss_Gain[nss - 1]

    if B == 20:
        ST = [ST[i][0] for i in range(len(ST))]
    elif B == 40:
        ST = [ST[i][1] for i in range(len(ST))]
    elif B == 80:
        ST = [ST[i][2] for i in range(len(ST))]
    elif B == 160:
        ST = [ST[i][3] for i in range(len(ST))]

    if dcm == 1:
        ST = [ST[0], ST[2], ST[4], ST[5], ST[7], ST[9], ST[10], ST[11], ST[12], ST[13], ST[14], ST[15]];

    elif dcm == 0:
        ST = [ST[1], ST[3], ST[4], ST[6], ST[8], ST[9], ST[10], ST[11], ST[12], ST[13], ST[14], ST[15]];

    return ST


def Throughput_vs_Dist():
    """
       Test des débit en fonction de la distance.
       En lecture les fichiers CSV issus de Matlab ( distance en lignes  vs mcs )
       Converti la MCS en Débit selon les setups  défins dans les boucles.
       En sortie, des fichiers CSV  (1 par setup) qui contient les débits 'Phy' , 'DL', 'UL' et 'TCP' en fct de la distance
    """

    now = datetime.datetime.now()

    ListS = [64]  # En mumimo-ofdma, en 20Mhz pas de S = 32 ni 64, en 40Mhz pa de S = 64  aussi
    fieldnames = ['Phy', 'DL', 'UL', 'TCP']  # , 'DLUL_DL' ,'DLUL_UL'  ]
    for S in ListS:
        path = 'RES\S' + str(S)

        Band20 = IEEE80211ax(20, 4, 8, S, 256, 7, 3.2, 3.2, 0.2, 0.8, 'AX_BE', 20, 8, 8, 1, 1, 0)
        Band40 = IEEE80211ax(40, 4, 8, S, 256, 7, 3.2, 3.2, 0.2, 0.8, 'AX_BE', 20, 8, 8, 1, 1, 0)
        Band80 = IEEE80211ax(80, 4, 8, S, 256, 7, 3.2, 3.2, 0.2, 0.8, 'AX_BE', 20, 8, 8, 1, 1, 0)
        Band160 = IEEE80211ax(160, 4, 8, S, 256, 7, 3.2, 3.2, 0.2, 0.8, 'AX_BE', 20, 8, 8, 1, 1, 0)
        pr = cProfile.Profile()
        pr.enable()

        ################################################  #BF # No_BF ### OFDMA_NO_MUMIMO   #Band20  #############################################
        print('---------S = {}   / #BF # No_BF ### OFDMA_NO_MUMIMO   #Band20 -------------  {} '.format(S, str(now)))
        nru = 1
        with open(path + '\BF_OFDMAonly20_1.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band20.Get_NSS()

                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru)))];
                mcs20_BF = MCS_Matlab_BF[i, 0]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        pr.disable()
        ss = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=ss).sort_stats(sortby)
        ps.print_stats()
        print(ss.getvalue())
        with open(path + '\OFDMAonly20_1.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band20.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru)))];
                mcs20_BF = MCS_Matlab_BF[i, 0]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        nru = 2
        with open(path + '\BF_OFDMAonly20_2.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band20.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru)))];
                mcs20_BF = MCS_Matlab_BF[i, 0]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\OFDMAonly20_2.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band20.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru)))];
                mcs20_BF = MCS_Matlab_BF[i, 0]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        nru = 4
        with open(path + '\BF_OFDMAonly20_4.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band20.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru)))];
                mcs20_BF = MCS_Matlab_BF[i, 0]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\OFDMAonly20_4.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band20.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru)))];
                mcs20_BF = MCS_Matlab_BF[i, 0]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        nru = 8
        with open(path + '\BF_OFDMAonly20_8.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band20.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru)))];
                mcs20_BF = MCS_Matlab_BF[i, 0]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\OFDMAonly20_8.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band20.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru)))];
                mcs20_BF = MCS_Matlab_BF[i, 0]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(20 / (S * 20 / nru))) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
            ################################################  #BF # No_BF ### OFDMA_NO_MUMIMO   #Band40  #############################################
        print('---------S = {}   / #BF # No_BF ### OFDMA_NO_MUMIMO   #Band40 -------------  {} '.format(S, str(now)))
        nru = 1
        with open(path + '\BF_OFDMAonly40_1.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()

                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly40_1.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        nru = 2
        with open(path + '\BF_OFDMAonly40_2.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\OFDMAonly40_2.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        nru = 4
        with open(path + '\BF_OFDMAonly40_4.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\OFDMAonly40_4.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        nru = 8
        with open(path + '\BF_OFDMAonly40_8.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\OFDMAonly40_8.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        nru = 16
        with open(path + '\BF_OFDMAonly40_16.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\OFDMAonly40_16.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band40.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru)))];
                mcs40_BF = MCS_Matlab_BF[i, 1]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(40 / (S * 40 / nru))) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
            ################################################  #BF # No_BF ### OFDMA_NO_MUMIMO   #Band80  #############################################
        print('---------S = {}   / #BF # No_BF ### OFDMA_NO_MUMIMO   #Band80 -------------  {} '.format(S, str(now)))
        nru = 1
        with open(path + '\BF_OFDMAonly80_1.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly80_1.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 2
        with open(path + '\BF_OFDMAonly80_2.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\OFDMAonly80_2.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 4
        with open(path + '\BF_OFDMAonly80_4.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly80_4.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 8
        with open(path + '\BF_OFDMAonly80_8.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly80_8.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 16
        with open(path + '\BF_OFDMAonly80_16.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly80_16.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 32
        with open(path + '\BF_OFDMAonly80_32.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly80_32.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band80.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru)))];
                mcs80_BF = MCS_Matlab_BF[i, 2]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(80 / (S * 80 / nru))) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

                ################################################  #BF # No_BF ### OFDMA_NO_MUMIMO   #Band160  #############################################
        print('---------S = {}   / #BF # No_BF ### OFDMA_NO_MUMIMO   #Band160 -------------  {} '.format(S, str(now)))
        nru = 1
        with open(path + '\BF_OFDMAonly160_1.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly160_1.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 2
        with open(path + '\BF_OFDMAonly160_2.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly160_2.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 4
        with open(path + '\BF_OFDMAonly160_4.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly160_4.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 8
        with open(path + '\BF_OFDMAonly160_8.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly160_8.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 16
        with open(path + '\BF_OFDMAonly160_16.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly160_16.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        nru = 32
        with open(path + '\BF_OFDMAonly160_32.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly160_32.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 64
        with open(path + '\BF_OFDMAonly160_64.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 1, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSavecBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\OFDMAonly160_64.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 0, 1, nru, 0, 1, 1, 1)
                nss = Band160.Get_NSS()
                Mat_File_BF = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + '.mat'
                MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                MCS_Matlab_BF = MCS_Matlab_BF['OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru)))];
                mcs160_BF = MCS_Matlab_BF[i, 3]

                Mat_File_BFUL = 'SNR\OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL[
                    'OFDMAOnlyMCSsansBF84' + str(nss) + str(int(160 / (S * 160 / nru))) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

            ##########################################################################################################################################

        nru = 1
        ################################################  #BF # No_BF ### MUMIMO_NO_OFDMA   #Band20  #############################################
        print('---------S = {}   / #BF # No_BF ### MUMIMO_NO_OFDMA   #Band20 -------------  {} '.format(S, str(now)))
        with open(path + '\BF_MUMIMOonly20.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 1, 0, 1, 1, 1, 1, 1)
                if S == 1:
                    nss = Band20.Get_NSS()
                else:
                    nss = 0
                Mat_File = 'SNR\MCSavecBF84' + str(nss) + '.mat'
                MCS_Matlab = sio.loadmat(Mat_File)
                MCS_Matlab = MCS_Matlab['MCSavecBF84' + str(nss)];
                mcs20 = MCS_Matlab[i, 2]

                Mat_File_BFUL = 'SNR\MCSavecBF84' + str(nss) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSavecBF84' + str(nss) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 2]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\MUMIMOonly20.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band20.setup(1350, 1460, 0, 0, 0, 1, 1, 1, 1, 1)
                if S == 1:
                    nss = Band20.Get_NSS()
                else:
                    nss = 0
                Mat_File = 'SNR\MCSsansBF84' + str(nss) + '.mat'
                MCS_Matlab = sio.loadmat(Mat_File)
                MCS_Matlab = MCS_Matlab['MCSsansBF84' + str(nss)];
                mcs20 = MCS_Matlab[i, 2]

                Mat_File_BFUL = 'SNR\MCSsansBF84' + str(nss) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSsansBF84' + str(nss) + 'UL'];
                mcs20_BFUL = MCS_Matlab_BFUL[i, 2]

                Band20.SetNRU(nru)
                Band20.RunConfig(mcs20, mcs20_BFUL)
                PhyDR = Band20.Get_Phy_Datarate()
                DL = Band20.Get_AP_UDP_Throughput_DL()
                UL = Band20.Get_AP_UDP_Throughput_UL()
                TCP = Band20.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
            ################################################  #BF # No_BF ### MUMIMO_NO_OFDMA   #Band40  #############################################
        print('---------S = {}   / #BF # No_BF ### MUMIMO_NO_OFDMA   #Band40 -------------  {} '.format(S, str(now)))
        with open(path + '\BF_MUMIMOonly40.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 1, 0, 1, 1, 1, 1, 1)
                if S == 1:
                    nss = Band40.Get_NSS()
                else:
                    nss = 0
                Mat_File = 'SNR\MCSavecBF84' + str(nss) + '.mat'
                MCS_Matlab = sio.loadmat(Mat_File)
                MCS_Matlab = MCS_Matlab['MCSavecBF84' + str(nss)];
                mcs40 = MCS_Matlab[i, 2]

                Mat_File_BFUL = 'SNR\MCSavecBF84' + str(nss) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSavecBF84' + str(nss) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 2]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\MUMIMOonly40.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band40.setup(1350, 1460, 0, 0, 0, 1, 1, 1, 1, 1)
                if S == 1:
                    nss = Band40.Get_NSS()
                else:
                    nss = 0
                Mat_File = 'SNR\MCSsansBF84' + str(nss) + '.mat'
                MCS_Matlab = sio.loadmat(Mat_File)
                MCS_Matlab = MCS_Matlab['MCSsansBF84' + str(nss)];
                mcs40 = MCS_Matlab[i, 2]

                Mat_File_BFUL = 'SNR\MCSsansBF84' + str(nss) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSsansBF84' + str(nss) + 'UL'];
                mcs40_BFUL = MCS_Matlab_BFUL[i, 2]

                Band40.SetNRU(nru)
                Band40.RunConfig(mcs40, mcs40_BFUL)
                PhyDR = Band40.Get_Phy_Datarate()
                DL = Band40.Get_AP_UDP_Throughput_DL()
                UL = Band40.Get_AP_UDP_Throughput_UL()
                TCP = Band40.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

            ################################################  #BF # No_BF ### MUMIMO_NO_OFDMA   #Band80  #############################################
        print('---------S = {}   / #BF # No_BF ### MUMIMO_NO_OFDMA   #Band80 -------------  {} '.format(S, str(now)))
        with open(path + '\BF_MUMIMOonly80.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 1, 0, 1, 1, 1, 1, 1)
                if S == 1:
                    nss = Band80.Get_NSS()
                else:
                    nss = 4
                Mat_File = 'SNR\MCSavecBF84' + str(nss) + '.mat'
                MCS_Matlab = sio.loadmat(Mat_File)
                MCS_Matlab = MCS_Matlab['MCSavecBF84' + str(nss)];
                mcs80 = MCS_Matlab[i, 2]

                Mat_File_BFUL = 'SNR\MCSavecBF84' + str(nss) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSavecBF84' + str(nss) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
        with open(path + '\MUMIMOonly80.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band80.setup(1350, 1460, 0, 0, 0, 1, 1, 1, 1, 1)
                if S == 1:
                    nss = Band80.Get_NSS()
                else:
                    nss = 0
                Mat_File = 'SNR\MCSsansBF84' + str(nss) + '.mat'
                MCS_Matlab = sio.loadmat(Mat_File)
                MCS_Matlab = MCS_Matlab['MCSsansBF84' + str(nss)];
                mcs80 = MCS_Matlab[i, 2]

                Mat_File_BFUL = 'SNR\MCSsansBF84' + str(nss) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSsansBF84' + str(nss) + 'UL'];
                mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                Band80.SetNRU(nru)
                Band80.RunConfig(mcs80, mcs80_BFUL)
                PhyDR = Band80.Get_Phy_Datarate()
                DL = Band80.Get_AP_UDP_Throughput_DL()
                UL = Band80.Get_AP_UDP_Throughput_UL()
                TCP = Band80.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

                ################################################  #BF # No_BF ### MUMIMO_NO_OFDMA   #Band160  #############################################
        print('---------S = {}   / #BF # No_BF ### MUMIMO_NO_OFDMA   #Band160 -------------  {} '.format(S, str(now)))
        with open(path + '\BF_MUMIMOonly160.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 1, 0, 1, 1, 1, 1, 1)
                if S == 1:
                    nss = Band160.Get_NSS()
                else:
                    nss = 0
                Mat_File = 'SNR\MCSavecBF84' + str(nss) + '.mat'
                MCS_Matlab = sio.loadmat(Mat_File)
                MCS_Matlab = MCS_Matlab['MCSavecBF84' + str(nss)];
                mcs160 = MCS_Matlab[i, 3]

                Mat_File_BFUL = 'SNR\MCSavecBF84' + str(nss) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSavecBF84' + str(nss) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        with open(path + '\MUMIMOonly160.csv', 'w') as csvfile:
            for i in range(0, 100, 1):
                Band160.setup(1350, 1460, 0, 0, 0, 1, 1, 1, 1, 1)
                if S == 1:
                    nss = Band160.Get_NSS()
                else:
                    nss = 0
                Mat_File = 'SNR\MCSsansBF84' + str(nss) + '.mat'
                MCS_Matlab = sio.loadmat(Mat_File)
                MCS_Matlab = MCS_Matlab['MCSsansBF84' + str(nss)];
                mcs160 = MCS_Matlab[i, 3]

                Mat_File_BFUL = 'SNR\MCSsansBF84' + str(nss) + 'UL.mat'
                MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSsansBF84' + str(nss) + 'UL'];
                mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                Band160.SetNRU(nru)
                Band160.RunConfig(mcs160, mcs160_BFUL)
                PhyDR = Band160.Get_Phy_Datarate()
                DL = Band160.Get_AP_UDP_Throughput_DL()
                UL = Band160.Get_AP_UDP_Throughput_UL()
                TCP = Band160.Get_AP_TCP_Throughput()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        nru = 1
        ################################################  #BF # No_BF ### MUMIMO_OFDMA   #Band20  #############################################
        print('---------S = {}   / #BF # No_BF ### MUMIMO_OFDMA   #Band20 -------------  {} '.format(S, str(now)))
        maliste = [1]

        for alpha in maliste:
            alpha = alpha - 1
            for beta in maliste:
                Band20 = IEEE80211ax(20, 4, 8, S, 256, 256, 3.2, 3.2, alpha, beta, 'legacy', 20, 8, 8, 1, 1, 0)
                with open(path + '\BF_MUMIMO_OFDMA_20_' + str(alpha * 10) + '_' + str(beta * 10) + '.csv',
                          'w') as csvfile:
                    for i in range(0, 100, 1):
                        Band20.setup(1350, 1460, 0, 1, 1, 1, 1, 1, 1, 1)
                        if S == 1:
                            nss = Band20.Get_NSS()
                        else:
                            nss = 0

                        Mat_File_BF = 'SNR\MCSavecBF84' + str(nss) + '.mat'
                        MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                        MCS_Matlab_BF = MCS_Matlab_BF['MCSavecBF84' + str(nss)];
                        mcs20_BF = MCS_Matlab_BF[i, 0]

                        Mat_File_BFUL = 'SNR\MCSavecBF84' + str(nss) + 'UL.mat'
                        MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                        MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSavecBF84' + str(nss) + 'UL'];
                        mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                        Band20.SetNRU(nru)
                        Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                        PhyDR = Band20.Get_Phy_Datarate()
                        (DL, UL) = Band20.Get_AP_UDP_Throughput_DL_UL()
                        TCP = Band20.Get_AP_TCP_Throughput()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                        writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

                with open(path + '\MUMIMO_OFDMA_20_' + str(alpha * 10) + '_' + str(beta * 10) + '.csv', 'w') as csvfile:
                    for i in range(0, 100, 1):
                        Band20.setup(1350, 1460, 0, 0, 1, 1, 1, 1, 1, 1)
                        if S == 1:
                            nss = Band20.Get_NSS()
                        else:
                            nss = 0
                        Mat_File_BF = 'SNR\MCSsansBF84' + str(nss) + '.mat'
                        MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                        MCS_Matlab_BF = MCS_Matlab_BF['MCSsansBF84' + str(nss)];
                        mcs20_BF = MCS_Matlab_BF[i, 0]

                        Mat_File_BFUL = 'SNR\MCSsansBF84' + str(nss) + 'UL.mat'
                        MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                        MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSsansBF84' + str(nss) + 'UL'];
                        mcs20_BFUL = MCS_Matlab_BFUL[i, 0]

                        Band20.SetNRU(nru)
                        Band20.RunConfig(mcs20_BF, mcs20_BFUL)
                        PhyDR = Band20.Get_Phy_Datarate()
                        (DL, UL) = Band20.Get_AP_UDP_Throughput_DL_UL()
                        TCP = Band20.Get_AP_TCP_Throughput()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                        writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        ################################################  #BF # No_BF ### MUMIMO_OFDMA   #Band40  #############################################
        print('---------S = {}   / #BF # No_BF ### MUMIMO_OFDMA   #Band40 -------------  {} '.format(S, str(now)))
        for alpha in maliste:
            alpha = alpha - 1
            for beta in maliste:
                Band40 = IEEE80211ax(40, 4, 8, S, 256, 256, 3.2, 3.2, alpha, beta, 'legacy', 20, 8, 8, 1, 1, 0)
                with open(path + '\BF_MUMIMO_OFDMA_40_' + str(alpha * 10) + '_' + str(beta * 10) + '.csv',
                          'w') as csvfile:
                    for i in range(0, 100, 1):
                        Band40.setup(1350, 1460, 0, 1, 1, 1, 1, 1, 1, 1)
                        if S == 1:
                            nss = Band40.Get_NSS()
                        else:
                            nss = 0
                        Mat_File_BF = 'SNR\MCSavecBF84' + str(nss) + '.mat'
                        MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                        MCS_Matlab_BF = MCS_Matlab_BF['MCSavecBF84' + str(nss)];
                        mcs40_BF = MCS_Matlab_BF[i, 1]

                        Mat_File_BFUL = 'SNR\MCSavecBF84' + str(nss) + 'UL.mat'
                        MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                        MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSavecBF84' + str(nss) + 'UL'];
                        mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                        Band40.SetNRU(nru)
                        Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                        PhyDR = Band40.Get_Phy_Datarate()
                        (DL, UL) = Band40.Get_AP_UDP_Throughput_DL_UL()
                        TCP = Band40.Get_AP_TCP_Throughput()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                        writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
                with open(path + '\MUMIMO_OFDMA_40_' + str(alpha * 10) + '_' + str(beta * 10) + '.csv', 'w') as csvfile:
                    for i in range(0, 100, 1):
                        Band40.setup(1350, 1460, 0, 0, 1, 1, 1, 1, 1, 1)
                        if S == 1:
                            nss = Band40.Get_NSS()
                        else:
                            nss = 0
                        Mat_File_BF = 'SNR\MCSsansBF84' + str(nss) + '.mat'
                        MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                        MCS_Matlab_BF = MCS_Matlab_BF['MCSsansBF84' + str(nss)];
                        mcs40_BF = MCS_Matlab_BF[i, 1]

                        Mat_File_BFUL = 'SNR\MCSsansBF84' + str(nss) + 'UL.mat'
                        MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                        MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSsansBF84' + str(nss) + 'UL'];
                        mcs40_BFUL = MCS_Matlab_BFUL[i, 1]

                        Band40.SetNRU(nru)
                        Band40.RunConfig(mcs40_BF, mcs40_BFUL)
                        PhyDR = Band40.Get_Phy_Datarate()
                        (DL, UL) = Band40.Get_AP_UDP_Throughput_DL_UL()
                        TCP = Band40.Get_AP_TCP_Throughput()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                        writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        ################################################  #BF # No_BF ### MUMIMO_OFDMA   #Band80  #############################################
        print('---------S = {}   / #BF # No_BF ### MUMIMO_OFDMA   #Band80 -------------  {} '.format(S, str(now)))
        for alpha in maliste:
            alpha = alpha - 1
            for beta in maliste:
                Band80 = IEEE80211ax(80, 4, 8, S, 256, 256, 3.2, 3.2, alpha, beta, 'legacy', 20, 8, 8, 1, 1, 0)
                with open(path + '\BF_MUMIMO_OFDMA_80_' + str(alpha * 10) + '_' + str(beta * 10) + '.csv',
                          'w') as csvfile:
                    for i in range(0, 100, 1):
                        Band80.setup(1350, 1460, 0, 1, 1, 1, 1, 1, 1, 1)
                        if S == 1:
                            nss = Band80.Get_NSS()
                        else:
                            nss = 0
                        Mat_File_BF = 'SNR\MCSavecBF84' + str(nss) + '.mat'
                        MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                        MCS_Matlab_BF = MCS_Matlab_BF['MCSavecBF84' + str(nss)];
                        mcs80_BF = MCS_Matlab_BF[i, 2]

                        Mat_File_BFUL = 'SNR\MCSavecBF84' + str(nss) + 'UL.mat'
                        MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                        MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSavecBF84' + str(nss) + 'UL'];
                        mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                        Band80.SetNRU(nru)
                        Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                        PhyDR = Band80.Get_Phy_Datarate()
                        (DL, UL) = Band80.Get_AP_UDP_Throughput_DL_UL()
                        TCP = Band80.Get_AP_TCP_Throughput()
                        print(DL)
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                        writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
                with open(path + '\MUMIMO_OFDMA_80_' + str(alpha * 10) + '_' + str(beta * 10) + '.csv', 'w') as csvfile:
                    for i in range(0, 100, 1):
                        Band80.setup(1350, 1460, 0, 0, 1, 1, 1, 1, 1, 1)
                        if S == 1:
                            nss = Band80.Get_NSS()
                        else:
                            nss = 0
                        Mat_File_BF = 'SNR\MCSsansBF84' + str(nss) + '.mat'
                        MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                        MCS_Matlab_BF = MCS_Matlab_BF['MCSsansBF84' + str(nss)];
                        mcs80_BF = MCS_Matlab_BF[i, 2]

                        Mat_File_BFUL = 'SNR\MCSsansBF84' + str(nss) + 'UL.mat'
                        MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                        MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSsansBF84' + str(nss) + 'UL'];
                        mcs80_BFUL = MCS_Matlab_BFUL[i, 2]

                        Band80.SetNRU(nru)
                        Band80.RunConfig(mcs80_BF, mcs80_BFUL)
                        PhyDR = Band80.Get_Phy_Datarate()
                        (DL, UL) = Band80.Get_AP_UDP_Throughput_DL_UL()
                        TCP = Band80.Get_AP_TCP_Throughput()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                        writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

        ################################################  #BF # No_BF ### MUMIMO_OFDMA   #Band160  #############################################
        print('---------S = {}   / #BF # No_BF ### MUMIMO_OFDMA   #Band160 -------------  {} '.format(S, str(now)))
        for alpha in maliste:
            alpha = alpha - 1
            for beta in maliste:
                Band160 = IEEE80211ax(160, 4, 8, S, 256, 256, 3.2, 3.2, alpha, beta, 'legacy', 20, 8, 8, 1, 1, 0)
                with open(path + '\BF_MUMIMO_OFDMA_160_' + str(alpha * 10) + '_' + str(beta * 10) + '.csv',
                          'w') as csvfile:
                    for i in range(0, 100, 1):
                        Band160.setup(1350, 1460, 0, 1, 1, 1, 1, 1, 1, 1)
                        if S == 1:
                            nss = Band160.Get_NSS()
                        else:
                            nss = 0
                        Mat_File_BF = 'SNR\MCSavecBF84' + str(nss) + '.mat'
                        MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                        MCS_Matlab_BF = MCS_Matlab_BF['MCSavecBF84' + str(nss)];
                        mcs160_BF = MCS_Matlab_BF[i, 3]

                        Mat_File_BFUL = 'SNR\MCSavecBF84' + str(nss) + 'UL.mat'
                        MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                        MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSavecBF84' + str(nss) + 'UL'];
                        mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                        Band160.SetNRU(nru)
                        Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                        PhyDR = Band160.Get_Phy_Datarate()
                        (DL, UL) = Band160.Get_AP_UDP_Throughput_DL_UL()
                        TCP = Band160.Get_AP_TCP_Throughput()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                        writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})
                with open(path + '\MUMIMO_OFDMA_160_' + str(alpha * 10) + '_' + str(beta * 10) + '.csv',
                          'w') as csvfile:
                    for i in range(0, 100, 1):
                        Band160.setup(1350, 1460, 0, 0, 1, 1, 1, 1, 1, 1)
                        if S == 1:
                            nss = Band160.Get_NSS()
                        else:
                            nss = 0
                        Mat_File_BF = 'SNR\MCSsansBF84' + str(nss) + '.mat'
                        MCS_Matlab_BF = sio.loadmat(Mat_File_BF)
                        MCS_Matlab_BF = MCS_Matlab_BF['MCSsansBF84' + str(nss)];
                        mcs160_BF = MCS_Matlab_BF[i, 3]

                        Mat_File_BFUL = 'SNR\MCSsansBF84' + str(nss) + 'UL.mat'
                        MCS_Matlab_BFUL = sio.loadmat(Mat_File_BFUL)
                        MCS_Matlab_BFUL = MCS_Matlab_BFUL['MCSsansBF84' + str(nss) + 'UL'];
                        mcs160_BFUL = MCS_Matlab_BFUL[i, 3]

                        Band160.SetNRU(nru)
                        Band160.RunConfig(mcs160_BF, mcs160_BFUL)
                        PhyDR = Band160.Get_Phy_Datarate()
                        (DL, UL) = Band160.Get_AP_UDP_Throughput_DL_UL()
                        TCP = Band160.Get_AP_TCP_Throughput()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel-tab', delimiter=',')
                        writer.writerow({'Phy': PhyDR, 'DL': DL, 'UL': UL, 'TCP': TCP})

                ##########################################################################################################################################


def NRU_Index(Nru):
    """
       Fonction de décalage
    """

    if Nru == 1:
        x = 1;
    elif Nru == 2:
        x = 2;
    elif Nru == 4:
        x = 4;
    elif Nru == 8:
        x = 9;
    elif Nru == 16:
        x = 18;
    else:
        print('mauvaise config, Nru non defini');
    return x


def VoIPAirtime(band, Msta, Map, nru, S, mcs):
    """
       Calcul du airtime en foncion de la configuration utilisée
    """
    # S = 74
    test1 = IEEE80211ax(band, Msta, Map, S, 1, 1, 0.8, 0.8, 0, 1, 'AX_VO', 20, 8, 4, 1, 1, 0)
    test1.setup(180, 180, mcs, 1, 1, nru, 0, 1, 1, 0)
    y = (test1.Get_AP_UDP_Throughput_DL()[2] + test1.Get_AP_UDP_Throughput_UL()[2])
    x = int((20 * 10 ** (-3)) / (y))

    nusers = x * min(test1.Get_AP_UDP_Throughput_DL()[1], test1.Get_AP_UDP_Throughput_UL()[1])

    ##    D1 = test1.Get_AP_UDP_Throughput_DL()[1]
    ##    D2 = test1.Get_AP_UDP_Throughput_UL()[1]
    ##
    ##    N1 = test1.Get_AP_UDP_Throughput_DL()[1]
    ##    N2 = test1.Get_AP_UDP_Throughput_UL()[1]
    ##
    ##    T1 = test1.Get_AP_UDP_Throughput_DL()[2]
    ##    T2 = test1.Get_AP_UDP_Throughput_UL()[2]
    ##
    ##    n=min(N1,N2)

    # print  ( 1 / nusers )
    return round(1 / nusers, 5)


def WIFI_11AX_Tables():
    """
       Génération des tables de débits pour Xanda/Wanda
    """

    # ListS = [ 1,4,8,16,32,64 ]
    ListB = [20, 40, 80, 160]
    ListAP = [4, 8]
    ListSTA = [1, 2]
    ListGiDL = [0.8, 1.6, 3.2]
    ListGiUL = [0.8, 1.6, 3.2]
    ListRts = [1]  # [0,1]
    ListTCSI = [1]  # [0,1]
    ListMCS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ListLdata = [1350]  # [250,500,1500]

    ListOFDMA = [0, 1]
    ListMUMIMO = [0, 1]

    ListAgg1 = [1, 4, 8, 16, 32, 64, 128, 256]
    ListAgg2 = [1, 2, 3, 4, 5, 6, 7]
    LambdaCSI = 20

    DCM = [0, 1]
    NSS = 8
    NRX = 8  # ???
    AngleQuantif = 1  # psi and phi config
    Grpmt = 1  # 4 Or 16
    ##    udp=1
    ##    tcp=1
    ListNRU = [9]
    ##
    QoS = 'AX_BE'
    ############# UL/DL & SU/MU Percentiles
    a = 0
    b = 1

    # Debut du decompte du temps

    path = 'SENSI'
    fieldnames1 = ['Technology', 'Band', 'Bandwidth', 'Number_of_AP_Antenna', 'Number_of_Spatial_Streams', 'RTS_info',
                   'SGIDL_info', 'Number_of_Aggregate_MPDU', 'Number_of_Aggregate_MSDU', 'TRANSMISSION_OPTION',
                   'TCP_OPTION', 'N_Users']

    fieldnames2 = ['SINR', 'Sensi', 'MCS', 'Data_rate', 'UDP_Throughput', 'TCP_Throughput',
                   'VoIPAirtime_percent_utilization']

    with open('ThptPrinterAX_5GHz.csv', 'w') as csvfile:

        writer1 = csv.DictWriter(csvfile, fieldnames=fieldnames1, delimiter=';', lineterminator='\n')
        writer2 = csv.DictWriter(csvfile, fieldnames=fieldnames2, delimiter=';', lineterminator='\n')

        for band in ListB:
            for Map in ListAP:
                for Msta in ListSTA:
                    for nru in ListNRU:
                        for mumimo in ListMUMIMO:
                            for ofdma in ListOFDMA:
                                for Agg1 in ListAgg1:
                                    for Agg2 in ListAgg2:
                                        for GI in ListGiUL:
                                            if ofdma == 0 and mumimo == 1:
                                                S = Map / Msta
                                                test1 = IEEE80211ax(band, Msta, Map, S, Agg1, Agg2, GI, GI, a, b, QoS,
                                                                    LambdaCSI, NSS, NRX, AngleQuantif, Grpmt, DCM[0])
                                                test1.setup(Listlength_datas[0], 1460, 0, ListTCSI[0], ofdma, nru,
                                                            mumimo,
                                                            ListRts[0], 1, 1)
                                                nss = test1.Get_NSS()
                                                # Mat_File  =  path + '\S'  +str(band) +'_' +str(nss)  +str(DCM[0])  +str(ListTCSI[0])    +'.mat'
                                                # MCS_Matlab = sio.loadmat(Mat_File)
                                                # MCS_Matlab = MCS_Matlab ['S'  +str(band) +'_' +str(nss)  +str(DCM[0])  +str(ListTCSI[0])];
                                                MCS_Matlab = SensTreshold(band, nss, DCM[0])
                                                writer1.writeheader()
                                                writer1.writerow(
                                                    {'Technology': 'WiFi 802.11ax', 'Band': '5 GHz', 'Bandwidth': band,
                                                     'Number_of_AP_Antenna': Map,
                                                     'Number_of_Spatial_Streams': test1.Get_NSS(),
                                                     'RTS_info': test1.RTSCTS, 'SGIDL_info': int(GI * 1000),
                                                     'Number_of_Aggregate_MPDU': test1.AggMPDU,
                                                     'Number_of_Aggregate_MSDU': test1.AggMSDU,
                                                     'TRANSMISSION_OPTION': 2, 'TCP_OPTION': 0,
                                                     'N_Users': int(test1.S)})

                                                writer2.writeheader()
                                                for mcs in ListMCS:
                                                    Sensi = MCS_Matlab[mcs] + Calcul_Gain_MIMO(Map, Msta, nss, 0, 0, 0)
                                                    SINR = Sensi - round((10 * np.log10(1.3806 * 10 ** (-23) * (
                                                            20 + 273.15) * band * 10 ** 6) + 30 + 9), 2)
                                                    test1.setup(Listlength_datas[0], 1460, mcs, ListTCSI[0], ofdma, nru,
                                                                mumimo, ListRts[0], 1, 1)
                                                    writer2.writerow(
                                                        {'SINR': round(SINR, 1), 'Sensi': Sensi, 'MCS': mcs,
                                                         'Data_rate': test1.Get_Phy_Datarate(),
                                                         'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL()[0],
                                                         'TCP_Throughput': test1.Get_AP_TCP_OP_Throughput()[0],
                                                         'VoIPAirtime_percent_utilization': VoIPAirtime(band, Msta, Map,
                                                                                                        nru, S, mcs)})
                                                    # writer2.writerow({ 'SINR':0,	'Sensi':0, 'MCS' : mcs, 'Numb_Users':test1.S, 'Bandwidth':test1.B, 'Nb_Antenna_AP':test1.Map ,'Nb_Antenna_STA' : test1.Msta, 'Nb_Spatia_Stream'  : test1.Get_NSS(), 'GI_DL':GiDL , 'GI_UL':GiUL , 'length_datas': test1.Ldata , 'CWMIN' : test1.CWmin ,'OFDMA' : test1.ofdma, 'MU-MIMO' : test1.mumimo,	'RTSCTS'  : test1.RTSCTS ,'TCSI'  : test1.tcsi,	'A' : test1.a, 'B' : test1.b,	'Data_rate' : test1.Get_Phy_Datarate()  ,	'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL_UL()[0],	'TCP_Throughput': test1.Get_AP_TCP_Throughput() ,	'VoIPAirtime_percent_utilization': 0.5	    } )

                                                writer1.writeheader()
                                                writer1.writerow(
                                                    {'Technology': 'WiFi 802.11ax', 'Band': '5 GHz', 'Bandwidth': band,
                                                     'Number_of_AP_Antenna': Map,
                                                     'Number_of_Spatial_Streams': test1.Get_NSS(),
                                                     'RTS_info': test1.RTSCTS, 'SGIDL_info': int(GI * 1000),
                                                     'Number_of_Aggregate_MPDU': test1.AggMPDU,
                                                     'Number_of_Aggregate_MSDU': test1.AggMSDU,
                                                     'TRANSMISSION_OPTION': 2, 'TCP_OPTION': 1,
                                                     'N_Users': int(test1.S)})

                                                writer2.writeheader()
                                                for mcs in ListMCS:
                                                    Sensi = MCS_Matlab[mcs] + Calcul_Gain_MIMO(Map, Msta, nss, 0, 0, 0)
                                                    SINR = Sensi - round((10 * np.log10(1.3806 * 10 ** (-23) * (
                                                            20 + 273.15) * band * 10 ** 6) + 30 + 9), 2)
                                                    test1.setup(ListLdata[0], 1460, mcs, ListTCSI[0], ofdma, nru,
                                                                mumimo, ListRts[0], 1, 1)
                                                    writer2.writerow(
                                                        {'SINR': round(SINR, 1), 'Sensi': Sensi, 'MCS': mcs,
                                                         'Data_rate': test1.Get_Phy_Datarate(),
                                                         'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL()[0],
                                                         'TCP_Throughput': test1.Get_AP_TCP_Throughput()[0],
                                                         'VoIPAirtime_percent_utilization': VoIPAirtime(band, Msta, Map,
                                                                                                        nru, S, mcs)})
                                                    # writer2.writerow({ 'SINR':0,	'Sensi':0, 'MCS' : mcs, 'Numb_Users':test1.S, 'Bandwidth':test1.B, 'Nb_Antenna_AP':test1.Map ,'Nb_Antenna_STA' : test1.Msta, 'Nb_Spatia_Stream'  : test1.Get_NSS(), 'GI_DL':GiDL , 'GI_UL':GiUL , 'Ldata': test1.Ldata , 'CWMIN' : test1.CWmin ,'OFDMA' : test1.ofdma, 'MU-MIMO' : test1.mumimo,	'RTSCTS'  : test1.RTSCTS ,'TCSI'  : test1.tcsi,	'A' : test1.a, 'B' : test1.b,	'Data_rate' : test1.Get_Phy_Datarate()  ,	'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL_UL()[0],	'TCP_Throughput': test1.Get_AP_TCP_Throughput() ,	'VoIPAirtime_percent_utilization': 0.5	    } )




                                            elif ofdma == 1 and mumimo == 0:
                                                S = (nru)
                                                test1 = IEEE80211ax(band, Msta, Map, S, Agg1, Agg2, GI, GI, a, b, QoS,
                                                                    LambdaCSI, NSS, NRX, AngleQuantif, Grpmt, DCM[0])
                                                test1.setup(ListLdata[0], 1460, 0, ListTCSI[0], ofdma, nru, mumimo,
                                                            ListRts[0], 1, 1)
                                                nss = test1.Get_NSS()
                                                ##                                                Mat_File  =  path + '\S'  +str(band) +'_' +str(nss)  +str(DCM[0])  +str(ListTCSI[0])    +'.mat'
                                                ##                                                MCS_Matlab = sio.loadmat(Mat_File )
                                                ##                                                MCS_Matlab = MCS_Matlab ['S'  +str(band) +'_' +str(nss)  +str(DCM[0])  +str(ListTCSI[0])] ;
                                                MCS_Matlab = SensTreshold(band, nss, DCM[0])

                                                writer1.writeheader()
                                                writer1.writerow(
                                                    {'Technology': 'WiFi 802.11ax', 'Band': '5 GHz', 'Bandwidth': band,
                                                     'Number_of_AP_Antenna': Map,
                                                     'Number_of_Spatial_Streams': test1.Get_NSS(),
                                                     'RTS_info': test1.RTSCTS, 'SGIDL_info': int(GI * 1000),
                                                     'Number_of_Aggregate_MPDU': test1.AggMPDU,
                                                     'Number_of_Aggregate_MSDU': test1.AggMSDU,
                                                     'TRANSMISSION_OPTION': 1, 'TCP_OPTION': 0,
                                                     'N_Users': int(test1.S)})

                                                writer2.writeheader()
                                                for mcs in ListMCS:
                                                    Sensi = MCS_Matlab[mcs] + Calcul_Gain_MIMO(Map, Msta, nss, 0, 0, 0)
                                                    SINR = Sensi - round((10 * np.log10(1.3806 * 10 ** (-23) * (
                                                            20 + 273.15) * band * 10 ** 6) + 30 + 9), 2)
                                                    test1.setup(ListLdata[0], 1460, mcs, ListTCSI[0], ofdma, nru,
                                                                mumimo, ListRts[0], 1, 1)
                                                    writer2.writerow(
                                                        {'SINR': round(SINR, 1), 'Sensi': Sensi, 'MCS': mcs,
                                                         'Data_rate': test1.Get_Phy_Datarate(),
                                                         'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL()[0],
                                                         'TCP_Throughput': test1.Get_AP_TCP_OP_Throughput()[0],
                                                         'VoIPAirtime_percent_utilization': VoIPAirtime(band, Msta, Map,
                                                                                                        nru, S, mcs)})
                                                    # writer2.writerow({ 'SINR':0,	'Sensi':0, 'MCS' : mcs, 'Numb_Users':test1.S, 'Bandwidth':test1.B, 'Nb_Antenna_AP':test1.Map ,'Nb_Antenna_STA' : test1.Msta, 'Nb_Spatia_Stream'  : test1.Get_NSS(), 'GI_DL':GiDL , 'GI_UL':GiUL , 'Ldata': test1.Ldata , 'CWMIN' : test1.CWmin ,'OFDMA' : test1.ofdma, 'MU-MIMO' : test1.mumimo,	'RTSCTS'  : test1.RTSCTS ,'TCSI'  : test1.tcsi,	'A' : test1.a, 'B' : test1.b,	'Data_rate' : test1.Get_Phy_Datarate()  ,	'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL_UL()[0],	'TCP_Throughput': test1.Get_AP_TCP_Throughput() ,	'VoIPAirtime_percent_utilization': 0.5	    } )

                                                writer1.writeheader()
                                                writer1.writerow(
                                                    {'Technology': 'WiFi 802.11ax', 'Band': '5 GHz', 'Bandwidth': band,
                                                     'Number_of_AP_Antenna': Map,
                                                     'Number_of_Spatial_Streams': test1.Get_NSS(),
                                                     'RTS_info': test1.RTSCTS, 'SGIDL_info': int(GI * 1000),
                                                     'Number_of_Aggregate_MPDU': test1.AggMPDU,
                                                     'Number_of_Aggregate_MSDU': test1.AggMSDU,
                                                     'TRANSMISSION_OPTION': 1, 'TCP_OPTION': 1,
                                                     'N_Users': int(test1.S)})

                                                writer2.writeheader()
                                                for mcs in ListMCS:
                                                    Sensi = MCS_Matlab[mcs] + Calcul_Gain_MIMO(Map, Msta, nss, 0, 0, 0)
                                                    SINR = Sensi - round((10 * np.log10(1.3806 * 10 ** (-23) * (
                                                            20 + 273.15) * band * 10 ** 6) + 30 + 9), 2)
                                                    test1.setup(ListLdata[0], 1460, mcs, ListTCSI[0], ofdma, nru,
                                                                mumimo, ListRts[0], 1, 1)
                                                    writer2.writerow(
                                                        {'SINR': round(SINR, 1), 'Sensi': Sensi, 'MCS': mcs,
                                                         'Data_rate': test1.Get_Phy_Datarate(),
                                                         'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL()[0],
                                                         'TCP_Throughput': test1.Get_AP_TCP_Throughput()[0],
                                                         'VoIPAirtime_percent_utilization': VoIPAirtime(band, Msta, Map,
                                                                                                        nru, S, mcs)})
                                                    # writer2.writerow({ 'SINR':0,	'Sensi':0, 'MCS' : mcs, 'Numb_Users':test1.S, 'Bandwidth':test1.B, 'Nb_Antenna_AP':test1.Map ,'Nb_Antenna_STA' : test1.Msta, 'Nb_Spatia_Stream'  : test1.Get_NSS(), 'GI_DL':GiDL , 'GI_UL':GiUL , 'Ldata': test1.Ldata , 'CWMIN' : test1.CWmin ,'OFDMA' : test1.ofdma, 'MU-MIMO' : test1.mumimo,	'RTSCTS'  : test1.RTSCTS ,'TCSI'  : test1.tcsi,	'A' : test1.a, 'B' : test1.b,	'Data_rate' : test1.Get_Phy_Datarate()  ,	'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL_UL()[0],	'TCP_Throughput': test1.Get_AP_TCP_Throughput() ,	'VoIPAirtime_percent_utilization': 0.5	    } )

                                                test1 = IEEE80211ax(band, Msta, Map, S, Agg1, Agg2, GI, GI, a, b, QoS,
                                                                    LambdaCSI, NSS, NRX, AngleQuantif, Grpmt, DCM[0])
                                                test1.setup(ListLdata[0], 1460, 0, 0, ofdma, nru, mumimo, ListRts[0], 1,
                                                            1)
                                                nss = test1.Get_NSS()
                                                ##                                                Mat_File  =  path + '\S'  +str(band) +'_' +str(nss)  +str(DCM[0])  +str(0)    +'.mat'
                                                ##                                                MCS_Matlab = sio.loadmat(Mat_File )
                                                ##                                                MCS_Matlab = MCS_Matlab ['S'  +str(band) +'_' +str(nss)  +str(DCM[0])  +str(0)];
                                                MCS_Matlab = SensTreshold(band, nss, DCM[0])
                                                writer1.writeheader()
                                                writer1.writerow(
                                                    {'Technology': 'WiFi 802.11ax', 'Band': '5 GHz', 'Bandwidth': band,
                                                     'Number_of_AP_Antenna': Map,
                                                     'Number_of_Spatial_Streams': test1.Get_NSS(),
                                                     'RTS_info': test1.RTSCTS, 'SGIDL_info': int(GI * 1000),
                                                     'Number_of_Aggregate_MPDU': test1.AggMPDU,
                                                     'Number_of_Aggregate_MSDU': test1.AggMSDU,
                                                     'TRANSMISSION_OPTION': 0, 'TCP_OPTION': 0,
                                                     'N_Users': int(test1.S)})

                                                writer2.writeheader()
                                                for mcs in ListMCS:
                                                    Sensi = MCS_Matlab[mcs] + Calcul_Gain_MIMO(Map, Msta, nss, 0, 0, 0)
                                                    SINR = Sensi - round((10 * np.log10(1.3806 * 10 ** (-23) * (
                                                            20 + 273.15) * band * 10 ** 6) + 30 + 9), 2)
                                                    test1.setup(ListLdata[0], 1460, mcs, 0, ofdma, nru, mumimo,
                                                                ListRts[0], 1, 1)
                                                    writer2.writerow(
                                                        {'SINR': round(SINR, 1), 'Sensi': Sensi, 'MCS': mcs,
                                                         'Data_rate': test1.Get_Phy_Datarate(),
                                                         'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL()[0],
                                                         'TCP_Throughput': test1.Get_AP_TCP_OP_Throughput()[0],
                                                         'VoIPAirtime_percent_utilization': VoIPAirtime(band, Msta, Map,
                                                                                                        nru, S, mcs)})
                                                    # writer2.writerow({ 'SINR':0,	'Sensi':0, 'MCS' : mcs, 'Numb_Users':test1.S, 'Bandwidth':test1.B, 'Nb_Antenna_AP':test1.Map ,'Nb_Antenna_STA' : test1.Msta, 'Nb_Spatia_Stream'  : test1.Get_NSS(), 'GI_DL':GiDL , 'GI_UL':GiUL , 'Ldata': test1.Ldata , 'CWMIN' : test1.CWmin ,'OFDMA' : test1.ofdma, 'MU-MIMO' : test1.mumimo,	'RTSCTS'  : test1.RTSCTS ,'TCSI'  : test1.tcsi,	'A' : test1.a, 'B' : test1.b,	'Data_rate' : test1.Get_Phy_Datarate()  ,	'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL_UL()[0],	'TCP_Throughput': test1.Get_AP_TCP_Throughput() ,	'VoIPAirtime_percent_utilization': 0.5	    } )

                                                writer1.writeheader()
                                                writer1.writerow(
                                                    {'Technology': 'WiFi 802.11ax', 'Band': '5 GHz', 'Bandwidth': band,
                                                     'Number_of_AP_Antenna': Map,
                                                     'Number_of_Spatial_Streams': test1.Get_NSS(),
                                                     'RTS_info': test1.RTSCTS, 'SGIDL_info': int(GI * 1000),
                                                     'Number_of_Aggregate_MPDU': test1.AggMPDU,
                                                     'Number_of_Aggregate_MSDU': test1.AggMSDU,
                                                     'TRANSMISSION_OPTION': 0, 'TCP_OPTION': 1,
                                                     'N_Users': int(test1.S)})

                                                writer2.writeheader()
                                                for mcs in ListMCS:
                                                    Sensi = MCS_Matlab[mcs] + Calcul_Gain_MIMO(Map, Msta, nss, 0, 0, 0)
                                                    SINR = Sensi - round((10 * np.log10(1.3806 * 10 ** (-23) * (
                                                            20 + 273.15) * band * 10 ** 6) + 30 + 9), 2)
                                                    test1.setup(ListLdata[0], 1460, mcs, 0, ofdma, nru, mumimo,
                                                                ListRts[0], 1, 1)
                                                    writer2.writerow(
                                                        {'SINR': round(SINR, 1), 'Sensi': Sensi, 'MCS': mcs,
                                                         'Data_rate': test1.Get_Phy_Datarate(),
                                                         'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL()[0],
                                                         'TCP_Throughput': test1.Get_AP_TCP_Throughput()[0],
                                                         'VoIPAirtime_percent_utilization': VoIPAirtime(band, Msta, Map,
                                                                                                        nru, S, mcs)})
                                                    # writer2.writerow({ 'SINR':0,	'Sensi':0, 'MCS' : mcs, 'Numb_Users':test1.S, 'Bandwidth':test1.B, 'Nb_Antenna_AP':test1.Map ,'Nb_Antenna_STA' : test1.Msta, 'Nb_Spatia_Stream'  : test1.Get_NSS(), 'GI_DL':GiDL , 'GI_UL':GiUL , 'Ldata': test1.Ldata , 'CWMIN' : test1.CWmin ,'OFDMA' : test1.ofdma, 'MU-MIMO' : test1.mumimo,	'RTSCTS'  : test1.RTSCTS ,'TCSI'  : test1.tcsi,	'A' : test1.a, 'B' : test1.b,	'Data_rate' : test1.Get_Phy_Datarate()  ,	'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL_UL()[0],	'TCP_Throughput': test1.Get_AP_TCP_Throughput() ,	'VoIPAirtime_percent_utilization': 0.5	    } )




                                            elif ofdma == 1 and mumimo == 1:
                                                if band == 20:
                                                    nru = 1
                                                elif band == 40:
                                                    nru = 2
                                                elif band == 80:
                                                    nru = 4
                                                elif band == 160:
                                                    nru = 8
                                                S = ((nru) * Map) / Msta
                                                test1 = IEEE80211ax(band, Msta, Map, S, Agg1, Agg2, GI, GI, a, b, QoS,
                                                                    LambdaCSI, NSS, NRX, AngleQuantif, Grpmt, DCM[0])
                                                test1.setup(ListLdata[0], 1460, 0, ListTCSI[0], ofdma, nru, mumimo,
                                                            ListRts[0], 1, 1)
                                                nss = test1.Get_NSS()
                                                ##                                                Mat_File  =   path +'\S'  +str(band) +'_' +str(nss)  +str(DCM[0])  +str(ListTCSI[0])    +'.mat'
                                                ##                                                MCS_Matlab = sio.loadmat(Mat_File )
                                                ##                                                MCS_Matlab = MCS_Matlab ['S'  +str(band) +'_' +str(nss)  +str(DCM[0])  +str(ListTCSI[0])];
                                                MCS_Matlab = SensTreshold(band, nss, DCM[0])
                                                writer1.writeheader()
                                                writer1.writerow(
                                                    {'Technology': 'WiFi 802.11ax', 'Band': '5 GHz', 'Bandwidth': band,
                                                     'Number_of_AP_Antenna': Map,
                                                     'Number_of_Spatial_Streams': test1.Get_NSS(),
                                                     'RTS_info': test1.RTSCTS, 'SGIDL_info': int(GI * 1000),
                                                     'Number_of_Aggregate_MPDU': test1.AggMPDU,
                                                     'Number_of_Aggregate_MSDU': test1.AggMSDU,
                                                     'TRANSMISSION_OPTION': 3, 'TCP_OPTION': 0,
                                                     'N_Users': int(test1.S)})

                                                writer2.writeheader()
                                                for mcs in ListMCS:
                                                    Sensi = MCS_Matlab[mcs] + Calcul_Gain_MIMO(Map, Msta, nss, 0, 0, 0)
                                                    SINR = Sensi - round((10 * np.log10(1.3806 * 10 ** (-23) * (
                                                            20 + 273.15) * band * 10 ** 6) + 30 + 9), 2)
                                                    test1.setup(ListLdata[0], 1460, mcs, ListTCSI[0], ofdma, nru,
                                                                mumimo, ListRts[0], 1, 1)
                                                    writer2.writerow(
                                                        {'SINR': round(SINR, 1), 'Sensi': Sensi, 'MCS': mcs,
                                                         'Data_rate': test1.Get_Phy_Datarate(),
                                                         'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL()[0],
                                                         'TCP_Throughput': test1.Get_AP_TCP_OP_Throughput()[0],
                                                         'VoIPAirtime_percent_utilization': VoIPAirtime(band, Msta, Map,
                                                                                                        NRU_Index(nru),
                                                                                                        S, mcs)})
                                                    # writer2.writerow({ 'SINR':0,	'Sensi':0, 'MCS' : mcs, 'Numb_Users':test1.S, 'Bandwidth':test1.B, 'Nb_Antenna_AP':test1.Map ,'Nb_Antenna_STA' : test1.Msta, 'Nb_Spatia_Stream'  : test1.Get_NSS(), 'GI_DL':GiDL , 'GI_UL':GiUL , 'Ldata': test1.Ldata , 'CWMIN' : test1.CWmin ,'OFDMA' : test1.ofdma, 'MU-MIMO' : test1.mumimo,	'RTSCTS'  : test1.RTSCTS ,'TCSI'  : test1.tcsi,	'A' : test1.a, 'B' : test1.b,	'Data_rate' : test1.Get_Phy_Datarate()  ,	'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL_UL()[0],	'TCP_Throughput': test1.Get_AP_TCP_Throughput() ,	'VoIPAirtime_percent_utilization': 0.5	    } )

                                                writer1.writeheader()
                                                writer1.writerow(
                                                    {'Technology': 'WiFi 802.11ax', 'Band': '5 GHz', 'Bandwidth': band,
                                                     'Number_of_AP_Antenna': Map,
                                                     'Number_of_Spatial_Streams': test1.Get_NSS(),
                                                     'RTS_info': test1.RTSCTS, 'SGIDL_info': int(GI * 1000),
                                                     'Number_of_Aggregate_MPDU': test1.AggMPDU,
                                                     'Number_of_Aggregate_MSDU': test1.AggMSDU,
                                                     'TRANSMISSION_OPTION': 3, 'TCP_OPTION': 1,
                                                     'N_Users': int(test1.S)})

                                                writer2.writeheader()
                                                for mcs in ListMCS:
                                                    Sensi = MCS_Matlab[mcs] + Calcul_Gain_MIMO(Map, Msta, nss, 0, 0, 0)
                                                    SINR = Sensi - round((10 * np.log10(1.3806 * 10 ** (-23) * (
                                                            20 + 273.15) * band * 10 ** 6) + 30 + 9), 2)
                                                    test1.setup(ListLdata[0], 1460, mcs, ListTCSI[0], ofdma, nru,
                                                                mumimo, ListRts[0], 1, 1)
                                                    writer2.writerow(
                                                        {'SINR': round(SINR, 1), 'Sensi': Sensi, 'MCS': mcs,
                                                         'Data_rate': test1.Get_Phy_Datarate(),
                                                         'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL()[0],
                                                         'TCP_Throughput': test1.Get_AP_TCP_Throughput()[0],
                                                         'VoIPAirtime_percent_utilization': VoIPAirtime(band, Msta, Map,
                                                                                                        NRU_Index(nru),
                                                                                                        S, mcs)})
                                                    # writer2.writerow({ 'SINR':0,	'Sensi':0, 'MCS' : mcs, 'Numb_Users':test1.S, 'Bandwidth':test1.B, 'Nb_Antenna_AP':test1.Map ,'Nb_Antenna_STA' : test1.Msta, 'Nb_Spatia_Stream'  : test1.Get_NSS(), 'GI_DL':GiDL , 'GI_UL':GiUL , 'Ldata': test1.Ldata , 'CWMIN' : test1.CWmin ,'OFDMA' : test1.ofdma, 'MU-MIMO' : test1.mumimo,	'RTSCTS'  : test1.RTSCTS ,'TCSI'  : test1.tcsi,	'A' : test1.a, 'B' : test1.b,	'Data_rate' : test1.Get_Phy_Datarate()  ,	'UDP_Throughput': test1.Get_AP_UDP_Throughput_DL_UL()[0],	'TCP_Throughput': test1.Get_AP_TCP_Throughput() ,	'VoIPAirtime_percent_utilization': 0.5	    } )



                                            else:
                                                continue;
