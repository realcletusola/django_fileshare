<h3>Async File Sharing REST API</h3>


<p>This project is a Django Rest Framework (DRF) based asynchronous file-sharing REST API. It offers efficient and scalable file sharing capabilities with comprehensive logging functionalities to ensure robust error handling and monitoring.</p>

<h4>Features</h4>

		Asynchronous Operations: Utilizes async views and ASGI middleware to handle high concurrency and improve performance.

		File Sharing: Provides secure endpoints for uploading, and managing files.
		Logging: Implements detailed logging for tracking activities and troubleshooting errors, with logs categorized and stored per application module.

		Authentication: Includes user authentication and authorization to ensure secure access to file-sharing endpoints.

Technology Stack

		Django: Web framework for the backend.
		Django Rest Framework (DRF): For building the RESTful API.
		ASGI: For asynchronous support.
		Logging: Configured to handle and store logs for different components separately.

Setup Instructions

		Clone the repository.
		Install the required dependencies.
		Configure the database and environment variables.
		Run the migrations and start the development server with "uvicorn fileshare.asgi:application --reload".
