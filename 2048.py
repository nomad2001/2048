import bottle
import model

glavno = model.Glavno()

@bottle.route('/views/<filename:path>')
def send_static(filename):
    return bottle.static_file(filename, root = '/views')

@bottle.get("/")
def index():
    return bottle.template("index.html")

bottle.run(reloader=True, debug=True)