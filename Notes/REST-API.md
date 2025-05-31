# 📘 REST API Preparation Guide

## Table of Contents

1. [What is a REST API?](#what-is-a-rest-api)
2. [Key Concepts of REST](#key-concepts-of-rest)
3. [HTTP Methods](#http-methods)
4. [HTTP Status Codes](#http-status-codes)
5. [URI Design Best Practices](#uri-design-best-practices)
6. [Request and Response Format](#request-and-response-format)
7. [Authentication and Authorization](#authentication-and-authorization)
8. [Versioning](#versioning)
9. [Error Handling](#error-handling)
10. [Pagination, Filtering, and Sorting](#pagination-filtering-and-sorting)
11. [Rate Limiting](#rate-limiting)
12. [API Documentation (Swagger/OpenAPI)](#api-documentation-swaggeropenapi)
13. [Tools for Testing REST APIs](#tools-for-testing-rest-apis)
14. [REST vs SOAP](#rest-vs-soap)
15. [Best Practices](#best-practices)

---

## What is a REST API?

A REST (Representational State Transfer) API is a web service that adheres to REST architectural principles, allowing clients to perform operations using standard HTTP methods.

Example:
```http
GET /api/users/1 HTTP/1.1
Host: example.com

## Key Concepts of REST

- **Stateless**:  
  Every request from the client must contain all the information needed for the server to process it. The server does not store anything about the client's session between requests.

- **Client-Server**:  
  The client and server operate independently, wi
