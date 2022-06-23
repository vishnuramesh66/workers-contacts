from fastapi import FastAPI, Depends
import uvicorn
import models
import schemas
from models import ContactData
from database import SessionLocal, engine
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
server = app.servers


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_table(db: Session):
    return db.query(ContactData).all()


@app.get("/")
async def root():
    return {"Hello Digitalleaf!"}


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


if __name__ == "__main__":
    uvicorn.run("main:app", port=8004)
