from flask import *
import requests
from nearby import get_nearby_sorted_places

app = Flask(__name__)
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for simplicity

@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/fetchlocation", methods=['post','get'])
@app.route("/fetchlocation/<location>", methods=['get'])
def location_fetch_post(*location):
    if request.method=='POST':
        location = request.form.get("location")
        result_locations = get_nearby_sorted_places(location)
    else:
        result_locations = get_nearby_sorted_places(location)
    return render_template("results.html", result_locations=result_locations, location=location)


if __name__ == '__main__':
    app.run(debug=True)