from flask import Flask, render_template, request, jsonify
import sqlite3 as sql
import random
app = Flask(__name__)

DATABASE_FILE = "database.db"
DEFAULT_BUGGY_ID = "1"
DEFAULT_COST_SET_ID = "1"

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
    msg_armour=""
    msg_attack=""
    msg_qty_attacks=""
    msg_fireproof=""
    msg_insulated=""
    msg_antibiotic=""
    msg_banging=""
    msg_algo=""

    qty_wheels = request.form['qty_wheels']
    check_wheels = 0
    if qty_wheels.isdigit():
      qty_wheels = int(request.form['qty_wheels'])
      check_wheels = qty_wheels % 2
      if qty_wheels < 4:
        msg_wheels = f"Number of Wheels Error:  Minimum number of wheels is 4 and you have put {qty_wheels}, please update."
        if check_wheels > 0:
          msg_wheels = f"Number of Wheels Error:  This is not EVEN and you have put {qty_wheels}, so please re-do"
    else:
      msg_wheels = f"Number of Wheels Error:  It is blank, please put a number >=4."

    tyres = request.form['tyres']
    if tyres == "":
      msg_tyres_type = f"Tyres Type Error:  It is blank, please select from the drop-down."
    qty_tyres = request.form['qty_tyres']
    if qty_tyres.isdigit():
      qty_tyres = int(request.form['qty_tyres'])
      if qty_wheels != "":
        if qty_tyres < qty_wheels:
          msg_tyres = f"Number of Tyres Error:  Your Number of Tyres ({qty_tyres}) should be >= Number of Wheels ({qty_wheels})."
    else:
      msg_tyres = f"Number of Tyres Error:  It is blank, please put a number >= Number of Wheels."

    flag_pattern = request.form['flag_pattern']
    flag_color = request.form['flag_color']
    flag_color_secondary = request.form['flag_color_secondary']
    if flag_pattern == "":
      msg_flag_pattern = f"Flag's Pattern Error:  It is blank, please select from the drop-down."
    elif (flag_pattern != "plain" and flag_color_secondary==flag_color):
      msg_flag_color_secondary = f"Flag's Patter Error:  Every Flag Pattern except Plain needs two colours (a primary colour, and a secondary)."

    power_type = request.form['power_type']
    power_units = request.form['power_units']
    if power_type == "":
      msg_power = f"Primary Motive Power Type Error:  It is blank, put select from the drop-down."

    if power_units.isdigit():
      power_units = int(request.form['power_units'])
      if (power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind") and power_units > 1:
        msg_power = f"Primary Motive Power Type Error:  You can only have one primary power unit of non-consumable power (e.g., a single reactor)."
    else:
      msg_power_units = f"Primary Motive Power Units Error:  It is blank, please put a number >=1."

    aux_power_type = request.form['aux_power_type']
    aux_power_units = request.form['aux_power_units']
    if aux_power_units == "":
      msg_aux_power_units = f"Auxiliary Motive Power Units Error:  It is blank, please put a number >=0."
    else:
      aux_power_units = int(request.form['aux_power_units'])
      if (aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind") and (aux_power_units > 1):
        msg_auxiliary2 = f"Auxiliary Motive Power Unit Error:  You can only have one auxiliary power unit of non-consumable power (e.g., a single reactor)."
      if aux_power_type == "" and aux_power_units > 0:
        msg_auxiliary = f"Auxiliary Motive Power Unit Error:  If No Auxiliary Motive Power, please put 0 on the Auxiliary Power Unit."

    hamster_booster = request.form['hamster_booster']
    if hamster_booster.isdigit():
      hamster_booster = int(request.form['hamster_booster'])
      if (power_type != "hamster" and aux_power_type != "hamster") and hamster_booster != 0:
        msg_hamster_booster = f"Hamster Booster Error:  Both Main Power and Other Power Types are not using hamster so there is no need for a hamster booster therefore please put 0."
    else:
      msg_hamster_booster = f"Hamster Booster Error:  It is blank, please put a number >=0."

    armour = request.form['armour']
    if armour == "":
      msg_armour = f"Armour Type Error:  It is blank, put select from the drop-down."

    attack = request.form['attack']
    if attack == "":
      msg_attack = f"Offensive Capability Error:  It is blank, put select from the drop-down."

    qty_attacks = request.form['qty_attacks']
    if qty_attacks != "":
      qty_attacks = int(request.form['qty_attacks'])
    else:
      msg_qty_attacks = f"Number of Attacks Error:  It is blank, please put a number >=0."

    fireproof = request.form['fireproof']
    if fireproof.isdigit():
      fireproof = int(request.form['fireproof'])
    else:
      msg_fireproof = f"Fireproof Error:  It is blank, put select Yes or No."

    insulated = request.form['insulated']
    if insulated.isdigit():
      insulated = int(request.form['insulated'])
    else:
      msg_insulated = f"Insulated Error:  It is blank, put select Yes or No."

    antibiotic = request.form['antibiotic']
    if antibiotic.isdigit():
      antibiotic = int(request.form['antibiotic'])
    else:
      msg_antibiotic = f"Antibiotic Error:  It is blank, put select Yes or No."

    banging = request.form['banging']
    if banging.isdigit():
      banging = int(request.form['banging'])
    else:
      msg_banging = f"Banging Sound System Error:  It is blank, put select Yes or No."

    algo = request.form['algo']
    if algo == "":
      msg_algo = f"Race Computer Algorithm Error:  It is blank, put select from the drop-down."
    else:
      if attack == "none" and algo != "defensive" and algo != "steady":
        msg_algo = f"Race Computer Algorithm Error:  If you have equipped your buggy with no offensive capabilities, choose either defensive or steady. "

    if qty_wheels == "" or tyres == "" or qty_tyres == "" or flag_pattern == "" or flag_color == "" or flag_color_secondary == "" or power_type == "" or \
        power_units == "" or  aux_power_units == "" or hamster_booster == "" or armour == "" or attack == "" or qty_attacks == "" or \
        fireproof == "" or insulated == "" or antibiotic == "" or banging == "" or algo == "" or \
        qty_wheels < 4 or check_wheels > 0 or qty_tyres < qty_wheels or \
        ((power_type != "hamster" and aux_power_type != "hamster") and hamster_booster != 0) or \
        (flag_pattern != "plain" and flag_color_secondary==flag_color) or \
        ((power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind") and power_units > 1) or \
        ((aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind") and (aux_power_units > 1)) or \
        (aux_power_type == "" and aux_power_units > 0) or (attack == "none" and algo != "defensive" and algo != "steady"):
      return render_template("updated.html", msg_wheels = msg_wheels, msg_tyres_type=msg_tyres_type, msg_tyres=msg_tyres, msg_flag_pattern=msg_flag_pattern, \
      msg_flag_color=msg_flag_color, msg_flag_color_secondary=msg_flag_color_secondary, msg_power=msg_power, msg_power_units=msg_power_units, \
      msg_auxiliary=msg_auxiliary, msg_auxiliary2=msg_auxiliary2, msg_aux_power_units=msg_aux_power_units, msg_hamster_booster=msg_hamster_booster, \
      msg_armour=msg_armour, msg_attack=msg_attack, msg_qty_attacks=msg_qty_attacks, msg_fireproof=msg_fireproof, msg_insulated=msg_insulated, \
      msg_antibiotic=msg_antibiotic, msg_banging=msg_banging, msg_algo=msg_algo)

    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM costs WHERE cost_set_id=?", (DEFAULT_COST_SET_ID,))
    record_cost = cur.fetchone();

    power_cost = 0
    if power_type == "petrol":
      power_cost = record_cost['petrol_cost'] * power_units
    elif power_type == "fusion":
      power_cost = record_cost['fusion_cost']
    elif power_type == "steam":
      power_cost = record_cost['steam_cost'] * power_units
    elif power_type == "bio":
      power_cost = record_cost['bio_cost'] * power_units
    elif power_type == "electric":
      power_cost = record_cost['electric_cost'] * power_units
    elif power_type == "rocket":
      power_cost = record_cost['rocket_cost'] * power_units
    elif power_type == "hamster":
      power_cost = record_cost['hamster_cost'] * power_units
    elif power_type == "thermo":
      power_cost = record_cost['thermo_cost']
    elif power_type == "solar":
      power_cost = record_cost['solar_cost']
    elif power_type == "wind":
      power_cost = record_cost['wind_cost']

    aux_power_cost = 0
    if aux_power_type == "petrol":
      aux_power_cost = record_cost['petrol_cost'] * aux_power_units
    elif aux_power_type == "fusion":
      aux_power_cost = record_cost['fusion_cost']
    elif aux_power_type == "steam":
      aux_power_cost = record_cost['steam_cost'] * aux_power_units
    elif aux_power_type == "bio":
      aux_power_cost = record_cost['bio_cost'] * aux_power_units
    elif aux_power_type == "electric":
      aux_power_cost = record_cost['electric_cost'] * aux_power_units
    elif aux_power_type == "rocket":
      aux_power_cost = record_cost['rocket_cost'] * aux_power_units
    elif aux_power_type == "hamster":
      aux_power_cost = record_cost['hamster_cost'] * aux_power_units
    elif aux_power_type == "thermo":
      aux_power_cost = record_cost['thermo_cost']
    elif aux_power_type == "solar":
      aux_power_cost = record_cost['solar_cost']
    elif aux_power_type == "wind":
      aux_power_cost = record_cost['wind_cost']

    tyre_cost = 0
    if tyres == "knobbly":
      tyre_cost = record_cost['tyres_knobbly_cost'] * qty_tyres
    elif tyres == "slick":
      tyre_cost = record_cost['tyres_slick_cost'] * qty_tyres
    elif tyres == "steelband":
      tyre_cost = record_cost['tyres_steelband_cost'] * qty_tyres
    elif tyres == "reactive":
      tyre_cost = record_cost['tyres_reactive_cost'] * qty_tyres
    elif tyres == "maglev":
      tyre_cost = record_cost['tyres_maglev_cost'] * qty_tyres

    if qty_wheels == 4:
      armour_uplift = 1
    elif qty_wheels > 4:
      armour_uplift = (qty_wheels - 4) * 0.1 + 1
    armour_cost = 0
    if armour == "none":
      armour_cost = record_cost['armour_none_cost']
    elif armour == "wood":
      armour_cost = record_cost['armour_wood_cost'] * armour_uplift
    elif armour == "aluminium":
      armour_cost = record_cost['armour_aluminium_cost'] * armour_uplift
    elif armour == "thinsteel":
      armour_cost = record_cost['armour_thinsteel_cost'] * armour_uplift
    elif armour == "thicksteel":
      armour_cost = record_cost['armour_thicksteel_cost'] * armour_uplift
    elif armour == "titanium":
      armour_cost = record_cost['armour_titanium_cost'] * armour_uplift

    attack_cost = 0
    if attack == "none":
      attack_cost = record_cost['attack_none_cost']
    elif attack == "spike":
      attack_cost = record_cost['attack_spike_cost'] * qty_attacks
    elif attack == "flame":
      attack_cost = record_cost['attack_flame_cost'] * qty_attacks
    elif attack == "charge":
      attack_cost = record_cost['attack_charge_cost'] * qty_attacks
    elif attack == "biohazard":
      attack_cost = record_cost['attack_biohazard_cost'] * qty_attacks

    total_cost = (hamster_booster * record_cost['hamster_booster_cost']) + (fireproof * record_cost['fireproof_cost']) + (insulated * record_cost['insulated_cost']) + \
        (antibiotic * record_cost['antibiotic_cost']) + (banging * record_cost['banging_cost']) + power_cost + aux_power_cost + \
        tyre_cost + armour_cost + attack_cost

    con.close()

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
# a page for displaying the costs summary
#------------------------------------------------------------
@app.route('/costs', methods = ['POST', 'GET'])
def costs_buggies():
  if request.method == 'GET':
    con = sql.connect(DATABASE_FILE)
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM costs WHERE cost_set_id=?", (DEFAULT_COST_SET_ID,))
    record = cur.fetchone();
    return render_template("costs-form.html", costs=record)
  elif request.method == 'POST':
    hamster_booster_cost = int(request.form['hamster_booster_cost'])
    fireproof_cost = int(request.form['fireproof_cost'])
    insulated_cost = int(request.form['insulated_cost'])
    antibiotic_cost = int(request.form['antibiotic_cost'])
    banging_cost = int(request.form['banging_cost'])
    petrol_cost = int(request.form['petrol_cost'])
    fusion_cost = int(request.form['fusion_cost'])
    steam_cost = int(request.form['steam_cost'])
    bio_cost = int(request.form['bio_cost'])
    electric_cost = int(request.form['electric_cost'])
    rocket_cost = int(request.form['rocket_cost'])
    hamster_cost = int(request.form['hamster_cost'])
    thermo_cost = int(request.form['thermo_cost'])
    solar_cost = int(request.form['solar_cost'])
    wind_cost = int(request.form['wind_cost'])
    tyres_knobbly_cost = int(request.form['tyres_knobbly_cost'])
    tyres_slick_cost = int(request.form['tyres_slick_cost'])
    tyres_steelband_cost = int(request.form['tyres_steelband_cost'])
    tyres_reactive_cost = int(request.form['tyres_reactive_cost'])
    tyres_maglev_cost = int(request.form['tyres_maglev_cost'])
    armour_none_cost = int(request.form['armour_none_cost'])
    armour_wood_cost = int(request.form['armour_wood_cost'])
    armour_aluminium_cost = int(request.form['armour_aluminium_cost'])
    armour_thinsteel_cost = int(request.form['armour_thinsteel_cost'])
    armour_thicksteel_cost = int(request.form['armour_thicksteel_cost'])
    armour_titanium_cost = int(request.form['armour_titanium_cost'])
    attack_none_cost = int(request.form['attack_none_cost'])
    attack_spike_cost = int(request.form['attack_spike_cost'])
    attack_flame_cost = int(request.form['attack_flame_cost'])
    attack_charge_cost = int(request.form['attack_charge_cost'])
    attack_biohazard_cost = int(request.form['attack_biohazard_cost'])
    try:
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("UPDATE costs set hamster_booster_cost=?, fireproof_cost=?, insulated_cost=?, antibiotic_cost=?, banging_cost=?, petrol_cost=?, \
        fusion_cost=?, steam_cost=?, bio_cost=?, electric_cost=?, rocket_cost=?, hamster_cost=?, thermo_cost=?, solar_cost=?, wind_cost=?, \
        tyres_knobbly_cost=?, tyres_slick_cost=?, tyres_steelband_cost=?, tyres_reactive_cost=?, tyres_maglev_cost=?, armour_none_cost=?, \
        armour_wood_cost=?, armour_aluminium_cost=?, armour_thinsteel_cost=?, armour_thicksteel_cost=?, armour_titanium_cost=?, \
        attack_none_cost=?, attack_spike_cost=?, attack_flame_cost=?, attack_charge_cost=?, attack_biohazard_cost=? WHERE cost_set_id=?", \
        (hamster_booster_cost, fireproof_cost, insulated_cost, antibiotic_cost, banging_cost, petrol_cost, fusion_cost, steam_cost, \
        bio_cost, electric_cost, rocket_cost, hamster_cost, thermo_cost, solar_cost, wind_cost, tyres_knobbly_cost, tyres_slick_cost, tyres_steelband_cost, \
        tyres_reactive_cost, tyres_maglev_cost, armour_none_cost, armour_wood_cost, armour_aluminium_cost, \
        armour_thinsteel_cost, armour_thicksteel_cost, armour_titanium_cost, attack_none_cost, attack_spike_cost, attack_flame_cost, attack_charge_cost, \
        attack_biohazard_cost, DEFAULT_COST_SET_ID))
        con.commit()
        msg = "Costs Summary Table Record successfully updated"
    except:
      con.rollback()
      msg = "Error in Update Operation"
    finally:
      con.close()
      return render_template("updated.html", msg = msg)


#------------------------------------------------------------
# a page for put costs back to default values
#------------------------------------------------------------
@app.route('/costs_default', methods = ['POST'])
def costs_default():
    try:
      with sql.connect(DATABASE_FILE) as con:
        cur = con.cursor()
        cur.execute("UPDATE costs set hamster_booster_cost=5, fireproof_cost=70, insulated_cost=100, antibiotic_cost=90, banging_cost=42, petrol_cost=4, \
        fusion_cost=400, steam_cost=3, bio_cost=5, electric_cost=20, rocket_cost=16, hamster_cost=3, thermo_cost=300, solar_cost=40, wind_cost=20, \
        tyres_knobbly_cost=15, tyres_slick_cost=10, tyres_steelband_cost=20, tyres_reactive_cost=40, tyres_maglev_cost=50, armour_none_cost=0, \
        armour_wood_cost=40, armour_aluminium_cost=200, armour_thinsteel_cost=100, armour_thicksteel_cost=200, armour_titanium_cost=290, \
        attack_none_cost=0, attack_spike_cost=5, attack_flame_cost=20, attack_charge_cost=28, attack_biohazard_cost=30 WHERE cost_set_id=1")
        con.commit()
        msg = "Costs Summary Table Record back to Default Values"
    except:
      con.rollback()
      msg = "Error in Update Operation"
    finally:
      con.close()
      return render_template("updated.html", msg = msg)


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
# a page for creating default buggy
#------------------------------------------------------------
@app.route('/default_buggy')
def default_buggy():
  qty_wheels = 4
  total_cost = 64
  con = sql.connect(DATABASE_FILE)
  cur = con.cursor()
  cur.execute("INSERT INTO buggies (qty_wheels, total_cost) VALUES (?,?)", (qty_wheels, total_cost))
  con.commit()
  con.close()
  msg = "Default Buggy Created"
  return render_template("updated.html", msg=msg)


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
# delete each buggy
#------------------------------------------------------------
@app.route('/delete/<buggy_id>')
def delete_buggy(buggy_id):
  msg = ""
  try:
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("SELECT * FROM buggies")
      rows = cur.fetchall()
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
# delete all buggies
#------------------------------------------------------------
@app.route('/delete_all')
def delete_all():
  msg = ""
  try:
    with sql.connect(DATABASE_FILE) as con:
      cur = con.cursor()
      cur.execute("SELECT * FROM buggies")
      rows = cur.fetchall()
      if len(rows) == 0:
          msg = "No buggies to be deleted."
      else:
          cur.execute("DELETE FROM buggies")
          con.commit()
          msg = "All Buggies Deleted"
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
  max_number = 30
  max_attempts = 10000
  target_cost = request.form['target_cost']
  msg_wheels=""
  msg_tyres=""
  msg_flag_color_secondary=""
  msg_power=""
  msg_auxiliary=""
  msg_auxiliary2=""
  msg_hamster_booster=""
  msg_algo=""

  if qty_wheels == "":
    qty_wheels = random.randint(4,max_number)
    check_wheels = qty_wheels % 2
    while check_wheels > 0:
      qty_wheels = random.randint(4,max_number)
      check_wheels = qty_wheels % 2
  else:
    qty_wheels = int(request.form['qty_wheels'])
    if qty_wheels < 4:
      msg_wheels = f"Number of Wheels Error:  Minimum number of wheels is 4 and you have put {qty_wheels}, please update."
    check_wheels = qty_wheels % 2
    if check_wheels > 0:
      msg_wheels = f"Number of Wheels Error:  This is not EVEN and you have put {qty_wheels}, so please re-do"

  if qty_tyres == "":
    qty_tyres = random.randint(4,max_number)
    while qty_tyres < qty_wheels:
      qty_tyres = random.randint(4,max_number)
  else:
    qty_tyres = int(request.form['qty_tyres'])
    if qty_tyres < qty_wheels:
      msg_tyres = f"Number of Tyres Error:  Your Number of Tyres ({qty_tyres}) should be >= Number of Wheels ({qty_wheels})."

  if tyres == "":
    tyres = random.choice(["knobbly","slick","steelband","reactive","maglev"])

  if flag_pattern == "":
    flag_pattern = random.choice(["plain","vstripe","hstripe","dstripe","checker","spot"])
  else:
    flag_pattern = request.form['flag_pattern']
    if (flag_pattern != "plain" and flag_color_secondary==flag_color):
      msg_flag_color_secondary = f"Flag's Patter Error:  Every Flag Pattern except Plain needs two colours (a primary colour, and a secondary)."

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
      power_units = random.randint(1,max_number)
  else:
    power_units = int(request.form['power_units'])
    if (power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind") and power_units > 1:
      msg_power = f"Primary Motive Power Type Error:  You can only have one primary power unit of non-consumable power (e.g., a single reactor)."

  if aux_power_type == "":
    aux_power_type = random.choice([None,"petrol","fusion","steam","bio","electric","rocket","hamster","thermo","solar","wind"])

  if aux_power_units == "":
    if aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind":
      aux_power_units = 1
    elif aux_power_type == None:
      aux_power_units = 0
    else:
      aux_power_units = random.randint(1,max_number)
  else:
    aux_power_units = int(request.form['aux_power_units'])
    if (aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind") and (aux_power_units > 1):
      msg_auxiliary2 = f"Auxiliary Motive Power Unit Error:  You can only have one auxiliary power unit of non-consumable power (e.g., a single reactor)."
    if aux_power_type == "" and aux_power_units > 0:
      msg_auxiliary = f"Auxiliary Motive Power Unit Error:  If No Auxiliary Motive Power, please put 0 on the Auxiliary Power Unit."

  if hamster_booster == "":
    if power_type == "hamster" or  aux_power_type == "hamster":
      hamster_booster = random.randint(1,max_number)
    else:
      hamster_booster = 0
  else:
    hamster_booster = int(request.form['hamster_booster'])
    if (power_type != "hamster" and aux_power_type != "hamster") and hamster_booster != 0:
      msg_hamster_booster = f"Hamster Booster Error:  Both Main Power and Other Power Types are not using hamster so there is no need for a hamster booster therefore please put 0."

  if armour == "":
    armour = random.choice(["none","wood","aluminium","thinsteel","thicksteel","titanium"])

  if attack == "":
    attack = random.choice(["none","spike","flame","charge","biohazard"])
    while attack == "none" and algo != "defensive" and algo != "steady":
      attack = random.choice(["none","spike","flame","charge","biohazard"])

  if qty_attacks == "":
    qty_attacks = random.randint(1,max_number)
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
    while attack == "none" and algo != "defensive" and algo != "steady":
      algo = random.choice(["steady","defensive","offensive","titfortat","random"])
  else:
    if attack == "none" and algo != "defensive" and algo != "steady":
      msg_algo = f"Race Computer Algorithm Error:  If you have equipped your buggy with no offensive capabilities, choose either defensive or steady. "

  if qty_wheels < 4 or check_wheels > 0 or qty_tyres < qty_wheels or \
        ((power_type != "hamster" and aux_power_type != "hamster") and hamster_booster != 0) or \
        (flag_pattern != "plain" and flag_color_secondary==flag_color) or \
        ((power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind") and power_units > 1) or \
        ((aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind") and (aux_power_units > 1)) or \
        (aux_power_type == "" and aux_power_units > 0) or (attack == "none" and algo != "defensive" and algo != "steady"):
    return render_template("updated.html", msg_wheels = msg_wheels, msg_tyres=msg_tyres, msg_flag_color_secondary=msg_flag_color_secondary, msg_power=msg_power, \
    msg_auxiliary=msg_auxiliary, msg_auxiliary2=msg_auxiliary2, msg_hamster_booster=msg_hamster_booster, msg_algo=msg_algo)

  con = sql.connect(DATABASE_FILE)
  con.row_factory = sql.Row
  cur = con.cursor()
  cur.execute("SELECT * FROM costs WHERE cost_set_id=?", (DEFAULT_COST_SET_ID,))
  record_cost = cur.fetchone();

  min_power_cost = min(record_cost['petrol_cost'] * 1,record_cost['fusion_cost'],record_cost['steam_cost'] * 1,record_cost['bio_cost'] * 1, \
  record_cost['electric_cost'] * 1,record_cost['rocket_cost'] * 1,record_cost['hamster_cost'] * 1,record_cost['thermo_cost'], \
  record_cost['solar_cost'],record_cost['wind_cost'])

  min_aux_power_cost = 0

  min_tyre_cost = min(record_cost['tyres_knobbly_cost'] * 4,record_cost['tyres_slick_cost'] * 4,record_cost['tyres_steelband_cost'] * 4, \
  record_cost['tyres_reactive_cost'] * 4,record_cost['tyres_maglev_cost'] * 4)

  min_armour_cost = 0

  min_attack_cost = 0

  min_hamster_booster_cost = 0

  min_cost = min_power_cost + min_aux_power_cost + min_tyre_cost + min_armour_cost + min_attack_cost + min_hamster_booster_cost

  max_power_cost = max(record_cost['petrol_cost'] * max_number,record_cost['fusion_cost'],record_cost['steam_cost'] * max_number,record_cost['bio_cost'] * max_number, \
  record_cost['electric_cost'] * max_number,record_cost['rocket_cost'] * max_number,record_cost['hamster_cost'] * max_number,record_cost['thermo_cost'], \
  record_cost['solar_cost'],record_cost['wind_cost'])

  max_aux_power_cost = max(record_cost['petrol_cost'] * max_number,record_cost['fusion_cost'],record_cost['steam_cost'] * max_number,record_cost['bio_cost'] * max_number, \
  record_cost['electric_cost'] * max_number,record_cost['rocket_cost'] * max_number,record_cost['hamster_cost'] * max_number,record_cost['thermo_cost'], \
  record_cost['solar_cost'],record_cost['wind_cost'])

  max_tyre_cost = max(record_cost['tyres_knobbly_cost'] * max_number,record_cost['tyres_slick_cost'] * max_number,record_cost['tyres_steelband_cost'] * max_number, \
  record_cost['tyres_reactive_cost'] * max_number,record_cost['tyres_maglev_cost'] * max_number)

  max_armour_uplift = (max_number - 4) * 0.1 + 1
  max_armour_cost = max(record_cost['armour_none_cost'],record_cost['armour_wood_cost'] * max_armour_uplift,record_cost['armour_aluminium_cost'] * max_armour_uplift, \
  record_cost['armour_thinsteel_cost'] * max_armour_uplift,record_cost['armour_thicksteel_cost'] * max_armour_uplift,record_cost['armour_titanium_cost'] * max_armour_uplift)

  max_attack_cost = max(record_cost['attack_none_cost'],record_cost['attack_spike_cost'] * max_number,record_cost['attack_flame_cost'] * max_number, \
  record_cost['attack_charge_cost'] * max_number,record_cost['attack_biohazard_cost'] * max_number)

  max_hamster_booster_cost = record_cost['hamster_booster_cost'] * max_number

  max_cost = max_power_cost + max_aux_power_cost + max_tyre_cost + max_armour_cost + max_attack_cost + max_hamster_booster_cost + \
  record_cost['fireproof_cost'] + record_cost['insulated_cost'] + record_cost['antibiotic_cost'] + record_cost['banging_cost']

  if target_cost.isdigit():
      target_cost = int(request.form['target_cost'])
      if target_cost > max_cost:
        msg_target_cost = f"Target Cost Error:  Target Cost is higher than the Maximum Cost ({max_cost}).  Please put lower Target Cost."
        return render_template("updated.html", msg_target_cost = msg_target_cost)
      elif target_cost < min_cost:
        msg_target_cost = f"Target Cost Error:  Target Cost is lower than the Minimum Cost ({min_cost}).  Please put higher Target Cost."
        return render_template("updated.html", msg_target_cost = msg_target_cost)

      total_cost = 0

      attempt = 0
      while target_cost != total_cost:
          attempt = attempt + 1
          if attempt == max_attempts:
            msg_attempt = f"Iteration Attempts Error:  The programme has attempted {attempt} times which is the maximum.  Please input another Target Cost."
            return render_template("updated.html", msg_attempt = msg_attempt)

          qty_wheels = random.randint(4,max_number)
          check_wheels = qty_wheels % 2
          while check_wheels > 0:
            qty_wheels = random.randint(4,max_number)
            check_wheels = qty_wheels % 2

          qty_tyres = random.randint(4,max_number)
          while qty_tyres < qty_wheels:
            qty_tyres = random.randint(4,max_number)

          tyres = random.choice(["knobbly","slick","steelband","reactive","maglev"])

          power_type = random.choice(["petrol","fusion","steam","bio","electric","rocket","hamster","thermo","solar","wind"])

          if power_type == "fusion" or power_type == "thermo" or power_type == "solar" or power_type == "wind":
            power_units = 1
          else:
            power_units = random.randint(1,max_number)

          aux_power_type = random.choice([None,"petrol","fusion","steam","bio","electric","rocket","hamster","thermo","solar","wind"])

          if aux_power_type == "fusion" or aux_power_type == "thermo" or aux_power_type == "solar" or aux_power_type == "wind":
            aux_power_units = 1
          elif aux_power_type == None:
            aux_power_units = 0
          else:
            aux_power_units = random.randint(1,max_number)

          if power_type == "hamster" or  aux_power_type == "hamster":
            hamster_booster = random.randint(1,max_number)
          else:
            hamster_booster = 0

          armour = random.choice(["none","wood","aluminium","thinsteel","thicksteel","titanium"])

          attack = random.choice(["none","spike","flame","charge","biohazard"])
          while attack == "none" and algo != "defensive" and algo != "steady":
            attack = random.choice(["none","spike","flame","charge","biohazard"])

          qty_attacks = random.randint(1,max_number)

          fireproof = random.randint(0,1)
          insulated = random.randint(0,1)
          antibiotic = random.randint(0,1)
          banging = random.randint(0,1)

          algo = random.choice(["steady","defensive","offensive","titfortat","random"])
          while attack == "none" and algo != "defensive" and algo != "steady":
            algo = random.choice(["steady","defensive","offensive","titfortat","random"])

          power_cost = 0
          if power_type == "petrol":
            power_cost = record_cost['petrol_cost'] * power_units
          elif power_type == "fusion":
            power_cost = record_cost['fusion_cost']
          elif power_type == "steam":
            power_cost = record_cost['steam_cost'] * power_units
          elif power_type == "bio":
            power_cost = record_cost['bio_cost'] * power_units
          elif power_type == "electric":
            power_cost = record_cost['electric_cost'] * power_units
          elif power_type == "rocket":
            power_cost = record_cost['rocket_cost'] * power_units
          elif power_type == "hamster":
            power_cost = record_cost['hamster_cost'] * power_units
          elif power_type == "thermo":
            power_cost = record_cost['thermo_cost']
          elif power_type == "solar":
            power_cost = record_cost['solar_cost']
          elif power_type == "wind":
            power_cost = record_cost['wind_cost']

          aux_power_cost = 0
          if aux_power_type == "petrol":
            aux_power_cost = record_cost['petrol_cost'] * aux_power_units
          elif aux_power_type == "fusion":
            aux_power_cost = record_cost['fusion_cost']
          elif aux_power_type == "steam":
            aux_power_cost = record_cost['steam_cost'] * aux_power_units
          elif aux_power_type == "bio":
            aux_power_cost = record_cost['bio_cost'] * aux_power_units
          elif aux_power_type == "electric":
            aux_power_cost = record_cost['electric_cost'] * aux_power_units
          elif aux_power_type == "rocket":
            aux_power_cost = record_cost['rocket_cost'] * aux_power_units
          elif aux_power_type == "hamster":
            aux_power_cost = record_cost['hamster_cost'] * aux_power_units
          elif aux_power_type == "thermo":
            aux_power_cost = record_cost['thermo_cost']
          elif aux_power_type == "solar":
            aux_power_cost = record_cost['solar_cost']
          elif aux_power_type == "wind":
            aux_power_cost = record_cost['wind_cost']

          tyre_cost = 0
          if tyres == "knobbly":
            tyre_cost = record_cost['tyres_knobbly_cost'] * qty_tyres
          elif tyres == "slick":
            tyre_cost = record_cost['tyres_slick_cost'] * qty_tyres
          elif tyres == "steelband":
            tyre_cost = record_cost['tyres_steelband_cost'] * qty_tyres
          elif tyres == "reactive":
            tyre_cost = record_cost['tyres_reactive_cost'] * qty_tyres
          elif tyres == "maglev":
            tyre_cost = record_cost['tyres_maglev_cost'] * qty_tyres

          if qty_wheels == 4:
            armour_uplift = 1
          elif qty_wheels > 4:
            armour_uplift = (qty_wheels - 4) * 0.1 + 1
          armour_cost = 0
          if armour == "none":
            armour_cost = record_cost['armour_none_cost']
          elif armour == "wood":
            armour_cost = record_cost['armour_wood_cost'] * armour_uplift
          elif armour == "aluminium":
            armour_cost = record_cost['armour_aluminium_cost'] * armour_uplift
          elif armour == "thinsteel":
            armour_cost = record_cost['armour_thinsteel_cost'] * armour_uplift
          elif armour == "thicksteel":
            armour_cost = record_cost['armour_thicksteel_cost'] * armour_uplift
          elif armour == "titanium":
            armour_cost = record_cost['armour_titanium_cost'] * armour_uplift

          attack_cost = 0
          if attack == "none":
            attack_cost = record_cost['attack_none_cost']
          elif attack == "spike":
            attack_cost = record_cost['attack_spike_cost'] * qty_attacks
          elif attack == "flame":
            attack_cost = record_cost['attack_flame_cost'] * qty_attacks
          elif attack == "charge":
            attack_cost = record_cost['attack_charge_cost'] * qty_attacks
          elif attack == "biohazard":
            attack_cost = record_cost['attack_biohazard_cost'] * qty_attacks

          total_cost = (hamster_booster * record_cost['hamster_booster_cost']) + (fireproof * record_cost['fireproof_cost']) + (insulated * record_cost['insulated_cost']) + \
            (antibiotic * record_cost['antibiotic_cost']) + (banging * record_cost['banging_cost']) + power_cost + aux_power_cost + \
            tyre_cost + armour_cost + attack_cost

  power_cost = 0
  if power_type == "petrol":
    power_cost = record_cost['petrol_cost'] * power_units
  elif power_type == "fusion":
    power_cost = record_cost['fusion_cost']
  elif power_type == "steam":
    power_cost = record_cost['steam_cost'] * power_units
  elif power_type == "bio":
    power_cost = record_cost['bio_cost'] * power_units
  elif power_type == "electric":
    power_cost = record_cost['electric_cost'] * power_units
  elif power_type == "rocket":
    power_cost = record_cost['rocket_cost'] * power_units
  elif power_type == "hamster":
    power_cost = record_cost['hamster_cost'] * power_units
  elif power_type == "thermo":
    power_cost = record_cost['thermo_cost']
  elif power_type == "solar":
    power_cost = record_cost['solar_cost']
  elif power_type == "wind":
    power_cost = record_cost['wind_cost']

  aux_power_cost = 0
  if aux_power_type == "petrol":
    aux_power_cost = record_cost['petrol_cost'] * aux_power_units
  elif aux_power_type == "fusion":
    aux_power_cost = record_cost['fusion_cost']
  elif aux_power_type == "steam":
    aux_power_cost = record_cost['steam_cost'] * aux_power_units
  elif aux_power_type == "bio":
    aux_power_cost = record_cost['bio_cost'] * aux_power_units
  elif aux_power_type == "electric":
    aux_power_cost = record_cost['electric_cost'] * aux_power_units
  elif aux_power_type == "rocket":
    aux_power_cost = record_cost['rocket_cost'] * aux_power_units
  elif aux_power_type == "hamster":
    aux_power_cost = record_cost['hamster_cost'] * aux_power_units
  elif aux_power_type == "thermo":
    aux_power_cost = record_cost['thermo_cost']
  elif aux_power_type == "solar":
    aux_power_cost = record_cost['solar_cost']
  elif aux_power_type == "wind":
    aux_power_cost = record_cost['wind_cost']

  tyre_cost = 0
  if tyres == "knobbly":
    tyre_cost = record_cost['tyres_knobbly_cost'] * qty_tyres
  elif tyres == "slick":
    tyre_cost = record_cost['tyres_slick_cost'] * qty_tyres
  elif tyres == "steelband":
    tyre_cost = record_cost['tyres_steelband_cost'] * qty_tyres
  elif tyres == "reactive":
    tyre_cost = record_cost['tyres_reactive_cost'] * qty_tyres
  elif tyres == "maglev":
    tyre_cost = record_cost['tyres_maglev_cost'] * qty_tyres

  if qty_wheels == 4:
    armour_uplift = 1
  elif qty_wheels > 4:
    armour_uplift = (qty_wheels - 4) * 0.1 + 1
  armour_cost = 0
  if armour == "none":
    armour_cost = record_cost['armour_none_cost']
  elif armour == "wood":
    armour_cost = record_cost['armour_wood_cost'] * armour_uplift
  elif armour == "aluminium":
    armour_cost = record_cost['armour_aluminium_cost'] * armour_uplift
  elif armour == "thinsteel":
    armour_cost = record_cost['armour_thinsteel_cost'] * armour_uplift
  elif armour == "thicksteel":
    armour_cost = record_cost['armour_thicksteel_cost'] * armour_uplift
  elif armour == "titanium":
    armour_cost = record_cost['armour_titanium_cost'] * armour_uplift

  attack_cost = 0
  if attack == "none":
    attack_cost = record_cost['attack_none_cost']
  elif attack == "spike":
    attack_cost = record_cost['attack_spike_cost'] * qty_attacks
  elif attack == "flame":
    attack_cost = record_cost['attack_flame_cost'] * qty_attacks
  elif attack == "charge":
    attack_cost = record_cost['attack_charge_cost'] * qty_attacks
  elif attack == "biohazard":
    attack_cost = record_cost['attack_biohazard_cost'] * qty_attacks

  total_cost = (hamster_booster * record_cost['hamster_booster_cost']) + (fireproof * record_cost['fireproof_cost']) + (insulated * record_cost['insulated_cost']) + \
    (antibiotic * record_cost['antibiotic_cost']) + (banging * record_cost['banging_cost']) + power_cost + aux_power_cost + \
    tyre_cost + armour_cost + attack_cost

  con.close()

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

@app.route('/poster')
def poster():
    return render_template("poster.html")

if __name__ == '__main__':
   app.run(debug = True, host="0.0.0.0")
