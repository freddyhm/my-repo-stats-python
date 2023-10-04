# **Add Persistent Storage Decision**

## Date

09/28/2023

## **Status**

Accepted

## **Context**

Instead of relying on Github’s service to fetch the same data at each request, we will store the results in persistent storage. This will improve performance and lower the number of requests sent to Github.

## **Decision**

Given our focus is to use the most common tools for Django development, we will use the same storage technology that comes with Django - PostgreSQL

## Alternatives

- In-memory storage such as Redis
- Other relational lightweight databases such as SQLite, MySQL, etc
- Lightweight non-relational databases such as Azure Table Storage

## Risks

Our application may be best built with a more lightweight storage solution. It may also be cheaper when deploying and hosting with a provider.

## **Consequences**

Our application may not use the best choice of storage for the app’s requirements but it will allow us to gain more experience with the most common database solution.
