from flask import Flask, redirect, url_for, render_template, request, flash
from models import db, Contact, Note
from forms import ContactForm
from sqlalchemy import desc
from filters import datetimeformat
import secrets

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'
app.config['DEBUG'] = False

# Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:flaskuser@localhost/flask_contacts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.jinja_env.filters['datetimeformat'] = datetimeformat

@app.route("/")
def index():
    '''
    Home page
    '''
    return redirect(url_for('contacts'))

@app.route("/contact/<string:uid>")
def contact(uid):
    contact = Contact.query.filter_by(uid=uid).first()
    Notes = Note.query.filter_by(to=uid).order_by(desc(Note.date)).all()
    if (contact):
        return render_template('web/contact.html',Notes=Notes, contact=contact)
    else:
        flash('No Contact with ('+uid+') found','danger')
        return redirect(url_for('contacts'))


@app.route("/remark", methods=('GET', 'POST'))
def remark():
    if (request.method == 'POST'):
        to = request.form.get('to')
        text = request.form.get('remark')
        new_note = Note(
                        rid=secrets.token_urlsafe(8),
                        to = to,
                        text = text
                        )
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('contact',uid=to))
    else:
        return 'This URL doesen\'t exist'

@app.route("/remark/delete/<string:rid>")
def delremark(rid):
    rem = Note.query.filter_by(rid=rid).first()
    to = rem.to
    db.session.delete(rem)
    db.session.commit()
    return redirect(url_for('student',uid=to))
    

@app.route("/csv", methods=['GET','POST'])
def csvread():
    if (request.method == 'POST'):
        csvf = request.files['file']        
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(csvf.filename)
        filename = random_hex + f_ext
        file_path = os.path.join(app.root_path, 'static/csv', filename)
        csvf.save(file_path)
        with open(file_path, newline='') as csvfile:
            read = csv.DictReader(csvfile)
            for row in read:
                name = row['first_name']
                surname = row['last_name']
                email = row['email']
                phone = row['phone']


                new_contact = Contact(
                    name = name, 
                    surname = surname, 
                    email = email, 
                    phone = phone
                    )
                db.session.add(new_contact)
                db.session.commit()

    
            flash('Contacts added successfully', 'success')
            return redirect(url_for('contacts'))
    else:
        return render_template('web/csv.html')

@app.route("/new_contact", methods=('GET', 'POST'))
def new_contact():
    '''
    Create new contact
    '''
    form = ContactForm()
    if form.validate_on_submit():
        my_contact = Contact()
        form.populate_obj(my_contact)
        db.session.add(my_contact)
        try:
            db.session.commit()
            # User info
            flash('Contact created correctly', 'success')
            return redirect(url_for('contacts'))
        except:
            db.session.rollback()
            flash('Error generating contact.', 'danger')

    return render_template('web/new_contact.html', form=form)


@app.route("/edit_contact/<id>", methods=('GET', 'POST'))
def edit_contact(id):
    '''
    Edit contact

    :param id: Id from contact
    '''
    my_contact = Contact.query.filter_by(id=id).first()
    form = ContactForm(obj=my_contact)
    if form.validate_on_submit():
        try:
            # Update contact
            form.populate_obj(my_contact)
            db.session.add(my_contact)
            db.session.commit()
            # User info
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error update contact.', 'danger')
    return render_template(
        'web/edit_contact.html',
        form=form)


@app.route("/contacts")
def contacts():
    '''
    Show alls contacts
    '''
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=contacts)


@app.route("/search")
def search():
    '''
    Search
    '''
    name_search = request.args.get('name')
    all_contacts = Contact.query.filter(
        Contact.name.contains(name_search)
        ).order_by(Contact.name).all()
    return render_template('web/contacts.html', contacts=all_contacts)


@app.route("/contacts/delete", methods=('POST',))
def contacts_delete():
    '''
    Delete contact
    '''
    try:
        mi_contacto = Contact.query.filter_by(id=request.form['id']).first()
        db.session.delete(mi_contacto)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  contact.', 'danger')

    return redirect(url_for('contacts'))


if __name__ == "__main__":
    app.run()
