from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List,Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from Operations import crud
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text:str
    is_correct:bool

class QuestionBase(BaseModel):
    question_text :str
    choices: List[ChoiceBase]

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
            db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    try:
        db_question = models.Questions(question_text=question.question_text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        for choice in question.choices:
            db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
            db.add(db_choice)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the question and choices.")

@app.get("/questions/")
def read_questions(db: Session = Depends(get_db)):
    result= crud.get_questions(db)
    # print(result)
    return result

