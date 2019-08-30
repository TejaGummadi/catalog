from flask import Flask,redirect,url_for,render_template,request,flash
#for including mail
from flask_mail import Mail,Message
#for random number generation we include this package and module
from random import randint
#base for design
from project_database import Register,Base,User
#sessionmaker uses for delete and add and everything(it checks given data is right or wrong)
from sqlalchemy.orm import sessionmaker
#for accessing html
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required
engine=create_engine('sqlite:///iiit.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
#red color:keywords,whitecolor:userdefined,blue color=methods or classes,orange color=special keys,green: functins
DBSession=sessionmaker(bind=engine)
session=DBSession()

app=Flask(__name__)

login_manager=LoginManager(app)
#for authentication
login_manager.login_view='login'
login_manager.login_message_category='info'
app.secret_key='super_secret_key'

#for mail extension
app.config['MAIL_SERVER']='smtp.gmail.com'
#for default port number that is 465
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='tejagummadi515@gmail.com'
app.config['MAIL_PASSWORD']='ammasiva'
#if it is secure then it gives data if we put true
#to access any data we give a false
app.config['MAIL_USE_TLS']=False
#it checks secure or not
app.config['MAIL_USE_SSL']=True

mail=Mail(app)
#for otp random generation
otp=randint(000000,999999)
@app.route("/hello")
def demo():
	return "Hello world welcome to IIIT"

@app.route("/t")
def indexa():
	return "<h1><font color:red>Hello index page</font></h1>"
@app.route("/student/register")
def reg():
	return "register page"
@app.route("/data/<name>/<int:number>")
def data(name,number):
	return "hello {} and my number {}".format(name,number)

@app.route("/admin")
def admin():
	return "hello admin"

@app.route("/student")
def student():
	return "hello student"

@app.route("/info/<name>")
def info(name):
	if name=='admin':
		return redirect(url_for('admin'))
	elif name=='student':
		return redirect(url_for('student'))		
	else:
		return "no url"		
@app.route("/demo_html")
def sample_html():
	return render_template('index.html')
@app.route("/person/<pname>/<int:number>/<branch>")
def hai_html(pname,number,branch):
	return render_template('sample.html',name=pname,number=number,branch=branch)
@app.route("/table/<int:number>")
def table_html(number):
	return render_template('table.html',n=number)

dummy_data=[{"name":'teja','dob':'1999','org':'rgukt'},{"name":'siva','dob':'2002','org':'student'}]
@app.route("/data")
def data_html():
	return render_template('data.html',s=dummy_data)

@app.route("/file_upload",methods=['POST','GET'])
def file_upload():
	return render_template('file_upload.html')

@app.route("/success",methods=['POST','GET'])
def success():
	if request.method=='POST':
		f=request.files['file']
		f.save(f.filename)
		return render_template("files.html",file_name=f.filename)

@app.route("/email")
def email():
	return render_template("demo_email.html")

@app.route("/email_verify",methods=['POST','GET'])
def verify_email():
	email=request.form['email']
	msg=Message('One Time Password',sender='tejagummadi515@gmail.com',recipients=[email])
	msg.body=str(otp)
	mail.send(msg)
	flash("otp has been sent your mail")
	return render_template('email_verify.html')


@app.route("/email_validate",methods=['POST','GET'])
def email_validate():
	user_otp=request.form['otp']
	if otp==int(user_otp):
		register=session.query(Register).all()
		flash("Successfully login....")
		return redirect(url_for('showData',reg=register))
	flash("please check your otp")
	return render_template("email_verify.html")

@app.route("/")
def ind():
	return render_template('ind.html')
@login_required
@app.route('/show',methods=['POST','GET'])
def showData():
	register=session.query(Register).all()
	return render_template('show.html',reg=register)

@app.route("/add",methods=['POST','GET'])
def addData():
	if request.method=='POST':
		newData=Register(name=request.form['name'],
			surname=request.form['surname'],
			email=request.form['email'],
			branch=request.form['branch'])
		session.add(newData)
		session.commit()
		flash("Successfully added newdata %s" %(newData.name))
		return redirect(url_for('showData'))

	else:
		return render_template("add.html")

@app.route("/<int:register_id>/edit", methods=['POST','GET'])
def editData(register_id):
	editedData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		editedData.name=request.form['name']
		editedData.surname=request.form['surname']
		editedData.email=request.form['email']
		editedData.branch=request.form['branch']

		session.add(editedData)
		session.commit()
		flash("Successfully Edited %s" %(editedData.name))
		return redirect(url_for('showData'))
	else:
		return render_template('edit.html',register=editedData)
@app.route("/<int:register_id>/delete",methods=['POST','GET'])
def deleteData(register_id):
	delData=session.query(Register).filter_by(id=register_id).one()
	if request.method=='POST':
		session.delete(delData)
		session.commit()
		flash("Successfully Deleted %s" %(delData.name))
		return redirect(url_for('showData',register_id=register_id))
	else:
		return render_template('delete.html',register=delData)

@app.route("/account",methods=['POST','GET'])
@login_required
def account():
	return render_template('account.html')

@app.route("/register",methods=['POST','GET'])
def register():
	if request.method=='POST':
		userData=User(name=request.form['name'],
			email=request.form['email'],
			password=request.form['password'])
		session.add(userData)
		session.commit()
		return redirect(url_for('ind'))
	else:
		return render_template('register.html')

@login_required
@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('showData'))
	try:
		if request.method=='POST':
			user = session.query(User).filter_by(
				email=request.form['email'],
				password=request.form['password']).first()
		

			if user:
				login_user(user)
				#next_page=request.args.get('next')
				return redirect(url_for('showData'))
				#return redirect(next_page) if next_page else redirect(url_for('showData'))
			else:
				flash("login failed")
		else:
			return render_template('login.html',title="login")
	except Exception as e:
		flash("login failed....")
	else:
		return render_template('login.html',title="login")

def logout():
	logout_user()
	return render_template('login.html')
#for getting user from database and usermixin is for checking
@login_manager.user_loader
def load_user(user_id):
	return session.query(user).get(int(user_id))


@app.route("/main")
def main():
	return render_template('start.html')



@app.route("/amma")
def amma():
	return render_template('something.html')

if __name__=='__main__':
	app.run(debug=True)