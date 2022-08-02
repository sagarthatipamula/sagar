import json
import psycopg2
from flask import Flask, request
from sqlalchemy import Column, String, Integer, Date, BOOLEAN, and_ ,or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os


app = Flask(__name__)

Base = declarative_base()
database_url = "postgresql://postgres:2402@localhost:5432/postgres"

# disable sqlalchemy pool using NullPool as by default Postgres has its own pool
engine = create_engine(database_url, echo=True, poolclass=NullPool)

Session = sessionmaker(bind=engine)
session = Session()


# original table
class studentinfo(Base):
    __tablename__ = 'student_info'
    name_info = Column("name", String)
    Gender = Column("gender", String)
    Age = Column("age", Integer)
    mobile_no = Column("mobile", Integer, primary_key=True)


@app.route('/fetch-student-info-mobile-name', methods=['GET'])
def home():
    request_name = request.args.get('name')
    request_mobile = request.args.get('mobile')
    results = session.query(studentinfo).filter(and_(studentinfo.mobile_no == request_mobile,\
                                                     studentinfo.name_info == request_name)).all()
    result = [item.__dict__ for item in results]

    for dict_item in result:
        del dict_item['_sa_instance_state']

    return json.dumps(result)


app.run(debug=False)
