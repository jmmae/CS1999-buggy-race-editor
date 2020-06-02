from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"


#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
  if request.method == 'GET':
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
    return render_template("buggy-form.html", buggy = record)
  elif request.method == 'POST':
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM buggies")
    record = cur.fetchone();
    msg=""
    msg_wheels=""
    msg_tyres=""
    msg_flag_color_secondary=""
    msg_power=""
    msg_auxiliary=""
    msg_auxiliary2=""
    msg_algo=""

    qty_wheels = int(request.form['qty_wheels'])
    check_wheels = qty_wheels % 2
    tyres = request.form['tyres']
    qty_tyres = int(request.form['qty_tyres'])
    flag_color = request.form['flag_color']
    flag_pattern = request.form['flag_pattern']
    flag_color_secondary = request.form['flag_color_secondary']
    power_type = request.form['power_type']
    power_units = int(request.form['power_units'])
    aux_power_type = request.form['aux_power_type']
    aux_power_units = int(request.form['aux_power_units'])
    hamster_booster = int(request.form['hamster_booster'])
    armour = request.form['armour']
    attack = request.form['attack']
    qty_attacks = int(request.form['qty_attacks'])
    fireproof = int(request.form['fireproof'])
    insulated = int(request.form['insulated'])
    antibiotic = int(request.form['antibiotic'])
    banging = int(request.form['banging'])

    if check_wheels > 0:
      msg_wheels = f"The Number of Wheels is Not Even, you have put:  {qty_wheels}"
    if qty_tyres < qty_wheels:
      msg_tyres = f"Your Number of Tyres ({qty_tyres}) should be greater or equal to the Number of Wheels ({qty_wheels})."
    if (flag_pattern != "plain" and flag_color_secondary==flag_color) or (flag_pattern == "plain" and flag_color_secondary!=flag_color):
      msg_flag_color_secondary = f"Every Flag Pattern except Plain needs two colours (a primary colour, and a secondary)."
    if (power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind") and power_units > 1:
      msg_power = f"You can only have one primary power unit of non-consumable power (e.g., a single reactor) per Primary Motive Power."
    if (aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind") and aux_power_units > 1:
      msg_auxiliary = f"You can only have one auxiliary power unit of non-consumable power (e.g., a single reactor) per Auxiliary Motive Power."
    if aux_power_type == "None" and aux_power_units > 0:
      msg_auxiliary2 = f"If No Auxiliary Motive Power, please set to 0 the Auxiliary Power Unit."
    if check_wheels > 0 or qty_tyres < qty_wheels or \
        (flag_pattern != "plain" and flag_color_secondary==flag_color) or (flag_pattern == "plain" and flag_color_secondary!=flag_color) or \
        ((power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind") and power_units > 1) or \
        ((aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind") and aux_power_units > 1) or \
        (aux_power_type == "None" and aux_power_units > 0):
      return render_template("buggy-form.html", msg_wheels = msg_wheels, msg_tyres=msg_tyres, msg_flag_color_secondary=msg_flag_color_secondary,
      msg_power=msg_power, msg_auxiliary=msg_auxiliary, msg_auxiliary2=msg_auxiliary2, buggy = record)

    power_cost = 0
    if power_type == "petrol":
      power_cost = 4 * power_units
    elif power_type == "fusion":
      power_cost = 400
    elif power_type == "steam":
      power_cost = 3 * power_units
    elif power_type == "bio":
      power_cost = 5 * power_units
    elif power_type == "electric":
      power_cost = 20 * power_units
    elif power_type == "rocket":
      power_cost = 16 * power_units
    elif power_type == "hamster":
      power_cost = 3 * power_units
    elif power_type == "thermo":
      power_cost = 300
    elif power_type == "solar":
      power_cost = 40
    elif power_type == "wind":
      power_cost = 20

    aux_power_cost = 0
    if aux_power_type == "petrol":
      aux_power_cost = 4 * power_units
    elif aux_power_type == "fusion":
      aux_power_cost = 400
    elif aux_power_type == "steam":
      aux_power_cost = 3 * power_units
    elif aux_power_type == "bio":
      aux_power_cost = 5 * power_units
    elif aux_power_type == "electric":
      aux_power_cost = 20 * power_units
    elif aux_power_type == "rocket":
      aux_power_cost = 16 * power_units
    elif aux_power_type == "hamster":
      aux_power_cost = 3 * power_units
    elif aux_power_type == "thermo":
      aux_power_cost = 300
    elif aux_power_type == "solar":
      aux_power_cost = 40
    elif aux_power_type == "wind":
      aux_power_cost = 20

    tyre_cost = 0
    if tyres == "knobbly":
      tyre_cost = 15 * qty_tyres
    elif tyres == "slick":
      tyre_cost = 10 * qty_tyres
    elif tyres == "steelband":
      tyre_cost = 20 * qty_tyres
    elif tyres == "reactive":
      tyre_cost = 40 * qty_tyres
    elif tyres == "maglev":
      tyre_cost = 50 * qty_tyres

    armour_uplift = (qty_tyres - 4) * 0.1 + 1
    armour_cost = 0
    if armour == "None":
      armour_cost = 0
    elif armour == "wood":
      armour_cost = 40 * armour_uplift
    elif armour == "aluminium":
      armour_cost = 200 * armour_uplift
    elif armour == "thinsteel":
      armour_cost = 100 * armour_uplift
    elif armour == "thicksteel":
      armour_cost = 200 * armour_uplift
    elif armour == "titanium":
      armour_cost = 290 * armour_uplift

    attack_cost = 0
    if attack == "None":
      attack_cost = 0
    elif attack == "spike":
      attack_cost = 5 * qty_attacks
    elif attack == "flame":
      attack_cost = 20 * qty_attacks
    elif attack == "charge":
      attack_cost = 28 * qty_attacks
    elif attack == "biohazard":
      attack_cost = 30 * qty_attacks

    total_cost = (hamster_booster * 5) + (fireproof * 70) + (insulated * 100) + (antibiotic * 90) + (banging * 42) + power_cost + aux_power_cost + \
        tyre_cost + armour_cost + attack_cost

    try:
      algo = request.form['algo']
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("UPDATE buggies set qty_wheels=? WHERE id=?", (qty_wheels, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set flag_color=? WHERE id=?", (flag_color, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set flag_color_secondary=? WHERE id=?", (flag_color_secondary, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set flag_pattern=? WHERE id=?", (flag_pattern, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set power_type=? WHERE id=?", (power_type, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set power_units=? WHERE id=?", (power_units, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set aux_power_type=? WHERE id=?", (aux_power_type, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set aux_power_units=? WHERE id=?", (aux_power_units, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set hamster_booster=? WHERE id=?", (hamster_booster, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set tyres=? WHERE id=?", (tyres, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set qty_tyres=? WHERE id=?", (qty_tyres, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set armour=? WHERE id=?", (armour, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set attack=? WHERE id=?", (attack, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set qty_attacks=? WHERE id=?", (qty_attacks, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set fireproof=? WHERE id=?", (fireproof, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set insulated=? WHERE id=?", (insulated, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set antibiotic=? WHERE id=?", (antibiotic, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set banging=? WHERE id=?", (banging, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set algo=? WHERE id=?", (algo, DEFAULT_BUGGY_ID))
        cur.execute("UPDATE buggies set total_cost=? WHERE id=?", (total_cost, DEFAULT_BUGGY_ID))
        con.commit()
        msg = "Record successfully saved"
    except:
      con.rollback()
      msg = "error in update operation"
    finally:
      con.close()
      return render_template("updated.html", msg = msg)


#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/buggy')
def show_buggies():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies")
  record = cur.fetchone();
  return render_template("buggy.html", buggy = record)

#------------------------------------------------------------
# a page for displaying the buggy
#------------------------------------------------------------
@app.route('/new')
def edit_buggy():
  return render_template("buggy-form.html")


#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json')
def summary():
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (DEFAULT_BUGGY_ID))
  return jsonify(
      {k: v for k, v in dict(zip(
        [column[0] for column in cur.description], cur.fetchone())).items()
        if (v != "" and v is not None)
      }
    )

#------------------------------------------------------------
# delete the buggy
#   don't want DELETE here, because we're anticipating
#   there always being a record to update (because the
#   student needs to change that!)
#------------------------------------------------------------
@app.route('/delete', methods = ['POST'])
def delete_buggy():
  try:
    msg = "deleting buggy"
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("DELETE FROM buggies")
      con.commit()
      msg = "Buggy deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
