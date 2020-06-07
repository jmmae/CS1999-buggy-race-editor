from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import random
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"

BUGGY_RACE_SERVER_URL = "http://rhul.buggyrace.net"
BUGGY_RACE_RULES_URL = "http://rhul.buggyrace.net/specs/"

#------------------------------------------------------------
# the index page
#------------------------------------------------------------
@app.route('/')
def home():
   return render_template('index.html', server_url=BUGGY_RACE_SERVER_URL, rules_url=BUGGY_RACE_RULES_URL)

#------------------------------------------------------------
# creating a new buggy:
#  if it's a POST request process the submitted data
#  but if it's a GET request, just show the form
#------------------------------------------------------------
@app.route('/new', methods = ['POST', 'GET'])
def create_buggy():
  if request.method == 'GET':
    return render_template("buggy-form.html", buggy=None)
  elif request.method == 'POST':
    msg=""
    msg_wheels=""
    msg_tyres_type=""
    msg_tyres=""
    msg_power_units=""
    msg_flag_pattern=""
    msg_flag_color=""
    msg_flag_color_secondary=""
    msg_power=""
    msg_power_units=""
    msg_auxiliary=""
    msg_auxiliary2=""
    msg_aux_power_units=""
    msg_hamster_booster=""

    qty_wheels = request.form['qty_wheels']
    check_wheels = 0
    if qty_wheels == "":
      msg_wheels = f"The Number of Wheels is blank, please put a number >=4."
    else:
      qty_wheels = int(request.form['qty_wheels'])
      check_wheels = qty_wheels % 2
    if check_wheels > 0:
      msg_wheels = f"The Number of Wheels is Not Even, you have put:  {qty_wheels}"

    tyres = request.form['tyres']
    if tyres == "":
      msg_tyres_type = f"The Tyres Type is blank, please put select from the drop-down."
    qty_tyres = request.form['qty_tyres']
    if qty_tyres == "":
      msg_tyres = f"The Number of Tyres is blank, please put a number >= Number of Wheels."
    else:
      qty_tyres = int(request.form['qty_tyres'])
      if qty_tyres < qty_wheels:
        msg_tyres = f"Your Number of Tyres ({qty_tyres}) should be >= Number of Wheels ({qty_wheels})."

    flag_pattern = request.form['flag_pattern']
    flag_color = request.form['flag_color']
    flag_color_secondary = request.form['flag_color_secondary']
    if flag_pattern == "":
      msg_flag_pattern = f"The Flag's Pattern is blank, please select from the drop-down."
    elif (flag_pattern != "plain" and flag_color_secondary==flag_color):
      msg_flag_color_secondary = f"Every Flag Pattern except Plain needs two colours (a primary colour, and a secondary)."

    power_type = request.form['power_type']
    power_units = request.form['power_units']
    if power_type == "":
      msg_power = f"The Primary motive power type is blank, please select from the drop-down."
    if power_units == "":
      msg_power_units = f"The Primary motive power units is blank, please put a number >=1."
    else:
      power_units = int(request.form['power_units'])
      if (power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind") and power_units > 1:
        msg_power = f"Primary Motive Power Type Error:  You can only have one primary power unit of non-consumable power (e.g., a single reactor)."

    aux_power_type = request.form['aux_power_type']
    aux_power_units = request.form['aux_power_units']
    if aux_power_units == "":
      msg_aux_power_units = f"The Auxiliary motive power units is blank, please put a number >=0."
    else:
      aux_power_units = int(request.form['aux_power_units'])
      if (aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind") and (aux_power_units > 1):
        msg_auxiliary2 = f"Auxiliary Motive Power Type Error:  You can only have one auxiliary power unit of non-consumable power (e.g., a single reactor)."
    if aux_power_type == "" and aux_power_units > 0:
      msg_auxiliary = f"If No Auxiliary Motive Power, please put 0 on the Auxiliary Power Unit."

    hamster_booster = request.form['hamster_booster']
    if hamster_booster == "":
      msg_hamster_booster = f"The Hamster Booster is blank, please put a number >=0."
    else:
      hamster_booster = int(request.form['hamster_booster'])
      if (power_type != "hamster" and aux_power_type != "hamster") and hamster_booster != 0:
        msg_hamster_booster = f"Both Main Power and Other Power Types are not using hamster so there is no need for a hamster booster therefore please put 0."


    armour = request.form['armour']
    attack = request.form['attack']
    qty_attacks = int(request.form['qty_attacks'])
    fireproof = int(request.form['fireproof'])
    insulated = int(request.form['insulated'])
    antibiotic = int(request.form['antibiotic'])
    banging = int(request.form['banging'])
    algo = request.form['algo']

    if qty_wheels == "" or tyres == "" or check_wheels > 0 or qty_tyres == "" or qty_tyres < qty_wheels or power_units == "" or aux_power_units == "" or \
        hamster_booster == "" or ((power_type != "hamster" and aux_power_type != "hamster") and hamster_booster != 0) or flag_pattern == "" or (flag_pattern != "plain" and flag_color_secondary==flag_color) or \
        ((power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind") and power_units > 1) or \
        ((aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind") and (aux_power_units > 1)) or \
        (aux_power_type == "" and aux_power_units > 0):
      return render_template("updated.html", msg_wheels = msg_wheels, msg_tyres_type=msg_tyres_type, msg_tyres=msg_tyres, msg_power_units=msg_power_units, \
      msg_aux_power_units=msg_aux_power_units, msg_hamster_booster=msg_hamster_booster, msg_flag_pattern=msg_flag_pattern, \
      msg_flag_color_secondary=msg_flag_color_secondary, msg_power=msg_power, msg_auxiliary=msg_auxiliary, msg_auxiliary2=msg_auxiliary2)

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
      aux_power_cost = 4 * aux_power_units
    elif aux_power_type == "fusion":
      aux_power_cost = 400
    elif aux_power_type == "steam":
      aux_power_cost = 3 * aux_power_units
    elif aux_power_type == "bio":
      aux_power_cost = 5 * aux_power_units
    elif aux_power_type == "electric":
      aux_power_cost = 20 * aux_power_units
    elif aux_power_type == "rocket":
      aux_power_cost = 16 * aux_power_units
    elif aux_power_type == "hamster":
      aux_power_cost = 3 * aux_power_units
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
    if armour == "none":
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
    if attack == "none":
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
      buggy_id = request.form['id']
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        if buggy_id.isdigit():
          cur.execute("UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?, \
          aux_power_type=?, aux_power_units=?, hamster_booster=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, \
          antibiotic=?, banging=?, algo=?, total_cost=? WHERE id=?", \
          (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, \
          hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, \
          algo, total_cost, buggy_id))
        else:
          cur.execute("INSERT INTO buggies (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, \
          aux_power_type, aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, \
          antibiotic, banging, algo, total_cost) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
          (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, \
          aux_power_type, aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, \
          antibiotic, banging, algo, total_cost))
        con.commit()
        msg = "Record successfully saved"
    except:
      con.rollback()
      msg = "Error in Update Operation"
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
  records = cur.fetchall();
  return render_template("buggy.html", buggies=records)

#------------------------------------------------------------
# a page for editing the buggy
#------------------------------------------------------------
@app.route('/edit/<buggy_id>')
def edit_buggy(buggy_id):
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=?", (buggy_id,))
  record = cur.fetchone();
  return render_template("buggy-form.html", buggy=record)

#------------------------------------------------------------
# get JSON from current record
#   this is still probably right, but we won't be
#   using it because we'll be dipping diectly into the
#   database
#------------------------------------------------------------
@app.route('/json/<buggy_id>')
def summary(buggy_id):
  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id))
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
@app.route('/delete/<buggy_id>')
def delete_buggy(buggy_id):
  msg = ""
  try:
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("SELECT * FROM buggies")
      rows = cur.fetchall()
      if len(rows) == 1:
          msg = "Cannot delete last Buggy."
      else:
          cur.execute("DELETE FROM buggies WHERE id=?", (buggy_id,))
          con.commit()
          msg = "Buggy #" + buggy_id + " deleted"
  except:
    con.rollback()
    msg = "error in delete operation"
  finally:
    con.close()
    return render_template("updated.html", msg = msg)


