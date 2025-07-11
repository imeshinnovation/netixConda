
def movieEntity(movie) -> dict:
    return {
        "id": str(movie["_id"]),
        "title": movie["title"],
        "uri": movie["uri"],
        "poster": movie["poster"],
        "producer": movie["producer"],
        "subtitle": movie["subtitle"],
        "description": movie["description"],
        "owner": movie["owner"],
        "likes": movie["likes"],
        "messages": movie["messages"]
    }
    
def moviesEntity(movies) -> list:
    return [movieEntity(movie) for movie in movies]