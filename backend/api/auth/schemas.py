from pydantic import BaseModel, field_validator, ConfigDict
import re

class SetPasswordSchema(BaseModel):
    model_config = ConfigDict(strict=True)
     # token to set password you have to get from URL  todo
    password: str

    @field_validator('password')
    @classmethod
    def validate_received_password(cls, password: str) -> str:

        pattern = r"^[A-Za-z\d@$!%*?&]{8,}$"

        if not re.fullmatch(pattern, password):
            raise ValueError('Password must contain at least 8 characters, '
                                  '1 special symbol, 1 letter, 1 number')
        return password


