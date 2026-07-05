from app.database.database import Base, engine

from app.models.observation_sessions import ObservationSession
from app.models.photo_detections import Detection


def init_database():
    Base.metadata.create_all(bind=engine)
    print("Database dan tabel berhasil diinisialisasi!")


if __name__ == "__main__":
    init_database()