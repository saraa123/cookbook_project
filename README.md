# Sara Akhtar's Cookbook Project

## Overview

This cookbook project looked at creating a responsive website that allowed a user to view recipes, but also to edit, delete and add new recipes. Recipes are sorted with the highest rated shown first, with the ability to change the ratings.
I wanted to create a website that was simple and showcased my ability to connect to a mongo database successfully. 

As this cookbook doesn’t have username capability, but users do have the ability to delete recipes, I wanted to ensure that all the recipes in the database wouldn’t be deleted and the website would be left empty. Therefore I created a certain amount of recipes in mongoDB that couldn’t be deleted, however the rest of the recipes could. This was achieved by adding a hidden value for all recipes. 

For the sake of this project, I created headings so that I could clearly distinguish which recipes you could and couldn’t delete.  


## UX and UI

In order to create a good UX and UI design I made sure the website was easy to manoeuvre through, therefore I opted for an overall simple layout. I also ensured that the website was responsive to cater to the various screen sizes available. 
Wireframes were used in order to ensure these design goals were achieved and to promote a smoother planning process.

## Features

* Materialize  – used to create a responsive navbar, rows and columns.
* Flask – allowed me to use a base template for the layout of the website
* jQuery – used to make certain features of Materialize to work,  e.g. dropdown boxes  

### Features left to implement 

I would like to learn and experiment with django in order to see the workings of a more powerful piece of software. Being able to provide username functionality is also a feature that I would like to use in the future. 

## Methods used

1. HTML
2. CSS
3. Materialize  
4. Javascript & jQuery 
5. Flask

## Testing techniques 

When testing the code for this website http://jshint.com, manual testing and Google’s responsive web tester were implemented. 

### Jasmine

The website http://jshint.com and Jasmine were both used in order to check for any potential errors within the Javascript code. There weren't any errors detected, and all the code ran as it should. 

### Manual testing

https://chrome.google.com/webstore/detail/responsive-web-design-tes/bdpelkpfhjfiacjeobkhlkkgaphbobea.
This chrome plug in was used when testing HTML and CSS to assess the responsiveness of the website on different screen sizes. 

## Deployment

Github and Heroku were used for the deployment of this project.

## Credits

### Media

The images that have been used on this website have all been searched on Google.

### Acknowledgements 


**This is for educational purposes**