from flask import Flask, render_template, request,jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/send_data_py', methods=['POST','GET'])
def send_data_py():

    dataGet = request.get_json(force=True)

    print("Results:",dataGet)

    connection_success = False

    try:

      DATABASE_URL = os.environ.get('DATABASE_URL')
      conn = psycopg2.connect(DATABASE_URL)

      ## mapbox gives us an extremely accurate/detailed set of coordinates.
      ## this is great but is largely unneccesary and will be more expensive to store

      dataGet['updated_coordinates'] = []

      for lat,long in dataGet['coordinates']:
          dataGet['updated_coordinates'].append([float(str(lat)[:12]),float(str(long)[:10])])       

      cursor = conn.cursor()
      insert_query = """ INSERT INTO what_is_ca_test_v2 (id, coordinates, demo_hometown, demo_current_town, demo_live_years, 
                        demo_californian, demo_care, demo_justify) 
                        VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')""".format(dataGet['id'],dataGet['updated_coordinates'],
                                                        dataGet['demo_hometown'],dataGet['demo_current_town'],
                                                        dataGet['demo_live_years'],dataGet['demo_californian'],
                                                        dataGet['demo_care'],dataGet['demo_justify'])
      cursor.execute(insert_query)
      conn.commit()
      conn.close()

      connection_success = True

    except:
      connection_success = False

    dataReply = {'connection_status':connection_success}

    return jsonify(dataReply)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=False)
