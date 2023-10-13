import re
import json

# The input string with ModalItem tags
input_string = """
<ModalItem icon={<FaSkull className="h-8 w-8" />} name="Terror" />
<ModalItem icon={<FaMasksTheater className="h-8 w-8" />} name="Drama" />
<ModalItem icon={<FaHandcuffs className="h-8 w-8" />} name="Thriller" />
<ModalItem icon={<FaMicrophone className="h-8 w-8" />} name="Musical" />
<ModalItem icon={<FaFaceGrinHearts className="h-8 w-8" />} name="Romance" />
<ModalItem icon={<FaFortAwesome className="h-8 w-8" />} name="Fantasy" />
<ModalItem icon={<FaHatCowboy className="h-8 w-8" />} name="Western" />
<ModalItem icon={<FaPersonMilitaryRifle className="h-8 w-8" />} name="War" />
<ModalItem icon={<FaGun className="h-8 w-8" />} name="Action" />
<ModalItem icon={<FaHelmetUn className="h-8 w-8" />} name="Sport" />
<ModalItem icon={<FaStethoscope className="h-8 w-8" />} name="Medicine" />
<ModalItem icon={<FaRedditAlien className="h-8 w-8" />} name="Sci-Fi" />
<ModalItem icon={<FaFilm className="h-8 w-8" />} name="Documentary" />
<ModalItem icon={<FaFaceGrinSquintTears className="h-8 w-8" />} name="Comedy" />
<ModalItem icon={<FaPeopleRoof className="h-8 w-8" />} name="Family" />
"""

# Regular expression to match genre names
genre_pattern = r'name="([^"]+)"'

# Find all genre names using regular expressions
genres = re.findall(genre_pattern, input_string)

# Create a list of dictionaries for the fixture
fixture_data = [
    {
        "model": "bookmarks.genre",  # Replace with your actual app name
        "fields": {
            "name": genre,
        },
    }
    for genre in genres
]

# Save the fixture data to a JSON file
with open("genres_fixture.json", "w") as json_file:
    json.dump(fixture_data, json_file, indent=4)

print("Fixture data saved to 'genres_fixture.json'")