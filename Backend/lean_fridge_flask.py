from flask import Flask, render_template, url_for, request, redirect, flash
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lean_fridge_setup import Base, Stock

engine = create_engine('sqlite:///lean_fridge_app.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/stock/')
def index():
    stock = session.query(Stock).all()
    return render_template('index.html', stock = stock)

@app.route('/stock/<int:item_id>/')
def itemDisplay(item_id):
    item = session.query(Stock).filter_by(id = item_id).one()
    output = ''
    item_id = '<strong>id</strong>: ' + str(item.id) + '</br>'
    item_name = '<strong>item</strong>: ' + item.name + '</br>'
    item_sum = '<strong>total</strong>: ' + str(item.total) + '</br>'
    output = output + item_id + item_name + item_sum
    return output

@app.route('/stock/new/', methods = ['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        newItem = Stock(name = request.form['name'],total = request.form['total'])
        print request.form['name'], request.form['total']
        session.add(newItem)
        session.commit()
        flash("Awesome, a new item has been added to the stock!")
        return redirect(url_for('index'))
    else:
        return render_template('newItem.html')

@app.route('/stock/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(item_id):
    editedItem = session.query(Stock).filter_by(id = item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['total']:
            editedItem.total = request.form['total']
        session.add(editedItem)
        session.commit()
        flash("You've successfully updated this item!")
        return redirect(url_for('index', item_id = editedItem.id))
    else:
        return render_template('editItem.html', item_id = editedItem.id, item = editedItem)

@app.route('/stock/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(item_id):
    itemToDelete = session.query(Stock).filter_by(id = item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("You've successfully deleted this item!")
        return redirect(url_for('index'))
    else:
        return render_template('deleteItem.html', item = itemToDelete)

if __name__ == '__main__':
    app.secret_key = 'flask' ##for coding purpose only
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
