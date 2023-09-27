# REST API Documentation

- Inspired by Swagger API docs style & structure

Next I will enumerate all the endpoints across all my services and define the data to be transferred.

## Authentication

Endpoints related to authentication.

<details>
<summary>
    <code>POST</code>
    <code>/auth/signup</code>
    <code>Register User</code>
</summary>

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

| Code | Description         | Content                                                               |
| :--- | :------------------ | :-------------------------------------------------------------------- |
| 400  | Bad Request         | `{ error: "Validation failed", details: { field: "error message" } }` |
| 422  | Unprocessable Entry | `{ error : "Email Invalid" }`                                         |
</details>

<details>
<summary>
    <code>POST</code>
    <code>/auth/login</code>
    <code>Login User</code>
</summary>
</details>

---

### Flight Search

Endpoints related to searching flights.

<details>
<summary>
    <code>GET</code>
    <code>/flights/search</code>
    <code>Search for flights</code>
</summary>
</details>

<details>
<summary>
    <code>GET</code>
    <code>/flights/search?filterBy=filter</code>
    <code>Search for flights based on specific filter</code>
</summary>
</details>

<details>
<summary>
    <code>GET</code>
    <code>/flights/{flightId}</code>
    <code>Retrieve detailed information about that specific flight</code>
</summary>
</details>

---

### Flight Booking

<details>
<summary>
    <code>POST</code>
    <code>/bookings</code>
    <code>Create a new flight booking by providing details</code>
</summary>
</details>

<details>
<summary>
    <code>GET</code>
    <code>/bookings/{bookingId}</code>
    <code>Retrieve details about a specific booking</code>
</summary>
</details>

<details>
<summary>
    <code>PUT</code>
    <code>/bookings/{bookingId}</code>
    <code>Allows users to modify their booking details</code>
</summary>
</details>

<details>
<summary>
    <code>DELETE</code>
    <code>/bookings/{bookingId}</code>
    <code>Delete a specific booking</code>
</summary>
</details>

<details>
<summary>
    <code>GET</code>
    <code>/bookings/user/{userId}</code>
    <code>Retrieve a list of bookings associated with a specific user</code>
</summary>
</details>

---
