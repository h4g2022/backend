# Hire4Good Backend

### Requirements
- Docker Compose V2

### About CI/CD Pipelines
The current CI/CD pipelines are set up to build and deploy at [h4g.kitsuiro.com](https://h4g.kitsuiro.com/api/v1/).

### Development
1. Remove `_example` from filename of both `app.env_example` and `db.env_example` and edit the variables accordingly.
2. Run the following shell command: `make dev`
3. Access the API at [localhost:8000/api/v1](https://localhost:8000/api/v1) or the auto-generated Swagger docs at [localhost:8000/api/v1/docs](https://localhost:8000/api/v1/docs).

### Deployment
Similar to Development, but edit `deploy.docker-compose.yml` according to any needs and run `make deploy`.

## Endpoints
Payload structure and response body can be found on the [Swagger docs](https://h4g.kitsuiro.com/api/v1/docs).

### Authentication API
`POST` /auth/create - Create a user for auth purposes for either talent/employer

Note: Upon auth account creation, talent/employer instance will be created respectively.

`POST` /auth/login - Log in user and obtain access token, refresh token, and other user data

`POST` /auth/refresh - Obtain a new access token using refresh token

Note: Access tokens are set to 60 minute expiry, refresh tokens are set to 1440 minute expiry

`POST` /auth/logout - Log out user and invalidates all refresh tokens associated with that user

### Talent API
`GET` /talent/all - Get information on all talents that are set to be displayed

Only accessible to Employer accounts

`GET` /talent/detail - Get detailed information on a specific talent

Only accessible to Employer accounts

`GET` /talent/me - Get information on currently logged in talent

Only accessible to Talent accounts

`PUT` /talent/me - Edit information on currently logged in talent

Only accessible to Talent accounts

### Employer API
`GET` /employer/me - Get information on currently logged in employer

Only accessible to Employer accounts

`PUT` /employer/me - Edit information on currently logged in employer

Only accessible to Employer accounts

### Job Listing API
`GET` /talent/all - Get information on all listings available

`POST` /listing/create - Create a new listing

Only accessible to Employer accounts

`PUT` /listing/update - Update an existing listing associated with currently logged in employer

Only accessible to Employer accounts

`DELETE` /listing/delete - Delete an existing listing associated with currently logged in employer

Only accessible to Employer accounts

### File Upload API (for profile image)
`GET` /file/img/{image_id} - Get an uploaded image

`POST` /file/upload - Upload an image

Note: User must be logged in. Each photo is tagged to the uploader and cannot be used by anyone else for profile photo