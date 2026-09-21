import pytest
from fastapi.testclient import TestClient
from app import app, books  # Assuming books is your in-memory list/dict


@pytest.fixture
def client():
  books.clear()  # reset in-memory store
  with TestClient(app) as client:
    yield client


def test_crud(client):
  # Create
  rv = client.post(
      "/books", json={"title": "Book A", "author": "Author A", "price": 10}
  )
  assert rv.status_code == 201
  assert rv.json()["id"] == 1

  # Read
  rv = client.get("/books/1")
  assert rv.status_code == 200
  assert rv.json()["title"] == "Book A"

  # Update
  rv = client.put("/books/1", json={"title": "Book A Updated"})
  assert rv.status_code == 200
  assert rv.json()["title"] == "Book A Updated"


