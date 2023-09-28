# REST API Documentation

- Inspired by Swagger API docs style & structure

Next I will enumerate all the endpoints across all my services and define the data to be transferred.

## Authentication

Endpoints related to authentication.

<details>

<summary>
    <code>POST</code>
    <code>/api/auth/signup</code>
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
    <code>/api/auth/login</code>
    <code>Login User</code>
</summary>

Login and retrieve user token.

- URL

`/api/auth/login`

- Method

`POST`

- URL Params

`None`

- Data Params

Required:

`email`(string): The user's email address for authentication.

`password`(string): The user's chosed password for authentication.

- Success Response

| Code | Description      | Content                                                           |
| ---- | ---------------- | ----------------------------------------------------------------- |
| 200  | Login Successful | `{"message": "Login successful", "token": "your.jwt.token.here"}` |

- Error Response

| Code | Description  | Content                                                                |
| ---- | ------------ | ---------------------------------------------------------------------- |
| 400  | Bad Request  | `{"error": "Validation failed","details": {"field": "error message"}}` |
| 401  | Unauthorized | `{"error": "Authentication failed"}`                                   |

</details>

---

### Flight Search

Endpoints related to searching flights.

<details>
<summary>
    <code>GET</code>
    <code>/api/flights/search</code>
    <code>Search for flights</code>
</summary>

Additional information about searching for flights.

- **URL**

`/api/flights/search`

- **Method**

`GET`

- **URL Params**

`None`

- **Data Params**

`None`

- **Success Response**

| Code | Description | Content                                |
| ---- | ----------- | -------------------------------------- |
| 200  | Success     | `{ flights: [flight1, flight2, ...] }` |

- **Error Response**

| Code | Description  | Content                              |
| ---- | ------------ | ------------------------------------ |
| 401  | Unauthorized | `{ error: "Authentication failed" }` |

</details>

<details>
<summary>
    <code>GET</code>
    <code>/api/flights/search?filterBy=filter</code>
    <code>Search for flights based on specific filter</code>
</summary>

Search for flights based on specific filter

- **URL**

`/api/flights/search?filterBy=filter`

- **Method**

`GET`

- **URL Params**

**Required:**

`origin=[string]` - The code or name of the origin airport.

`destination=[string]` - The code or name of the destination airport.

`departureDate=[string]` - The date of departure (YYYY-MM-DD).

**Optional:**

`airline=[string]` - The name of the airline (for filtering by airline).

`maxPrice=[number]` - The maximum price for a flight.

`cabinClass=[string]` - The desired cabin class (e.g., "Economy," "Business").

`flexibleDates=[boolean]` - Indicates whether flexible date search is enabled (true/false).

- **Success Response**

| Code | Description | Content                                |
| ---- | ----------- | -------------------------------------- |
| 200  | Success     | `{ flights: [flight1, flight2, ...] }` |

- **Error Response**

| Code | Description         | Content                              |
| ---- | ------------------- | ------------------------------------ |
| 401  | Unauthorized        | `{ error: "Authentication failed" }` |
| 422  | Unprocessable Entry | `{ error: "Invalid input data" }`    |

</details>

<details>
<summary>
    <code>GET</code>
    <code>/api/flights/{flightId}</code>
    <code>Retrieve detailed information about that specific flight</code>
</summary>

- **URL**

`/api/flights/{flightId}`

- **Method**

`GET`

- **URL Params**

`flightId`(string) - The ID of the flight we are looking for.

- **Data Params**

`None`

- **Success Respone**

Code: `200`

Content:

```json
{
  "flightId": "FL12345",
  "airline": "Airline Name",
  "originAirport": "Origin Airport Code (e.g., JFK)",
  "destinationAirport": "Destination Airport Code (e.g., LAX)",
  "departureDateTime": "2023-09-30T08:00:00Z",
  "arrivalDateTime": "2023-09-30T11:30:00Z",
  "duration": "3 hours 30 minutes",
  "availableSeats": 120,
  "totalSeats": 150,
  "cabinClass": "Economy",
  "price": {
    "amount": 250.0,
    "currency": "USD"
  },
  "layovers": [
    {
      "airport": "Connecting Airport Code (if applicable)",
      "layoverDuration": "2 hours"
    }
  ],
  "flightNumber": "AI123",
  "aircraftType": "Boeing 737",
  "status": "Scheduled"
}
```

- **Error Response:**

| Code | Description  | Content                              |
| ---- | ------------ | ------------------------------------ |
| 401  | Unauthorized | `{ error: "Authentication failed" }` |
| 404  | Not Found    | `{ error: "Flight not found" }`      |

- **Sample Call:**

  ```javascript
  $.ajax({
    url: "/flights/search/FL12345",
    dataType: "json",
    type: "GET",
    success: function (response) {
      console.log(response);
    },
    error: function (error) {
      console.error(error);
    },
  });
  ```

</details>

---

### Flight Booking

<details>
<summary>
    <code>POST</code>
    <code>/api/bookings</code>
    <code>Create a new flight booking by providing details</code>
</summary>

- **URL**

`/api/bookings`

- **Method**

`POST`

- URL Params

`None`

- Data Params

  - **Required:**
    - `userId=[string]` - The unique identifier of the user making the booking.
    - `flights=[array]` - An array of flight objects representing the flights to be booked. Each flight object should include:
      - `flightId=[string]` - The unique identifier of the flight.
      - `passengers=[array]` - An array of passenger objects for this flight. Each passenger object should include:
        - `firstName=[string]` - The first name of the passenger.
        - `lastName=[string]` - The last name of the passenger.
        - `dateOfBirth=[string]` - The date of birth of the passenger (YYYY-MM-DD).
        - `gender=[string]` - The gender of the passenger.

- **Success Response**

| Code | Description | Content                                            |
| ---- | ----------- | -------------------------------------------------- |
| 201  | Created     | `{ bookingId: "B123456789", status: "Confirmed" }` |

- **Error Response**

| Code | Description         | Content                              |
| ---- | ------------------- | ------------------------------------ |
| 401  | Unauthorized        | `{ error: "Authentication failed" }` |
| 422  | Unprocessable Entry | `{ error: "Invalid input data" }`    |

</details>

<details>
<summary>
    <code>GET</code>
    <code>/api/bookings/{bookingId}</code>
    <code>Retrieve details about a specific booking</code>
</summary>

- **URL**

`/api/bookings/{bookingId}`

- **Method**

`GET`

- **URL Params**

`bookingId`(string) - The identifier of the booking to get information about.

- **Data Params**

`None`

- **Success Response**

| Code | Description | Content                            |
| ---- | ----------- | ---------------------------------- |
| 200  | Success     | `{ bookingId: "B123456789", ... }` |

- **Error Response:**

| Code | Description  | Content                              |
| ---- | ------------ | ------------------------------------ |
| 401  | Unauthorized | `{ error: "Authentication failed" }` |
| 404  | Not Found    | `{ error: "Booking not found" }`     |

</details>

<details>
<summary>
    <code>PUT</code>
    <code>/api/bookings/{bookingId}</code>
    <code>Allows users to modify their booking details</code>
</summary>
</details>

<details>
<summary>
    <code>DELETE</code>
    <code>/api/bookings/{bookingId}</code>
    <code>Delete a specific booking</code>
</summary>
</details>

<details>
<summary>
    <code>GET</code>
    <code>/api/bookings/user/{userId}</code>
    <code>Retrieve a list of bookings associated with a specific user</code>
</summary>
</details>

---
