from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
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

    def set_values(self, **kwargs):
        self.sid_status = kwargs["sid_status"]
        self.sid_urgency = kwargs["sid_urgency"]
        self.sid_fixed_version = kwargs["sid_fixed_version"]
        self.bullseye_status = kwargs["bullseye_status"]
        self.bullseye_urgency = kwargs["bullseye_urgency"]
        self.bullseye_fixed_version = kwargs["bullseye_fixed_version"]
        self.buster_status = kwargs["buster_status"]
        self.buster_urgency = kwargs["buster_urgency"]
        self.buster_fixed_version = kwargs["buster_fixed_version"]
        self.stretch_status = kwargs["stretch_status"]
        self.stretch_urgency = kwargs["stretch_urgency"]
        self.stretch_fixed_version = kwargs["stretch_fixed_version"]

    @staticmethod
    def get_pk(package_name, cve_name):
        return f"{package_name}:{cve_name}"

    @property
    def pk(self):
        return self.get_pk(self.package_name, self.cve_name)


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

    def set_values(self, **kwargs):
        self.scope = kwargs["scope"]
        self.description = kwargs["description"]
        self.debianbug = kwargs["debianbug"]

    def __repr__(self):
        return f"CVE(name={self.name} scope={self.scope} debianbug={self.debianbug})"


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    chat_id = Column(Integer, nullable=False)
    cve = relationship(
        "CVE",
        secondary=Table(
            "subscription_cve",
            Base.metadata,
            Column("cve_name", Integer, ForeignKey("cve.name"), primary_key=True, nullable=False),
            Column("subscription_id", Integer, ForeignKey("subscriptions.id"), primary_key=True, nullable=False),
        ),
        backref="subscriptions",
    )

    def __repr__(self):
        return f"Subscription(id={self.id} chat_id={self.chat_id} cve={self.cve})"


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    subscription = relationship("Subscription")
    information = Column(Text, nullable=False)

    def __repr__(self):
        return f"Notification(id={self.id} chat_id={self.chat_id})"
