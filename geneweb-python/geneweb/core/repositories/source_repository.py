from sqlalchemy.orm import Session
from datetime import date
from geneweb.core.models.Source import Source


class SourceRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_source(
        self,
        title: str,
        reference: str,
        type: str,
        repository: str = None,
        notes: str = None,
    ):
        source = Source(
            title=title,
            reference=reference,
            type=type,
            repository=repository,
            notes=notes,
        )
        self.session.add(source)
        self.session.commit()
        return source

    def get_source_by_id(self, source_id):
        return self.session.query(Source).filter(
            Source.id == source_id).first()

    def update_source_by_id(
        self,
        source_id: int,
        title: str = None,
        reference: str = None,
        type: str = None,
        repository: str = None,
        notes: str = None,
    ):
        source = self.get_source_by_id(source_id)
        new_source = Source(
            title=title,
            reference=reference,
            type=type,
            repository=repository,
            notes=notes,
        )
        if not source:
            raise ValueError("source_id is invalid")

        for attr, value in vars(new_source).items():
            if attr != "id" and value is not None:
                setattr(source, attr, value)
        self.session.commit()
        return source

    def delete_source_by_id(self, source_id):
        source = self.get_source_by_id(source_id)
        if source:
            self.session.delete(source)
            self.session.commit()
            return True
        return False
