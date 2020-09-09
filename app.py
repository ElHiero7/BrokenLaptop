from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

# install using,  pip3 install sqlalchemy flask-sqlalchemy 
from flask_sqlalchemy import SQLAlchemy

# this is the database connection string or link 
# brokenlaptops.db is the name of database and it will be created inside 
# project directory. You can choose any other directory to keep it, 2
# in that case the string will look different. 
database = "sqlite:///brokenlaptops.db"

app = Flask(__name__)

# important configuration parameter, don't miss it 
app.config["SQLALCHEMY_DATABASE_URI"] = database

# database instance. this db will be used in this project 
db = SQLAlchemy(app)

##################################################
# use python shell to create the database (from inside the project directory) 
# >>> from app import db
# >>> db.create_all()
# >>> exit()
# if you do not do this step, the database file will not be created and you will receive an error message saying "table does not exist".
###################################################

@app.route('/')
def index():
    brokenlaptops = BrokenLaptop.query.all()
    return render_template("index.html",brokenlaptops=brokenlaptops)
    

@app.route('/create', methods=['GET','POST'])
def create():
    if request.form:
        brand = request.form.get("brand")
        price = request.form.get("price")
        brokenlaptop = BrokenLaptop(brand=brand,price=price)
        db.session.add(brokenlaptop)
        db.session.commit()
    
    brokenlaptops = BrokenLaptop.query.all()
    return render_template("create.html",brokenlaptops=brokenlaptops)    
    
    
@app.route('/delete/<laptop_id>') 
def delete(laptop_id):
    try:
        brokenlaptop = BrokenLaptop.query.get(laptop_id)
        db.session.delete(brokenlaptop)
        db.session.commit()
         
        
        brokenlaptops = BrokenLaptop.query.all()
        return render_template("delete.html",brokenlaptops=brokenlaptops)
    except:
        return render_template("trash.html")

    
@app.route('/update/<laptop_id>', methods=['GET','POST']) 
def update(laptop_id):
    if request.form:
        newbrand = request.form.get("brand")
        newprice = request.form.get("price")
        
        brokenlaptop = BrokenLaptop.query.get(laptop_id)
        brokenlaptop.brand = newbrand
        brokenlaptop.price = newprice

        db.session.commit()
        return redirect("/")

    brokenlaptop = BrokenLaptop.query.get(laptop_id)
    return render_template("update.html",brokenlaptop=brokenlaptop)


# this class creates a table in the database named broken_laptop with 
# entity fields id as integer, brand as text, and price as decimal number 
# create a module containing this class and import that class into this application and use it
class BrokenLaptop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    brand = db.Column(db.String(40), nullable = False)
    price = db.Column(db.Float, nullable = True)
    

if __name__ == '__main__':
    app.run(debug=True)
