import sqlite3

DATABASE_FILE = "database.db"

# important:
#-------------------------------------------------------------
# This script initialises your database for you using SQLite,
# just to get you started... there are better ways to express
# the data you're going to need... especially outside SQLite.
# For example... maybe flag_pattern should be an ENUM (which
# is available in most other SQL databases), or a foreign key
# to a pattern table?
#
# Also... the name of the database (here, in SQLite, it's a
# filename) appears in more than one place in the project.
# That doesn't feel right, does it?
#
#-------------------------------------------------------------

con = sqlite3.connect(DATABASE_FILE)
print("- Opened database successfully in file \"{}\"".format(DATABASE_FILE))

# using Python's triple-quote for multi-line strings:

con.execute("""

  CREATE TABLE IF NOT EXISTS buggies (
    id                    INTEGER PRIMARY KEY,
    qty_wheels            INTEGER DEFAULT 4,
    flag_color            VARCHAR(20) DEFAULT "white",
    flag_color_secondary  VARCHAR(20) DEFAULT "black",
    flag_pattern          VARCHAR(20) DEFAULT "plain",
    power_type            VARCHAR(20) DEFAULT "petrol",
    power_units           INTEGER DEFAULT 1,
    aux_power_type        VARCHAR(20),
    aux_power_units       INTEGER DEFAULT 0,
    hamster_booster       INTEGER DEFAULT 0,
    tyres                 VARCHAR(20) DEFAULT "knobbly",
    qty_tyres             INTEGER DEFAULT 4,
    armour                VARCHAR(20) DEFAULT "none",
    attack                VARCHAR(20) DEFAULT "none",
    qty_attacks           INTEGER DEFAULT 0,
    fireproof             INTEGER DEFAULT 0,
    insulated             INTEGER DEFAULT 0,
    antibiotic            INTEGER DEFAULT 0,
    banging               INTEGER DEFAULT 0,
    algo                  VARCHAR(20) DEFAULT "steady",
    total_cost            INTEGER
  )

""")

con.execute("""

  CREATE TABLE IF NOT EXISTS costs (
    cost_set_id             INTEGER PRIMARY KEY,
    hamster_booster_cost    INTEGER DEFAULT 5,
    fireproof_cost          INTEGER DEFAULT 70,
    insulated_cost          INTEGER DEFAULT 100,
    antibiotic_cost         INTEGER DEFAULT 90,
    banging_cost            INTEGER DEFAULT 42,
    petrol_cost             INTEGER DEFAULT 4,
    fusion_cost             INTEGER DEFAULT 400,
    steam_cost              INTEGER DEFAULT 3,
    bio_cost                INTEGER DEFAULT 5,
    electric_cost           INTEGER DEFAULT 20,
    rocket_cost             INTEGER DEFAULT 16,
    hamster_cost            INTEGER DEFAULT 3,
    thermo_cost             INTEGER DEFAULT 300,
    solar_cost              INTEGER DEFAULT 40,
    wind_cost               INTEGER DEFAULT 20,
	tyres_knobbly_cost	    INTEGER DEFAULT 15,
	tyres_slick_cost		INTEGER DEFAULT 10,
	tyres_steelband_cost	INTEGER DEFAULT 20,
	tyres_reactive_cost		INTEGER DEFAULT 40,
	tyres_maglev_cost		INTEGER DEFAULT 50,
    armour_none_cost        INTEGER DEFAULT 0,
    armour_wood_cost        INTEGER DEFAULT 40,
    armour_aluminium_cost   INTEGER DEFAULT 200,
    armour_thinsteel_cost   INTEGER DEFAULT 100,
    armour_thicksteel_cost  INTEGER DEFAULT 200,
    armour_titanium_cost    INTEGER DEFAULT 290,
    attack_none_cost        INTEGER DEFAULT 0,
    attack_spike_cost       INTEGER DEFAULT 5,
    attack_flame_cost       INTEGER DEFAULT 20,
    attack_charge_cost      INTEGER DEFAULT 28,
    attack_biohazard_cost   INTEGER DEFAULT 30
  )

""")

print("- Table \"buggies\" exists OK")
print("- Table \"costs\" exists OK")

cur = con.cursor()

cur.execute("SELECT * FROM buggies LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
  cur.execute("INSERT INTO buggies (qty_wheels) VALUES (4)")
  con.commit()
  print("- Added one 4-wheeled buggy")
else:
  print("- Found a buggy in the database, nice")

cur.execute("SELECT * FROM costs LIMIT 1")
rows = cur.fetchall()
if len(rows) == 0:
  cur.execute("INSERT INTO costs (hamster_booster_cost) VALUES (5)")
  con.commit()
  print("- Added default cost")
else:
  print("- Found the default cost in the database, nice")

print("- done")

con.close()
