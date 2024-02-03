from typing import Union, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from fastapi.responses import PlainTextResponse
from collections import OrderedDict

app = FastAPI()

DOGS = {} 
COUNTER = 0 

class DogType(Enum):
    TERRIER: str = 'terrier'
    BULLDOG: str = 'bulldog'
    DALMATIN: str = 'dalmatian'


class Dog(BaseModel):
    name: str
    pk: Optional[int] = None
    kind: DogType


@app.get('/', response_class=PlainTextResponse)
def root():
    return 'ok' 


@app.post('/post')
def get_post(): 
    return {
  "id": 0,
  "timestamp": 0
}


@app.post('/dog')
def create_dog(dog: Dog): 
    global COUNTER
    if dog.pk is None: 
        dog.pk = COUNTER
        COUNTER += 1 
    dog_dict = dog.dict()
    pk = dog_dict['pk']
    DOGS[pk] = OrderedDict(dog_dict) 
    return dog 


@app.get("/dog/{pk}")
def get_dog_by_pk(pk: int):
    if pk not in DOGS.keys(): 
        raise HTTPException(status_code=404, detail="Dog not found") 
    return DOGS[pk]


@app.get("/dog")
def get_dogs(kind: DogType = None):
    list_of_dogs = [] 
    if kind is not None:
        for dog in DOGS.values(): 
            if dog['kind'] == kind: 
                list_of_dogs.append(dog)
    else:
        list_of_dogs = list(DOGS.values())
    return list_of_dogs
    

@app.patch("/dog/{pk}")
def update_dog(pk: int, dog: Dog):
    if pk not in DOGS.keys(): 
        raise HTTPException(status_code=404, detail="Dog not found") 
    dog_data = dog.dict() | {'pk': DOGS[pk]['pk']}
    DOGS[pk].update(OrderedDict(dog_data)) 
    return DOGS[pk]

