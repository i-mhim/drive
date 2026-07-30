from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, nullable= False, unique=False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))

class Folder(Base):
    __tablename__ = "folders"
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default=text('now()'))
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parent_folder_id = Column(
        Integer, ForeignKey("folders.id",ondelete="CASCADE"), nullable=True)
    __table_args__ = (
        UniqueConstraint(
            "owner_id",
            "parent_folder_id",
            "name",
            name="uq_owner_parent_name"
        ),
    )

class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key = True, nullable = False)
    filename = Column(String, nullable= False)
    storage_path = Column(String, nullable= False)
    size = Column(Integer, nullable = False)
    mimetype = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable = False, 
        server_default=text('now()'))
    updated_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False,
    server_default=text("now()"),
    onupdate=text("now()"))
    owner_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        )
    folder_id = Column(
        Integer, 
        ForeignKey("folders.id", ondelete="CASCADE"), nullable=True
        )

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key = True, nullable = False)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable = False, 
        server_default=text('now()'))
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        )
    file_id = Column(
        Integer, 
        ForeignKey("files.id", ondelete="CASCADE"), nullable=False
        )
    folder_id = Column(
        Integer, 
        ForeignKey("folders.id", ondelete="CASCADE"), nullable=True
        )
    role = Column(Enum("viewer", "editor", "owner", name = "permission_role"), nullable=False)



