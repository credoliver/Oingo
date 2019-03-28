from ext import db
from sqlalchemy import Column, DateTime, ForeignKey, String, Table, BINARY, create_engine, LargeBinary
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


class Schedule(db.Model):
    __tablename__ = 'schedule'

    sid = Column(INTEGER(11), primary_key=True)
    starttime = Column(DateTime)
    endtime = Column(DateTime)
    repetition = Column(INTEGER(11))

    def __init__(self, starttime, endtime, repetition):
        self.starttime = starttime
        self.endtime = endtime
        self.repetition = repetition

    def to_json(self):
        json_comment = {
            'sid': self.sid,
            'starttime': self.starttime,
            'endtime': self.endtime,
            'repetition': self.repetition,
        }
        return json_comment


class User(db.Model):
    __tablename__ = 'user'

    uid = Column(INTEGER(11), primary_key=True)
    uname = Column(String(255), nullable=False)
    uemail = Column(String(255), nullable=False)
    upassword = Column(VARCHAR(16), nullable=False)
    ustate = Column(String(50))
    ulongi = Column(String(255))
    ulati = Column(String(255))
    ucurrentTime = Column(DateTime)

    parents = relationship(
        'User',
        secondary='friend',
        primaryjoin='User.uid == friend.c.uid1',
        secondaryjoin='User.uid == friend.c.uid2'
    )

    def __init__(self, uname, uemail, upassword, ustate, ulongi, ulati):
        self.uname = uname
        self.uemail = uemail
        self.upassword = upassword
        self.ustate = ustate
        self.ulongi = ulongi
        self.ulati = ulati

    def to_json(self):
        json_comment = {
            'uid': self.uid,
            'uname': self.uname,
            'uemail': self.uemail,
            'ustate': self.ustate,
            'ulongi': self.ulongi,
            'ulati': self.ulati,
        }
        return json_comment


class Filter(db.Model):
    __tablename__ = 'filter'

    fid = Column(INTEGER(11), primary_key=True)
    ffrom = Column(String(11))
    ftag = Column(String(20))
    flongi = Column(String(255))
    flati = Column(String(255))
    fradius = Column(INTEGER(11))
    fuid = Column(ForeignKey('user.uid'), index=True)
    fsid = Column(ForeignKey('schedule.sid'), index=True)
    ftime = Column(DateTime)
    fstate = Column(String(50))

    user = relationship('User')
    schedule = relationship('Schedule')

    def __init__(self, ffrom, ftag, flongi, flati, fradius, ftime, fstate):
        self.ffrom = ffrom
        self.ftag = ftag
        self.flongi = flongi
        self.flati = flati
        self.fradius = fradius
        self.ftime = ftime
        self.fstate = fstate

    def to_json(self):
        json_comment = {
            'fid': self.fid,
            'ffrom': self.ffrom,
            'ftag': self.ftag,
            'flongi': self.flongi,
            'flati': self.flati,
            'fradius': self.fradius,
            'fuid': self.fuid,
            'fsid': self.fsid,
            'ftime': self.ftime,
            'fstate': self.fstate,
        }
        return json_comment


class Friend(db.Model):
    __tablename__ = 'friend'
    uid1 = Column('uid1', ForeignKey('user.uid'),
                  primary_key=True, nullable=False)
    uid2 = Column('uid2', ForeignKey('user.uid'),
                  primary_key=True, nullable=False, index=True)

    def __init__(self, uid1, uid2):
        self.uid1 = uid1
        self.uid2 = uid2


class Friendrequest(db.Model):
    __tablename__ = 'friendrequest'

    rid = Column(INTEGER(11), primary_key=True)
    ruid1 = Column(ForeignKey('user.uid'), nullable=False, index=True)
    ruid2 = Column(ForeignKey('user.uid'), nullable=False, index=True)

    user = relationship('User', primaryjoin='Friendrequest.ruid1 == User.uid')
    user1 = relationship('User', primaryjoin='Friendrequest.ruid2 == User.uid')


class Note(db.Model):
    __tablename__ = 'note'

    nid = Column(INTEGER(11), primary_key=True)
    ntext = Column(String(255), nullable=False)
    ntime = Column(DateTime, nullable=False)
    nlongi = Column(String(255), nullable=False)
    nlati = Column(String(255), nullable=False)
    nradius = Column(INTEGER(11), nullable=False)
    nsid = Column(ForeignKey('schedule.sid'), index=True)
    createdBy = Column(ForeignKey('user.uid'), nullable=False, index=True)
    visibility = Column(String(255), nullable=False)
    commentable = Column(String(10))

    user = relationship('User')
    schedule = relationship('Schedule')

    def __init__(self, ntext, ntime, nlongi, nlati, nradius, visibitily, commentable):
        self.ntext = ntext
        self.ntime = ntime
        self.nlongi = nlongi
        self.nlati = nlati
        self.nradius = nradius
        # self.nsid = nsid
        # self.createdBy = createdBy
        self.visibility = visibitily
        self.commentable = commentable

    def to_json(self):
        json_comment = {
            'nid': self.nid,
            'ntext': self.ntext,
            'ntime': self.ntime,
            'nlongi': self.nlongi,
            'nlati': self.nlati,
            'nradius': self.nradius,
            'nsid': self.nsid,
            'createdBy': self.createdBy,
            'visibility': self.visibility,
            'commentable': self.commentable,
        }
        return json_comment


class Comment(db.Model):
    __tablename__ = 'comment'

    cid = Column(INTEGER(11), primary_key=True)
    nid = Column(ForeignKey('note.nid'), nullable=False, index=True)
    ctext = Column(String(255), nullable=False)
    createdBy = Column(ForeignKey('user.uid'), nullable=False, index=True)

    user = relationship('User')
    note = relationship('Note')

    def __init__(self, ctext):
        self.ctext = ctext

    def to_json(self):
        json_comment = {
            'cid': self.cid,
            'nid': self.nid,
            'ctext': self.ctext,
            'createdBy': self.createdBy,
        }
        return json_comment


class Notetag(db.Model):
    __tablename__ = 'notetag'

    tname = Column(String(20), primary_key=True, nullable=False)
    nid = Column(ForeignKey('note.nid'), primary_key=True,
                 nullable=False, index=True)

    def __init__(self, tname):
        self.tname = tname

    note = relationship('Note')
