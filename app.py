from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:KuroYuki2006@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
@app.route('/check')
def check():
    try:
        db.session.execute(db.text('SELECT 1'))
        return 'Подключение к базе работает'
    except Exception as e:
        return str(e)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/tours')
def tours():
    result = db.session.execute(db.text("""
    SELECT
        countries.country_name,
        cities.city_name,
        tour_types.type_name,
        orders.departurre_date,
        orders.persons,
        orders.price
    FROM orders
    JOIN cities ON orders.city_id = cities.idcities
    JOIN countries ON cities.country_id = countries.idcountries
    JOIN tour_types ON orders.type_id = tour_types.type_id
    """))

    tours = result.fetchall()
    return render_template('tours.html', tours=tours)

@app.route('/clients')
def clients():
    result = db.session.execute(db.text("""
        SELECT
            full_name,
            phone
        FROM clients
    """))

    clients = result.fetchall()

    return render_template('clients.html', clients=clients)

@app.route("/orders")
def orders():
    result = db.session.execute(db.text("""
        SELECT
            clients.full_name,
            countries.country_name,
            cities.city_name,
            tour_types.type_name,
            orders.departurre_date,
            orders.persons,
            orders.price
        FROM orders
        JOIN clients ON orders.client_id = clients.client_id
        JOIN cities ON orders.city_id = cities.idcities
        JOIN countries ON cities.country_id = countries.idcountries
        JOIN tour_types ON orders.type_id = tour_types.type_id
    """))

    orders = result.fetchall()

    return render_template("orders.html", orders=orders)

if __name__ == "__main__":
    app.run(debug=True) 