from datetime import datetime
from typing import Optional

from sqlmodel import (JSON, Column, DateTime, Field, Relationship, SQLModel,
                      func)


class User(SQLModel, table=True):
    __tablename__ = "user"
    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    password: str = Field()
    user_token: str = Field(unique=True)
    name: str = Field(default=None, nullable=True)
    phone: str = Field(default=None, nullable=True)
    unit: int = Field(foreign_key="unit.id")
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    user_roles: list["UserRole"] = Relationship(back_populates="roles_user")
    user_permissions: list["UserPermission"] = Relationship(back_populates="permission_user_list", sa_relationship_kwargs={'lazy': 'joined'})
    user_unit: "Unit" = Relationship(back_populates="unit_set", sa_relationship_kwargs={'lazy': 'joined'})
    user_profile: "UserProfile" = Relationship(back_populates="user_set", sa_relationship_kwargs={'lazy': 'joined'})


class Unit(SQLModel, table=True):
    __tablename__ = "unit"
    id: int = Field(primary_key=True)
    unit_name: str = Field(unique=True)

    unit_set: list["User"] = Relationship(back_populates="user_unit", sa_relationship_kwargs={'lazy': 'joined'})


class Role(SQLModel, table=True):
    __tablename__ = "role"
    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
    slug: str = Field(unique=True, nullable=True)
    description: str = Field(default=None, nullable=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))


class UserRole(SQLModel, table=True):
    __tablename__ = "user_role"
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    role_id: int = Field(foreign_key="role.id")
    roles_user: User | None = Relationship(back_populates="user_roles", sa_relationship_kwargs={'lazy': 'joined'})
    role_set: Role | None = Relationship(sa_relationship_kwargs={'lazy': 'joined'})


class Modules(SQLModel, table=True):
    __tablename__ = "modules"
    id: int = Field(primary_key=True)
    module_name: str = Field(unique=True)
    module_description: str = Field(default=None, nullable=True)


class Permissions(SQLModel, table=True):
    __tablename__ = "permissions"
    id: int = Field(primary_key=True)
    permisson_name: str = Field(unique=True)
    permisson_description: str = Field(default=None, nullable=True)


class UserPermission(SQLModel, table=True):
    __tablename__ = "role_permission"
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    permission_id: int = Field(foreign_key="permissions.id")
    module_id: int = Field(foreign_key="modules.id")
    permission: Permissions | None = Relationship(sa_relationship_kwargs={'lazy': 'joined'})
    permission_user_list: list["User"] = Relationship(back_populates="user_permissions", sa_relationship_kwargs={'lazy': 'joined'})
    module: Modules | None = Relationship(sa_relationship_kwargs={'lazy': 'joined'})


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profile"
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    first_name: Optional[str] = Field(default=None, nullable=True)
    last_name: Optional[str] = Field(default=None, nullable=True)
    phone: Optional[str] = Field(default=None, nullable=True)
    address: Optional[str] = Field(default=None, nullable=True)
    city: Optional[str] = Field(default=None, nullable=True)
    state: Optional[str] = Field(default=None, nullable=True)
    country: Optional[str] = Field(default=None, nullable=True)
    zip_code: Optional[str] = Field(default=None, nullable=True)
    cpf: Optional[str] = Field(default=None, nullable=True)
    avatar: Optional[dict] = Field(sa_column=Column(JSON, default={}))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))

    user_set: User | None = Relationship(sa_relationship_kwargs={'lazy': 'joined'})


class UserLoginHistory(SQLModel, table=True):
    __tablename__ = "user_login_history"
    id: int = Field(primary_key=True)
    login_time: datetime = Field(default=datetime.utcnow)
    logout_time: datetime = Field(default=datetime.utcnow)
    login_ip: str = Field(default=None, nullable=True)
    logout_ip: str = Field(default=None, nullable=True)
    login_status: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))


class UserPasswordHistory(SQLModel, table=True):
    __tablename__ = "user_password_history"
    id: int = Field(primary_key=True)
    psh_password: str = Field()
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now()))
