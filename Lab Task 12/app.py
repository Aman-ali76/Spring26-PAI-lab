from flask import Flask, render_template, request, jsonify
import numpy as np
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

app = Flask(__name__)

# Load model, embeddings, and FAISS index
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Check if embeddings and index files exist
if os.path.exists('yelp_embeddings.npy') and os.path.exists('faiss_yelp_index.index'):
    embeddings = np.load('yelp_embeddings.npy')
    faiss_index = faiss.read_index('faiss_yelp_index.index')
    print("Loaded embeddings and FAISS index")
else:
    print("Warning: Embeddings or FAISS index not found. Run the Jupyter notebook first.")
    embeddings = None
    faiss_index = None



try:
    df = pd.read_csv('yelp_reviews.csv')
    print("Loaded Yelp reviews")
except Exception as e:
    print(f"Error loading dataset: {e}")
    df = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search_reviews():
    if faiss_index is None or df is None:
        return jsonify({'error': 'System not ready. Please run the Jupyter notebook first.'}), 500
    
    try:
        data = request.json
        query = data.get('query', '').strip()
        num_results = int(data.get('results', 5))
        
        if not query:
            return jsonify({'error': 'Query cannot be empty'}), 400
        
        if num_results > 20:
            num_results = 20
        
        # Encode query and search
        query_embedding = model.encode([query])
        distance, indices = faiss_index.search(query_embedding, num_results)
        
        results = []
        for i in range(num_results):
            idx = indices[0][i]
            results.append({
                'id': int(idx),
                'review': df['text'].iloc[idx][:500],  # Limit to 500 chars
                'stars': int(df['stars'].iloc[idx]),
                'distance': float(distance[0][i]),
                'full_review': df['text'].iloc[idx]
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    if df is None:
        return jsonify({'error': 'Dataset not loaded'}), 500
    
    try:
        stats = {
            'total_reviews': len(df),
            'avg_stars': float(df['stars'].mean()),
            'star_distribution': df['stars'].value_counts().to_dict()
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
