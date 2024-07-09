from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Connect the Flask app with SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an object of SQLAlchemy class
db = SQLAlchemy(app)

# Define the Admin class
class Admin(db.Model):
    admNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stuName = db.Column(db.String(100), nullable=False)
    FatherName = db.Column(db.String(200), nullable=False)
    stuDob = db.Column(db.String(100), nullable=False)
    stuGender = db.Column(db.String(1), nullable=False)
    stuMobile = db.Column(db.String(15), nullable=False)

# Create the database and the table
with app.app_context():
    db.create_all()

# Define the index route
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Fetch the values
        admin_stuName = request.form.get('studentName')
        admin_FatherName = request.form.get('fatherName')
        admin_stuDob = request.form.get('DateofBirth')
        admin_stuGender = request.form.get('studentGender')
        admin_stuMobile = request.form.get('Mob_number')
        
        # Print the values (for debugging)
        print(
            admin_stuName,
            admin_FatherName,
            admin_stuDob,
            admin_stuGender,
            admin_stuMobile
        )
        
        # Add it to the database
        admin = Admin(
            stuName=admin_stuName,
            FatherName=admin_FatherName,
            stuDob=admin_stuDob,
            stuGender=admin_stuGender,
            stuMobile=admin_stuMobile
        )

        db.session.add(admin)
        db.session.commit()
        return redirect('/')
    
    else:
        allTasks = Admin.query.all()
        # Print allTasks (for debugging)
        print(allTasks)
        return render_template('index.html', allTasks=allTasks)
    

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/delete')
def delete():
    serial_number = request.args.get('admNo')
    if serial_number:
        admini = Admin.query.filter_by(admNo=serial_number).first()
        if admini:
            db.session.delete(admini)
            db.session.commit()
    return redirect('/')



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
