
# Moringa Capstone Project: [Your Project Name Here - e.g., Judiciary Performance Management System]

## Description

[**Replace this with a concise and informative description of your project.**]

This Django project aims to [**briefly explain the purpose of your application.**  For example: "This Django project is a web application designed to manage and track performance data within the judiciary. It includes modules for document management, statistical reporting (DCRT), meeting scheduling, workplan management, and budget tracking."].

It is built using Django framework and incorporates:

*   **Modular Design:** Organized into Django apps for different functionalities (authentication, home, statistics, document management, organization, meetings).
*   **Bootstrap UI:**  Utilizes Bootstrap for a responsive and visually appealing user interface, enhanced with Material Design Icons.
*   **Dockerized:**  Easily deployable and runnable using Docker.
*   **Database:** Uses SQLite3 for development (can be configured for other databases in production).

## Features

[**List the main features of your application.  Refer to the file structure and modules you have implemented to create this list.**  For example:]

*   **User Authentication:** Secure user registration, login, and logout functionality.
*   **Department and Role Management:**  Organization module to define departments and roles within the judiciary.
*   **Dashboard:** Central dashboard to view departments and access module functionalities.
*   **Document Management:** Module for uploading, organizing, and managing documents.
*   **Statistics (DCRT):** Module for data entry, analysis, and reporting of Daily Court Returns data.
*   **Meetings Management:** Module for scheduling, managing, and tracking meetings.
*   **Workplan Management:** Module for creating and tracking departmental workplans.
*   **Budget Management:** Module for managing and tracking departmental budgets.
*   **Role-Based Permissions:**  Module-level access control based on user roles and permissions.
*   **Responsive Design:**  UI is designed to be responsive and work well on different screen sizes.

## Getting Started

Follow these instructions to set up and run the project locally for development.

### Prerequisites

*   **Python 3.9+** (as specified in the `Dockerfile`)
*   **pip** (Python package installer)
*   **Docker** and **Docker Compose** (if you want to use Docker)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository URL]
    cd moringa_capstone
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Seed initial data (optional but recommended):**

    To populate the database with initial organizational structure and modules, run the seed commands:

    ```bash
    python manage.py seed_organization
    python manage.py seed_modules
    python manage.py seeddivisions
    python manage.py unit_seeder
    python manage.py unit_division_seeder
    python manage.py populate_unit_ranks
    python manage.py seedfinancialdata
    python manage.py seed_months
    ```

6.  **Create a superuser (admin account):**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```bash
    python manage.py runserver 0.0.0.0:8001
    ```

    Access the application in your browser at `http://127.0.0.1:8001/`.

## Running with Docker

1.  **Build the Docker image:**

    ```bash
    docker-compose build web
    ```

2.  **Run the Docker containers:**

    ```bash
    docker-compose up
    ```

    The application will be accessible at `http://127.0.0.1:8001/`.

3.  **Access Docker Bash (optional):**

    To run management commands or inspect the container, you can access the Docker bash:

    ```bash
    docker-compose exec web bash
    ```

    From within the Docker container's bash, you can run Django management commands like `python manage.py createsuperuser`, `python manage.py migrate`, `python manage.py seed_organization`, etc.

## Usage

1.  **Access the application in your browser** at `http://127.0.0.1:8001/`.
2.  **Log in** using the superuser account you created or register a new user.
3.  **Navigate to the Dashboard** to see the list of departments.
4.  **Click "View Modules"** on a department card to access the available modules.
5.  **Explore the modules** you have access to, such as DCRT (Statistics), Workplans, and Budget.

## Theme Colors

The application's UI theme uses the following colors, as defined in `UI.md`:

*   **Primary:** `#26443c`
*   **Accent:** `#c4a938`
*   **Background:** `#f7f9f8`
*   **Text (Black):** `#000000`

These colors are used for headings, card headers, icons, and other UI elements to create a consistent and visually appealing design.

## Contributing

[**Optional: Add guidelines for contributing if you plan to allow contributions.**  For example:]

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with clear commit messages.
4.  Submit a pull request to the main branch.

## License

[**Optional: Specify the project license, e.g., MIT License, Apache 2.0, or leave it as "Proprietary" if it's not open-source.**  For example:]

This project is licensed under the [MIT License](LICENSE) - see the `LICENSE.md` file for details.

## Contact

[**Optional: Add contact information or links, e.g., your email, GitHub profile.**  For example:]

For questions or inquiries, please contact [Your Name] at [your.email@example.com].

---
