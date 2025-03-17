# 📖 Manga Scraper 🚀

## 📌 Overview

Manga Scraper is a fully automated web scraping project designed to extract manga data from online sources. It utilizes **Apache Airflow** for task scheduling and **Docker** for easy deployment. This project simplifies the process of downloading and organizing manga chapters into structured formats.

## 📸 Screenshots / Demo

![airflow-ui](https://github.com/user-attachments/assets/d4c9879c-cc72-4670-9a3f-7d7afa4df57e)
--- 
![manga_extract](https://github.com/user-attachments/assets/21508e62-18d8-4893-bf2a-45f9fad1d87a)
---

## ✨ Features

✅ Automated manga extraction 📜  
✅ Apache Airflow for task scheduling ⏳  
✅ Docker containerization for seamless deployment 🐳  
✅ Scalable and customizable workflow ⚙️

## 🔧 Prerequisites

Before running the project, ensure you have the following installed:

- [🐳 Docker](https://www.docker.com/)
- [🛠️ Docker Compose](https://docs.docker.com/compose/)
- [💨 Apache Airflow](https://airflow.apache.org/)
- 🐍 Python 3.8+

## 🚀 Installation & Setup

1️⃣ Clone the repository:

```sh
git clone https://github.com/Ajay1812/airflow-docker-projects.git
cd airflow-docker-projects
```

2️⃣ Build and start the Docker containers:

```sh
docker-compose up --build -d
```

3️⃣ To check running containers::

```sh
docker ps
```

4️⃣ To check the logs:

```sh
docker logs <CONTAINER-ID>
```

5️⃣ Access the Airflow UI:

- Open [🌐 http://localhost:8080](http://localhost:8080) in your browser.
- Use default credentials (`airflow`/`airflow`).

6️⃣ To stop and remove all volumes:

```sh
docker compose down -v
```

## 🎮 How to Use

1. Navigate to the **Airflow UI** and trigger the `manga_scraper` DAG.
2. Wait for the pipeline to fetch, process, and store manga data.
3. Scraped manga will be available in structured format in the `data/` directory.

## 📁 Project Structure

```
airflow-docker-projects/
├── dags/
│   └── ETL_manga_data.py    # Airflow DAG definition for scraping manga data
├── data/                    # Data folder to persist scraped manga
│   ├── stored_manga/
│   │   ├── pdfs/
│   │   │   ├── solo_leveling/
│   │   │       ├── chapter_1.pdf
│   │   │       ├── chapter_2.pdf
│   │   │       ├── ...
│   │   │       ├── chapter_30.pdf
│   │   ├── solo_leveling/
│   │       ├── chapter_1/
│   │       │   ├── 01.jpg
│   │       │   ├── 02.jpg
│   │       │   ├── ...
│   │       │   ├── 30.jpg
│   │       ├── chapter_2/
│   │       │   ├── 01.jpg
│   │       │   ├── 02.jpg
│   │       │   ├── ...
│   │       │   ├── 30.jpg
│   ├── manga_data.db
├── docker-compose.yml       # Docker Compose configuration for Airflow and volume mounts
└── README.md                # Project documentation
```

## 🤝 Contributing

Want to improve this project? Feel free to submit issues or pull requests! 💡

## 📬 Contact

For any queries, reach out to [Ajay1812](https://github.com/Ajay1812). 🚀
