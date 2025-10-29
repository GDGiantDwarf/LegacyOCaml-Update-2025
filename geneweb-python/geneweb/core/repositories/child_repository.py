from sqlalchemy.orm import Session
from geneweb.core.models.ChildInFamily import ChildInFamily


class ChildRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_child(
            self,
            person_id: int,
            family_id: int,
            relation_type: str = None):
        if not person_id:
            raise ValueError("A person_id must be provided")
        if not family_id:
            raise ValueError("A family_id must be provided")
        new_child = ChildInFamily(
            person_id=person_id,
            family_id=family_id,
            relation_type=relation_type)
        self.session.add(new_child)
        self.session.commit()
        return new_child

    def get_child_by_id(self, child_id):
        return (
            self.session.query(ChildInFamily)
            .filter(ChildInFamily.id == child_id)
            .first()
        )

    def update_child_by_id(
        self,
        child_family_id: int,
        person_id: int = None,
        family_id: int = None,
        relation_type: str = None,
    ):
        child = self.get_child_by_id(child_family_id)
        new_child = ChildInFamily(
            person_id=person_id,
            family_id=family_id,
            relation_type=relation_type)
        if not child:
            raise ValueError("child_family_id Invalid")

        for attr, value in vars(new_child).items():
            if attr != "id" and value is not None:
                setattr(child, attr, value)
        self.session.commit()
        return child

    def delete_child_by_id(self, child_id):
        child = self.get_child_by_id(child_id)
        if child:
            self.session.delete(child)
            self.session.commit()
            return True
        return False
