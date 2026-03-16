# WebScour – Distributed Web Crawler and Search Engine

## Project Overview
This project implements a mini distributed web crawler and search engine.  
The system crawls web pages, extracts content, builds an inverted index, and provides a searchable interface using FastAPI.

The project demonstrates the core components of modern search engines, including:
- Web crawling
- Indexing
- Ranking using TF-IDF
- API-based search services

---

## System Architecture
The system consists of four main components:

1. Distributed Web Crawler  
2. Indexing Engine  
3. Search Engine  
4. API and User Interface  

---

## Features
- Distributed crawling using RabbitMQ  
- Multi-worker architecture for parallel crawling  
- HTML parsing using BeautifulSoup  
- Text preprocessing and tokenization  
- Term Frequency (TF) calculation  
- Inverted Index construction  
- IDF computation for ranking  
- TF-IDF based document ranking  
- Search API built with FastAPI  
- Simple UI to test search queries  

---

## Technologies Used
- Python  
- RabbitMQ  
- BeautifulSoup  
- FastAPI  
- JSON  
- TF-IDF Information Retrieval  
