Design Choices:
    I focused on creating a responsive and user-friendly interface that adapts seamlessly across devices. The design emphasizes clarity and accessibility, with intuitive navigation and a clean, minimalistic aesthetic. I implemented a consistent color scheme and spacing to enhance readability and ensure that users can easily interact with the app. Additionally, I integrated a mobile-friendly hamburger menu and optimized the chat experience by aligning messages appropriately for the user and their chat partner, providing a clear and organized layout. For styling and layout, I used CSS along with modern web development practices, ensuring cross-browser compatibility and responsive behavior. The frontend was built with React, leveraging its component-based architecture to maintain clean and reusable code.

Prerequisites and Dependencies:
    1. Python (3.x)
        The backend is built using Django, which requires Python. Ensure Python is installed on your machine.    
    2. Django (5.0.7)
        The core framework used to build the backend. This application uses Django's built-in SQLite3 database, which requires no additional setup for development purposes.
    3. React (18.3.1)
        The frontend is developed using React. You'll need Node.js and npm to manage the dependencies and run the development server.
    4. Node.js and npm
        Required to run the React development server and build the production assets.        
    5. Django Channels and Daphne
        For handling real-time communication (WebSocket) in the chat functionality. These dependencies are critical for the application's real-time features.
    6. SQLite3
        Used as the default database for development purposes. No additional configuration is needed if you are using the default setup.
    7. Testing
        The backend was tested using Django's built-in django.test framework. This provides a robust testing environment integrated with Django's features.
    8. Redis
        Required for WebSocket management and background task handling, particularly in a real-time chat environment. Ensure Redis is installed and running.

Step-by-step installation and setup instructions:

Github: https://github.com/souravchakraborty700/social_chat_app

I Kept backend(social_chat) and frontend(frontend) in a main direcotry social_chat_app. Please follow the instruction below to install the project.

Step 1: Clone the project https://github.com/souravchakraborty700/social_chat_app
        $ cd social_chat_app
Step 2: For Django Backend(social_chat):
        $ cd social_chat
        $ pip install -r requirenets.txt

        In the social_chat Django project directory, modify the settings.py file: 
        Comment out the Redis configuration for local development and uncomment the Redis configuration for production deployment if you are deploying the app to a production environment.

        To run the application:
        $ daphne -b 0.0.0.0 -p 8000 social_chat.asgi:application

Step 3: For React Frontend(frontend):
        Go to the .env file under the frontend directory and uncomment 
        REACT_APP_API_BASE_URL=http://localhost:8000
        And comment out
        REACT_APP_API_BASE_URL=https://sourav-social-chat-app-62eb0b733f26.herokuapp.com

        $ cd frontend
        $ npm install
        $ npm start

Additional Notes:

Third-Party Cookies:
        Make sure third-party cookies are enabled in your browser, especially in Chrome's incognito mode, for proper functionality.

Environment Variables:
        Ensure environment variables are correctly set in the .env file before starting the frontend or backend.

Running the Project in Development Mode:
        Mention that both the backend and frontend need to be running simultaneously for the application to function properly.

How to run the application:
    https://social-chat-app-psi.vercel.app/
    Home page on the initial open page gives two options: Login and Register. A new user can register by going into Register page and giving their Username and Password. Upon doing that they will get a Login page to login with the username and password they provided for registration. Once they successfully log in to the application, they will be on the home page with options in the navbar: Friends, People, Notifications, Logout.

    Friends: 
        Users who accept interest messages become friends of the logged in user. By clicking the Chat button beside the user's name, they can always stay in the conversation. If they have received any messages from any friend that have not been read yet, loggedin user will see (new messages) notification in red beside the Chat button.
        
    People:
        User who are registered in this chat application will be visible here. The loggedin user can decide to send an interest message to anyone by clicking on Send Interest, then a pop up text box will open up and they can type in the interest message.

    Notifications:
        Logged in user can see if others sent any interest message, by reading the message they can choose to Accept Request or Reject Request. Upon clicking Accept Request a Chat box will open up to begin the conversation.

    Logout:
        This will make current user log out from the application.


Incomplete Aspects:
    I encountered challenges in successfully implementing tests for the chat functionality, particularly when dealing with WebSocket communication. Despite multiple attempts, I was unable to fully validate the chat functionality through automated testing. This area requires further investigation and refinement to achieve comprehensive test coverage.







