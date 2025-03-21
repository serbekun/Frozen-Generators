import random
import time
from colorama import init, Fore, Style

# Константы
MAX_ENERGY = 100
MIN_ENERGY = 0
MAX_HP = 100
ENGINE_USE_ENERGY = 5
DOOARS_USE_ENERGY = 10
BROKE_TRANSFORMER_USE_ENERGY = 2
DOUWN_STREAT_TEMPRECHE_TURN_COUNT = 15
BASE_DOWN_TEMPRECHE_VALUE = 0.2
BASE_UP_TEMPRECHE_VALUE = 1
DOWN_STREAT_TEMPRECHE_VALUE = 0.5
ENGINE_TEMPERATURE_LIMITS = [25, 25, 20]
MIN_TEMPERATURE_LEVEL_TWO = 5
MIN_TEMPERATURE = 10
HEAL_TEMPRICHE = 20
TEMPERATURE_DAMEGE = 5
TEMPERATURE_HEAL = 2
MONSTOR_DAMEGE = 20
LAST_TURN = 100
DEAD_HP = 0
TRANSFORMAR_BREAKE_CHANSE_UP = 0.05

init()

def display_status(player_hp, turn_count, energy, temperature, engine, player_position, transformer_status, tablet_energy, doors, engine_work):
    print(f"Turn - {turn_count}/{LAST_TURN} ================================================================")
    print(f"Player HP - {player_hp}")
    for i in range(len(energy)):
        print(f"Energy block {i} - {energy[i]}% | Temp {temperature[i]:.1f}")
    print("tablet energy -", tablet_energy)
    print(f"Street temperature - {temperature[3]:.1f}")
    print(f"Engine of/onn status | 0 - {engine[0]} | 1 - {engine[1]} | 2 - {engine[2]}")
    print(f"Engine can work status | 0 - {engine_work[0]} | 1 - {engine_work[1]} | 2 - {engine_work[2]}")
    print(f"Doors status | 0 - {doors[0]} | 1 - {doors[1]} | 2 - {doors[2]}")
    print(f"Total energy - {sum(energy)}")
    print(f"You are {'outside' if player_position == 3 else f'in energy block {player_position}'}")
    print("Transformer active" if transformer_status else Fore.RED + "Transformer inactive!" + Style.RESET_ALL)
    print("1. Move energy\n2. Turn engine on/off\n3. Move between blocks or street\n4. Restart transformer (if outside)\n5. Strat Scan\n6. charge tablet\n7. Doors lock\n8. Skip turn\n=====================================")

def move_energy(energy, player_position, transformer_status):
    """Функция перемещения энергии между блоками."""
    if not transformer_status:
        print("Transformer is broken! You can't move energy.")
        return
    try:
        amount = int(input("How much energy do you want to move: "))
        target_block = int(input("To which block do you want to move energy (0-2): "))
        if 0 <= amount <= energy[player_position] and 0 <= target_block < len(energy) and target_block != player_position:
            energy[player_position] -= amount
            energy[target_block] += amount
            print(f"Moved {amount} energy from block {player_position} to block {target_block}.")
        else:
            print("Invalid move! Check energy levels or block selection.")
    except ValueError:
        print("Invalid input. Please enter numbers.")

def energy_check(energy, tablet_energy, transformer_status, engine, doors):
    
    for i in range(len(doors)): # если двери закрыты то тратется энергия
        if doors[i] == True:
            energy[i] -= DOOARS_USE_ENERGY

    if transformer_status == False: # если трансформатор сломался то идёт учечка энергий
        for i in range(len(energy)):
            energy[i] -= BROKE_TRANSFORMER_USE_ENERGY

    for i in range(len(energy)): # если энергия в блоков превышает 100% то уменшаем до 100%
        if energy[i] > MAX_ENERGY:
            energy[i] = MAX_ENERGY
    
    if tablet_energy >= MAX_ENERGY: # тоже самое толька для планшета
        tablet_energy = MAX_ENERGY

    for i in range(len(energy)):
        if energy[i] <= 0:
            engine[i] = False
            doors[i] = False
    
    for i in range(len(energy)):
        if energy[i] < MIN_ENERGY:
            energy[i] = MIN_ENERGY

    return tablet_energy

def toggle_engine(engine, player_position, engine_work):
    """Функция включения/выключения двигателя в текущем блоке."""
    if player_position == 3:
        print("you can't toogle engyne in streat becose here not exist engyne")
        return
    
    if engine_work[player_position] == False:
        print("you can't toggle engyne becosse he broke")
        return
    
    engine[player_position] = not engine[player_position]
    print(f"Engine in block {player_position} {'on' if engine[player_position] else 'off'}.")

def toggle_doors(doors, player_position):
    if player_position == 3:
        print("you can't toogle doors in streat becose here not exist doors")
        return
    doors[player_position] = not doors[player_position]
    print(f"Door in block")

