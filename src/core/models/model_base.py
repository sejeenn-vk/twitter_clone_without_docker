from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr
from src.core.config import settings
from src.utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    def __repr__(self) -> str:
        return "{class_name}({properties})".format(
            class_name=self.__class__.__name__,
            properties={
                p: getattr(self, p)
                for p in dir(self.__class__)
                if isinstance(getattr(self.__class__, p), property)
            },
        )