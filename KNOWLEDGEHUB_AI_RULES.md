# KNOWLEDGEHUB AI -- PROJECT RULES & MENTOR CONTEXT

## Purpose

This document contains the complete project vision, architecture, coding
standards, roadmap, and mentoring rules so any AI assistant can
immediately continue the project without losing context.

# Project

KnowledgeHub AI -- Enterprise Knowledge Assistant

## Problem Statement

Build an enterprise knowledge platform where employees can upload
internal documents (SOPs, HR policies, warehouse manuals, etc.) and ask
natural-language questions. The system uses RAG (LangChain + Vector
Database) to answer with cited sources.

## Tech Stack

### Frontend

-   React 19
-   TypeScript
-   Vite
-   Tailwind CSS v4
-   shadcn/ui
-   React Router
-   TanStack Query
-   React Hook Form
-   Zod
-   Fetch API (preferred over Axios)

### Backend

-   Node.js
-   Express
-   TypeScript
-   Prisma ORM
-   PostgreSQL
-   JWT
-   bcrypt

### AI Service

-   Python
-   FastAPI
-   LangChain
-   ChromaDB
-   Ollama (local LLM)

## Architecture

knowledgehub-ai/ - frontend/ - backend/ - ai-service/ - docs/

## Frontend Architecture

Use feature-based architecture.

src/ - app/ - components/ - features/ - auth/ - dashboard/ -
documents/ - chat/ - users/ - layouts/ - shared/ - lib/ - hooks/ -
services/ - types/

## Backend Architecture

src/ - app/ - config/ - middleware/ - modules/ - auth/ - users/ -
documents/ - chat/ - prisma/

Never use controller/service folders at project root.

## Current Progress

### Sprint 0 ✅

-   Git repository
-   React + Vite
-   Tailwind CSS v4
-   Path aliases
-   Application shell
-   React Router

### Sprint 1 ✅

-   Feature-based auth structure
-   Login UI
-   Register UI
-   React Hook Form
-   Zod validation
-   Auth hooks
-   Auth service abstraction
-   Routing

### Next Sprint

Backend foundation: 1. Express 2. TypeScript 3. Prisma 4. PostgreSQL 5.
Register API 6. Login API 7. JWT 8. Protected routes

## Coding Rules

1.  Always explain WHY before writing code.
2.  Build feature-by-feature, not technology-by-technology.
3.  Prefer clean architecture over quick solutions.
4.  Use TypeScript everywhere.
5.  Avoid duplicated code.
6.  Prefer reusable components.
7.  One Git commit per working milestone.
8.  Explain interview reasoning behind every major decision.
9.  Use modern best practices for 2026.
10. Never generate tutorial-style code if a production approach exists.

## UI Philosophy

Target a production SaaS look inspired by: - Linear - Notion - Vercel -
Clerk - Supabase

## API Philosophy

Frontend communicates with backend using Fetch API. Backend communicates
with AI service through REST.

## Authentication Flow

Login -\> Backend -\> JWT -\> Store token -\> Protected routes.

## AI Flow

Upload PDF -\> Extract text -\> Chunk -\> Embedding -\> ChromaDB -\>
Retrieval -\> LLM -\> Answer with source citation

## Mentoring Style

Act as a senior full-stack engineer (5+ years).

For every topic: - Explain the problem. - Explain why this solution. -
Explain alternatives. - Explain interview talking points. - Then
implement.

Do not skip architectural reasoning.

Prefer concise explanations and maintain steady progress.

## Goal

The final result should be: - Production quality - Resume worthy -
Interview ready - Deployable SaaS foundation
