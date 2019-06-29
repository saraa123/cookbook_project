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
    delete_recipe=mongo.db.recipes.find({"delete_recipe": "true"}).sort("rating", -1)
    non_delete_recipe=mongo.db.recipes.find({"delete_recipe": "false"}).sort("rating", -1)
    
    return render_template("index.html", 
                            # recipes=mongo.db.recipes.find().sort("rating", -1), 
                            count = mongo.db.recipes.count(), 
                            author=author, 
                            delete_recipe=delete_recipe,
                            non_delete_recipe=non_delete_recipe) 
    
@app.route('/full_recipe/<recipe_id>')
def full_recipe(recipe_id):
    recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    
    return render_template('full_recipe.html', recipe=recipe)


@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html", 
    foodCategory=mongo.db.foodCategory.find(), 
    recipeType=mongo.db.recipeType.find(),
    specialReq=mongo.db.specialRequirement.find(),
    rating=mongo.db.rating.find(),
    cuisine=mongo.db.cuisine.find())
    

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    
    recipes = mongo.db.recipes
    
    # ------------- ingredients list -----------------------------
    new_ing = request.form.to_dict()
    ingredients_list = []
    
    # Delete blank lines in ingredients list
    ingredients_list = [x for x in ingredients_list if x] 
    
    
    for key, value in new_ing.items():
        print(key, "----->", value)
        
        index = range(len(ingredients_list))
        number = 1
        value = ("{0} {1}").format(number, value)
        
    
        if 'ingredient_' in key:
            ingredients_list.append(value)
            
            
            for x in ingredients_list:
                    if x=='':
                        ingredients_list.remove(x)
    
            # print ("SORTED ING ---->", sorted(list(ingredients_list)))
            print ("non sorted ingredients list ---->", ingredients_list)
    
    # for item in range(len(ingredients_list)):
    #     print("LIST INDEX", index, ingredients_list)
    
    for item in ingredients_list:
        
        
        ingredients_list.append(ingredients_list.index(item))
        
    # ----------- methods list ------------------------------------ 
    
    new_method = request.form.to_dict()
    methods_list=[]
    # new_method_list=methods_list.split(',')
    
    for key, value in new_method.items():
        print(key, '----->', value)
        
        if '_method' in key:
            methods_list.append(value)
            print (sorted(list(methods_list)))
            
            for x in methods_list:
                    if x=='':
                        methods_list.remove(x)
            
    
    
    if 'add_recipe' in request.form:
        recipes.insert_one({
        'recipe_name':request.form.get('recipe_name'),
        'ingredient_name': sorted(list(ingredients_list)),
        'cuisine_name':request.form.get('cuisine_name'),
        'author_name':request.form.get('author_name'),
        'recipe_method': sorted(list(methods_list)),
        'recipe_type': request.form.get('recipe_type'),
        'rating': request.form.get('rating'),
        'recipe_category': request.form.get('recipe_category'),
        'special_requirement': request.form.get('special_requirement'),
        'recipe_url': request.form.get('recipe_url'),
        'delete_recipe':request.form.get('delete_recipe'),
        'recipe_info': request.form.get('recipe_info')
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
    cuisine=mongo.db.cuisine.find()
    
    
    return render_template('editrecipe.html', recipe=the_recipe, foodCategory=all_foodCategory,
    recipeType=all_recipeType, rating=rating, specialReq=specialReq, cuisine=cuisine)

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    
    # Get all recipes from mongodb
    recipes = mongo.db.recipes

    # Take the object ID in the URL and use it to get the current recipe
    current_recipe = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)});
    
    # Use the current recipe to get its ingredients list
    current_ingredients = current_recipe['ingredient_name']
    
    # Delete blank lines in ingredients list
    current_ingredients = [x for x in current_ingredients if x] 
    
    
    print('current recipe -->', current_recipe)
    print('current ingredients', current_ingredients)
    
    # --------------- ingredients array ---------------------------
    
    # get all form data and turn it into a dictionary
    recipe = request.form.to_dict()
    
    # For each item in the form ...
    for key, value in recipe.items():
        print(key, "----->", value)
        
        # Check whether we're working with an ingredient
        if 'ingredient_' in key:
            # If so, check if it was new ingredient (this comes from addInput.js line 33)
            if '_added' in key:
                # If so, add it to the list
                current_ingredients.append(value)
            else:
                # Otherwise, figure out which one we're working on and update it
                form_ing_index = int(key.split('_')[1]) # ingredient_1_name --> ['ingredient', '1', 'name']
                print("VALUE ---->", value)
                current_ingredients[form_ing_index - 1] = value
                
                # this is where you need an if to say if the value = '', remove
                # this index from the current_ingredients list, otherwise, just 
                # update it like this
                for x in current_ingredients:
                    if x == '':
                        current_ingredients.remove(x)
                
                    # elif: 
                    #     current_ingredients[form_ing_index - 1] = value
                
            
            print ("SORTED LIST ---->",sorted(list(current_ingredients)))
            
    print("CURRENT ingredients list ----->",current_ingredients)
    
    

    # --------------- method array ----------------------------
    method = request.form.to_dict()
    current_recipe_method = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)});
    methods_list=current_recipe_method["recipe_method"]
    
    # For each item in the form ...
    for key, value in method.items():
        print(key, "----->", value)
        
        # Check whether we're working with an ingredient
        if '_method' in key:
            # If so, check if it was added (this comes from addInput.js line 33)
            if '_added' in key:
                # If so, add it to the list
                methods_list.append(value)
            # else:
            #     # Otherwise, figure out which one we're working on and update it
                form_ing_index = int(key.split('_')[1]) # recipe_1_method --> ['ingredient', '1', 'name']
            #     print("VALUE ---->", value)
                
        print("METHOD ---->", methods_list)
    # for key, value in new_method.items():
    #     print(key, '----->', value)
        
        
    #     if '_method' in key:
    #         methods_list.append(value)
    #         print (methods_list)
            
    
    
    recipes.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'ingredient_name':current_ingredients,
        'cuisine_name':request.form.get('cuisine_name'),
        'author_name':request.form.get('author_name'),
        'recipe_method': sorted(list(methods_list)),
        'recipe_type': request.form.get('recipe_type'),
        'rating': request.form.get('rating'),
        'recipe_category': request.form.get('recipe_category'),
        'special_requirement': request.form.get('special_requirement'),
        'recipe_url': request.form.get('recipe_url'),
        'delete_recipe':request.form.get('delete_recipe'),
        'recipe_info': request.form.get('recipe_info')
    })
    
    return render_template('full_recipe.html', recipe=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}))
    
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
        
        
        return render_template('recipe_search.html', 
                                recipes=mongo.db.recipeType.find(), 
                                recipeCategory=mongo.db.foodCategory.find(),
                                special_recipes=mongo.db.specialRequirement.find(),
                                cuisine_recipes = mongo.db.cuisine.find(),
                                results=results,
                                count=results.count())
    
        
    else:
        return render_template('recipe_search.html')    
    
    # if request.method == 'POST':
        
        # recipe_type = request.form.get('recipe_type')
        # special_requirement = request.form.get('special_requirement')
        # recipe_category = request.form.get('recipe_category')
        # cuisine_name = request.form.get('cuisine_name')
        
        # if recipe_type:
        #     results=mongo.db.recipes.find({"recipe_type": recipe_type})
        
        # elif special_requirement:
        #     special_results=mongo.db.recipes.find({'special_requirement': special_requirement})
        
        # elif recipe_category:
        #     category_results = mongo.db.recipes.find({'recipe_category': recipe_category})
    
        # elif cuisine_name:
        #     cuisine_results = mongo.db.recipes.find({'cuisine_name': cuisine_name})
        
            
            
    #         return render_template('recipe_search.html', 
    #         recipes=mongo.db.recipeType.find(), 
    #         recipeCategory=mongo.db.foodCategory.find(),
    #         special_recipes=mongo.db.specialRequirement.find(),
    #         cuisine_recipes = mongo.db.cuisine.find())
            
            
    #         # results=results,
    #         # special_results=special_results,
    #         # category_results=category_results)
        
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
        
        return render_template('recipe_search.html', 
                                recipes=mongo.db.recipeType.find(),
                                recipeCategory=mongo.db.foodCategory.find(), 
                                special_recipes=mongo.db.specialRequirement.find(),
                                cuisine_recipes = mongo.db.cuisine.find(),
                                category_results=category_results, 
                                category_count=category_results.count())
    
    else:
        return render_template('recipe_search.html')

