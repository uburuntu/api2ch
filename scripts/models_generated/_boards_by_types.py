# generated by datamodel-codegen:
#   filename:  <stdin>
#   timestamp: 2022-04-30T21:52:44+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class VzroslymItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class IgryItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class Icon(BaseModel):
    name: str
    num: int
    url: str


class PolitikaItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List[Icon]
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class Icon1(BaseModel):
    name: str
    num: int
    url: str


class PolZovatelSkieItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List[Icon1]
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class RaznoeItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class TvorchestvoItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class Icon2(BaseModel):
    name: str
    num: int
    url: str


class TematikaItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List[Icon2]
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class TehnikaISoftItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class JaponskajaKulTuraItem(BaseModel):
    bump_limit: int
    category: str
    default_name: str
    enable_dices: int
    enable_flags: int
    enable_icons: int
    enable_likes: int
    enable_names: int
    enable_oekaki: int
    enable_posting: int
    enable_sage: int
    enable_shield: int
    enable_subject: int
    enable_thread_tags: int
    enable_trips: int
    icons: List
    id: str
    name: str
    pages: int
    sage: int
    tripcodes: int


class Model(BaseModel):
    Vzroslym: List[VzroslymItem]
    Igry: List[IgryItem]
    Politika: List[PolitikaItem]
    Pol_zovatel_skie: List[PolZovatelSkieItem] = Field(..., alias="Pol'zovatel'skie")
    Raznoe: List[RaznoeItem]
    Tvorchestvo: List[TvorchestvoItem]
    Tematika: List[TematikaItem]
    Tehnika_i_soft: List[TehnikaISoftItem] = Field(..., alias='Tehnika i soft')
    Japonskaja_kul_tura: List[JaponskajaKulTuraItem] = Field(
        ..., alias="Japonskaja kul'tura"
    )
