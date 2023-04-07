<h1 align="center">Blue Orange Microservices</h1>

<p align="center">
  ![build](https://github.com/endritber/microo-blue-orange/actions/workflows/github-ci.yml/badge.svg)
  <img alt="License" src="https://img.shields.io/badge/license-MIT-%2304D361">
</p>

# Architecture

This systems is an exmaple to scalable django features that is based on microservices pattern. Is it a good idea? Depends on the perspective.
The difference is that, microservices running here propose a loosely coupled and contradicted against django with tightly coupled style

## Trade-off

Possibly, depending how many traffics or services there are several pros and cons to get going with this pattern. If you got a problem with reusability or customizable - this pattern might come handy since it is independently integrating with any frontend framework that has a high start-up speed of less than a second. 

### Tools
 ```
 Django
 Django REST Framework (Simple JWT)
 Postgresql
 Celery
 RabbitMQ
 Adminer
 ```

-----

See Docker folder how to get started with backend service.

-----

## License
This project is under the MIT license. See the [LICENSE](LICENSE) for more information.
---
