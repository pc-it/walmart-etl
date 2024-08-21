from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config.database import database_settings
from src.config.database_migration import database_migration_settings

engine = create_engine(f'{str(database_settings.SQLALCHEMY_DATABASE_URI)}/walmart', pool_pre_ping=True)
migration_engine = create_engine(f'{str(database_migration_settings.SQLALCHEMY_DATABASE_URI)}/walmart', pool_pre_ping=True)
Base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=False)
Session.configure(binds={
    Base: engine,
})
