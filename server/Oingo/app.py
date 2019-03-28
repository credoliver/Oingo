import configparser as cparser
import json
import os
import traceback

import pymysql
from ext import db
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from models import User, Filter, Schedule, Note, Notetag, Friend, Friendrequest, Comment

# Initial
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:FrAnK3.1415926@localhost:3308/proj?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

CORS(app, resources=r'/*')

conn = pymysql.connect("localhost", "root", "FrAnK3.1415926", "proj", 3308)


# Control
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return str(session)
    if request.method == 'POST':
        return str(session)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if User.query.filter_by(uemail=data['uemail']).first() is None:
            db.session.add(
                User(data['uname'], data['uemail'], data['upassword'], data['ustate'], data['ulongi'], data['ulati']))
            db.session.commit()
            return jsonify({'status': 1, 'message': 'Register successfully!'})
        else:
            return jsonify({'status': 0, 'message': 'Email already exists!'})


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if data['uemail'] in session:
            return jsonify({'status': 0, 'message': 'The same user cannot log in repeatedly!'})
        else:
            user = User.query.filter_by(uemail=data['uemail']).first()
            if user:
                if data['upassword'] == user.upassword:
                    session[data['uemail']] = user.uid
                    return jsonify({'status': 1, 'message': 'Login Successfully!'})
                else:
                    return jsonify({'status': 0, 'message': 'Incorrect Password!'})
            else:
                return jsonify({'status': 0, 'message': 'User haven\'t register yet!'})


@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if data['uemail'] in session:
            session.pop(data['uemail'], None)
            return jsonify({'status': 1, 'message': 'Logout Successfully!'})
        else:
            return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/updateUserLocation', methods=['POST'])
def updateUserLocation():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if data['uemail'] in session:
            user = User.query.filter_by(uemail=data['uemail']).first()
            user.ulongi, user.ulati = data['ulongi'], data['ulati']
            db.session.commit()
            return jsonify({'status': 1, 'message': 'Update user location successful!'})
        else:
            return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


# only for TA test
@app.route('/updateUserCurrentTime', methods=['POST'])
def updateUserCurrentTime():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if data['uemail'] in session:
            user = User.query.filter_by(uemail=data['uemail']).first()
            user.ucurrentTime = data['ucurrentTime']
            db.session.commit()
            return jsonify({'status': 1, 'message': 'Update user time successful!'})
        else:
            return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


