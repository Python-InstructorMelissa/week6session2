# from flask import Flask, render_template

# if __name__ ==  "__main__":
#     app.run(debug=True)

from flask_app import app
from flask_app.controllers import flights, airlines, users, bookings

if __name__ == "__main__":
    app.run(debug=True)