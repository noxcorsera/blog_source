import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Recipes, Tags

def recipe_index(request):
    selected_tags = request.GET.getlist('tags')
    selected_tags = [int(tag_id) for tag_id in selected_tags]
    tags = Tags.objects.using('recipes_db').all()
    
    if selected_tags:
        recipes = Recipes.objects.using('recipes_db').filter(
            recipe_tags__tag_id__in=selected_tags
        ).distinct()
    else:
        recipes = Recipes.objects.using('recipes_db').all()
    
    # Prefetch related tags to optimize database queries
    recipes = recipes.prefetch_related('recipe_tags__tag')
    
    return render(request, 'recipe_index.html', {
        'recipes': recipes,
        'tags': tags,
        'selected_tags': selected_tags,
    })


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipes.objects.using('recipes_db'), recipe_id=recipe_id)
    instructions = recipe.instructions.all()
    ingredients = recipe.recipe_ingredients.all()
    tags = recipe.recipe_tags.all()
    
    # Determine the image path
    recipe_image_name = f"{recipe.title}.png"
    image_path = os.path.join(settings.MEDIA_ROOT, 'image', recipe_image_name)
    
    if os.path.exists(image_path):
        # If the image exists, use its URL
        recipe_image_url = os.path.join(settings.MEDIA_URL, 'image', recipe_image_name)
    else:
        # Otherwise, use the default image
        recipe_image_url = os.path.join(settings.MEDIA_URL, 'image', 'default_recipe_photo.webp')
    
    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'instructions': instructions,
        'ingredients': ingredients,
        'tags': tags,
        'recipe_image_url': recipe_image_url,  # Pass the image URL to the template
    })