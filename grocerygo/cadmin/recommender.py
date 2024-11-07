import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .models import UserInteraction, Product

def get_recommendations(user_id, n=4):
    try:
        # Get all user interactions
        interactions = UserInteraction.objects.all()
        
        if not interactions.exists():
            return Product.objects.all()[:n]

        # Create a user-item matrix
        df = pd.DataFrame(list(interactions.values('user_id', 'product_id', 'interaction_type')))
        
        if df.empty:
            return Product.objects.all()[:n]

        # Create pivot table
        user_item_matrix = pd.pivot_table(
            df, 
            values='interaction_type',
            index='user_id',
            columns='product_id',
            aggfunc='count',
            fill_value=0
        )

        # Calculate similarity between users
        user_similarity = cosine_similarity(user_item_matrix)
        
        # Convert to DataFrame
        user_similarity_df = pd.DataFrame(
            user_similarity,
            index=user_item_matrix.index,
            columns=user_item_matrix.index
        )

        # Find similar users
        if user_id in user_similarity_df.index:
            similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:6].index
        else:
            return Product.objects.all()[:n]

        # Get products that similar users interacted with
        recommended_products = set()
        for similar_user in similar_users:
            products = UserInteraction.objects.filter(
                user_id=similar_user
            ).values_list('product_id', flat=True)
            recommended_products.update(products)

        # Remove products the user has already interacted with
        user_products = UserInteraction.objects.filter(
            user_id=user_id
        ).values_list('product_id', flat=True)
        recommended_products = recommended_products - set(user_products)

        # Get product objects
        return Product.objects.filter(id__in=list(recommended_products)[:n])
    
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        return Product.objects.all()[:n]