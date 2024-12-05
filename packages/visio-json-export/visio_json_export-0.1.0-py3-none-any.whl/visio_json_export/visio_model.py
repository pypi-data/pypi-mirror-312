from pydantic import BaseModel, Field
from typing import Dict, Optional

class ConnectionPoint(BaseModel):
    d: Optional[str] = Field(alias='D')

class UserRow(BaseModel):
    value: Optional[str] = Field(alias='Value')
    prompt: Optional[str] = Field(alias='Prompt')

class PropRow(BaseModel):
    label: Optional[str] = Field(alias='Label')
    prompt: Optional[str] = Field(alias='Prompt')
    type: Optional[int] = Field(alias='Type')
    format: Optional[str] = Field(alias='Format')
    value: Optional[str] = Field(alias='Value')

class Shape(BaseModel):
    id: Optional[int] = Field(alias='ID')
    name: Optional[str] = Field(alias='Name')
    name_u: Optional[str] = Field(alias='NameU')
    name_id: Optional[str] = Field(alias='NameID')
    master: Optional[str] = Field(alias='Master')
    text: Optional[str] = Field(alias='Text')
    one_d: Optional[bool] = Field(alias='OneD')
    user_rows: Dict[str, UserRow] = Field(default_factory=dict, alias='UserRows')
    prop_rows: Dict[str, PropRow] = Field(default_factory=dict, alias='PropRows')
    connection_points: Dict[str, ConnectionPoint] = Field(default_factory=dict, alias='ConnectionPoints')

class Connector(BaseModel):
    id: Optional[int] = Field(alias='ID')
    from_shape: Optional[int] = Field(alias='FromShape')
    to_shape: Optional[int] = Field(alias='ToShape')
    from_point: Optional[str] = Field(alias='FromPoint')
    to_point: Optional[str] = Field(alias='ToPoint')
    from_point_d: Optional[str] = Field(alias='FromPointD')
    to_point_d: Optional[str] = Field(alias='ToPointD')

class Page(BaseModel):
    id: Optional[int] = Field(alias='ID')
    name: Optional[str] = Field(alias='Name')
    name_u: Optional[str] = Field(alias='NameU')
    user_rows: Dict[str, UserRow] = Field(default_factory=dict, alias='UserRows')
    prop_rows: Dict[str, PropRow] = Field(default_factory=dict, alias='PropRows')
    shapes: Dict[int, Shape] = Field(default_factory=dict, alias='Shapes')
    connectors: Dict[int, Connector] = Field(default_factory=dict, alias='Connectors')

class Master(BaseModel):
    id: Optional[int] = Field(alias='ID')
    name: Optional[str] = Field(alias='Name')
    name_u: Optional[str] = Field(alias='NameU')
    one_d: Optional[bool] = Field(alias='OneD')

class Document(BaseModel):
    name: Optional[str] = Field(alias='Name')
    full_name: Optional[str] = Field(alias='FullName')
    path: Optional[str] = Field(alias='Path')
    title: Optional[str] = Field(alias='Title')
    subject: Optional[str] = Field(alias='Subject')
    description: Optional[str] = Field(alias='Description')
    creator: Optional[str] = Field(alias='Creator')
    manager: Optional[str] = Field(alias='Manager')
    company: Optional[str] = Field(alias='Company')
    category: Optional[str] = Field(alias='Category')
    keywords: Optional[str] = Field(alias='Keywords')
    language: Optional[str] = Field(alias='Language')
    time_created: Optional[str] = Field(alias='TimeCreated')
    time_edited: Optional[str] = Field(alias='TimeEdited')
    time_saved: Optional[str] = Field(alias='TimeSaved')
    user_rows: Dict[str, UserRow] = Field(default_factory=dict, alias='UserRows')
    prop_rows: Dict[str, PropRow] = Field(default_factory=dict, alias='PropRows')
    masters: Dict[str, Master] = Field(default_factory=dict, alias='Masters')
    pages: Dict[str, Page] = Field(default_factory=dict, alias='Pages')

class VisioModel(BaseModel):
    document: Document = Field(default_factory=Document, alias='Document')
    export_time: Optional[str] = Field(alias='ExportTime')