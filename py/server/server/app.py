import csv
import datetime
import math
import sys
import os
from dataclasses import dataclass

import flask
import flask_restful
from flask_cors import CORS
from sqlalchemy import (Boolean, Column, Integer, MetaData, String,
                        create_engine, or_)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.types import Date

from server.create_db import create_db


POSTGRES_USER=os.getenv("postgresUser")
POSTGRES_PASSWORD=os.getenv("postgresPassword")
POSTGRES_DB=os.getenv("postgresDb")

# SQLALCHEMY_DATABASE_URL = "sqlite:///server/enchantments.db"
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
meta = MetaData()


@dataclass
class Zone(Base):
    __tablename__ = "zones"
    zone_id: int
    name: str

    zone_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    def jsonify(self):
        return {self.zone_id: {"zone_id": self.zone_id, "name": self.name}}


@dataclass
class Award(Base):
    __tablename__ = "awards"
    award_id: int
    application_id: int
    zone_id: int
    pref: int
    entry: str
    size: int

    award_id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer)
    zone_id = Column(Integer)
    pref = Column(Integer)
    entry = Column(Date)
    size = Column(Integer)

    def jsonify(self):
        return {
            self.award_id: {
                "award_id": self.award_id,
                "application_id": self.application_id,
                "zone_id": self.zone_id,
                "pref": self.pref,
                "entry": self.entry.isoformat(),
                "size": self.size,
            }
        }


@dataclass
class Application(Base):
    __tablename__ = "applications"

    application_id: int
    date1: str
    date2: str
    date3: str
    zone1: int
    zone2: int
    zone3: int
    awarded: bool

    application_id = Column(Integer, primary_key=True, index=True)
    date1 = Column(Date)
    date2 = Column(Date)
    date3 = Column(Date)
    zone1 = Column(Integer)
    zone2 = Column(Integer)
    zone3 = Column(Integer)
    awarded = Column(Boolean)
    award_id = Column(Integer)

    def jsonify(self):
        return {
            self.application_id: {
                "application_id": self.application_id,
                "date1": self.date1.isoformat(),
                "date2": self.date2.isoformat(),
                "date3": self.date3.isoformat(),
                "zone1": self.zone1,
                "zone2": self.zone2,
                "zone3": self.zone3,
                "awarded": self.awarded,
                "award_id": self.award_id,
            }
        }


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = b">`vK\x11)\xf2\xe9\x03\x08.\x84|)\xf5yX\x81i\xee\xb9h*8"
    APP_NAME = "Enchantments API"
    LOG_FILE = "api.log"


class DevelopmentConfig(Config):
    DEBUG = True
    XSS_ALLOWED_ORIGINS = ["http://localhost:3000", "https://localhost:3000"]


def sa_to_json(sa_obj):
    if type(sa_obj) is list:
        return {"data": [dc_obj.jsonify() for dc_obj in sa_obj]}
    return sa_obj.jsonify()


def page_to_json(sa_obj, pagination):
    data = sa_to_json(sa_obj)
    return {"data": data["data"], "pagination": pagination}


class StatsResource(flask_restful.Resource):
    pass


class ApplicationsResource(flask_restful.Resource):
    def get(self, obj_id: str = None):
        params = flask.request.args
        page = int(params.get("page")) if params.get("page") else 0
        limit = int(params.get("limit")) if params.get("limit") else 100
        dat_param = params.get("date")
        zone_param = params.get("zone")
        if limit > 100:
            limit = 100
        if limit < 1:
            limit = 1
        offset = page * limit
        db = SessionLocal()
        query = db.query(Application)
        if obj_id:
            sa_obj = db.query(Application).filter_by(application_id=obj_id).first()
            return sa_to_json(sa_obj), 200
        if dat_param:
            if "-" in dat_param:
                dat = dat_param.split("-")
            else:
                dat = [99, 1, 1]
            dat_filter = datetime.date(int(dat[0]), int(dat[1]), int(dat[2]))
            query = db.query(Application).filter(
                or_(
                    Application.date1 == dat_filter,
                    Application.date2 == dat_filter,
                    Application.date3 == dat_filter,
                )
            )
        if zone_param:
            query = query.filter(
                or_(
                    Application.zone1 == zone_param,
                    Application.zone2 == zone_param,
                    Application.zone3 == zone_param,
                )
            )

        sa_obj = query.limit(limit).offset(offset).all()
        total_records = query.count()
        total_pages = math.ceil(total_records / limit)
        has_next = page < total_pages
        has_previous = page > 0
        next_page = (
            f"/api/applications?page={page+1}&limit={limit}" if has_next else False
        )
        previous_page = (
            f"/api/applications?page={page-1}&limit={limit}" if has_previous else False
        )
        pagination = {
            "page": page,
            "limit": limit,
            "offset": offset,
            "total_pages": total_pages,
            "total_records": total_records,
            "has_next": has_next,
            "has_previous": has_previous,
            "next_page": next_page,
            "previous_page": previous_page,
        }
        return page_to_json(sa_obj, pagination), 200


