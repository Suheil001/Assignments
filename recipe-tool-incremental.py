from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Global list to store recipes, initially with some sample recipes.
recipes = [
    {"id": "1", "name": "Spaghetti Carbonara", "description": "A classic Italian pasta dish with creamy sauce."},
    {"id": "2", "name": "Grilled Chicken Salad", "description": "A healthy and flavorful salad with grilled chicken."},
    {"id": "3", "name": "Pancakes", "description": "Fluffy pancakes served with syrup and berries."},
    {"id": "4", "name": "Tomato Basil Soup", "description": "A warm, comforting soup for a rainy day."},
    {"id": "5", "name": "Chocolate Cake", "description": "Rich and decadent dessert with layers of chocolate."}
]

def generate_recipe_id():
    """Generate a new unique recipe ID based on the current recipes."""
    if recipes:
        max_id = max(int(recipe["id"]) for recipe in recipes)
        return str(max_id + 1)
    return "1"

# Home page: displays the search form and navigation links for saved and new recipes
@app.route('/')
def home():
    home_html = """
    <h1>Recipe Search and Save Tool</h1>
    <p>
        <a href="{{ url_for('create_recipe') }}">Create a New Recipe</a> |
        <a href="{{ url_for('saved_recipes') }}">View Saved Recipes</a> |
        <a href="{{ url_for('all_recipes') }}">View All Recipes</a>
    </p>
    <form action="{{ url_for('search') }}" method="get">
        <input type="text" name="query" placeholder="Search for recipes..." required>
        <input type="submit" value="Search">
    </form>
    """
    return render_template_string(home_html)

# Display all recipes
@app.route('/all')
def all_recipes():
    all_html = """
    <h1>All Recipes</h1>
    <ul>
    {% for recipe in recipes %}
        <li>
            <strong>{{ recipe.name }}</strong>: {{ recipe.description }}
            - <a href="{{ url_for('save_recipe', recipe_id=recipe.id) }}">Save Recipe</a>
        </li>
    {% endfor %}
    </ul>
    <br>
    <a href="{{ url_for('home') }}">Back to Home</a>
    """
    return render_template_string(all_html, recipes=recipes)

# Form and endpoint to create a new recipe
@app.route('/create', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if name and description:
            new_recipe = {
                "id": generate_recipe_id(),
                "name": name,
                "description": description
            }
            recipes.append(new_recipe)
            return redirect(url_for('all_recipes'))
        else:
            error = "Both name and description are required."
            return render_template_string(create_form_html, error=error)
    
    # GET request: display the recipe creation form
    create_form_html = """
    <h1>Create a New Recipe</h1>
    {% if error %}
        <p style="color:red;">{{ error }}</p>
    {% endif %}
    <form method="post">
        <label for="name">Recipe Name:</label><br>
        <input type="text" id="name" name="name" required><br><br>
        <label for="description">Description:</label><br>
        <textarea id="description" name="description" required></textarea><br><br>
        <input type="submit" value="Create Recipe">
    </form>
    <br>
    <a href="{{ url_for('home') }}">Back to Home</a>
    """
    return render_template_string(create_form_html)

# Search results page: displays recipes matching the search query
@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    matched_recipes = [
        recipe for recipe in recipes 
        if query in recipe['name'].lower() or query in recipe['description'].lower()
    ]
    search_html = """
    <h1>Search Results for "{{ request.args.get('query') }}"</h1>
    {% if recipes %}
        <ul>
        {% for recipe in recipes %}
            <li>
                <strong>{{ recipe.name }}</strong>: {{ recipe.description }}
                - <a href="{{ url_for('save_recipe', recipe_id=recipe.id) }}">Save Recipe</a>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No recipes found matching your query.</p>
    {% endif %}
    <br>
    <a href="{{ url_for('home') }}">Back to Home</a>
    """
    return render_template_string(search_html, recipes=matched_recipes)

# Route to save a recipe; stores saved recipe IDs in the session
@app.route('/save/<recipe_id>')
def save_recipe(recipe_id):
    if "saved_recipes" not in session:
        session["saved_recipes"] = []
    if recipe_id not in session["saved_recipes"]:
        session["saved_recipes"].append(recipe_id)
        session.modified = True
    return redirect(url_for('saved_recipes'))

# Saved recipes page: shows all recipes saved by the user
@app.route('/saved')
def saved_recipes():
    saved = session.get("saved_recipes", [])
    saved_list = [recipe for recipe in recipes if recipe["id"] in saved]
    saved_html = """
    <h1>Saved Recipes</h1>
    {% if saved_list %}
        <ul>
        {% for recipe in saved_list %}
            <li><strong>{{ recipe.name }}</strong>: {{ recipe.description }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>You haven't saved any recipes yet.</p>
    {% endif %}
    <br>
    <a href="{{ url_for('home') }}">Back to Home</a>
    """
    return render_template_string(saved_html, saved_list=saved_list)

if __name__ == '__main__':
    app.run(debug=True)
