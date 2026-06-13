
from app.config.settings import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

print(f"===== INICIO DO DEBUG =====")
print(f"TIPO DA VARIAVEL: {type(DATABASE_URL)}")
print(f"VALOR EXATO: {repr(DATABASE_URL)}")
print(f"===== FIM DO DEBUG =====")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()