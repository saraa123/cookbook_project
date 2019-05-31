import os 
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from collections import OrderedDict


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'Cookbook'
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


# recipes: get, add, edit and delete 
@app.route('/')
@app.route('/get_recipe')
def get_recipe():
    # -------------- to only print author name if it is given, need to fix! ----------
    author=mongo.db.author_name.find() 
    
    
    return render_template("index.html", 
    recipes=mongo.db.recipes.find().sort("rating", -1), count = mongo.db.recipes.count(), author=author) 
    


@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html", 
    foodCategory=mongo.db.foodCategory.find(), 
    recipeType=mongo.db.recipeType.find(),
    specialReq=mongo.db.specialRequirement.find(),
    rating=mongo.db.rating.find())
    

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    
    recipes = mongo.db.recipes
    
    # ------------- ingredients list -----------------------------
    new_ing = request.form.to_dict()
    ingredients_list = [ ]
    
    
    for key, value in new_ing.items():
        print(key, "----->", value)
        
        if 'ingredient_' in key:
            ingredients_list.append(value)
    
            print (sorted(list(ingredients_list)))
            
        
    # ----------- methods list ------------------------------------ 
    
    new_method = request.form.to_dict()
    # methods=new_method['recipe_method']
    methods_list=[ ]
    
    for key, value in new_method.items():
        print(key, '----->', value)
        
        if '_method' in key:
            methods_list.append(value)
            print (methods_list)
            
    # print(methods)
    
    print(request.form.get('recipe_method'))
    
    
    # method = request.form.get('recipe_method')
    # new_method = request.form.to_dict(method)
    # method = new_method['recipe_method'] ----- do I need this?
    
    # method = request.form.get('recipe_method').split('\r\n')
    
    
    if 'add_recipe' in request.form:
        recipes.insert_one({
        'recipe_name':request.form.get('recipe_name'),
        'ingredient_name':sorted(list(ingredients_list)),
        'cuisine_name':request.form.get('cuisine_name'),
        'author_name':request.form.get('author_name'),
        'recipe_method': sorted(list(methods_list)),
        'recipe_type': request.form.get('recipe_type'),
        'rating': request.form.get('rating'),
        'recipe_category': request.form.get('recipe_category'),
        'special_requirement': request.form.get('special_requirement'),
        'recipe_url': request.form.get('recipe_url'),
        'delete_recipe':request.form.get('delete_recipe')
    })
    elif 'cancel_add_recipe' in request.form:
        return redirect(url_for('get_recipe'))
    
    
    return redirect(url_for('get_recipe'))
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_foodCategory=mongo.db.foodCategory.find()
    all_recipeType=mongo.db.recipeType.find()
    specialReq=mongo.db.specialRequirement.find()
    rating=mongo.db.rating.find()
    
    
    return render_template('editrecipe.html', recipe=the_recipe, foodCategory=all_foodCategory,
    recipeType=all_recipeType, rating=rating, specialReq=specialReq)

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    
    recipe = request.form.to_dict()
    recipes = mongo.db.recipes
    
    # --------------- ingredients array ---------------------------
    
    new_ing = request.form.to_dict()
    ingredients_list = [ ]
    
    
    for key, value in new_ing.items():
        print(key, "----->", value)
        
        if 'ingredient_' in key:
            ingredients_list.append(value)
            
            print (sorted(list(ingredients_list)))
    
    # new_recipe = request.form.to_dict()
    # # ingredients=new_recipe['ingredient_name']
    # ingredients_list=[]
    
    # for key, value in new_recipe.items():
    #     print(key, '----->', value)
        
        
    #     if 'ingredient_' in key:
    #         ingredients_list.append(value)
    #         print (ingredients_list)
    
     
    
    
    ingredients=recipe['ingredient_name']
    # ingredients_list=ingredients.split('\r\n')
    
    
    # --------------- method array ----------------------------
    new_method = request.form.to_dict()
    # methods=new_method['recipe_method']
    methods_list=[]
    
    for key, value in new_method.items():
        print(key, '----->', value)
        
        
        if '_method' in key:
            methods_list.append(value)
            print (methods_list)
            
    # print(methods)
    
    # method = request.form.get('recipe_method').split('\r\n')
    
    
    recipes.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'ingredient_name':sorted(list(ingredients_list)),
        'cuisine_name':request.form.get('cuisine_name'),
        'author_name':request.form.get('author_name'),
        'recipe_method': sorted(list(methods_list)),
        'recipe_type': request.form.get('recipe_type'),
        'rating': request.form.get('rating'),
        'recipe_category': request.form.get('recipe_category'),
        'special_requirement': request.form.get('special_requirement'),
        'recipe_url': request.form.get('recipe_url')
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
    # category.insert_one(category_doc)
    
    if 'open' in request.form:
        category.insert_one(category_doc)
    elif 'close' in request.form:
        return redirect(url_for('get_categories'))
    return redirect(url_for('get_categories'))

