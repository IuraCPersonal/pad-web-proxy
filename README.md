# FAF.PAD16.2 Autumn 2023

<p align="center">
  <img alt="NestJS" src="https://img.shields.io/badge/nestjs-%23E0234E.svg?style=for-the-badge&logo=nestjs&logoColor=white" />
  <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
  <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" />
  <img alt="Kubernetes" src="https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white" />
  <img alt="MongoDB" src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white" />
</p>

## LAB 1: WEB PROXY (CHECKPOINT 01)

##### Due: September 21/28, 2023

### ABOUT THIS BRANCH

This branch contains first checkpoint for the `PAD LAB 1`.

### CHECKPOINT TERMS

#### Assess Application Suitability - 2p

Here are some reasons why my idea might be relevant for a microservices architecture and real-world examples of well-known projects.

1. **Scalability:** Very often, _Airline Reservation Systems_ need to handle a high level of traffic,
   especially during peak travel seasons or special events. With the help of _microservices_, we can scale
   specific components, to handle an increased load in a more efficient way.
2. **Rapid Development and Deployment**: With the help of _microservices_, we allow teams and developers to develop and deploy
   individual components independently. This will lead to faster development. `Airbnb` is an example of a company that uses microservices to continuously deploy updates and improvements to its platform.
3. **Easier Maintenance:** With microservices, you can update and maintain individual components without affecting the entire system.
4. **Geographic Distribution:** Airlines operate globally, and a distributed system can facilitate geographic distribution. By deploying microservices in different regions or countries, you can reduce latency for users in those areas, providing a better user experience.
5. **Enhanced Resilience:** By adding microservices, we can build redundancy into critical components, ensuring high availability and disaster recovery. `Uber` uses microservices to maintain service availability even in the face of hardware or software failures.

---

#### Define Service Boundaries - 2p

Microservices require clear service boundaries. Each microservice should encapsulate specific functionality, such as user authentication, product
catalog, or order processing, to ensure modularity and independence. Here is a simple `architecture diagram`:

