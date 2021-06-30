# CiscoProject

An example project I was asked to create before my interview at Cisco.

## Reason behind Architecture

I decided to go with python on AWS lambda for this project for three main reasons:

1. Costs
    1. Whatever I chose had to be running 24/7 for interviews to test the week prior to my interview (ruled out self hosting)
    2. I was weary of running a free tier EC2 instance because it is not rightsized for the task of creating a simple API
2. Setup
    1. From a setup perspective, it is much more feasible to create several small lambdas than set up a EC2 / Clustering / Docker in a week (less piping)
    2. Exisitng AWS Tools to more easily test and deploy
3. Security
    1. Each piece of the CRUD operations could be isolated to exactly the calls it needed to preform its job
    2. Didn't expose my own computer to the internet

