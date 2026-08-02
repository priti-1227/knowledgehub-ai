# KNOWLEDGEHUB AI
## Master Project Rules & Development Guide

Version: 2.0
Status: Active Development
Last Updated: August 2026

---

# Project Overview

KnowledgeHub AI is an Enterprise AI-powered Knowledge Management System.

Organizations upload company documents (PDF, DOCX, TXT, Policies, SOPs, HR Manuals, etc.).

Employees can ask questions in natural language, and the AI answers using only the uploaded company documents through a Retrieval-Augmented Generation (RAG) pipeline.

The project is intended to be production-ready and portfolio-quality.

---

# Main Objectives

- Enterprise document management
- AI-powered document search
- RAG (Retrieval Augmented Generation)
- Role-based authentication
- Department-wise document management
- Modern scalable architecture
- Production-ready code

---

# User Roles

## Admin

- Login
- Manage Departments
- Upload Documents
- Delete Documents
- Manage Users
- Monitor AI

## Employee

- Login
- View Documents
- Ask AI Questions
- Search Knowledge Base

---

# Tech Stack

## Frontend

- React 19
- TypeScript
- Vite
- Tailwind CSS v4
- shadcn/ui
- React Router DOM
- TanStack Query
- React Hook Form
- Zod
- Axios
- Lucide Icons

---

## Backend

- Node.js
- Express
- TypeScript
- Prisma ORM
- PostgreSQL
- JWT Authentication
- bcrypt
- Multer
- Swagger

---

## AI Service (Upcoming)

- Python
- FastAPI
- LangChain
- ChromaDB
- Sentence Transformers
- Ollama
- OpenAI Compatible Models

---

# Folder Structure

knowledgehub-ai/

    frontend/
    backend/
    ai-service/
    docs/
    KNOWLEDGEHUB_AI_RULES.md

---

# Backend Structure

src/

    config/

    lib/

    middlewares/

    routes/

    utils/

    features/

        auth/

        departments/

        documents/

---

Every feature follows

Repository

↓

Service

↓

Controller

↓

Routes

Pattern

Business logic never belongs inside controllers.

---

# Frontend Structure

src/

    components/

        shared/

        ui/

    layouts/

    routes/

    hooks/

    lib/

    features/

        auth/

        departments/

        documents/

Each feature contains

api/

hooks/

components/

pages/

types/

columns.tsx

---

# Coding Standards

## Backend

- TypeScript Strict Mode
- Feature Based Architecture
- Repository Pattern
- Async/Await only
- Prisma ORM
- JWT Authentication
- Swagger Documentation
- Global Error Middleware
- API Response Standardization

Never place business logic inside controllers.

---

## Frontend

Use

- Functional Components
- Hooks
- TanStack Query
- Axios
- React Hook Form
- Zod Validation

Avoid prop drilling.

Prefer reusable components.

---

# UI Guidelines

Always use

- shadcn/ui

Never create custom buttons when shadcn component exists.

Use

- Dialog
- AlertDialog
- Sheet
- Table
- Select
- Form
- Badge
- Card

Maintain consistent spacing.

---

# API Rules

Authentication

Authorization Header

Bearer <token>

Response Format

Success

{
    "success": true,
    "message": "...",
    "data": {}
}

Failure

{
    "success": false,
    "message": "..."
}

---

# Database

Current Tables

User

Department

Document

Relationships

Department

↓

Documents

User

↓

Documents

---

# Completed Features

## Authentication

✔ Register

✔ Login

✔ JWT

✔ Protected Routes

✔ Public Routes

✔ Password Hashing

✔ Swagger

---

## Departments

✔ Create

✔ Read

✔ Update

✔ Delete

✔ Search

✔ Pagination

✔ DataTable

✔ React Query

✔ Toast

✔ Validation

---

## Documents

✔ Upload

✔ View

✔ Download

✔ Delete

✔ Search

✔ Drag & Drop

✔ Department Assignment

✔ Multer Upload

✔ Swagger

✔ File Storage

---

# API Endpoints

## Auth

POST /api/auth/register

POST /api/auth/login

---

## Departments

GET /api/departments

POST /api/departments

PUT /api/departments/:id

DELETE /api/departments/:id

---

## Documents

GET /api/documents

GET /api/documents/:id

GET /api/documents/:id/view

GET /api/documents/:id/download

POST /api/documents/upload

DELETE /api/documents/:id

---

# Current Progress

Authentication

100%

Departments

100%

Document Management

100%

Dashboard

20%

AI

0%

Overall

~55%

---

# Upcoming Sprints

Sprint 5

AI Service

- FastAPI
- Swagger
- Health API

---

Sprint 6

Document Processing

- PDF Parsing
- DOCX Parsing
- TXT Parsing
- Chunking

---

Sprint 7

Embeddings

- Sentence Transformers
- ChromaDB

---

Sprint 8

RAG

- Retriever
- Context Builder
- Prompt Engineering

---

Sprint 9

AI Chat

- Streaming Responses
- Conversation History
- Source References

---

Sprint 10

Dashboard

- Analytics
- Statistics
- Recent Uploads
- AI Usage
- Charts

---

Sprint 11

Deployment

- Docker
- AWS
- CI/CD

---

# Future AI Architecture

Upload Document

↓

Extract Text

↓

Clean Text

↓

Chunk Text

↓

Generate Embeddings

↓

Store in Vector Database

↓

Retriever

↓

Prompt Builder

↓

LLM

↓

Answer

---

# AI Rules

The AI must answer ONLY from uploaded documents.

If the answer is unavailable,

respond that the information could not be found.

Never hallucinate.

Always return document sources when available.

---

# Performance Goals

Lazy Loading

Code Splitting

Pagination

Optimized Queries

Caching

Streaming Responses

Reusable Components

---

# Security

JWT Authentication

Password Hashing

Role-based Access

Protected APIs

Input Validation

File Validation

SQL Injection Protection

---

# Development Workflow

New Feature

↓

Backend

↓

Swagger Testing

↓

Frontend Integration

↓

React Query

↓

Testing

↓

Documentation Update

Never skip Swagger testing before frontend integration.

---

# Git Workflow

main

Production

develop

Development

feature/<feature-name>

Feature Branch

---

Commit Format

feat:

fix:

refactor:

docs:

style:

test:

chore:

Example

feat: implement document upload module

---

# Project Goal

Build a production-ready Enterprise Knowledge Management System using modern Full Stack + AI technologies.

This project should demonstrate:

- Enterprise Architecture
- Clean Code
- Scalable Folder Structure
- AI Integration
- RAG Pipeline
- Production Deployment

Suitable for portfolio, interviews, and real-world deployment.

---

# Important Rule

This document is the single source of truth for the project.

Whenever a sprint is completed:

1. Update this document.
2. Mark completed features.
3. Update folder structure if changed.
4. Add new APIs.
5. Add architectural decisions.
6. Keep future roadmap synchronized.

Every AI assistant working on this project must follow this document before writing new code.