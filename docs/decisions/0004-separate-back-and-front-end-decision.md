# **Separate Back and Front End Decision**

## Date

09/26/2023

## **Status**

Accepted

## **Context**

Most modern apps of medium scale will seek to separate the back-end and the front-end. This provides many benefits such as loose coupling, letting both parts evolve independently.
For this app, it is not necessary given it’s limited size, however, the real goal of the app is to gain more experience with Django’s ecosystem. 

## **Decision**

Given our focus is on getting hands-on experience, we will split the back-end and the front-end. the front-end will be implemented using React.js and the backend with the Django REST framework (DRF)

## Alternatives

- **Front-End**: Many other front-end frameworks such as Next.js, Svelte, etc.
- **Back-End:** Manually setting up an API with Django

## Risks

Our application may be best built with a more lightweight framework for both front and back-end. It may be easier to use as well.

## **Consequences**

Our application may be bloated from the start but it will allow us to gain more experience with the most common frameworks.
