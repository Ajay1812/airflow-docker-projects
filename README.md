# Airflow Docker Projects

Welcome to the **Airflow Docker Projects** repository! 🚀 This repository contains multiple projects that demonstrate the usage of **Apache Airflow** with **Docker** to orchestrate workflows efficiently.

## 📌 Overview

This repository provides hands-on projects that showcase different aspects of Apache Airflow, including DAGs, task dependencies, scheduling, and integrations with various tools. All projects are located inside the `dags/` folder.

## 📂 Projects Included

Below is a list of projects available in this repository:

1. **ETL Manga Data** (`ETL_manga_data.py`)

   - Extracts, transforms, and loads manga-related data.
   - Uses external data sources for scraping.

2. **ETL Toll Data** (`ETL_toll_data.py`)

   - Processes toll data from various sources.
   - Converts and stores data in structured formats.

3. **ETL Toll Python** (`ETL_toll_python.py`)

   - Another implementation of toll data processing.
   - Demonstrates alternative ETL approaches.

4. **ETL Web Server Log** (`etl_web_server_log.py`)

   - Parses web server logs for insights.
   - Stores and processes log data for analysis.

5. **Final Assignment** (`finalassignment/`)
   - Contains multiple ETL scripts for toll data.
   - Includes extracted datasets and structured output.

## 🏗️ Prerequisites

Before running the projects, ensure you have the following installed:

- **Docker** (latest version recommended)
- **Docker Compose**
- **Python 3.7+** (if required for additional configurations)

## 🚀 Getting Started

### Clone the Repository

```bash
git clone https://github.com/Ajay1812/airflow-docker-projects.git
cd airflow-docker-projects
```

### Start the Airflow Environment

Each project is included as a DAG inside the `dags/` folder. To start the environment, run:

```bash
docker-compose up -d
```

This will pull the necessary images and start the Airflow web server, scheduler, and workers.

### Access the Airflow UI

Once the services are up, you can access the **Airflow Web UI** at:

```
http://localhost:8080
```

Default credentials:

- **Username:** `airflow`
- **Password:** `airflow`

## 🛠️ Project Structure

```plaintext
├── dags/                  # Contains all Airflow DAGs (projects)
│   ├── ETL_manga_data.py  # DAG for manga data ETL
│   ├── ETL_toll_data.py   # DAG for toll data processing
│   ├── ETL_toll_python.py # Alternative toll data ETL approach
│   ├── etl_web_server_log.py # DAG for web server log analysis
│   ├── config.py          # Configuration file for DAGs
│   ├── data/              # Folder containing extracted data
│   ├── finalassignment/   # Additional ETL scripts & extracted data
│   ├── manga_scrapper/    # Additional script for manga scrapper
├── plugins/               # Custom operators and hooks
├── docker-compose.yml     # Docker configuration
└── README.md              # Main repository documentation
```

## 🔧 Customization

- Modify the **DAGs** inside the `dags/` directory to create your own workflows.
- Extend the **Docker Compose** file to include additional services such as databases, message queues, or APIs.
- Configure environment variables in `.env` files if required.

## 📜 License

This repository is licensed under the **MIT License**. Feel free to use and modify the projects as needed.

## 🤝 Contributing

Contributions are welcome! If you find a bug or want to enhance a project, feel free to submit a pull request.

## 📬 Contact

For any queries, reach out to:
📧 Email: [a.kumar01c@gmail.com]
🔗 GitHub: [https://github.com/Ajay1812]

Happy Coding! 🎉
