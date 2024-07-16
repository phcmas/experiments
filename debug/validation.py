from pydantic.v1 import BaseModel


class Test(BaseModel):
    a: int


test = Test(a=1.22)
print(test)
