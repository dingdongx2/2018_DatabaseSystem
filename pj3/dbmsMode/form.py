from wtforms import Form, StringField, SelectField, validators

class contactsForm(Form):
    sid = StringField('sid')
    phone = StringField('phone')
    email = StringField('email')