#------------------------------------------------------------
# a page for auto-fill the buggy inputs
#------------------------------------------------------------
@app.route('/autofill', methods = ['POST'])
def autofill():
  qty_wheels = request.form['qty_wheels']
  tyres = request.form['tyres']
  qty_tyres = request.form['qty_tyres']
  flag_color = request.form['flag_color']
  flag_pattern = request.form['flag_pattern']
  flag_color_secondary = request.form['flag_color_secondary']
  power_type = request.form['power_type']
  power_units = request.form['power_units']
  aux_power_type = request.form['aux_power_type']
  aux_power_units = request.form['aux_power_units']
  hamster_booster = request.form['hamster_booster']
  armour = request.form['armour']
  attack = request.form['attack']
  qty_attacks = request.form['qty_attacks']
  fireproof = request.form['fireproof']
  insulated = request.form['insulated']
  antibiotic = request.form['antibiotic']
  banging = request.form['banging']
  algo = request.form['algo']

  if qty_wheels == "":
    qty_wheels = random.randint(4,20)
    check_wheels = qty_wheels % 2
    while check_wheels > 0:
      qty_wheels = random.randint(4,20)
      check_wheels = qty_wheels % 2
  else:
    qty_wheels = int(request.form['qty_wheels'])

  if qty_tyres == "":
    qty_tyres = random.randint(4,30)
    while qty_tyres < qty_wheels:
      qty_tyres = random.randint(4,30)
  else:
    qty_tyres = int(request.form['qty_tyres'])

  if tyres == "":
    tyres = random.choice(["knobbly","slick","steelband","reactive","maglev"])

  if flag_pattern == "":
    flag_pattern = random.choice(["plain","vstripe","hstripe","dstripe","checker","spot"])
  else:
    flag_pattern = request.form['flag_pattern']

  if flag_pattern != "plain" and flag_color == flag_color_secondary:
    random_number = random.randint(0,16777215)
    flag_color =format(random_number,'x')
    flag_color = '#'+flag_color
    random_number2 = random.randint(0,16777215)
    flag_color_secondary =format(random_number2,'x')
    flag_color_secondary = '#'+flag_color_secondary

  if power_type == "":
    power_type = random.choice(["petrol","fusion","steam","bio","electric","rocket","hamster","thermo","solar","wind"])

  if power_units == "":
    if power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind":
      power_units = 1
    else:
      power_units = random.randint(1,30)
  else:
    power_units = int(request.form['power_units'])

  if aux_power_type == "":
    aux_power_type = random.choice([None,"petrol","fusion","steam","bio","electric","rocket","hamster","thermo","solar","wind"])

  if aux_power_units == "":
    if aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind":
      aux_power_units = 1
    elif aux_power_type == None:
      aux_power_units = 0
    else:
      aux_power_units = random.randint(1,30)
  else:
    aux_power_units = int(request.form['aux_power_units'])

  if hamster_booster == "":
    if power_type == "hamster" or  aux_power_type == "hamster":
      hamster_booster = random.randint(1,30)
    else:
      hamster_booster = 0
  else:
    hamster_booster = int(request.form['hamster_booster'])

  if armour == "":
    armour = random.choice(["none","wood","aluminium","thinsteel","thicksteel","titanium"])

  if attack == "":
    attack = random.choice(["none","spike","flame","charge","biohazard"])

  if qty_attacks == "":
    qty_attacks = random.randint(1,30)
  else:
    qty_attacks = int(request.form['qty_attacks'])

  if fireproof == "":
    fireproof = random.randint(0,1)
  else:
    fireproof = int(request.form['fireproof'])

  if insulated == "":
    insulated = random.randint(0,1)
  else:
    insulated = int(request.form['insulated'])

  if antibiotic == "":
    antibiotic = random.randint(0,1)
  else:
    antibiotic = int(request.form['antibiotic'])

  if banging == "":
    banging = random.randint(0,1)
  else:
    banging = int(request.form['banging'])

  if algo == "":
    algo = random.choice(["steady","defensive","offensive","titfortat","random"])

  try:
    buggy_id = request.form['id']
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      if buggy_id.isdigit():
        cur.execute("UPDATE buggies set qty_wheels=?, flag_color=?, flag_color_secondary=?, flag_pattern=?, power_type=?, power_units=?, \
        aux_power_type=?, aux_power_units=?, hamster_booster=?, tyres=?, qty_tyres=?, armour=?, attack=?, qty_attacks=?, fireproof=?, insulated=?, \
        antibiotic=?, banging=?, algo=? WHERE id=?", \
        (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, aux_power_type, aux_power_units, \
        hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, antibiotic, banging, \
        algo, buggy_id))
      else:
        cur.execute("INSERT INTO buggies (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, \
        aux_power_type, aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, \
        antibiotic, banging, algo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
        (qty_wheels, flag_color, flag_color_secondary, flag_pattern, power_type, power_units, \
        aux_power_type, aux_power_units, hamster_booster, tyres, qty_tyres, armour, attack, qty_attacks, fireproof, insulated, \
        antibiotic, banging, algo))
        con.commit()
        msg = "Record successfully saved"
  except:
    con.rollback()
  finally:
    con.close()

  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  if buggy_id.isdigit():
    cur.execute("SELECT * FROM buggies WHERE id=? LIMIT 1", (buggy_id,))
    record = cur.fetchone();
    return render_template("buggy-form.html", buggy = record)
  else:
    cur.execute("SELECT * FROM buggies ORDER BY id DESC LIMIT 1")
    record = cur.fetchone();
    return render_template("buggy-form.html", buggy = record)


if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
