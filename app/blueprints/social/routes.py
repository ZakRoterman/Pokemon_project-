from .import bp as social
from flask import flash, redirect, url_for, render_template
from app.models import User
from flask_login import login_required, current_user

@social.route('/pokebattle')
@login_required
def pokebattle():
    users = User.query.all()
    return render_template('battle.html.j2', users=users)

@social.route('/select_users')
@login_required
def select_user(id):
    user = User.query.get(id)
    return user

@social.route('/battle/<int:id>', methods=['GET'])
@login_required
def battle(id):
    user = User.query.get(id)
    if int(current_user.total_attack()) > int(user.total_attack()):
        current_user.wins += 1
        current_user.save()
        flash('You win!', 'success')
    elif int(current_user.total_attack()) < int(user.total_attack()):
        current_user.losses += 1
        current_user.save()
        flash(f'{user.first_name} wins!', 'danger')
    else:
        flash("Both you and your opponent's pokemon fainted at the same time.", 'warning')
        return redirect(url_for('social.pokebattle'))
    return redirect(url_for('social.pokebattle'))