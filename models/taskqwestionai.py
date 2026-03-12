from pydantic import BaseModel, Field
from typing import List, Optional



class Bonus(BaseModel):
    health: Optional[str] = Field(None,description="бонус к жизни")
    manna: Optional[str] = Field(None,description="бонус к мане")
    power: Optional[str] = Field(None,description="бонус к силе")
    intelligence: Optional[str] = Field(None,description="бонус к интелекту")
    agility: Optional[str] = Field(None,description="бонус к ловкости")
    loot: Optional[str] = Field(None,description="Добыча из босса")


class Mission(BaseModel):
    annotation: Optional[str] = Field(description="полно описание задачи от пользователя")
    name_quest: Optional[str] = Field(description='имя квеста или боса')
    quest: Optional[str] = Field(description='литературное описание задачи')
    bonus: Optional[str] = Field(description='бонусы получаемые за выполнения задачи')