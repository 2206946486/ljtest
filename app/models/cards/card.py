# -*- coding: utf-8 -*-
"""
@author: cc
@date: 2018/10/23
"""

from datetime import datetime
from app import db
from app.tools.dbs import JsonSerializer


class Card(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __json_hidden__ = ["partner_cards", "orders", "card_plans", 'auth']

    __tablename__ = "iot_card"

    id = db.Column(db.Integer, primary_key=True)
    iccid = db.Column(db.String(20), nullable=False, unique=True)
    msisdn = db.Column(db.String(20), nullable=False, index=True)
    operator = db.Column(db.SmallInteger, nullable=False)
    network = db.Column(db.SmallInteger, nullable=False)
    source = db.Column(db.SmallInteger, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=0)
    ent_auth = db.Column(db.Boolean, nullable=False)
    need_auth = db.Column(db.Boolean, nullable=False)
    auth_status = db.Column(db.SmallInteger, nullable=False, default=0)
    is_keep = db.Column(db.Boolean(), default=False)
    imei = db.Column("bind_imei", db.String(16))
    mobile = db.Column(db.String(20))
    register_mobile = db.Column(db.String(20))
    openid = db.Column(db.String(64))
    realname = db.Column(db.String(20))
    id_no = db.Column(db.String(20))
    authorized_at = db.Column(db.DateTime)
    activated_at = db.Column(db.DateTime)
    is_disabled = db.Column(db.Boolean(), nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    # 新增同步数据
    left_day = db.Column(db.Integer)
    left_flow = db.Column(db.Float)
    left_voice = db.Column(db.Float)

    def elastic(self):
        partner_cards = self.partner_cards.all()
        partner_ids = [x.partner_id for x in partner_cards]
        remarks = [u"{}_{}".format(x.partner_id, x.remark.replace("\n", "")) for x in partner_cards if x.remark]
        data = dict(
            id=self.id, iccid=self.iccid, msisdn=self.msisdn, operator=self.operator,
            network=self.network, source=self.source, auth_status=self.auth_status,
            status=self.status, partner_ids=partner_ids, remarks=remarks
        )
        return data

    def __init__(self, iccid, msisdn, operator, network, source,
                 status=0, auth_status=0, activated_at=None, need_auth=1,
                 authorized_at=None, is_disabled=False, mobile=None,
                 realname=None, id_no=None, is_keep=False, imei=None,
                 register_mobile=None, openid=None, ent_auth=False,
                 created_at=datetime.now(), updated_at=datetime.now(), left_day=None,
                 left_flow=None, left_voice=None,
                 *args, **kwargs):
        self.iccid = iccid
        self.msisdn = msisdn
        self.operator = operator
        self.network = network
        self.source = source
        self.status = status
        self.ent_auth = ent_auth
        self.need_auth = need_auth
        self.auth_status = status
        self.is_keep = is_keep
        self.imei = imei
        self.mobile = mobile
        self.register_mobile = register_mobile
        self.openid = openid
        self.realname = realname
        self.id_no = id_no
        self.activated_at = activated_at
        self.authorized_at = authorized_at
        self.is_disabled = is_disabled
        self.created_at = created_at
        self.updated_at = updated_at
        self.left_day = left_day
        self.left_flow = left_flow
        self.left_voice = left_voice

    def __str__(self):
        return "Card<{0}, {1}>".format(self.iccid, self.msisdn)

    __repr__ = __str__


class PartnerCard(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}

    __tablename__ = "iot_partner_card"
    __table_args__ = (
        db.UniqueConstraint("partner_id", "card_id", name="uiq_partner_card"),
    )

    id = db.Column(db.Integer, primary_key=True)

    partner_id = db.Column(db.Integer, db.ForeignKey("iot_partner.id"), nullable=False)
    partner = db.relationship("Partner", backref=db.backref("partner_cards", lazy="dynamic"))
    card_id = db.Column(db.Integer, db.ForeignKey("iot_card.id"), nullable=False, index=True)
    card = db.relationship("Card", backref=db.backref("partner_cards", lazy="dynamic"))

    remark = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, partner, card, created_at=datetime.now(),
                 remark=None, *args, **kwargs):
        self.partner = partner
        self.card = card
        self.remark = remark
        self.created_at = created_at

    def __str__(self):
        return "PartnerCard<{0}, {1}>".format(self.partner_id, self.card_id)

    __repr__ = __str__


class Auth(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}

    __tablename__ = "iot_auth"

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("iot_card.id"), nullable=False, index=True)
    card = db.relationship("Card", backref=db.backref("auth", lazy="dynamic"))
    user_ip = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    realname = db.Column(db.String(20), nullable=False)
    id_no = db.Column(db.String(20), nullable=False)
    cover = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, card, user_ip, mobile, id_no, realname, cover, back, people,
                 status=0, created_at=datetime.now(), updated_at=datetime.now(),
                 *args, **kwargs):
        self.card = card
        self.user_ip = user_ip
        self.mobile = mobile
        self.realname = realname
        self.id_no = id_no
        self.cover = cover
        self.back = back
        self.people = people
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return "Auth<{0}, {1}>".format(self.id_no, self.mobile)

    __repr__ = __str__


