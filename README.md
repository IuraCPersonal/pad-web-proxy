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

#### Define Service Boundaries - 2p

Microservices require clear service boundaries. Each microservice should encapsulate specific functionality, such as user authentication, product
catalog, or order processing, to ensure modularity and independence. Here is a simple `architecture diagram`:

![API Architecture Diagram](https://raw.githubusercontent.com/IuraCPersonal/pad-web-proxy/feature/checkpoint-1/public/API-architecture-diagram.png)

### CONTACT

If you have any question, please contact me through email: `iurie.cius@isa.utm.md`.
