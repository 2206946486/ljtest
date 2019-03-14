# -*- coding: utf-8 -*-
"""
@author: cc
@date: 2018/10/23
"""


CARD_READIED, CARD_ACTIVATED, CARD_DEACTIVATED, CARD_RETIRED = range(4)

CARD_UNAUTHORIZED, CARD_AUDITED, CARD_UNPASSED, CARD_AUTHORIZED = range(4)

CHINA_UNICOM, CHINA_MOBILE, CHINA_TELECOM = range(3)

NETWORK_2G, NETWORK_3G, NETWORK_4G = range(3)

CHANGZHOU, JIASHENG, SIMBOSS = range(3)


# 伊雷克录入卡和iccid任务名
IMEI_ICCID_CHECK = "imei_iccid_check111" 

# 划卡任务名
pushCardsTasks = 'pushCardsTasks'

#回收卡任务名
recoveryCardTask = 'recoveryCardTask'

# 企业实名修改wathch的RealName字段
changeCardhadRealName = 'changeCardhadRealName'

# IMEI任务导入
Importimei = 'Importimei'
