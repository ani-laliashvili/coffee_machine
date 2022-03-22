# Coffee machine project

def check_sufficient_resources(choice, resources):
    """
    Check if there are sufficient resources to make the coffee selected
    :param choice: user-selected coffee type
    :param resources: resources available
    :return: list of insufficient resources
    """
    insufficient_resources = []

    for key in MENU[choice]['ingredients']:
        if resources[key]['amount'] < MENU[choice]['ingredients'][key]['amount']:
            insufficient_resources.append(key)
    return insufficient_resources


def take_coins():
    """
    Take coins and return numbers of each
    :return quarters: number of quarters inserted
    :return dimes: number of dimes inserted
    :return nickels: number of nickels inserted
    :return pennies: number of pennies inserted
    """
    print('Please insert coins.')
    quarters = int(input('How many quarters?: '))
    dimes = int(input('How many dimes?: '))
    nickels = int(input('How many nickles?: '))
    pennies = int(input('How many pennies?: '))
    return quarters, dimes, nickels, pennies


def count_money(quarters, dimes, nickels, pennies):
    """
    Counts total money inserted
    :param quarters: number of quarters inserted
    :param dimes: number of dimes inserted
    :param nickels: number of nickels inserted
    :param pennies: number of pennies inserted
    :return: money value of coins inserted
    """
    return quarters*0.25 + nickels*0.05 + dimes*0.10 + pennies*0.01


def is_money_sufficient(choice, money_in):
    """
    Check if inserted coins are sufficient for selected coffee
    :param choice: user-selected coffee type
    :param money_in: total money inserted
    :return: True/False
    :return: change to be refunded
    """
    if money_in < MENU[choice]['cost']:
        return False, 0
    elif money_in >= MENU[choice]['cost']:
        return True, money_in - MENU[choice]['cost']


def brew(choice, resources):
    """
    Brew selected coffee
    :param choice: user-selected coffee type
    :param resources: resources available
    :param money_in: money paid
    :return: remaining resources after brewing
    """
    for key in MENU[choice]['ingredients']:
        resources[key]['amount'] = resources[key]['amount'] - MENU[choice]['ingredients'][key]['amount']
    resources['money']['amount'] = resources['money']['amount'] + MENU[choice]['cost']
    print(f'Here is your {choice}. Enjoy!')
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
    coffee_choice = input('What would you like? (espresso/latte/cappuccino): ')
    # provide a report of available resources if prompted
    if coffee_choice == 'report':
        print_report(resources)
    # Take coins, brew the coffee requested if money is sufficient
    elif coffee_choice in ['espresso', 'latte', 'cappuccino']:
        # check if resources are sufficient
        insufficient_resources = check_sufficient_resources(coffee_choice, resources)
        if len(insufficient_resources) != 0:
            print(f'Sorry there is not enough {" or ".join(insufficient_resources)}.')
        else:
            # brew coffee and return change
            quarters, dimes, nickels, pennies = take_coins()

            sufficient, change = is_money_sufficient(coffee_choice, count_money(quarters, dimes, nickels, pennies))
            if sufficient:
                if change > 0:
                    print(f'Here is ${round(change, 2)} in change.')
                resources = brew(coffee_choice, resources)
            else:
                print('Sorry that\'s not enough money. Money refunded.')
    # Invalid coffee choice
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