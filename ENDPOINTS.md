# ENDPOINTS

Next I will enumerate all the endpoints across all my services and define the data to be transferred.

##### Authentication

Apis related to authentication.

###### Register User

Signup and retrieve an authentication token.

- URL

`/auth/signup`

- Method

`POST`

- URL Params

`None`

- Data Params

Required:

`username` (string, unique): The username chosen by the user for authentication.

`email` (string, unique): The user's email address for communication and account recovery.

`password` (string): The user's chosen password for authentication.

- Success Respone

| Code | Description | Content                                                                       |
| :--- | :---------- | :---------------------------------------------------------------------------- |
| 201  | Created     | `{"message": "User registered successfully", "token": "the.jwt.token.here" }` |

- Error Response

| Code | Description | Content                                                               |
| :--- | :---------- | :-------------------------------------------------------------------- |
| 400  | Bad Request | `{ error: "Validation failed", details: { field: "error message" } }` |
