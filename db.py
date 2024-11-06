from sqlmodel import SQLModel, create_engine, Session

db_name = "task.db"
db_url = f"sqlite:///{db_name}"
engine = create_engine(db_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_engine():
    return engine

def get_session():
    with Session(engine) as session:
        yield session
