from .import bp as main 
from .forms import PokeSearch
from app.models import PokeParty, PokeUserJoin
from flask import render_template, request, flash, redirect, url_for
import requests
from flask_login import  login_required, current_user

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/party', methods=['GET', 'POST'])
@login_required
def party():
    form = PokeSearch()
    
    if request.method == 'POST' and form.validate_on_submit():
        
        search = request.form.get('search')
        
        url = f"https://pokeapi.co/api/v2/pokemon/{search}"
        response = requests.get(url)
        if response.ok:
            user_pokemon = []               
            poke_dict={
                "name":response.json()['forms'][0]['name'],
                "hp":response.json()['stats'][0]['base_stat'],
                "defense":response.json()['stats'][2]['base_stat'],
                "attack":response.json()['stats'][1]['base_stat'],
                "ability_1":response.json()['abilities'][0]['ability']['name'],                
                "sprite": response.json()['sprites']['front_shiny']
                }
            user_pokemon.append(poke_dict)
            if not PokeParty.exists(poke_dict["name"]):
                new_poke = PokeParty()
                new_poke.from_dict(poke_dict)
                new_poke.save()
        

            user = current_user
            user.add_to_team(PokeParty.exists(poke_dict['name']))

            return render_template('pokepage.html.j2', form=form, pokemon_party = user_pokemon)
        else:
            error_string = "Invalid Selection, please try again."
            return render_template('pokepage.html.j2', form=form, error = error_string)
    return render_template('pokepage.html.j2', form=form)

@main.route('/pokeparty', methods=['GET'])
@login_required
def pokeparty():
    team = current_user.team
    return render_template('pokeparty.html.j2', team = team)

@main.route('/remove/<int:id>')
@login_required
def remove(id):
    poke = []
    poke = PokeUserJoin.query.get((id, current_user.id))
    poke.remove()
    flash('You said your goodbyes and released this pokemon back into the wild.', 'success')
    return redirect(url_for('main.pokeparty'))
