import pymongo

from Utilities.movies import Movies

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["WatchWise"]
users_collection = db["users"]
login_collection = db["login"]

class Profile:
    @staticmethod
    def fetchUserInfo(user_id):
        try:
            user_data = users_collection.find_one({ "user_id": str(user_id) },
                                              { "created_at": 1, "bio": 1, "name": 1, "avatar": 1, "_id": 0 })

            # Fetch email from the 'login' collection
            login_data = login_collection.find_one({ "user_id": str(user_id) },
                                               { "email": 1, "_id": 0 })

            # Apply default values if user data is missing
            if not user_data:
                user_data = {
                    "name": "Unknown User",
                    "avatar": "https://wallpapers.com/images/featured/cool-profile-picture-87h46gcobjl5e4xu.jpg",
                    "bio": "No bio available",
                    "created_at": None
                }

            # Apply default email if not found
            email = login_data["email"] if login_data else "No email provided"

            # Combine and return the final response
            user_data["email"] = email
            
            print("User Data: ", user_data)
            
            return {"status": "success", "data": user_data}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    @staticmethod
    def fetchCount(user_id):
        watch_list = users_collection.find_one({ "user_id": str(user_id) }, { "watchlist": 1 })
        watch_history = users_collection.find_one({ "user_id": str(user_id) }, { "watch_history": 1 })
        
        counts = {
            "watch_list" : len(watch_list["watchlist"]),
            "watch_history" : len(watch_history["watch_history"])
        }
        
        print(counts)
        
        return counts
    
    @staticmethod
    def fetchRecentHistory(user_id):
        watch_history = users_collection.find_one({ "user_id": str(user_id) }, { "watch_history": 1 })
        watch_history = watch_history["watch_history"]
        
        moviesObj = Movies()
        
        recentlyWatched = []
        
        if (len(watch_history) < 4):
            pass 
        else:
            watch_history = watch_history[-1:-4:-1]
            
        show_ids = []
        for movie in watch_history:
            show_ids.append(movie["show_id"])
            
        details = moviesObj.fetch_details(show_ids, user_id)        
        recentlyWatched.append(details)
            
        return recentlyWatched