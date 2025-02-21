from pydantic import BaseModel  


class CategoryCreate(BaseModel):
    title: str
    desc: str = "fr"
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s

class CategoryCreateResponse(BaseModel):
    message: str


class FamilyCreate(BaseModel):
    title: str
    desc: str 
    image: str = "https://encrypted-tbn0.gstatic.com/images?q=" #tbn:ANd9GcROxd3wbPbbF0k8mwAE8RdwIZwxYftJFEtH0w&s
    cat_id: int

class FamilyCreateResponse(BaseModel):
    message: str