# Yelp Review Semantic Search

A web application that uses AI-powered embeddings to search through Yelp reviews semantically. Find similar reviews based on meaning rather than just keywords.

## How It Works

1. **Embeddings**: Reviews are converted to vector embeddings using Sentence Transformers
2. **Indexing**: Embeddings are indexed using FAISS (Facebook AI Similarity Search)
3. **Search**: Queries are also converted to embeddings and compared against the index
4. **Results**: Similar reviews are returned ranked by semantic similarity

## Setup Instructions

### Step 1: Run the Jupyter Notebook

1. Open `lab_12.ipynb` in Jupyter
2. Run all cells to:
   - Install dependencies
   - Load the Yelp dataset (1,500 reviews)
   - Generate embeddings
   - Save embeddings to `yelp_embeddings.npy`
   - Create and save the FAISS index to `faiss_yelp_index.index`

**Note**: This process may take 5-10 minutes depending on your system

### Step 2: Install Flask Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Flask App

```bash
python app.py
```

The app will start on `http://localhost:5000`

## Features

- 🔍 **Semantic Search**: Search by meaning, not just keywords
- ⭐ **Rating Distribution**: View dataset statistics
- 📊 **Similarity Scores**: See how similar each result is to your query
- 💾 **Full Reviews**: Click "Read Full Review" to see complete text
- 🎨 **Beautiful UI**: Modern, responsive design

## Usage Example

1. Go to `http://localhost:5000`
2. Enter a search query like:
   - "Great food and amazing service"
   - "Bad experience, rude staff"
   - "Loved the atmosphere"
3. Choose number of results (3-20)
4. Click Search
5. Browse similar reviews with similarity scores

## File Structure

```
Lab Task 12/
├── lab_12.ipynb              # Notebook for generating embeddings
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── yelp_embeddings.npy       # Generated embeddings (created after running notebook)
├── faiss_yelp_index.index    # Generated FAISS index (created after running notebook)
├── templates/
│   └── index.html            # Frontend HTML
└── static/
    ├── css/
    │   └── style.css         # Styling
    └── js/
        └── main.js           # Frontend logic
```

## API Endpoints

### POST `/api/search`
Search for similar reviews

**Request:**
```json
{
    "query": "Great food",
    "results": 5
}
```

**Response:**
```json
{
    "success": true,
    "query": "Great food",
    "results": [
        {
            "id": 42,
            "review": "The food was amazing...",
            "stars": 5,
            "distance": 0.123,
            "full_review": "..."
        }
    ]
}
```

### GET `/api/stats`
Get dataset statistics

**Response:**
```json
{
    "total_reviews": 1500,
    "avg_stars": 3.45,
    "star_distribution": {
        "5": 450,
        "4": 380,
        "3": 350,
        "2": 200,
        "1": 120
    }
}
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **AI Models**: Sentence Transformers (embedding generation)
- **Search**: FAISS (Facebook AI Similarity Search)
- **Data**: Yelp Review Full Dataset
- **Frontend**: HTML, CSS, JavaScript
- **Frameworks**: NumPy, Pandas, PyTorch

## Performance Notes

- Embeddings are generated once and cached
- FAISS index uses Euclidean distance (L2)
- Search queries are processed in real-time
- Results are limited to 20 maximum per query

## Troubleshooting

**Issue**: "System not ready" error
- **Solution**: Make sure you've run all cells in the Jupyter notebook

**Issue**: Slow search on first run
- **Solution**: Model loading may take time on first search. Subsequent searches will be faster.

**Issue**: CUDA/GPU not detected
- **Solution**: The app uses CPU by default. To use GPU, modify imports in `app.py` and `lab_12.ipynb`

## Future Enhancements

- Add GPU support for faster embeddings
- Implement caching for frequent queries
- Add filters by star rating
- Save and export search results
- Compare multiple queries side-by-side
