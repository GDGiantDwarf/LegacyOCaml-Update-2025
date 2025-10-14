from sqlalchemy.orm import Session
from geneweb.core.models.Relation import Relation

class RelationRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_relation(self, person1_id: int, person2_id: int, relation_type: str, event_id: int = None):
        if not person1_id:
            raise ValueError("person1_id is invalid")
        if not person2_id:
            raise ValueError("person2_id is invalid")
        if not relation_type:
            raise ValueError("relation_type is invalid")
        
        relation = Relation(
            person1_id=person1_id,
            person2_id=person2_id,
            relation_type=relation_type,
            event_id=event_id
        )
        self.session.add(relation)
        self.session.commit()
        return relation

    def get_relation_by_id(self, relation_id: int):
        return self.session.query(Relation).filter(Relation.id == relation_id).first()

    def update_relation_by_id(self, relation_id: int, person1_id: int = None, person2_id: int = None, relation_type: str = None, event_id: int = None):
        relation = self.get_relation_by_id(relation_id)
        new_relation = Relation(
            person1_id=person1_id,
            person2_id=person2_id,
            relation_type=relation_type,
            event_id=event_id
        )
        if not relation:
            raise ValueError("relation_id Invalid")
        
        for attr, value in vars(new_relation).items():
            if attr != "id" and value is not None:
                setattr(relation, attr, value)
        self.session.commit()
        return relation
    
    def delete_relation_by_id(self, relation_id: int):
        relation = self.get_relation_by_id(relation_id)
        if relation:
            self.session.delete(relation)
            self.session.commit()
            return True
        return False