import requests

#done with a video to assist - https://www.youtube.com/watch?v=JVQNywo4AbU
base_url = "https://pokeapi.co/api/v2/"

def get_pokemon_info(name):
    url = f"{base_url}/pokemon/{name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        pokemon_data = response.json()
        return pokemon_data
    else:
        print(f"Failed to retireve data {response.status_code}")
    pass

pokemon_name = ""
pokemon_info = get_pokemon_info(pokemon_name)

if pokemon_info:
    print(f"Name: {pokemon_info["name"].capitalize()}")
    print(f"Id: {pokemon_info["id"]}")
    print(f"Height: {pokemon_info["height"]}")
    print(f"Weight: {pokemon_info["weight"]}")


# done without a video
base_url2 = "https://meowfacts.herokuapp.com/"

def get_cat_fact(amount):
    url = f"{base_url2}/?count={amount}"
    response = requests.get(url)

    if response.status_code == 200:
        fact_data = response.json()
        return fact_data
    else:
        print(f"Failed to retireve data {response.status_code}")
    pass

numberOfFacts = 3
cat_fact = get_cat_fact(numberOfFacts)

if cat_fact:
    for fact in cat_fact["data"]:
        print(f"Cat Fact: {fact}\n")