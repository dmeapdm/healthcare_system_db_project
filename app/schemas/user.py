from pydantic import BaseModel, ConfigDict


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id_user: int
    username: str
    full_name: str
    role_name: str
    hospital_id: int
    name_hospital: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