def move_player(player_position):
    """Функция перемещения игрока между блоками и улицей."""
    try:
        new_position = int(input("Where do you want to move (0-2 or 3 for street): "))
        if player_position == 3 and new_position != 2:
            print("You can back from streat only to energy block 2")
        elif new_position == 3 and player_position != 2:
            print("You can only move to the street from energy block 2!")
        elif 0 <= new_position <= 3:
            player_position = new_position
            return player_position
        else:
            print("Invalid choice. Enter a valid block number.")
    except ValueError:
        print("Invalid input. Enter a number.")
    
def incatvie_transformer(transformer_status, transformer_break_chance):
    if random.random() < transformer_break_chance:
        print("The transformer is broken!")
        transformer_status = False
    return transformer_status

def up_incatvie_transformer(transformer_break_chance, turn_count):
    if turn_count % 15 == 0:
        transformer_break_chance += TRANSFORMAR_BREAKE_CHANSE_UP
    return transformer_break_chance

def restart_transformer(player_position, transformer_status):
    """Функция перезапуска трансформатора (только если игрок на улице)."""
    if player_position == 3:
        transformer_status = True
        print("Transformer restarted!")
        return transformer_status
    else:
        print("Move to the street to restart the transformer.")

def update_temperatures(temperature, engines, energy, turn_count):

    if turn_count % DOUWN_STREAT_TEMPRECHE_TURN_COUNT == 0:
        temperature[3] -= DOWN_STREAT_TEMPRECHE_VALUE
        
    temperature[2] -= BASE_DOWN_TEMPRECHE_VALUE
    
    for i in range(len(engines)):
        if engines[i] == True:
            energy[i] -= ENGINE_USE_ENERGY
        
        if engines[i] == True and temperature[i] < [25, 25, 20][i]:
            temperature[i] += BASE_UP_TEMPRECHE_VALUE
        else:
            temperature[i] -= BASE_DOWN_TEMPRECHE_VALUE

    # Выравнивание температуры с улицей
    for i in range(len(temperature)):
        if temperature[i] < temperature[3]:
            temperature[i] = temperature[3]

    return temperature

def check_temperature_damage(player_position, temperature, player_hp):
    """Функция проверки получения урона или лечения от температуры"""
    if player_position < len(temperature):
        if temperature[player_position] < MIN_TEMPERATURE_LEVEL_TWO:
            player_hp -= MIN_TEMPERATURE_LEVEL_TWO

        if temperature[player_position] < MIN_TEMPERATURE:
            player_hp -= TEMPERATURE_DAMEGE

        if temperature[player_position] > HEAL_TEMPRICHE:
            player_hp += TEMPERATURE_HEAL

    return player_hp

def check_monster_damage(player_position, player_hp, monster_position, doors):
    """Функция проверки получения урона от монстра"""
    if player_position == monster_position:
        if player_position < len(doors) and doors[player_position] == False and player_position != 3:
            player_hp -= MONSTOR_DAMEGE
            print(Fore.RED + "you has attack monster" + Style.RESET_ALL)
        elif player_position == 3:  # Игрок и монстр встретились на улице
            player_hp -= MONSTOR_DAMEGE
            print(Fore.RED + "Monster attacked you outside!" + Style.RESET_ALL)
        elif player_position < len(doors) and doors[player_position] == True:
            print("monster come to your place but you block")

    return player_hp

def player_change_hp(player_position, temperature, player_hp, monster_position, doors):
    """Функция проверки будет ли игрок получать урон или лечиться"""
    
    player_hp = check_monster_damage(player_position, player_hp, monster_position, doors)
    player_hp = check_temperature_damage(player_position, temperature, player_hp)

    if player_hp > MAX_HP:
        player_hp = MAX_HP

    if player_hp <= DEAD_HP:
        print(Fore.RED + "you died" + Style.RESET_ALL)
        time.sleep(5)
        exit()

    return player_hp

def show_scan_diplay(monster_action_ra, tablet_energy):
    tablet_energy -= 50
    if tablet_energy <= 0:
        tablet_energy = 0
        return tablet_energy
    if monster_action_ra == 3:
        print("next monster go outside")
    elif monster_action_ra == 4:
        print("stay in his home")
    else:
        print("next monster go energy block -", monster_action_ra)
    return tablet_energy

def charge_tablet(player_position, tablet_energy, energy):
    if player_position == 3:
        print("You can't charge the tablet on the street because there's no connection to energy.")
    else:
        tablet_energy += 20
        energy[player_position] -= 10
        print(f"You charge the tablet to {tablet_energy}%.")
    return tablet_energy

def set_monster_action():
    monster_action_ra = random.randint(0, 4)
    return monster_action_ra

def do_monster_action(monster_position, monster_action_ra):
    if monster_position != 4:
        monster_position = 4
        return monster_position
    else:
        monster_position = monster_action_ra
        return monster_position
    
def chek_monster_position(monster_position, engine_work, doors):
    if monster_position in [0, 1, 2]:
        if doors[monster_position] == False:
            engine_work[monster_position] = False

def reset_monster_position(monster_position):
    if monster_position != 4:
        monster_position = 4
    return monster_position

def chek_turn(turn_count):
    if turn_count > LAST_TURN:
        print(Fore.GREEN + "you win you survive." + Style.RESET_ALL)
        time.sleep(5)
        exit()
