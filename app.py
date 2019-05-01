import os 
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'Cookbook'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')


mongo = PyMongo(app)

# recipes: get, add, edit and delete 

@app.route('/')
@app.route('/get_recipe')
def get_recipe():
    return render_template("index.html", 
    recipes=mongo.db.recipes.find())
    

@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html", 
    foodCategory=mongo.db.foodCategory.find(), 
    recipeType=mongo.db.recipeType.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipe'))
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_foodCategory=mongo.db.foodCategory.find()
    all_recipeType=mongo.db.recipeType.find()
    return render_template('editrecipe.html', recipe=the_recipe, foodCategory=all_foodCategory,
    recipeType=all_recipeType)

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'ingredient_name':request.form.get('ingredient_name'),
        'cuisine_name':request.form.get('cuisine_name'),
        'author_name':request.form.get('author_name'),
        'recipe_method':request.form.get('recipe_method'),
        'recipe_type': request.form.get('recipe_type')
    })
    return redirect(url_for('get_recipe'))
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipe'))

# categories: get, add, edit and delete 
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
        {'recipe_category': request.form.get('recipe_category')})
    return redirect(url_for('get_categories'))
    
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    category=mongo.db.foodCategory
    category.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))
    
@app.route('/insert_category', methods=['POST'])
def insert_category():
    category=mongo.db.foodCategory
    category_doc= {'recipe_category': request.form.get('recipe_category')}
    category.insert_one(category_doc)
    return redirect(url_for('get_categories'))

@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')

# search a recipe based on recipe type 
@app.route('/search')
def search():
    return render_template('recipe_search.html',
    recipes=mongo.db.recipeType.find())
    

@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    # recipes=mongo.db.recipeType.find()
    
    if request.method ==  'POST':
        # Query database, render search template w/ results
        # results=mongo.db.recipeType.find(request.form.get('recipe_type'))
        
        recipe_type = request.form.get('recipe_type')
        results=mongo.db.recipes.find({"recipe_type": recipe_type})
        #print(list(recipe_type))
        return render_template('recipe_search.html', results=results, recipes=mongo.db.recipeType.find())
    else:
        # render search template w/ nothing ... nothing else needed
        return render_template('recipe_search.html')




    
    

# @app.route('/search_recipe/<recipe_type>')
# def search_recipe(recipe_type):
# #     search = recipeSearchForm(request.form)
# #     recipe=mongo.db.recipeType.find_one({'_id': ObjectId(recipe_id)})
# #     choices=mongo.db.recipeType.find
# #     if request.method == 'POST':
# #         return search_results(search)
        
#     return render_template('search_recipe.html',
#     recipes=mongo.db.recipeType.find()) 

# @app.route('/search_recipe', defaults={'recipe_type': None})    
# @app.route('/search_recipe/<recipe_type>')
# def search_recipe(recipe_type):
    
#     # If no recipe type has been submitted, just return the search template
#     # otherwise, search based on the form submitted and get the recipes
#     # in that category, and return them as "results"
#     # In the template, then you can do {% if results %} ... {% endif %}
#     if not recipe_type:
#         return render_template('search_recipe.html',
#         recipes=mongo.db.recipeType.find()) 
#     else:
#         # this should be your form, submitted w/ the submit button
#         print(request.form) 
        
#         # key for recipe category in your database, = request.form.get('category') or whatever you call it
#         results = mongo.db.recipeType.find('recipe_type')
        
#         # I'd recommend returning the results as a list so you can iterate
#         # multiple times without losing the data if you want
#         return render_template('search_recipe.html', results=list(results))
        
        
    
# @app.route('/search_results/<recipe_id>')
# def search_results(recipe_id):
#     if request.is_xhr:
#         recipe=mongo.db.recipeType.find
#         recipe_type=list(mongo.db.recipeType.find({'_id': ObjectId(recipe_id)})
#         return jsonify(recipe_id)
#     return redirect(url_for('search_recipe'))
    

# Run App

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
    