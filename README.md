# Task Management API Documentation

## Setup

To set up the Task Management API locally:

1. Clone the repository:

`git clone https://github.com/jferi/TaskModel.git`

2. Install the required dependencies:

`pip install -r requirements.txt`

3. Apply database migrations:

`python manage.py migrate`

4. Run the development server:

`python manage.py runserver 8888`

## Endpoints

### 1. List Tasks

- **GET** `/tasks/`

- Retrieves a list of tasks.

**Request:**

GET /tasks/

**Response:**

 JSON
 
    [
        {
            "id": 1,
            "title": "Task 1",
            "description": "Description of Task 1",
            "creation_date": "2024-03-15T14:30:00Z",
            "due_date": null,
            "status": "pending"
        },
        {
            "id": 2,
            "title": "Task 2",
            "description": "Description of Task 2",
            "creation_date": "2024-03-16T09:25:00Z",
            "due_date": "2024-03-20T12:00:00Z",
            "status": "in_progress"
        }
    ]


### 2. Create Task

**POST** `/tasks/`

- Creates a new task.

**Request Body:**



```
{
    "title": "New Task",
    "description": "Description of the new task",
    "due_date": "2024-03-30T12:00:00Z",
    "status": "pending"
}
```

**Response:**

JSON
```
{
	"id": 3,
	"title": "New Task",
	"description": "Description of the new task",
	"creation_date": "2024-03-15T16:45:00Z",
	"due_date": "2024-03-30T12:00:00Z",
	"status": "pending"
}
```

### 3. Update Task

**PATCH/PUT** `/tasks/{id}/`

- Updates the specified task.

**Request Body:**

```
{
    "title": "Updated Task Title",
    "description": "Updated description",
    "status": "completed"
}
```

**Response:**

JSON

```
{
    "id": 3,
    "title": "Updated Task Title",
    "description": "Updated description",
    "creation_date": "2024-03-15T16:45:00Z",
    "due_date": "2024-03-30T12:00:00Z",
    "status": "completed"
}
```

   ### Delete Task

   **DELETE** `/tasks/{id}/`

   - Removes the specified task.

   **Response:**

   **Success (200 OK):** Task successfully deleted message.

       {
           "message": "Task successfully deleted."
       }

   **Failure (404 Not Found):** Task not found message.

       {
           "error": "Task not found."
       }

   ## Project review

   ### Filtering and Ordering:
   **Decision:** Implemented filtering and ordering backends using DjangoFilterBackend and filters.OrderingFilter. This decision provides flexibility in querying tasks, improving user experience by allowing users to sort and filter tasks based on their needs.

   ### Task Suggestions Feature:
   **Decision:** Developed a `generate_suggestions` function based on analyzing completed tasks. This feature aims to provide value-added suggestions to users by identifying common patterns and keywords in completed tasks.

   ### Error Handling and Validation:
   **Decision:** Custom validation logic was implemented for task due dates and status transitions to enforce business rules (e.g., a task cannot be due in the past, certain status transitions are not allowed).
   **Assumption:** Assumed that enforcing these rules at the serializer level would prevent invalid data entries and maintain the integrity of the application state.
