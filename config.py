import os

'''
 __file__ is a variable that stores the path of the module which is called
 In this case Python is going to call this module and __file__ will store
the path of this current module or file.
'''


base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'U-would-never-know'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(base_dir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    