class AuthTrack(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}

    __tablename__ = "iot_auth_track"

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.Integer, db.ForeignKey("iot_auth.id"), nullable=False, index=True)
    auth = db.relationship("Auth", backref=db.backref("auth_tracks", lazy="dynamic"))
    old_status = db.Column(db.SmallInteger, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False)
    remark = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, auth, old_status, status, remark=None,
                 created_at=datetime.now(), updated_at=datetime.now(),
                 *args, **kwargs):
        self.auth = auth
        self.old_status = old_status
        self.status = status
        self.remark = remark
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return "AuthTrack<{0}, {1}>".format(self.auth.id_no, self.status)

    __repr__ = __str__


class Card_State_Change(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "card_state_change"
    id = db.Column(db.Integer, primary_key=True)
    iccid = db.Column(db.String(22), nullable=False)
    partner_id = db.Column(db.Integer)
    state = db.Column(db.SmallInteger, nullable=False)
    time = db.Column(db.DateTime)

    def __init__(self, iccid, partner_id, state, time=datetime.now(),
                 *args, **kwargs):
        self.iccid = iccid
        self.partner_id = partner_id
        self.state = state
        self.time = time

    def __str__(self):
        return "Card_State_Change<{0}, {1}>".format(self.iccid, self.state)

    __repr__ = __str__


class Card_Abandon_Time(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "card_abandon_time"
    id = db.Column(db.Integer, primary_key=True)
    iccid = db.Column(db.String(22), nullable=False)
    partner_id = db.Column(db.Integer)
    abandon_time = db.Column(db.DateTime)

    def __init__(self, iccid, partner_id, abandon_time=datetime.now(),
                 *args, **kwargs):
        self.iccid = iccid
        self.partner_id = partner_id
        self.abandon_time = abandon_time

    def __str__(self):
        return "Card_State_Change<{0}, {1}>".format(self.iccid, self.partner_id)

    __repr__ = __str__


class CountInfoServer(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_count_info"
    id = db.Column(db.Integer, primary_key=True)
    input_iccid_count = db.Column(db.Integer, nullable=False)
    scan_iccid_count = db.Column(db.Integer, nullable=False)
    input_imei_count = db.Column(db.Integer, nullable=False)
    scan_imei_count = db.Column(db.Integer, nullable=False)
    input_tel_count = db.Column(db.Integer, nullable=False)
    intput_code_count = db.Column(db.Integer, nullable=False)
    nextstep_count = db.Column(db.Integer, nullable=False)
    imeiActivited = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, input_iccid_count, scan_iccid_count, input_imei_count, scan_imei_count,
                 input_tel_count, intput_code_count, nextstep_count, imeiActivited,
                 created_at=datetime.now(), updated_at=datetime.now(), *args, **kwargs):
        self.input_iccid_count = input_iccid_count
        self.scan_iccid_count = scan_iccid_count
        self.input_imei_count = input_imei_count
        self.scan_imei_count = scan_imei_count
        self.input_tel_count = input_tel_count
        self.intput_code_count = intput_code_count
        self.nextstep_count = nextstep_count
        self.imeiActivited = imeiActivited
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return "iot_count_info<{0}, {1}>".format(self.input_iccid_count, self.scan_iccid_count)

    __repr__ = __str__


# 卡检测。组
class Card_Check_Group(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_check_group"
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    status = db.Column(db.SmallInteger)
    descibe = db.Column(db.String(255))

    def __init__(self, group_name, user_id, status=0, descibe='',
                 *args, **kwargs):
        self.group_name = group_name
        self.user_id = user_id
        self.status = status
        self.descibe = descibe

    def __str__(self):
        return "Card_Check_Group<{0}, {1}>".format(self.group_name, self.user_id)

    __repr__ = __str__


# 卡检测。ICCID
class Card_Check_ICCID(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_check_iccid"
    id = db.Column(db.Integer, primary_key=True)
    iccid = db.Column(db.String(255))
    status = db.Column(db.SmallInteger)
    descibe = db.Column(db.String(255))

    def __init__(self, iccid, status=0, descibe='',
                 *args, **kwargs):
        self.iccid = iccid
        self.status = status
        self.descibe = descibe

    def __str__(self):
        return "Card_Check_ICCID<{0}, {1}>".format(self.iccid, self.descibe)

    __repr__ = __str__


# 卡检测。ICCID Relation
class Card_Check_ICCID_Relation(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_check_iccid_relation"
    id = db.Column(db.Integer, primary_key=True)
    iccid = db.Column(db.String(255))
    group_id = db.Column(db.Integer)

    def __init__(self, iccid, group_id, descibe='',
                 *args, **kwargs):
        self.iccid = iccid
        self.group_id = group_id

    def __str__(self):
        return "Card_Check_ICCID_Relation<{0}, {1}>".format(self.group_id, self.iccid)

    __repr__ = __str__


# 卡检测。IMEI
class Card_Check_IMEI(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_check_imei"
    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(255))
    status = db.Column(db.SmallInteger)
    descibe = db.Column(db.String(255))

    def __init__(self, imei, status=0, descibe='',
                 *args, **kwargs):
        self.imei = imei
        self.status = status
        self.descibe = descibe

    def __str__(self):
        return "Card_Check_IMEI<{0}, {1}>".format(self.imei, self.descibe)

    __repr__ = __str__


# 卡检测。IMEI Relation
class Card_Check_IMEI_Relation(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_check_imei_relation"
    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(255))
    group_id = db.Column(db.Integer)

    def __init__(self, imei, group_id,
                 *args, **kwargs):
        self.imei = imei
        self.group_id = group_id

    def __str__(self):
        return "Card_Check_IMEI_Relation<{0}, {1}>".format(self.group_id, self.imei)

    __repr__ = __str__


# 卡源
class CardSource(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_card_source"
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(100), nullable=False)  # 卡源名
    rate_discount_rate = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)  # 流量折扣率
    call_settlement_price = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)  # 通话结算价
    sms_settlement_price = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)  # 短信结算价
    operators = db.Column(db.SmallInteger, nullable=False)  # 运营商

    def __init__(self, card_name, rate_discount_rate, call_settlement_price, sms_settlement_price, operators, *args, **kwargs):
        self.card_name = card_name
        self.rate_discount_rate = rate_discount_rate
        self.call_settlement_price = call_settlement_price
        self.sms_settlement_price = sms_settlement_price
        self.operators = operators

    def __str__(self):
        return "CardSource<{0}, {1}>".format(self.card_name, self.rate_discount_rate)

    __repr__ = __str__


# 结算档位价
class SettlementGearPrice(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_settlement_gear_price"
    id = db.Column(db.Integer, primary_key=True)
    rate_use = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)  # 流量档位
    price = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)  # 价格
    sms_settlement_price = db.Column(db.Numeric(10, 3, asdecimal=False), nullable=False)  # 短信结算价
    is_deleted = db.Column(db.Boolean(), nullable=False, default=False)  # 是否删除

    def __init__(self, rate_use, price, sms_settlement_price, is_deleted=False, *args, **kwargs):
        self.rate_use = rate_use
        self.price = price
        self.sms_settlement_price = sms_settlement_price
        self.is_deleted = is_deleted

    def __str__(self):
        return "SettlementGearPrice<{0}, {1}>".format(self.rate_use, self.price)

    __repr__ = __str__

#卡划拨记录表
class CardTransferRecord(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_car_transfer_record"
    id = db.Column(db.Integer, primary_key=True)
    operator_id = db.Column(db.Integer, nullable = False) #操作人ID
    operation_count = db.Column(db.Integer, nullable = False) #操作数量
    type = db.Column(db.Integer, nullable = False) #操作类型
    accept_id = db.Column(db.Integer, nullable = False)
    create_tm = db.Column(db.DateTime, nullable = False)
    reserved_field_1 = db.Column(db.String) # 预留字段1
    reserved_field_2 = db.Column()  # 预留字段2
    reserved_field_3 = db.Column()  # 预留字段3

    def __init__(self,operator_id,operation_count,type,accept_id,create_tm,reserved_field_1,
                 reserved_field_2,reserved_field_3,*args, **kwargs):
        self.operator_id = operator_id
        self.operation_count=operation_count
        self.type=type
        self.accept_id = accept_id
        self.create_tm = create_tm
        self.reserved_field_1 = reserved_field_1
        # self.reserved_field_2 = reserved_field_2
        # self.reserved_field_3 = reserved_field_3

    def __str__(self):
        return "accept---operator<{0}, {1}>".format(self.accept_id, self.operator_id)

    __repr__ = __str__

#卡划拨记录详情表
class CardTransferRecord_role(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_car_transfer_record_role"
    id = db.Column(db.Integer, primary_key=True)
    ctr_id = db.Column(db.Integer)
    iccid = db.Column(db.String)
    type = db.Column(db.Integer)

    def __init__(self,ctr_id,iccid,type):
        self.ctr_id = ctr_id
        self.iccid = iccid
        self.type = type

    def __str__(self):
        return "ctr_id---iccid<{0}, {1}>".format(self.ctr_id, self.iccid)

    __repr__ = __str__


#公告
class NoticeServer(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_notice"

    id = db.Column(db.Integer, primary_key=True)
    create_tm = db.Column(db.DateTime)
    create_id = db.Column(db.Integer)
    title = db.Column(db.String)
    text_content = db.Column(db.Text)
    reserved_field_1 = db.Column(db.String)
    reserved_field_2 = db.Column(db.String)

    def __init__(self,create_tm,create_id,title,text_content):
        self.create_tm = create_tm
        self.create_id = create_id
        self.title = title
        self.text_content = text_content

    def __str__(self):
        return "notice---title<{0}>".format(self.ctr_id, self.iccid)

    __repr__ = __str__

# 联通账号用量统计表
class SourceDataCount(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_source_data_count"

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.Integer, nullable = False)
    used_time = db.Column(db.DateTime, nullable=False) # 使用时间, H/M/S都为0
    usage_data = db.Column(db.Float, nullable=False)  # 流量／GB
    voice_data = db.Column(db.Integer, nullable=False)  # 语音／分钟
    msg_data = db.Column(db.Integer, nullable=False)  # 短信／条
    activated_count = db.Column(db.Integer, nullable=False) # 激活数/张
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self,  source, used_time, usage_data, voice_data , msg_data , activated_count, created_at=datetime.now(), updated_at=datetime.now(), *args, **kwargs ):
        self.source = source
        self.used_time = used_time
        self.usage_data = usage_data
        self.voice_data = voice_data
        self.msg_data = msg_data
        self.activated_count = activated_count
        self.created_at = created_at
        self.updated_at = updated_at


    def __str__(self):
        return '<iot_source_data_static>, source: {}, used_time: {}'.format(self.source, self.used_time)

    __repr__ = __str__

#实名流失率
class CardAuthLossRate(JsonSerializer, db.Model):
    __json_public__ = None
    __json_modifiers__ = {}
    __tablename__ = "iot_card_auth_loss_rate"
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey("iot_card.id"), nullable=False, index=True)
    card = db.relationship("Card", backref=db.backref("card_auth_loss_rates", lazy="dynamic"))
    iccid = db.Column(db.String(22), nullable=False,index=True)
    card_query = db.Column(db.Integer,nullable=False)
    card_charge = db.Column(db.Integer,nullable=False)
    card_auth = db.Column(db.Integer,nullable=False)
    card_taobao = db.Column(db.Integer,nullable=False)
    card_complete = db.Column(db.Integer,nullable=False)
    partner_id = db.Column(db.Integer,nullable=False)
    partner_name = db.Column(db.String(100),nullable=False)
    partner_card_auth = db.Column(db.SmallInteger,nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


    def __init__(self, card,iccid, card_query, card_charge,card_auth,card_taobao,card_complete,
                 partner_id,partner_name,partner_card_auth,
                 created_at=datetime.now(),updated_at=datetime.now(),
                 *args, **kwargs):
        self.card = card
        self.iccid = iccid
        self.card_query = card_query
        self.card_charge = card_charge
        self.card_auth = card_auth
        self.card_taobao = card_taobao
        self.card_complete = card_complete
        self.partner_id = partner_id
        self.partner_name = partner_name
        self.partner_card_auth = partner_card_auth
        self.created_at = created_at
        self.updated_at = updated_at

    def __str__(self):
        return "Card_Auth_Loss_Rate<{0}, {1}>".format(self.iccid, self.source)

    __repr__ = __str__
