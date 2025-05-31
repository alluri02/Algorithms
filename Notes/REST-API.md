# 🛠️ REST API Preparation Guide

## 📘 What is a REST API?

A **REST (Representational State Transfer) API** is a stateless, client-server architectural style that defines a set of constraints and properties based on HTTP. It enables communication between clients and servers via standard HTTP methods.

---

## 🌐 Key HTTP Methods

| Method  | Description          | Use Case                |
|---------|----------------------|--------------------------|
| GET     | Read data            | Fetch user info         |
| POST    | Create new data      | Add a new user          |
| PUT     | Update existing data | Replace full user record|
| PATCH   | Partial update       | Modify user email       |
| DELETE  | Remove data          | Delete a user           |

---

## 📌 REST API Constraints

1. **Client-Server**: Separation of concerns.
2. **Stateless**: Each request is independent.
3. **Cacheable**: Responses must define cacheability.
4. **Uniform Interface**: Simplified and standardized interface.
5. **Layered System**: Middleware permitted between client & server.
6. **Code-on-Demand (optional)**: Servers can send executable code.

---

## ✅ Best Practices

### 🧾 Resource Naming

- Use **nouns**, not verbs:
  - ✅ `GET /users`
  - ❌ `GET /getUsers`

- Use **plural nouns**:
  - ✅ `/users`
  - ❌ `/user`

### 📚 Versioning

- URL versioning:
  - `/api/v1/users`
- Header versioning:
  - `Accept: application/vnd.api.v1+json`

### 📈 Status Codes

| Code | Meaning                  |
|------|---------------------------|
| 200  | OK                        |
| 201  | Created                   |
| 204  | No Content                |
| 400  | Bad Request               |
| 401  | Unauthorized              |
| 403  | Forbidden                 |
| 404  | Not Found                 |
| 500  | Internal Server Error     |

### 🧮 Query Parameters

```http
GET /users?age=30&sort=name&page=2&limit=10