# Note
@app.route('/notes/timeline', methods=['GET'])
def applyFilter():
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        uid = session[data['uemail']]
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''SELECT * FROM applyfilter WHERE uid = %s ;''', uid)
            fetch = cursor.fetchall()
            notes = []
            tags = []
            notesWithTag = []
            for i, _ in enumerate(fetch):
                nid = fetch[0][i]
                notes += Note.query.filter_by(nid=nid).all()
                tags += Notetag.query.filter_by(nid=nid).all()
            
            for note in notes:
                noteWithTag = note.to_json()
                for tag in tags:
                    if note.nid == tag.note.nid: 
                        noteWithTag.setdefault('tag', []).append(tag.tname)
                notesWithTag.append(noteWithTag)
    
            return jsonify({'notesList': notesWithTag})
        except:
            traceback.print_exc()
            conn.rollback()
            return jsonify({'status': 0})
        finally:
            cursor.close()
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})

@app.route('/notes', methods=['GET'])
def listNotes():
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        nids = [note.nid for note in
                Note.query.filter_by(createdBy=session[data['uemail']]).all()]
        notes = []
        notesWithTag = []
        tags = []
        
        for nid in nids:
            tags += Notetag.query.filter_by(nid=nid).all()
            notes += Note.query.filter_by(nid=nid).all()

        for note in notes:
            noteWithTag = note.to_json()
            for tag in tags:
                if note.nid == tag.note.nid: 
                    noteWithTag.setdefault('tag', []).append(tag.tname)
            notesWithTag.append(noteWithTag)

        return jsonify({'notesList': notesWithTag})       
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/notes', methods=['POST'])
def addNote():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if data['uemail'] in session:
            note = Note(data['ntext'], data['ntime'], data['nlongi'],
                        data['nlati'], data['nradius'], data['visibility'], data['commentable'])
            schedule = Schedule(data['starttime'], data['endtime'], int(data['repetition'], 2))
            note.schedule = schedule
            note.user = User.query.filter_by(uid=session[data['uemail']]).first()
            for element in data['tag']:
                ntag = Notetag(element)
                ntag.note = note
                db.session.add(ntag)
            db.session.commit()
            return jsonify({'status': 1})
        else:
            return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/notes/<int:nid>', methods=['DELETE'])
def deleteNote(nid):
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        note = Note.query.filter_by(nid=nid).first()
        if note:
            Comment.query.filter_by(nid=note.nid).delete(synchronize_session=False)
            Schedule.query.filter_by(sid=note.nsid).delete()
            db.session.delete(note)
            db.session.commit()
            return jsonify({'status': 1})
        else:
            return jsonify({'status': 0, 'message': 'Note doesn\'t exist!'})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/notes/<int:nid>', methods=['PUT'])
def updateNote(nid):
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        note = Note.query.filter_by(nid=nid).first()
        note.ntext, note.ntime, note.nlongi, note.nlati, note.nradius, note.visibility, note.commentable = \
            data['ntext'], data['ntime'], data['nlongi'], data['nlati'], data['nradius'], data['visibility'], data[
                'commentable']
        note.schedule.starttime, note.schedule.endtime, note.schedule.repetition = data['starttime'], data[
            'endtime'], data['repetition']
        ntags = Notetag.query.filter_by(nid=note.nid).all()
        for element in data['tag']:
            for ntag in ntags:
                if ntag.tname == element:
                    ntag.note = note
                    db.session.add(ntag)
                else:
                    db.session.delete(ntag)
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})



@app.route('/filters', methods=['POST'])
def addFilter():
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        ofilter = Filter(data['ffrom'], data['ftag'], data['flongi'], data['flati'], data['fradius'], data['ftime'],
                         data['fstate'])
        ofilter.schedule = Schedule(data['starttime'], data['endtime'], data['repetition'])
        ofilter.user = User.query.filter_by(uid=session[data['uemail']]).first()
        db.session.add(ofilter)
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/filters/<int:fid>', methods=['DELETE'])
def deleteFilter(fid):
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        Filter.query.filter_by(fid=fid).delete()
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/filters/<int:fid>', methods=['PUT'])
def updateFilter(fid):
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        mfilter = Filter.query.filter_by(fid=fid).first()
        mfilter.ffrom, mfilter.ftag, mfilter.flongi, mfilter.flati, mfilter.radius, mfilter.ftime, mfilter.fstate = \
            data['ffrom'], data['ftag'], data['flongi'], data['flati'], data['fradius'], data['ftime'], data[
                'fstate']
        mfilter.schedule.starttime, mfilter.schedule.endtime, mfilter.schedule.repetition = data['starttime'], data[
            'endtime'], data['repetition']
        db.session.commit()
        return jsonify({'status': 1})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/filters', methods=['GET'])
def listFilters():
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        Fids = [ofilter.fid for ofilter in
                Filter.query.filter_by(fuid=session[data['uemail']]).all()]
        r = [Filter.query.filter_by(
            fid=fid).first().to_json() for fid in Fids]
        return jsonify({'filtersList': r})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


# Comment
@app.route('/notes/<int:nid>/comments', methods=['GET'])
def listComments(nid):
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        comments = Comment.query.filter_by(nid=nid).all()
        r = [comment.to_json() for comment in comments]
        return jsonify({'commentsList': r})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/notes/<int:nid>/comments', methods=['POST'])
def addComment(nid):
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        note = Note.query.filter_by(nid=nid).first()
        print(note.commentable)
        if not note:
            return jsonify({'status': 0, 'message': 'Unvalid nid!'})
        elif note.commentable == '0':
            return jsonify({'status': 0, 'message': 'Uncommentable note!'})
        elif note.commentable == '1':
            user = User.query.filter_by(uid=session[data['uemail']]).first()
            comment = Comment(data['ctext'])
            comment.note = note
            comment.user = user
            db.session.add(comment)
            db.session.commit()
            return jsonify({'status': 1})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/comments/<int:cid>', methods=['DELETE'])
def deleteComment(cid):
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        comment = Comment.query.filter_by(cid=cid).first()
        if comment.user.uid == session[data['uemail']] or comment.note.createdBy == session[data['uemail']] :
            db.session.delete(comment)
            db.session.commit()
            return jsonify({'status': 1})
        else:
            return jsonify({'status': 0, 'message': 'Operation is forbidden!'})

    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/comments/<int:cid>', methods=['PUT'])
def updateComment(cid):
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        comment = Comment.query.filter_by(cid=cid).first()
        if comment.user.uid == session[data['uemail']]:
            comment.ctext = data['ctext']
            db.session.commit()
            return jsonify({'status': 1})
        else:
            return jsonify({'status': 0, 'message': 'Operation is forbidden!'})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


# FriendRequest
@app.route('/requests', methods=['POST'])
def sendRequest():
    if request.method == 'POST':
        data = json.loads(request.get_data())
        print(data['sendTo'])
        if data['uemail'] in session:
            friendRequest = Friendrequest()
            friendRequest.user = User.query.filter_by(uid=session[data['uemail']]).first()
            friendRequest.user1 = User.query.filter_by(uemail=data['sendTo']).first()
            db.session.add(friendRequest)
            db.session.commit()
            return jsonify({'status': 1})
        else:
            return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/requests', methods=['GET'])
def listRequests():
    data = json.loads(request.get_data())
    if data['uemail'] in session:
        senderUids = [friendRequest.ruid1 for friendRequest in
                      Friendrequest.query.filter_by(ruid2=session[data['uemail']]).all()]
        r = [User.query.filter_by(
            uid=senderUid).first().to_json() for senderUid in senderUids]
        return jsonify({'requestsList': r})
    else:
        return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})


@app.route('/requests/<int:requestFrom>', methods=['POST'])
def acceptRequest(requestFrom):
    if request.method == 'POST':
        data = json.loads(request.get_data())
        if data['uemail'] in session:
            db.session.add(
                Friend(session[data['uemail']], requestFrom))
            db.session.commit()
            return jsonify({'status': 1})
        else:
            return jsonify({'status': 0, 'message': 'User haven\'t login yet!'})

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    app.run(debug=True)
