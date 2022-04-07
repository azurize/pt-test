import tokens

from flask import Flask, render_template

app = Flask(__name__)

#   Account creation widget - individual person
#   http://127.0.0.1:5000/individual/


@app.route('/individual/')
def individualAccount():
    TOKEN = tokens.individualToken()
    return render_template('account.html', tokens=TOKEN)


#   Account creation widget - company
#   http://127.0.0.1:5000/company/


@app.route('/company/')
def companyAccount():
    TOKEN = tokens.companyToken()
    return render_template('account.html', tokens=TOKEN)


#   Credit/Debit card linking widget
#   http://127.0.0.1:5000/addcard/
#
#   Test Values + Secrets:
#   -- (MasterCard) 5111330000000006 : 123456
#   -- (Visa)       4457000100000009 : secret


@app.route('/addcard/')
def addCard():
    TOKEN = tokens.linkToken()
    return render_template('addcard.html', tokens=TOKEN)