![API Architecture Diagram](https://github.com/IuraCPersonal/pad-web-proxy/blob/feature/checkpoint-1/public/API-architecture-diagram.png)

In my application architecture, I identified three main services: the `Authentication Service`, `Flight Search Service` and `Flight Search Service`. Each having it's own responsabilities and database.

Next is a description of each **service** and its specific functionalities.

1. Authentication

   - **User Authentication:**

     - User Login
     - Token-Based Authentication

   - **User Registration:**
     - User Signup
     - User Profile Creation

2. Flight Search

   - **Search Flights**
   - **Search Flights by Id**
   - **Retrieve Flight Details**

3. Flight Booking

   - **Book a Flight**
   - **Retrieve Booking Details**
   - **Edit Bxisting Booking**
   - **Delete Bxisting Booking**
   - **Retrieve a List of Bookings for Any User**

---

#### Choose Technology Stack and Communication Patterns - 2p

When implementing microservices, we must carefully choose the technology stack for each service. Using `JavaScript` (specifically `NestJS`) and `Python` for my microservices application can be a strategic and advantageous choice for various reasons:

1. Wide Adoption and Community Support
2. Versatility. NestJS leverages TypeScript, a statically typed superset of JavaScript, which brings strong typing and enhanced tooling support to my microservices. TypeScript helps catch errors early in the development process and makes my codebase more maintainable.
3. Asynchronous Capabilities. Node.js, the runtime environment for JavaScript, excels in handling asynchronous operations, which are common in microservices for tasks like handling concurrent requests and event-driven architectures. Even if I will be using synchronous communication - JavaScript will handle everything smoothly.

For this application, I will be using **synchronous communication - REST**. Using synchronous communication, such as REST (Representational State Transfer) offers several advantages.

- REST follows the stateless client-server architecture, where each request from a client to a server must contain all the information needed to understand and process the request. This statelessness simplifies the server's architecture, making it easier to scale and maintain.
- REST allows for caching of responses. This can significantly reduce the load on our microservices and improve performance by serving cached data to clients when appropriate.
- REST can be used with a variety of clients, including web browsers, mobile applications, and third-party integrations. It's suitable for building public APIs that external developers can use.
- REST relies on a set of well-defined standards, including HTTP methods (GET, POST, PUT, DELETE) and status codes (e.g., 200 for success, 404 for not found). This consistency simplifies the development process.
- Synchronous communication can be more straightforward to handle in terms of error handling and retries. When a client sends a request, it expects an immediate response, which simplifies error handling compared to asynchronous communication where handling retries and failures can be more complex.

---

#### Design Data Management - 3p

For this project, I will be working with **different databases for each microservice**.

- Each microservice has its own dedicated database, which encapsulates its data and ensures data isolation.
- It can simplify database schema design since each microservice only deals with its specific data model.

I will also have an API gateway that acts as a central entry point for clients to access data across multiple microservices. The API gateway can aggregate data from various microservices and present it to clients in a unified manner. This approach simplifies client interactions and reduces the need for clients to make multiple requests to different microservices.

Next I will enumerate all the endpoints across all my services and define the data to be transferred.

| Endpoint                              | Method   | Description                                                                            |
| ------------------------------------- | -------- | -------------------------------------------------------------------------------------- |
| `/api/auth/login`                     | `POST`   | Login and retrieve an authentication token                                             |
| `/api/auth/signup`                    | `POST`   | Signup and retrieve an authentication token                                            |
| `/api/flights/search`                 | `GET`    | Search for flights based on the origin and destination airports                        |
| `/api/flights/search?filterBy=filter` | `GET`    | Search for flights based on specific filter                                            |
| `/api/flights/{flightId}`             | `GET`    | Retrieve detailed information about that specific flight                               |
| `/api/bookings`                       | `POST`   | Create a new flight booking by providing details                                       |
| `/api/bookings/{bookingId}`           | `GET`    | Retrieve details about a specific booking by providing the booking ID                  |
| `/api/bookings/{bookingId}`           | `PUT`    | Allows users to modify their booking details                                           |
| `/api/bookings/{bookingId}`           | `DELETE` | Delete a specific booking by providing the booking ID                                  |
| `/api/bookings/user/{userId}`         | `GET`    | Retrieve a list of bookings associated with a specific user by providing their user ID |

For a more enhanced description of all the available `endpoints`, please refer to this DOCUMENT.

Example of how a `flight` object would look like:

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

And an example of a `booking` object:

```json
{
  "bookingId": "B123456789",
  "userId": "U123456789",
  "flights": [
    {
      "flightId": "FL12345",
      "airline": "Airline Name",
      "departureDateTime": "2023-09-30T08:00:00Z",
      "arrivalDateTime": "2023-09-30T11:30:00Z",
      "cabinClass": "Economy",
      "price": {
        "amount": 250.0,
        "currency": "USD"
      }
    }
  ],
  "passengers": [
    {
      "firstName": "John",
      "lastName": "Doe",
      "dateOfBirth": "1990-05-15",
      "gender": "Male"
    },
    {
      "firstName": "Jane",
      "lastName": "Doe",
      "dateOfBirth": "1992-08-20",
      "gender": "Female"
    }
  ],
  "totalPrice": {
    "amount": 500.0,
    "currency": "USD"
  },
  "status": "Confirmed",
  "bookingDate": "2023-09-15T10:30:00Z",
  "paymentMethod": "Credit Card",
  "paymentStatus": "Paid"
}
```

#### Set Up Deployment and Scaling - 1p

In this section I will introduce the tools I chose to deploy and scale my microservices. Deploying and scaling microservices efficiently is crucial for maintaining the reliability and availability of my application. Here's a high-level plan on how I will use Docker and Kubernetes for this purpose:

1. I will go with **Containerization with Docker**.
   - Docker allows to package each microservice and its dependencies into a lightweight, isolated container. This provides consistency in deployment across different environments (development, testing, production) and simplifies the packaging and distribution of microservices.
   - It allows create a Dockerfile for each microservice, specifying its runtime environment, dependencies, and how it should start. Build Docker images for each microservice.
2. Orchestration with Kubernetes (barely know how to)
   - It will help automate deployment, scaling, and management of containerized applications.
   - Set up a Kubernetes cluster, which consists of a master node and multiple worker nodes.

### CONTACT

If you have any question, please contact me through email: `iurie.cius@isa.utm.md`.
