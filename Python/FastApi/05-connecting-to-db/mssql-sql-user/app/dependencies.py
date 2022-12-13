from database import SessionLocal

#########################
## DATABASE CONNECTION ##
#########################


def get_db():
    """Method for handling the session to the db. This is used in all methods where
    a connection to the database is needed. It should be used as:
    'db: Session = Depends(get_db')
    Yields:
        sqlalchemy.orm.session.Session: Returns the sqlalchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
