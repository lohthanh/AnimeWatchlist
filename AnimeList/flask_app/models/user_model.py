from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
import re
from flask import flash
from flask_app.models import friendship_model

ALPHA = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
ALPHANUMERIC = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.profile_pic = data['profile_pic']
        self.anime_in_progress = data['anime_in_progress']
        self.watched_anime = data['watched_anime']
        self.animes_to_watch = data['animes_to_watch']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls, data):
        query = """INSERT INTO users (username, email, password)
                VALUES ( %(username)s, %(email)s, %(password)s);"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM users 
                WHERE id = %(id)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls (results[0])
        return False
    
    @classmethod
    def get_by_username(cls, data):
        query = """SELECT * FROM users 
                WHERE username = %(username)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls (results[0])
        return False
    
    @classmethod
    def get_unfriended_user_by_name (cls, data ):
        query = """SELECT * FROM users u LEFT JOIN friendships f on u.id = f.user_id WHERE f.user_id != %(id)s;
                """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls (results[0])
        return False

    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM users
                WHERE email = %(email)s;"""
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls (results[0])
        return False
    
    @classmethod
    def get_friends (cls, data):
        query = """
                SELECT users.username, users2.username AS friend_name FROM users JOIN friendships 
                ON users.id = friendships.user_id LEFT JOIN users AS users2 ON users2.id = friendships.friend_id;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            user_instance = cls(results[0])
            friends_list = []
            for row in results:
                if row['friend.id'] == None:
                    return user_instance
                friend_data = {
                    **row,
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at']
                }
                friendship_instance = friendship_model.Friendship(friend_data)
                friends_list.append(friendship_instance)
            user_instance.friends_list = friends_list
            return user_instance
        return False

    
    @staticmethod
    def validate_data (data):
        is_valid = True
        if len(data['username']) < 1:
            is_valid = False
            flash ('Username is required', 'registration')
        elif len(data['username']) < 2:
            is_valid = False
            flash ('Username must be at least 2 characters', 'registration')
        if len(data['email']) < 1:
            is_valid = False
            flash('Email required', 'registration')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be a valid format', 'registration')
        else:
            user_data = {
                'email' : data['email']
            }
            potiential_user = User.get_by_email(user_data)
            if potiential_user:
                flash ('Email already exists!', 'registration')
                is_valid = False
        if len(data['password']) < 1:
            is_valid = False
            flash ('Password required', 'registration')
        elif len(data['password']) < 8:
            is_valid = False
            flash ('Password must be at least 8 characters', 'registration')
        elif data['password'] != data['confirm_password']:
            is_valid = False
            flash ('Password does not match!', 'registration')
        elif not ALPHANUMERIC.match(data['password']):
            is_valid = False
            flash('Password must have at least one number', 'registration')
        elif not ALPHANUMERIC.match(data['password']):
            is_valid = False
            flash('Password must have at least one Uppercase letter', 'registration')
        elif not ALPHANUMERIC.match(data['password']):
            is_valid = False
            flash('Password must have at least one special character', 'registration')
        return is_valid