@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')

# search a recipe based on recipe type 
@app.route('/search')
def search():
    return render_template('recipe_search.html',
    recipes=mongo.db.recipeType.find(),
    recipeCategory=mongo.db.foodCategory.find(),
    special_recipes=mongo.db.specialRequirement.find(),
    cuisine_recipes=mongo.db.cuisine.find())
    
    
@app.route('/search_recipe', methods=['GET', 'POST'])
def search_recipe():
    
    if request.method == 'POST':
        # Query database, render search template w/ results
        
        recipe_type = request.form.get('recipe_type')
        results=mongo.db.recipes.find({"recipe_type": recipe_type})
        
        
        return render_template('recipe_search.html', recipes=mongo.db.recipeType.find(), results=results, 
                                recipeCategory=mongo.db.foodCategory.find(),
                                special_recipes=mongo.db.specialRequirement.find(),
                                count=results.count(),
                                cuisine_recipes = mongo.db.cuisine.find())
    
        
    else:
        return render_template('recipe_search.html')    
    
    # if request.method == 'POST':
        
    #     recipe_type = request.form.get('recipe_type')
    #     special_requirement = request.form.get('special_requirement')
    #     recipe_category = request.form.get('recipe_category')
        
    #     if recipe_type:
    #         results=mongo.db.recipes.find({"recipe_type": recipe_type})
        
    #     elif special_requirement:
    #         results=mongo.db.recipes.find({'special_requirement': special_requirement})
        
    #     elif recipe_category:
    #         results = mongo.db.recipes.find({'recipe_category': recipe_category})
            
    #         return render_template('recipe_search.html',
    #                                 results=results)
        
    # else:
    #     # if nothing searched
    #     return render_template('recipe_search.html')
        
    # print(recipe_type)
    # print(special_requirement)
    # print(recipe_category)
    
@app.route('/search_category', methods=['GET', 'POST'])
def search_category():
    
    if request.method == 'POST':
        recipe_category = request.form.get('recipe_category')
        category_results = mongo.db.recipes.find({'recipe_category': recipe_category})
        
        return render_template('recipe_search.html', recipeCategory=mongo.db.foodCategory.find(), category_results=category_results, 
                                special_recipes=mongo.db.specialRequirement.find(),
                                recipes=mongo.db.recipeType.find(),
                                category_count=category_results.count(),
                                cuisine_recipes = mongo.db.cuisine.find())
    
    else:
        return render_template('recipe_search.html')

@app.route('/search_special', methods=['GET', 'POST'])
def search_special():
    
    if request.method == 'POST':
        
        special_requirement = request.form.get('special_requirement')
        special_results=mongo.db.recipes.find({'special_requirement': special_requirement})
        
        return render_template('recipe_search.html', special_recipes=mongo.db.specialRequirement.find(), 
                                special_results=special_results,
                                recipeCategory=mongo.db.foodCategory.find(),
                                recipes=mongo.db.recipeType.find(),
                                special_count=special_results.count(),
                                cuisine_recipes = mongo.db.cuisine.find())
    
    else:
        return render_template('recipe_search.html')
  

@app.route('/search_cuisine', methods =['GET', 'POST'])
def search_cuisine():
    
    if request.method == 'POST':
        
        cuisine_name = request.form.get('cuisine_name')
        cuisine_results = mongo.db.recipes.find({'cuisine_name': cuisine_name})
        
        return render_template('recipe_search.html', cuisine_recipes = mongo.db.cuisine.find(),
                                cuisine_results=cuisine_results, cuisine_count=cuisine_results.count(),
                                special_recipes=mongo.db.specialRequirement.find(),
                                recipeCategory=mongo.db.foodCategory.find(),
                                recipes=mongo.db.recipeType.find())
        
        
    
# Run App

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
    