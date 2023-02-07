# Hire4Good Backend

### Requirements
- Docker Compose V2

### About CI/CD Pipelines
The current CI/CD pipelines are set up to build and deploy at [h4g.kitsuiro.com](https://h4g.kitsuiro.com/api/v1/).

### Development
1. Remove `_example` from filename of both `app.env_example` and `db.env_example` and edit the variables accordingly.
2. Run the following shell command: `make dev`
3. Access the API at [localhost:8000/api/v1](https://localhost:8000/api/v1) or the auto-generated Swagger docs at [localhost:8000/api/v1/docs](https://localhost:8000/api/v1/docs).