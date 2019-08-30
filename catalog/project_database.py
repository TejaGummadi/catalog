#this entire thing becomes under the model 
from sqlalchemy import Column,Integer,String
#for database structure
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
#orm:object relationship management
from sqlalchemy.orm import relationship
from flask_login import UserMixin
#it describes what is first and what is next
Base=declarative_base()

#register is for create a table
class Register(Base):
	__tablename__='register'

	id=Column(Integer,primary_key=True)
	name=Column(String(100))
	surname=Column(String(100))
	email=Column(String(50))
	branch=Column(String(30))

class User(Base,UserMixin):
	__tablename__='user'

	id=Column(Integer,primary_key=True)
	name=Column(String(100),nullable=False)
	email=Column(String(100),nullable=False)
	password=Column(String(100),nullable=False)


#it tells about creation and first two slashes indicates directory and last slash is for indication
engine=create_engine('sqlite:///iiit.db')
#it just identifies data(which formata of data) and create all describes structure
Base.metadata.create_all(engine)
print("database is created!!!")
