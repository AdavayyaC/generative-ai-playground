# --------Pydantic------>
# Pydantic makes sure your data is correct before your code trusts it.

from pydantic import BaseModel, EmailStr, Field
from typing import List, Literal, Optional

class student(BaseModel):
    
    name : str
    age: Optional[int] = None
    email : EmailStr
    cgpa : float = Field(gt=0 , lt=10 ,default=5)
    
new_student = {'name':'23', 'age':'345', 'email' : 'abc@gmail.com', 'cgpa':0.9}

student = student(**new_student)
# in dictionary
student_dict = dict(student)
# in json 
student_json = student.model_dump_json()
print(student)
print(student.name)
print(student.age)
print(type(student))

print(student_dict)
print(student_json)
    