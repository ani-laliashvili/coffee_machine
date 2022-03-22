# Coffee machine project

def check_sufficient_resources(drink_name, resources):
    """
    Check if there are sufficient resources to make the coffee selected
    :param choice: user-selected coffee type
    :param resources: resources available
    :return: list of insufficient resources
    """
    insufficient_resources = []

    for key in MENU[drink_name]['ingredients']:
        if resources[key]['amount'] < MENU[drink_name]['ingredients'][key]['amount']:
            insufficient_resources.append(key)
    return insufficient_resources


def take_coins():
    """
    Counts total from coins inserted
    :return: money value of coins inserted
    """
    print('Please insert coins.')
    total = int(input('How many quarters?: ')) * 0.25
    total += int(input('How many dimes?: ')) * 0.05
    total += int(input('How many nickles?: ')) * 0.10
    total += int(input('How many pennies?: ')) * 0.01
    return total


def is_money_sufficient(drink_name, money_in):
    """
    Check if inserted coins are sufficient for selected coffee
    :param choice: user-selected coffee type
    :param money_in: total money inserted
    :return: True/False
    """
    if money_in < MENU[drink_name]['cost']:
        return False
    elif money_in >= MENU[drink_name]['cost']:
        return True

def get_change(drink_name, money_in):
    """
    Get change
    :param money_in: total money inserted
    :return: change to be refunded
    """
    return money_in - MENU[drink_name]['cost']

def brew(drink_name, resources):
    """
    Brew selected coffee
    :param choice: user-selected coffee type
    :param resources: resources available
    :param money_in: money paid
    :return: remaining resources after brewing
    """
    for key in MENU[drink_name]['ingredients']:
        resources[key]['amount'] = resources[key]['amount'] - MENU[drink_name]['ingredients'][key]['amount']
    resources['money']['amount'] = resources['money']['amount'] + MENU[drink_name]['cost']
    print(f'Here is your {drink_name}. Enjoy!')
    return resources


def print_report(resources):
    """
    Prints report of available resources
    :param resources: available resources
    """
    for key in resources:
        if resources[key]['units'] == '$':
            print(f"{key.capitalize()}: {resources[key]['units']}{str(resources[key]['amount'])}")
        else:
            print(f"{key.capitalize()}: {str(resources[key]['amount'])}{resources[key]['units']}")


def coffee_machine(resources):
    """
    Ask for user input and perform functions using helper functions.
    :param resources: available resources
    """
    choice = input('What would you like? (espresso/latte/cappuccino): ')
    # turn the machine off
    if choice == 'off':
        quit()
    # provide a report of available resources if prompted
    elif choice == 'report':
        print_report(resources)
    # Take coins, brew the coffee requested if money is sufficient
    elif choice in ['espresso', 'latte', 'cappuccino']:
        # check if resources are sufficient
        insufficient_resources = check_sufficient_resources(choice, resources)
        if len(insufficient_resources) != 0:
            print(f'Sorry there is not enough {" or ".join(insufficient_resources)}.')
        else:
            # brew coffee and return change
            money_in = take_coins()
            sufficient = is_money_sufficient(choice, money_in)
            if sufficient:
                change = get_change(choice, money_in)
                if change > 0:
                    print(f'Here is ${round(change, 2)} in change.')
                resources = brew(choice, resources)
            else:
                print('Sorry that\'s not enough money. Money refunded.')
    # Invalid choice
    else:
        print('Sorry. We do not have the coffee you selected.')

    coffee_machine(resources)


if __name__ == '__main__':
    # set drinks menu
    MENU = {
        'espresso' : {'ingredients' :
                          {'water': {'amount' : 50, 'units' : 'ml'},
                           'coffee' : {'amount' : 18, 'units' : 'g'}},
                      'cost': 1.5},
        'latte' : {'ingredients':{'water': {'amount': 200, 'units': 'ml'},
                                  'coffee': {'amount': 24, 'units': 'g'},
                                  'milk': {'amount': 150, 'units': 'ml'}},
                   'cost': 2.5},
        'cappuccino' : {'ingredients':{'water': {'amount': 250, 'units': 'ml'},
                                       'coffee': {'amount': 24, 'units': 'g'},
                                       'milk': {'amount': 100, 'units': 'ml'}},
                        'cost': 3.0},
    }

    # set initial available resources
    resources = {
        'water' : {'amount' : 300, 'units' : 'ml'},
        'milk' : {'amount' : 200, 'units' : 'ml'},
        'coffee' : {'amount' : 100, 'units' : 'g'},
        'money' : {'amount' : 0, 'units' : '$'}
    }

    # run machine
    coffee_machine(resources)