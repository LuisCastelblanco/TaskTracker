from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
import json
from datetime import datetime
from typing import Dict, List, Any

router = APIRouter()

def generate_test_script(path: str, method: str, operation: Dict) -> List[str]:
    """Generate Postman test scripts for an endpoint."""
    tests = []
    
    # Basic response tests
    tests.extend([
        "// Basic Response Tests",
        "pm.test(\"Status code is 200\", function () {",
        "    pm.response.to.have.status(200);",
        "});",
        "",
        "pm.test(\"Response time is acceptable\", function () {",
        "    pm.expect(pm.response.responseTime).to.be.below(2000);",
        "});",
        "",
        "pm.test(\"Content-Type is application/json\", function () {",
        "    pm.response.to.have.header(\"Content-Type\");",
        "    pm.expect(pm.response.headers.get(\"Content-Type\")).to.include(\"application/json\");",
        "});"
    ])

    # Authentication tests for secured endpoints
    if any(security.get("OAuth2PasswordBearer") is not None 
           for security in operation.get("security", [])):
        tests.extend([
            "",
            "// Authentication Tests",
            "pm.test(\"Authorization header is present\", function () {",
            "    pm.request.to.have.header(\"Authorization\");",
            "});",
            "",
            "pm.test(\"Token format is valid\", function () {",
            "    const authHeader = pm.request.headers.get(\"Authorization\");",
            "    pm.expect(authHeader).to.match(/^Bearer .+$/);",
            "});"
        ])

    # Endpoint specific tests
    if path == "/auth/login":
        tests.extend([
            "",
            "// Token Response Tests",
            "pm.test(\"Login response contains token\", function () {",
            "    const responseData = pm.response.json();",
            "    pm.expect(responseData).to.have.property('access_token');",
            "    pm.expect(responseData).to.have.property('token_type');",
            "    ",
            "    // Save token to environment",
            "    if (pm.response.code === 200) {",
            "        pm.environment.set(\"access_token\", responseData.access_token);",
            "    }",
            "});"
        ])
    elif path.startswith("/tasks"):
        is_array = method == "GET" and "{task_id}" not in path
        tests.extend([
            "",
            "// Task Schema Tests",
            "pm.test(\"Task response has required fields\", function () {",
            "    const responseData = pm.response.json();",
            f"    {'pm.expect(responseData).to.be.an(\"array\");' if is_array else ''}",
            f"    {'responseData.forEach(task => {' if is_array else ''}",
            f"    {'    ' if is_array else ''}pm.expect({f'task' if is_array else 'responseData'}).to.include.all.keys(['id', 'texto', 'estado', 'category_id', 'fecha_creacion']);",
            f"    {'    ' if is_array else ''}pm.expect({f'task' if is_array else 'responseData'}.estado).to.be.oneOf(['Sin Empezar', 'Empezada', 'Finalizada']);",
            f"    {'});' if is_array else ''}",
            "});"
        ])

    return tests

def generate_sample_value(schema: Dict) -> Any:
    """Generate sample values based on schema type."""
    if schema.get("type") == "string":
        if schema.get("format") == "date-time":
            return datetime.now().isoformat()
        return "sample string"
    elif schema.get("type") == "integer":
        return 1
    elif schema.get("type") == "boolean":
        return True
    elif schema.get("type") == "array":
        return [generate_sample_value(schema["items"])]
    return None

def generate_postman_collection(app: FastAPI) -> Dict:
    """Generate a Postman collection from FastAPI app."""
    collection = {
        "info": {
            "name": "FastAPI Collection",
            "description": "Generated from FastAPI application",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [],
        "variable": [
            {
                "key": "baseUrl",
                "value": "http://localhost:8000",
                "type": "string"
            }
        ]
    }

    # Create folders for different endpoint groups
    folders = {
        "auth": {"name": "Auth", "item": []},
        "tasks": {"name": "Tasks", "item": []},
        "users": {"name": "Users", "item": []},
        "categories": {"name": "Categories", "item": []}
    }

    openapi_schema = app.openapi()
    
    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            request = {
                "name": operation.get("summary", path),
                "request": {
                    "method": method.upper(),
                    "header": [],
                    "url": {
                        "raw": "{{baseUrl}}" + path,
                        "host": ["{{baseUrl}}"],
                        "path": [p for p in path.split("/") if p]
                    }
                },
                "response": [],
                "event": [{
                    "listen": "test",
                    "script": {
                        "type": "text/javascript",
                        "exec": generate_test_script(path, method, operation)
                    }
                }]
            }

            # Add authorization if needed
            if any(security.get("OAuth2PasswordBearer") is not None 
                   for security in operation.get("security", [])):
                request["request"]["auth"] = {
                    "type": "bearer",
                    "bearer": [
                        {
                            "key": "token",
                            "value": "{{access_token}}",
                            "type": "string"
                        }
                    ]
                }

            # Add to appropriate folder
            if path.startswith("/auth"):
                folders["auth"]["item"].append(request)
            elif path.startswith("/tasks"):
                folders["tasks"]["item"].append(request)
            elif path.startswith("/users"):
                folders["users"]["item"].append(request)
            elif path.startswith("/categories"):
                folders["categories"]["item"].append(request)
            else:
                collection["item"].append(request)

    # Add folders to collection
    collection["item"].extend(folder for folder in folders.values() if folder["item"])

    return collection

@router.get("/generate-postman-collection")
async def get_postman_collection(app: FastAPI):
    """Endpoint to generate Postman collection."""
    collection = generate_postman_collection(app)
    return JSONResponse(content=collection)

