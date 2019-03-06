from tortoise import fields
from tortoise.models import Model, ModelMeta as _ModelMeta

IGNORE_ATTRS = ['redis']
_redis = None


# 创建基类
#new_cls 返回的是所有的基类和子类   暂时不知道为什么返回
class PropertyHolder(type):

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        new_cls.property_fields = []

        for attr in list(attrs) + sum([list(vars(base)) for base in bases], []):
            if attr.startswith('_') or attr in IGNORE_ATTRS:
                continue
            if isinstance(getattr(new_cls, attr), property):
                new_cls.property_fields.append(attr)
        print(new_cls)
        return new_cls


class ModelMeta(_ModelMeta, PropertyHolder):
    ...


class BaseModel(Model, metaclass=ModelMeta):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    _redis = None

    class Meta:
        abstract = True


class Post(BaseModel):
    pass


class Tag(BaseModel):
    pass


Post()
