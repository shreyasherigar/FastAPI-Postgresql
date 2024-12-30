from sqlalchemy.orm import Session
from models import Questions
from sqlalchemy import text

def get_questions(db: Session):
    # return db.query(Questions).all()
    query = text("""
        SELECT q.question_text, array_agg(c.choice_text) AS choices
        FROM questions q
        JOIN choices c ON q.id = c.question_id
        GROUP BY q.id;
    """)
    result = db.execute(query).fetchall()
    formatted_result = [{"question_text": row[0], "choices": row[1]} for row in result]
    return formatted_result

