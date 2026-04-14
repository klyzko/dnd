from pydantic import BaseModel, Field
from typing import List, Optional



class Bonus(BaseModel):
    health: Optional[int] = Field(None,description="бонус к жизни")
    manna: Optional[int] = Field(None,description="бонус к мане")
    power: Optional[int] = Field(None,description="бонус к силе")
    intelligence: Optional[int] = Field(None,description="бонус к интелекту")
    agility: Optional[int] = Field(None,description="бонус к ловкости")
    #gold: Optional[int] = Field(None,description="бонус к золоту")
    loot: Optional[str] = Field(None,description="Добыча из босса")


class Mission(BaseModel):
    annotation: Optional[str] = Field(description="полно описание задачи от пользователя")
    name_quest: Optional[str] = Field(description='имя квеста или боса')
    quest: Optional[str] = Field(description='литературное описание задачи')
    bonus: Optional[Bonus] = Field(description='бонусы получаемые за выполнения задачи')

