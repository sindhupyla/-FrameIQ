from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import os

client = QdrantClient(":memory:")  # Use `localhost:6333` if running Qdrant server

COLLECTION_NAME = "video_frames"

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=512, distance=Distance.COSINE)
)

def upload_to_qdrant(vectors):
    points = []
    for idx, (frame_name, vector) in enumerate(vectors):
        points.append(PointStruct(
            id=idx,
            vector=vector,
            payload={"frame": frame_name}
        ))
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search_similar_frames(query_vector):
    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=5
    )
    results = []
    for point in search_result:
        results.append({
            "frame": point.payload["frame"],
            "score": point.score
        })
    return results
