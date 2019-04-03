import os 
from flask import Flask, render_template, request, redirect, url_for 
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'Cookbook'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')


mongo = PyMongo(app)

@app.route('/')
@app.route('/get_recipe')
def get_recipe():
    return render_template("recipes.html", 
    recipes=mongo.db.recipes.find())

@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html", 
    foodCategory=mongo.db.foodCategory.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipe'))
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_foodCategory=mongo.db.foodCategory.find()
    return render_template('editrecipe.html', recipe=the_recipe, foodCategory=all_foodCategory)

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'ingredient_name':request.form.get('ingredient_name'),
        'cuisine_name':request.form.get('cuisine_name'),
        'author_name':request.form.get('author_name')
    })
    return redirect(url_for('get_recipe'))
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipe'))

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories=mongo.db.foodCategory.find())

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.foodCategory.find_one({'_id': ObjectId(category_id)}))
    
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    category=mongo.db.foodCategory
    category.update({'_id': ObjectId(category_id)},
        {'recipe_category': request.form.get('recipe_category')}
        )
    return redirect(url_for('get_categories'))
    
    
    
    
    
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
    
