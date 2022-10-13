import os
import netifaces

if os.name != 'nt':
    from pick import pick

def choose_adapter():
    if os.name == 'nt':
        print('You must specify the adapter with   -a ADAPTER')
        print('Choose from the following: ' +
                ', '.join(netifaces.interfaces()))
        sys.exit(1)
    title = 'Please choose the adapter you want to use: '
    try:
        choice = pick(netifaces.interfaces(), title)
        if type(choice) is list:
            choice = choice[0]
        adapter, index = choice
    except curses.error as e:
        print('Please check your $TERM settings: %s' % (e))
        sys.exit(1)

    return adapter
