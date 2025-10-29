from sqlalchemy.orm import Session
from geneweb.core.models.Family import Family


class FamilyRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_family(
        self,
        spouse1_id: int,
        spouse2_id: int,
        marriage_date=None,
        marriage_place=None,
        divorce_date=None,
        notes=None,
    ):
        family = Family(
            spouse1_id=spouse1_id,
            spouse2_id=spouse2_id,
            marriage_date=marriage_date,
            marriage_place=marriage_place,
            divorce_date=divorce_date,
            notes=notes,
        )
        self.session.add(family)
        self.session.commit()
        return family

    def get_family_by_id(self, family_id: int):
        return self.session.query(Family).filter(
            Family.id == family_id).first()

    def get_all_families(self):
        return self.session.query(Family).all()

    def update_family_by_id(
        self,
        family_id,
        spouse1_id: int = None,
        spouse2_id: int = None,
        marriage_date=None,
        marriage_place=None,
        divorce_date=None,
        notes=None,
    ):
        family = self.get_family_by_id(family_id)
        if not family:
            raise ValueError("family_id is invalid")
        new_family = Family(
            spouse1_id=spouse1_id,
            spouse2_id=spouse2_id,
            marriage_date=marriage_date,
            marriage_place=marriage_place,
            divorce_date=divorce_date,
            notes=notes,
        )

        for attr, value in vars(new_family).items():
            if attr != "id" and value is not None:
                setattr(family, attr, value)
        self.session.commit()
        return family

    def delete_family(self, family_id):
        family = self.get_family_by_id(family_id)
        if family:
            self.session.delete(family)
            self.session.commit()
            return True
        return False
