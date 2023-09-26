# FAF.PAD16.2 Autumn 2023

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

---

### CONTACT

If you have any question, please contact me through email: `iurie.cius@isa.utm.md`.
