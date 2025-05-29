import pg1core

# Initialize variables
player_hp = 100
turn_count = 0
energy = [100, 100, 100]
tablet_energy = 100
engine = [False, False, False]
engine_work = [True, True, True]
doors = [False, False, False]
temperature = [15, 15, 15, 7]
player_position = 0
transformer_status = True
monster_position = 4
transformer_break_chance = 0.05
do_new_action = True
monster_do_action_count = 0

# Main game loop
while True:
    turn_count += 1
    pg1core.display_status(player_hp, turn_count, energy, temperature, engine, player_position, transformer_status, tablet_energy, doors, engine_work)
    monster_do_action_count -= 1
    
    if do_new_action:
        monster_do_action_count = random.randint(5, 7)
        monster_action_ra = pg1core.set_monster_action()
        do_new_action = False

    print("Transformer break chance -", transformer_break_chance)

    action = input("Choose an action: ")

    if action == "1":
        pg1core.move_energy(energy, player_position, transformer_status)
    elif action == "2":
        pg1core.toggle_engine(engine, player_position, engine_work)
    elif action == "3":
        new_position = pg1core.move_player(player_position)
        if new_position is not None:
            player_position = new_position
    elif action == "4":
        transformer_status = pg1core.restart_transformer(player_position, transformer_status)
    elif action == "5":
        tablet_energy = pg1core.show_scan_display(monster_action_ra, tablet_energy, monster_do_action_count)
    elif action == "6":
        tablet_energy = pg1core.charge_tablet(player_position, tablet_energy, energy)
    elif action == "7":
        pg1core.toggle_doors(doors, player_position)
    else:
        print("Turn skipped")

    monster_position = pg1core.reset_monster_position(monster_position)
    if monster_do_action_count <= 0:
        monster_position = pg1core.do_monster_action(monster_position, monster_action_ra)
        do_new_action = True
    pg1core.check_monster_position(monster_position, engine_work, doors)
    pg1core.update_temperatures(temperature, engine, energy, turn_count)
    player_hp = pg1core.player_change_hp(player_position, temperature, player_hp, monster_position, doors)
    tablet_energy = pg1core.energy_check(energy, tablet_energy, transformer_status, engine, doors)
    transformer_status = pg1core.inactive_transformer(transformer_status, transformer_break_chance)
    transformer_break_chance = pg1core.up_inactive_transformer(transformer_break_chance, turn_count)
    pg1core.check_turn(turn_count)
