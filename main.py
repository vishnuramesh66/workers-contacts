from fastapi import FastAPI, Depends, Body
import pyodbc
import uvicorn
import models,schemas
from models import ContactData
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Optional, List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_table(db: Session):
    return db.query(ContactData).all()


@app.post("/api/v/contact_details")
async def create(request: schemas.ContactDetails, db: Session = Depends(get_db)):
    new_contact = models.ContactData(NAME=request.NAME, NUMBER=request.NUMBER)
    db.add(new_contact)
    db.commit()
    # db.refresh()
    return new_contact


@app.get("/api/v/contact_details")
async def all_data(db: Session = Depends(get_db)):
    contacts = db.query(models.ContactData).all()
    return contacts


@app.get("/")
async def root():
    return {"Hello Digitalleaf!"}
#
# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=LAPTOP-HNQEDSK0\SQLEXPRESS;'
#                       'Database=SampleTest;'
#                       'UID= sa;'
#                       'PWD = Digitalleaf66;'
#                       'Trusted_Connection=yes')
#
# cursor = conn.cursor()
# row_to_list = []
# r = cursor.execute('SELECT * FROM CONTACT_DETAILS')
#
# for row in cursor:
#     row_to_list.append([elem for elem in row])
# row_dict = dict(row_to_list)
# print(row_dict)
#
#
# @app.get("/contact_details")
# def details():
#     return {"WORKERS": row_dict}
#
#
# @app.post("/contact_details")
# def new_contact(name, number):
#     cursor.execute('''
#                     INSERT INTO CONTACT_DETAILS(NAME,[PHONE NUMBER])
#                     VALUES (?,?)
#                     ''', (name, number))
#     conn.commit()
#     return ()
#
#
if __name__ == "__main__":
    uvicorn.run("main:app", port=8004)
