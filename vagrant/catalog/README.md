# Udacity FSND Catalog Project

## Intro

This application provides a list of items within a variety of categories as well as a user registration and authentication system.
Registered users will have the ability to post, edit and delete their own items.

## Set Up Environment

- install vagrant and/or virtual box
- clone project
- cd into `/vagrant`
- run `vagrant up`

## How to run

- log in via `vagrant ssh`
- cd into `/vagrant/catalog/`
- create database by running `python database_setup.py`
- prefill database by running `python lotsofcategories.py`
- run `project.py`

## Usage
- `/categories/JSON` - json endpoint for categories
- `/items/JSON` - endpoint for items