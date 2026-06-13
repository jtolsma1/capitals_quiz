# Capitals Quiz

A Streamlit-based quiz app that:
- asks you to name the capital city of a random country ([sourced from this list](https://github.com/samayo/country-json/blob/master/src/country-by-capital-city.json))
- keeps track of which ones you've gotten right
- will not repeat countries where a correct answer has already been given
- resets quiz progress on demand

## What this actually is

This was a Kubernetes practice project that required a frontend, a backend, and persistent data storage.

## What it was meant to practice

- **Two-container architecture**: a Streamlit frontend and a FastAPI backend, each as their own Deployment and Service, talking to each other over Kubernetes' internal DNS.
- **Stateless backend, multiple replicas**: the backend doesn't hold any session state in memory. Every request carries a `user_id`, and the backend reads/writes whatever it needs from disk on every call. 
- **Static vs. durable data**: the master list of countries and capitals is baked into the backend's Docker image at build time. User progress, on the other hand, lives on a PersistentVolume so it survives pod restarts.
- **PersistentVolume / PersistentVolumeClaim**: started with a direct `hostPath` mount, then upgraded to the proper PV/PVC abstraction, which is the pattern that generalizes beyond a single-node Minikube setup.


## What it is not

A finished product, a thing anyone should use, or something with any kind of security, error handling, or polish beyond "it works on my Minikube." Future me may come back and bolt a Redis cache onto this project for further practice.
