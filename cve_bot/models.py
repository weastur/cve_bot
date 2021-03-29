from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class PackageCVE(Base):
    __tablename__ = "package_cve"

    package_name = Column(String, ForeignKey("packages.name", ondelete="cascade"), nullable=False, primary_key=True)
    cve_name = Column(String, ForeignKey("cve.name", ondelete="cascade"), nullable=False, primary_key=True)
    sid_status = Column(String(32), nullable=False, default="")
    sid_urgency = Column(String(64), nullable=False, default="")
    sid_fixed_version = Column(String(64), nullable=False, default="")
    bullseye_status = Column(String(32), nullable=False, default="")
    bullseye_urgency = Column(String(64), nullable=False, default="")
    bullseye_fixed_version = Column(String(64), nullable=False, default="")
    buster_status = Column(String(32), nullable=False, default="")
    buster_urgency = Column(String(64), nullable=False, default="")
    buster_fixed_version = Column(String(64), nullable=False, default="")
    stretch_status = Column(String(32), nullable=False, default="")
    stretch_urgency = Column(String(64), nullable=False, default="")
    stretch_fixed_version = Column(String(64), nullable=False, default="")
    package = relationship("Package", back_populates="cve")
    cve = relationship("CVE", back_populates="packages")


class Package(Base):
    __tablename__ = "packages"

    name = Column(String(64), primary_key=True, nullable=False)
    cve = relationship("PackageCVE", back_populates="package")

    def __repr__(self):
        return f"Package(name={self.name!r})"


class CVE(Base):
    __tablename__ = "cve"

    name = Column(String(32), primary_key=True, nullable=False)
    description = Column(Text, nullable=False, default="")
    scope = Column(String(64), nullable=False, default="")
    debianbug = Column(Integer, nullable=True)
    packages = relationship("PackageCVE", back_populates="cve")

    def __repr__(self):
        return f"CVE(name={self.name} scope={self.scope} debianbug={self.scope})"
