from .database import Base, db


class User(Base):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.CHAR(32))
    avatar = db.Column(db.String(50), nullable=False, server_default=db.text("'default.png'"))
    email = db.Column(db.String(50))
    role = db.Column(db.String(10), nullable=False, server_default=db.text("'user'"))

    @staticmethod
    def find_by_username(username):
        result = User.query.filter_by(username=username).all()
        return result

    @staticmethod
    def user_authenticate(username, password):
        """
        用于判断用户名和密码是否正确
        TODO: 存在SQL注入漏洞
        """
        sql = "select * from user where username='" + str(username) \
              + "' and password='" + str(password) + "';"
        print(sql)
        cursor = db.session.execute(sql)
        result = cursor.fetchall()
        return result

    @staticmethod
    def find_by_id(user_id):
        result = User.query.filter_by(user_id=user_id).all()
        return result

    @staticmethod
    def find_new(length):
        """return the first length newest user"""
        result = User.query.order_by(User.user_id.desc()).limit(5).all()
        return result

    @staticmethod
    def do_register(username, nickname, password):
        user = User(username=username, nickname=nickname, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def change_nickname(user_id, nickname):
        """change user's nickname"""
        result = User.query.filter_by(user_id=user_id).first()
        result.nickname = nickname
        db.session.commit()
        return result

    @staticmethod
    def change_password(user_id, new_password):
        """change user's password, verification happens in controller"""
        result = User.query.filter_by(user_id=user_id).first()
        if result is not None:
            result.password = new_password
            db.session.commit()

    @staticmethod
    def change_avatar(user_id, new_avatar):
        """change user's avatar"""
        result = User.query.filter_by(user_id=user_id).first()
        if result is not None:
            result.avatar = new_avatar
            db.session.commit()

    @staticmethod
    def fuzzy_search(f_nickname, offset, length):
        """fuzzy search users' nickname, return records from offset to offset + length"""
        result = User.query.filter(User.nickname.like(f_nickname)) \
            .order_by(User.user_id.desc()).limit(length).offset(offset).all()
        print(type(result))
        return result

    @staticmethod
    def defective_fuzzy_search(keyword, offset, length):
        # 注入语句为'); drop database bbs; --
        print(keyword)
        sql_cmd = f"select * from user where nickname like '{keyword}'"
        print(sql_cmd)
        cursor = db.session.execute(sql_cmd)
        result = cursor.fetchall()[offset: offset + length]
        # print(result)
        return result

    @staticmethod
    def count_fuzzy_result(f_nickname):
        """return the number of records that satisfy the fuzzy search condition"""
        return User.query.filter(User.nickname.like(f_nickname)).count()

    @staticmethod
    def header_injection(name):
        cursor = db.session.execute("select * from user WHERE username = '" + str(name) + "'")
        result = cursor.fetchall()
        return result
