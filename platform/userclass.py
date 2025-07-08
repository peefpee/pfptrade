from pydantic import BaseModel
class UserClass(BaseModel):
    id : int = 0
    username : str
    email : str
    password : str
    positions : list = []
    history : list = []
    orders : list = []
    balance : float = 0.0
    equity : float = 0.
    created_at : int
    leverage : int = 1
    
