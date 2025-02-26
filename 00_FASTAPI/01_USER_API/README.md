Objective: Develop a RESTful API using Python that implements all CRUD (Create, Read, Update, Delete) operations using HTTP methods.

API Endpoints:

- GET /users - Retrieves a list of all users.
- GET /users/{user_id} - Retrieves a specific user by ID.
- POST /users - Creates a new user. Data for the new user will be provided in the request body (e.g., JSON format).
- PUT /users/{user_id} - Updates an existing user by ID. Data for the update will be provided in the request body.
- DELETE /users/{user_id} - Deletes a user by ID.

Data Model:
The API will manage user resources. Each user will have attributes like ID (unique identifier), name, email, etc. You can customize the data model based on your specific requirements.

Technologies:

- Python 3.x
- FastApi https://fastapi.tiangolo.com/tutorial/first-steps/
- Any other tools that may help you achieve the

Implementation Details:

- Feel free to fill in implementation details scope as needed, e.g. think about error handling, data validation, etc.

Testing:

- Write unit tests for all API endpoints to ensure their functionality.

Further Enhancements:

- Implement user authentication and authorization to restrict access to API endpoints.
- Add pagination support for retrieving large datasets (GET /users?page=2&per_page=10).
- Implement filtering and sorting capabilities for users (GET /users?name=Alice)
