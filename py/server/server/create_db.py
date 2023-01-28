import csv
import datetime
import math
import sys
import os
from dataclasses import dataclass

from flask import current_app

POSTGRES_USER=os.getenv("postgresUser")
POSTGRES_PASSWORD=os.getenv("postgresPassword")
POSTGRES_DB=os.getenv("postgresDb")

def create_db():
    from server.app import SessionLocal, Zone, Award, Application, engine
    db = SessionLocal()

    zones = [
        "",
        "Colchuck Zone",
        "Core Enchantment Zone",
        "Eightmile/Caroline Zone",
        "Stuart  Zone",
        "Snow Zone",
        "Stuart Zone (stock)",
        "Eightmile/Caroline Zone (",
        "Eightmile/Caroline Zone (stock)",
    ]

    db.query(Zone).delete()
    for id in range(1, len(zones)):
        record = Zone(
            zone_id=id,
            name=zones[id],
        )
        db.add(record)
    db.commit()

    with open("/app/server/cleaned.csv", encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        db.query(Award).delete()
        db.query(Application).delete()
        app_id = 0
        award_id = 0
        for row in csvReader:
            zone1 = zones.index(row["zone1"])
            zone2 = zones.index(row["zone2"])
            zone3 = zones.index(row["zone3"])
            awarded = True if row["awarded"] == "Awarded" else False
            app_id += 1
            award_id_or_none = -1
            if awarded:
                award_id += 1
                awarded_zone = zones.index(row["awardZone"])
                dat = row["awardDate"].split("/")
                if "/" in row["awardDate"]:
                    dat = row["awardDate"].split("/")
                else:
                    dat = [1, 1, 99]
                record = Award(
                    award_id=award_id,
                    application_id=app_id,
                    zone_id=awarded_zone,
                    pref=row["awardPref"],
                    entry=datetime.date(int(dat[2]), int(dat[0]), int(dat[1])),
                    size=row["awardSize"],
                )
                db.add(record)
                db.commit()
                award_id_or_none = award_id
            if "/" in row["date1"]:
                dat1 = row["date1"].split("/")
            else:
                dat1 = [1, 1, 99]
            if "/" in row["date2"]:
                dat2 = row["date2"].split("/")
            else:
                dat2 = [1, 1, 99]
            if "/" in row["date3"]:
                dat3 = row["date3"].split("/")
            else:
                dat3 = [1, 1, 99]
            record = Application(
                application_id=app_id,
                date1=datetime.date(int(dat1[2]), int(dat1[0]), int(dat1[1])),
                date2=datetime.date(int(dat2[2]), int(dat2[0]), int(dat2[1])),
                date3=datetime.date(int(dat3[2]), int(dat3[0]), int(dat3[1])),
                zone1=zone1,
                zone2=zone2,
                zone3=zone3,
                awarded=awarded,
                award_id=award_id_or_none,
            )
            print(f"adding record {app_id} {awarded}")
            db.add(record)
            db.commit()

    with open("./enchantments.db", "w"):
        pass