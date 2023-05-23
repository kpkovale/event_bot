# Database module init
from .database import engine
from .db_models import Base

Base.metadata.create_all(engine)