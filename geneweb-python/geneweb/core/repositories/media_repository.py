from sqlalchemy.orm import Session
from geneweb.core.models.Media import Media


class MediaRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_media(
        self,
        file_path: str,
        description: str = None,
        linked_person_id: int = None,
        linked_event_id: int = None,
    ):
        media = Media(
            file_path=file_path,
            description=description,
            linked_person_id=linked_person_id,
            linked_event_id=linked_event_id,
        )
        self.session.add(media)
        self.session.commit()
        return media

    def get_media_by_id(self, media_id):
        return self.session.query(Media).filter(Media.id == media_id).first()

    def update_media_by_id(
        self,
        media_id,
        file_path: str = None,
        description: str = None,
        linked_person_id: int = None,
        linked_event_id: int = None,
    ):
        media = self.get_media_by_id(media_id)
        if not media:
            raise ValueError("media_id is invalid")
        new_media = Media(
            file_path=file_path,
            description=description,
            linked_person_id=linked_person_id,
            linked_event_id=linked_event_id,
        )
        for attr, value in vars(new_media).items():
            if attr != "id" and value is not None:
                setattr(media, attr, value)
        self.session.commit()
        return media

    def delete_media_by_id(self, media_id):
        media = self.get_media_by_id(media_id)
        if media:
            self.session.delete(media)
            self.session.commit()
            return True
        return False
