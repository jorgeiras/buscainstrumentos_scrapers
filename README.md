# BuscaInstrumentos Scrapers
  
<div align="center">
  <img src="https://github.com/jorgeiras/buscainstrumentos_scrapers/blob/main/images/buscainstrumentoslogo.png" alt="scrapers Logo">
</div>
  
### Description
This repository contains the web scraping scripts and the automation infrastructure used to collect data for the BuscaInstrumentos project. The scrapers are designed to extract information about musical instruments from various online sources, automate the data extraction process, and store the cleaned data in a structured format.

### Table of Contents
1. [Technical Stack](#technical-stack)
2. [Execution and ETL Workflow](#execution-and-etl-workflow)
3. [Infrastructure and Hosting](#infrastructure-and-hosting)
4. [Contact](#contact)

### Technical Stack
This project utilizes a range of technologies and tools to achieve its goals:
- **Python**: The primary language used for writing scraper scripts.
- **Scrapy**: A powerful web scraping framework for extracting structured data from websites.
- **Selenium**: Used for web scraping tasks that require interaction with dynamic web pages.
- **Terraform**: Automates the provisioning of the cloud infrastructure (DigitalOcean droplets) where the scrapers run.
- **Ansible**: Manages the configuration and deployment of the scrapers, ensuring that all dependencies are installed and the environment is properly set up.
- **GitHub Actions**: Schedules and triggers the execution workflow, ensuring that the scrapers run on a daily basis.
- **PostgreSQL**: Stores the cleaned and structured data extracted by the scrapers.

### Execution and ETL Workflow
<br><br>  
<div align="center">
  <img src="https://github.com/jorgeiras/buscainstrumentos_scrapers/blob/main/images/scrapers_etl.png" alt="scrapers etl" style="margin-top: 20px; margin-bottom: 20px;">
</div>
<br><br>  

This project automates the process of extracting, transforming, and loading (ETL) data from various websites into a structured format. The entire process is managed through a scheduled workflow that runs daily, ensuring that the latest data is always available. Below is an overview of the full workflow:

1. **Scheduled Trigger**
   - **GitHub Actions**: The process begins when a GitHub Actions workflow is triggered at the same time every day. This automation ensures that the scrapers run consistently without requiring manual intervention.

2. **Infrastructure Setup**
   - **Terraform Setup**: Terraform is used to automatically provision a new DigitalOcean droplet (a virtual private server) for the scrapers to run on. This droplet is temporary, existing only for the duration of the scraping process.
     - **Droplet Creation**: Terraform creates the droplet, setting up the necessary environment where the scraping tasks will be executed.
     - **Dynamic Configuration**: Terraform returns the IP address of the newly created droplet, which is then dynamically inserted into the `inventory.yaml` file used by Ansible. This ensures that Ansible knows where to deploy the necessary configurations.

   - **Ansible Setup Preparation**: Once the droplet is provisioned, Ansible takes over to configure the environment. 
     - **Inventory Setup**: Ansible reads the `inventory.yaml` file, which contains the IP of the newly created droplet.
     - **Environment Variable Setup**: Depending on the day of the week, specific environment variables are set. These variables determine the category of musical instruments that the scrapers will focus on for that day.

*(The following steps 4, 5, 6, and 7 are tasks executed by the Ansible playbook)*
  
4. **Package Installation**: Ansible installs all required software packages and dependencies on the droplet, such as Python, Selenium, Scrapy, and other necessary libraries.

5. **Data Extraction (Extract)**
   - **Repository Cloning**: Ansible clones the latest version of the repository onto the droplet, ensuring that the most up-to-date code is used.
   - **Selenium Execution**: 
     - Selenium is used to interact with websites that require dynamic content loading or user interaction, such as clicking buttons or filling out forms.
   - **Scrapy Execution**:
     - Scrapy is a powerful and flexible web scraping framework that handles the majority of the scraping tasks. It extracts structured data from static and dynamic web pages, parsing HTML content and extracting the required information about musical instruments.
   - **Custom Python Scripts**: 
     - In addition to Scrapy, custom Python scriptsare used to handle specific scraping scenarios or to preprocess data before transformation.

6. **Data Transformation (Transform)**
   - **Data Cleaning**: The raw data collected by the scrapers is cleaned to remove any inconsistencies, duplicates, or irrelevant information.
   - **Data Structuring**: The cleaned data is organized into a structured format, as CSV files. The structure is standardized, making it easy to load into a database and ensuring that the data can be efficiently queried and analyzed.

7. **Data Loading (Load)**
   - **Database Insertion**: The transformed data is loaded into a PostgreSQL database. This step involves inserting the cleaned and structured data into the Instrument table, making it accessible for further use by the BuscaInstrumentos backend.

8. **Teardown**
   - **Droplet Destruction**: After the ETL process is complete, Terraform automatically destroys the DigitalOcean droplet. This cleanup step is essential for cost management, ensuring that no unnecessary resources are left running.
   - **End of Workflow**: The GitHub Actions workflow completes, and the system returns to an idle state until the next scheduled trigger.


### Infrastructure and Hosting
The infrastructure for this project is fully automated and cloud-based. The following components are used:
- **Dynamic Droplet Provisioning**:
  - **Cost Efficiency**: Each time the scraping process is initiated, a new DigitalOcean droplet (virtual private servers) is provisioned, and it is destroyed once the process is complete. This approach is cost-effective because it ensures that resources are only used when necessary, rather than keeping a droplet running continuously.
  - **IP Rotation**: By creating a new droplet each time, the IP address used to access target websites changes daily. This helps to avoid IP-based blocks or restrictions from websites, which can occur if scraping activities are detected from a single, consistent IP address.

- **Operating System Choice**:
  - **Ubuntu 20.04**: The droplets are configured to use Ubuntu 20.04 as the operating system. This specific version was chosen because it allows Ansible to execute jobs without requiring user interaction. In contrast, more recent versions of Ubuntu, despite using non-interactive instructions, caused issues where the automation process could get stuck due to prompts for user input. Ubuntu 20.04 provides a stable environment that supports the fully automated nature of this project.

- **Automation Tools**:
  - **Terraform**: Manages the lifecycle of the droplets, including their creation and destruction, to ensure the infrastructure is available only when needed.
  - **Ansible**: Configures the droplets with all necessary dependencies and environment settings, ensuring that the scrapers can run without manual intervention.
  - **GitHub Actions**: Automates the entire process, triggering the infrastructure setup, running the scrapers, and tearing down the infrastructure daily.
  
This infrastructure setup not only supports the efficient and automated operation of the scrapers but also enhances the reliability and effectiveness of the data extraction process by leveraging dynamic IPs and a stable OS environment.

### Contact
For more information or inquiries, you can reach me on LinkedIn or via email:
- **LinkedIn**: (www.linkedin.com/in/jorge-alonso-urrutia-544022261)
- **Email**: [alonsourrutia.jor@gmail.com](mailto:alonsourrutia.jor@gmail.com)
