from fastapi import FastAPI
import pyodbc
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"Hello Digitalleaf!"}

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-HNQEDSK0\SQLEXPRESS;'
                      'Database=SampleTest;'
                      'UID= sa;'
                      'PWD = Digitalleaf66;'
                      'Trusted_Connection=yes')

cursor = conn.cursor()
row_to_list = []
r = cursor.execute('SELECT * FROM CONTACT_DETAILS')

for row in cursor:
    row_to_list.append([elem for elem in row])
row_dict = dict(row_to_list)
print(row_dict)


@app.get("/contact_details")
def details():
    return {"WORKERS": row_dict}


@app.post("/contact_details")
def new_contact(name, number):
    cursor.execute('''
                    INSERT INTO CONTACT_DETAILS(NAME,[PHONE NUMBER])
                    VALUES (?,?)
                    ''', (name, number))
    conn.commit()
    return ()


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001)
