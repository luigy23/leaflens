# 1. Introduction

## Background

Houseplants have become an increasingly popular part of modern living. According to industry reports, the global indoor plant market reached USD 26 billion in 2024 and is projected to grow at a compound annual rate above 6% through the decade. This growth has been accelerated by demographic trends such as urbanization, the rise of smaller living spaces, and the well-documented psychological benefits of caring for greenery.

However, the same growth has surfaced a recurring user problem: most owners cannot reliably identify the species they have purchased, and even fewer know how to care for them. Care requirements vary dramatically between species — *Sansevieria trifasciata* tolerates weeks of drought while *Maranta leuconeura* will collapse with the same neglect — and incorrect care is the single largest cause of plant death in households.

Commercial mobile applications such as **PictureThis**, **PlantNet**, and **Plantum** have demonstrated that this is a viable problem space for artificial intelligence. PictureThis alone reports more than 150 million downloads and a subscription business measured in hundreds of millions of dollars annually. The success of these products confirms two facts: (a) the problem is real and widely felt, and (b) image-based species classification is mature enough to ship in production.

## Project overview

**LeafLens** is a web application that brings the core PictureThis-style experience to a self-contained academic prototype. The user uploads a photograph of a houseplant; the system runs the image through a fine-tuned deep learning classifier and returns:

1. The most likely species (with confidence score)
2. Two alternative candidates for ambiguous images
3. A care card with watering frequency, light requirements, temperature range, fertilization tips, and toxicity warnings for cats and dogs

The system is implemented end-to-end: data preparation, model training and comparison, REST backend, web frontend, and cloud deployment.

## Scope

This project is the first of two required deliverables for the Artificial Intelligence course (BEINSOF52) at Universidad Surcolombiana. It satisfies the computer vision track: image classification with a useful real-world application. The deliverables include all elements of the course rubric: a working AI model, a Flask backend with persistent storage, a React frontend, and deployment to a free-tier cloud provider, supported by full English documentation.

## Document structure

This documentation set is organized as follows:

- **Section 2** states the problem in detail and the population it affects.
- **Section 3** lists the project objectives, both general and specific.
- **Section 4** surveys the state of the art in plant classification.
- **Section 5** captures functional and non-functional requirements.
- **Section 6** describes the use cases and user stories.
- **Section 7** specifies the data dictionary and entity-relationship model.
- **Section 8** presents the system class diagrams.
- **Section 9** shows the GUI mockups.
- **Section 10** catalogs the web service API.
- **Section 11** describes the testing strategy.
- **Section 12** depicts the proposed architecture.
- **Section 13** reports results and discussion.
- **Section 14** lists recommendations and future work.