@app.route('/search_special', methods=['GET', 'POST'])
def search_special():
    
    if request.method == 'POST':
        
        special_requirement = request.form.get('special_requirement')
        special_results=mongo.db.recipes.find({'special_requirement': special_requirement})
        
        return render_template('recipe_search.html', 
                                recipes=mongo.db.recipeType.find(),
                                recipeCategory=mongo.db.foodCategory.find(),
                                special_recipes=mongo.db.specialRequirement.find(), 
                                cuisine_recipes = mongo.db.cuisine.find(),
                                special_results=special_results,
                                special_count=special_results.count())
    
    else:
        return render_template('recipe_search.html')
  

@app.route('/search_cuisine', methods =['GET', 'POST'])
def search_cuisine():
    
    if request.method == 'POST':
        
        cuisine_name = request.form.get('cuisine_name')
        cuisine_results = mongo.db.recipes.find({'cuisine_name': cuisine_name})
        
        return render_template('recipe_search.html', 
                                recipes=mongo.db.recipeType.find(),
                                recipeCategory=mongo.db.foodCategory.find(),
                                special_recipes=mongo.db.specialRequirement.find(),
                                cuisine_recipes = mongo.db.cuisine.find(),
                                cuisine_results=cuisine_results, 
                                cuisine_count=cuisine_results.count())
                                
        
# Run App

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=int(os.environ.get('PORT')),
    debug=True)
    