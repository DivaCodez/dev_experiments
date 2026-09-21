import http
from operator import index

from fastapi import Depends, FastAPI, HTTPException 
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI(
	title="Mini Bookstore API",
    description="Une API pour gérer des livres et des auteurs, documentée automatiquement.",
    version="1.0.0"
)


books = [
    {
		"id": 1, "title": "The Great Gatsby", 
		"author": {
		 'id' : 1,
		 "name": "F. Scott Fitzgerald",
		 "mail": "scott@example.com"
	 	}, 
		"is_offer": True
	},
    {
		"id": 2, 
		"title": "1984", 
		"author": {
			"id" : 2,
			"name": "George Orwell",
			"mail": "orwell@example.com"
		}, 
		"is_offer": False},
    {
		"id": 3, 
		"title": "To Kill a Mockingbird", 
		"author": {
			"id" : 3,
			"name": "Harper Lee",
			"mail": "lee@example.com"
		}, 
		"is_offer": False},
    {
		"id": 4, 
		"title": "Pride and Prejudice", 
		"author": {
			"id" : 4,
			"name": "Jane Austen",
			"mail": "jane@example.com"
		}, 
		"is_offer": True
	}
]

# Pydantic test
class Author (BaseModel):
    id : int
    name : str | None
    mail : EmailStr | None

class Book (BaseModel):
	id : int
	title : str
	author : Author
	is_offer : bool = False




# Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
USER_DB = {"admin": "secret123"}

@app.post("/token", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    password = USER_DB.get(form_data.username)
    
    if not password or form_data.password != password:
        raise HTTPException(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            detail="Identifiants incorrects",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"access_token": form_data.username, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    if token != "admin":
        raise HTTPException(
            status_code=http.HTTPStatus.UNAUTHORIZED,
            detail="Jeton invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token




# Books endpoints
@app.get("/books")
def get_books():
	return books

@app.post("/books")
def create_book(book : Book, current_user: str = Depends(get_current_user)):
	if book:
		books.append(book.model_dump())
		raise HTTPException(status_code=201, detail="Book created successfully")
	else:
		raise HTTPException(status_code=400, detail="Invalid book data")


@app.get("/books/{id_book}")
def get_book(id_book : int):
	if id_book < 1 or id_book > len(books):
		raise HTTPException(status_code=400, detail="Invalid book ID")
	for book in books:
		if book['id'] == id_book:
			return book
		raise HTTPException(status_code=404, detail="Book no found")

	
@app.put("/books/{id_book}")
def update_book(id_book : int, updated_book : Book,current_user: str = Depends(get_current_user)):	
	if id_book < 1 or id_book > len(books):
		raise HTTPException(status_code=400, detail="Invalid book ID")
	#book = updated_book.model_dump()
	for book in books:
		if updated_book.id == id_book:
			book['title'] = updated_book.title
			book['author'] = updated_book.author
			book['is_offer'] = updated_book.is_offer
			index = books.index(book)
			raise HTTPException(status_code=200, detail="Book updated successfully")
	raise HTTPException(status_code=404, detail="Book no found")

	
@app.delete("/books/{id_book}")
def delete_book(id_book : int, current_user: str = Depends(get_current_user)):
	if id_book < 1 or id_book > len(books):
		raise HTTPException(status_code=400, detail="Invalid book ID")
	for book in books:
		if book['id'] == id_book:
			books.remove(book)
			raise HTTPException(status_code=200, detail="Book deleted successfully")
	raise HTTPException(status_code=404, detail="Book no found")

    
@app.get("/authors")
def get_author(id_author : int):
	if id_author:
		for book in books:
			if book['author']['id'] == id_author:
				return book['author']
		raise HTTPException(status_code=404, detail="Author no found")
	raise HTTPException(status_code=400, detail="Invalid author ID")