class AwardsResource(flask_restful.Resource):
    def get(self, obj_id: str = None):
        params = flask.request.args
        page = int(params.get("page")) if params.get("page") else 0
        limit = int(params.get("limit")) if params.get("limit") else 100
        dat_param = params.get("date")
        zone_param = params.get("zone")
        if limit > 100:
            limit = 100
        if limit < 1:
            limit = 1
        offset = page * limit
        db = SessionLocal()
        query = db.query(Award)
        if obj_id:
            sa_obj = db.query(Award).filter_by(award_id=obj_id).first()
            return sa_to_json(sa_obj), 200
        if dat_param:
            if "-" in dat_param:
                dat = dat_param.split("-")
            else:
                dat = [99, 1, 1]
            dat_filter = datetime.date(int(dat[0]), int(dat[1]), int(dat[2]))
            query = db.query(Award).filter(Award.entry == dat_filter)

        if zone_param:
            query = query.filter(Award.zone_id == zone_param)

        sa_obj = query.limit(limit).offset(offset).all()

        total_records = query.count()
        total_pages = math.ceil(total_records / limit)
        has_next = page < total_pages
        has_previous = page > 0
        next_page = f"/api/awards?page={page+1}&limit={limit}" if has_next else False
        previous_page = (
            f"/api/awards?page={page-1}&limit={limit}" if has_previous else False
        )
        pagination = {
            "page": page,
            "limit": limit,
            "offset": offset,
            "total_pages": total_pages,
            "total_records": total_records,
            "has_next": has_next,
            "has_previous": has_previous,
            "next_page": next_page,
            "previous_page": previous_page,
        }
        return page_to_json(sa_obj, pagination), 200


class ZonesResource(flask_restful.Resource):
    def get(self, obj_id: str = None):
        db = SessionLocal()
        Base.metadata.create_all(bind=engine)
        if obj_id:
            sa_obj = db.query(Zone).filter_by(zone_id=obj_id).first()
        else:
            sa_obj = db.query(Zone).all()
        return sa_to_json(sa_obj), 200


def create_app(config_obj=DevelopmentConfig):
    try:
        with open("./enchantments.db") as file:
            pass
    except Exception:
        create_db()

    app = flask.Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_obj)
    return app


def initialize(app):
    api = flask_restful.Api(app)

    api.add_resource(StatsResource, "/api/stats", "/api/stats/<obj_id>")
    api.add_resource(
        ApplicationsResource, "/api/applications", "/api/applications/<obj_id>"
    )
    api.add_resource(AwardsResource, "/api/awards", "/api/awards/<obj_id>")
    api.add_resource(ZonesResource, "/api/zones", "/api/zones/<obj_id>")

    CORS(app)

app = create_app()
initialize(app)

with app.app_context():
    Base.metadata.create_all(engine)



# Notes:
# To get into the python virtual environment, run poetry shell
# To create the sqlite database file (enchantments.db) - make sure it doesn't exist or delete it if it does
# and run app.py on it's own

# to run the server: flask --app server.app --debug run --host localhost
#
# To run as WSGI under gunicorn from a venv:
# gunicorn --bind 127.0.0.1:5000 wsgi:app
