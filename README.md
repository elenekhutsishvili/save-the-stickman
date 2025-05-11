
## Features

-  Random word selection from a predefined list  
-  Interactive letter-by-letter guessing  
-  Visual stickman drawing for incorrect guesses  
-  Win/loss detection logic  
-  User authentication system with login functionality  
-  Dockerized setup for streamlined deployment 


## Technologies Used

### Backend
- **Python 3** – programming language
- **Flask** – Web framework to handle routes, sessions, and game logic

### Frontend
- **HTML** – building structure for the web pages
- **CSS** – Styling for layout and visuals
- **JavaScript** – Interactivity 
- **Jinja** – Flask’s templating engine for HTML rendering (updating page)

### Deployment
- **Docker** – Containerization for consistent and portable environments
- **Docker Compose** – Multi-container management and setup

## Environment Setup

1. *Clone the repository:*
   
   ```bash
   git clone https://github.com/elenekhutsishvili/save-the-stickman.git  
   cd save-the-stickman
   ```

2. *build and start containers*
   To build and start the app with Docker Compose:

   ```bash
   docker-compose up --build  
   ```