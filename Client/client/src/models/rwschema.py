from .rwmodel import RWModel

#these are schemas (interfaces) used for typization of parameters and arguments

class RWSchema(RWModel):
    class Config(RWModel.Config):
        orm_mode = True