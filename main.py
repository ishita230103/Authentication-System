from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine  # Change this line
import models
import schemas
import bcrypt

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
        db_user = models.User(username=user.username, password=hashed_password.decode('utf-8'))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}
