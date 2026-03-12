from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Folder(Base):
    __tablename__ = "folders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    parent_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")
    parent = relationship("Folder", remote_side=[id], backref="children")
    files = relationship("File", back_populates="folder")

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(BigInteger)
    content_type = Column(String)
    storage_path = Column(String) # Path in MinIO/Disk
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User")
    folder = relationship("Folder", back_populates="files")
