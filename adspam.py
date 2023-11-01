from telethon import TelegramClient
from telethon.errors import rpcerrorlist, FloodWaitError, ChatWriteForbiddenError
import asyncio
import os
from colorama import Fore, Style

try:
    import progressbar
except ModuleNotFoundError:
    print("Please run > pip install progressbar2")

# Check if API credentials are already stored in a file
if os.path.isfile('spamer.txt'):
    with open('spamer.txt', 'r') as r:
        data = r.readlines()
    api_id = int(data[0])
    api_hash = data[1].strip()  # Remove leading/trailing whitespaces
else:
    api_id = input('Enter api_id: ')
    api_hash = input('Enter api_hash: ')
    with open('spamer.txt', 'w') as a:
        a.write(str(api_id) + '\n' + api_hash)

client = TelegramClient('spamer', api_id, api_hash)


async def check_responses(client):
    async for message in client.iter_messages('me'):
        print(f"Received Message:\n{message.text}")


async def send_message_to_group(client, target, message):
    try:
        await client.send_message(target.id, message)

        # Call check_responses function here after sending the message
        await check_responses(client)

    except rpcerrorlist.ChatAdminRequiredError:
        print(f"{Fore.RED}[!] You do not have permission to post messages in this chat!{Style.RESET_ALL}")
    except ChatWriteForbiddenError:
        print(f"{Fore.RED}[!] You have been restricted from writing messages in this chat...!{Style.RESET_ALL}")
    except FloodWaitError as e:
        print(f"{Fore.RED}[!] Try again after {e.seconds} seconds{Style.RESET_ALL}")
    except rpcerrorlist.InputUserDeactivatedError:
        print(f"{Fore.RED}[!] The specified user was deleted or deactivated.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] An error occurred: {e}{Style.RESET_ALL}")


async def normal_spammer():
    dialogs = await client.get_dialogs()
    print(f"{Fore.CYAN}Available Groups:{Style.RESET_ALL}")
    for i, dialog in enumerate(dialogs):
        print(f'{Fore.YELLOW}{i + 1} : {dialog.name} has ID {dialog.id}{Style.RESET_ALL}')

    try:
        group_number = int(input(f"{Fore.MAGENTA}Please insert group number to spam: {Style.RESET_ALL}"))
        if 1 <= group_number <= len(dialogs):
            selected_group = dialogs[group_number - 1]
            print(f"{Fore.GREEN}Selected Group: {selected_group.name} (ID: {selected_group.id}){Style.RESET_ALL}")
            interval = int(input(f"{Fore.MAGENTA}Enter the interval between messages (in seconds): {Style.RESET_ALL}"))
            message = input(f"{Fore.MAGENTA}Enter the spam message: {Style.RESET_ALL}")

            while True:
                sent_message = await send_message_to_group(client, selected_group, message.strip())
                print(f"{Fore.YELLOW}Next spam round in {interval} seconds{Style.RESET_ALL}")
                await asyncio.sleep(interval)
        else:
            print(f"{Fore.RED}Invalid group number. Please choose a number between 1 and {len(dialogs)}{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")


async def medium_spammer():
    dialogs = await client.get_dialogs()
    print(f"{Fore.CYAN}Available Groups:{Style.RESET_ALL}")
    for i, dialog in enumerate(dialogs):
        print(f'{Fore.YELLOW}{i + 1} : {dialog.name} has ID {dialog.id}{Style.RESET_ALL}')

    try:
        group_numbers = input(f"{Fore.MAGENTA}Please insert group numbers to spam (comma-separated): {Style.RESET_ALL}").split(',')
        selected_groups = [dialogs[int(num) - 1] for num in group_numbers if 1 <= int(num) <= len(dialogs)]

        if selected_groups:
            print(f"{Fore.GREEN}Selected Groups:")
            for group in selected_groups:
                print(f"{group.name} (ID: {group.id})")
            print(Style.RESET_ALL)

            interval = int(input(f"{Fore.MAGENTA}Enter the interval between messages (in seconds, more than 180 seconds): {Style.RESET_ALL}"))
            if interval < 180:
                print(f"{Fore.RED}Interval should be greater than 180 seconds (3 minutes).{Style.RESET_ALL}")
                return

            message = input(f"{Fore.MAGENTA}Enter the spam message: {Style.RESET_ALL}")

            while True:
                for selected_group in selected_groups:
                    sent_message = await send_message_to_group(client, selected_group, message.strip())
                    print(f"{Fore.YELLOW}Next spam round in {interval} seconds{Style.RESET_ALL}")
                    await asyncio.sleep(interval)
        else:
            print(f"{Fore.RED}Invalid group number(s). Please choose valid number(s) between 1 and {len(dialogs)}{Style.RESET_ALL}")
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter valid number(s).{Style.RESET_ALL}")


if __name__ == "__main__":
    with client:
        print(f"{Fore.CYAN}░░░░░▄▄▄▄▀▀▀▀▀▀▀▀▄▄▄▄▄▄░░░░░░░")
        print("░░░░░█░░░░▒▒▒▒▒▒▒▒▒▒▒▒░░▀▀▄░░░░")
        print("░░░░█░░░▒▒▒▒▒▒░░░░░░░░▒▒▒░░█░░░")
        print("░░░█░░░░░░▄██▀▄▄░░░░░▄▄▄░░░░█░░")
        print("░▄▀▒▄▄▄▒░█▀▀▀▀▄▄█░░░██▄▄█░░░░█░")
        print("█░▒█▒▄░▀▄▄▄▀░░░░░░░░█░░░▒▒▒▒▒░█")
        print("█░▒█░█▀▄▄░░░░░█▀░░░░▀▄░░▄▀▀▀▄▒█")
        print("░█░▀▄░█▄░█▀▄▄░▀░▀▀░▄▄▀░░░░█░░█░")
        print("░░█░░░▀▄▀█▄▄░█▀▀▀▄▄▄▄▀▀█▀██░█░░")
        print("░░░█░░░░██░░▀█▄▄▄█▄▄█▄████░█░░░")
        print("░░░░█░░░░▀▀▄░█░░░█░█▀██████░█░░")
        print("░░░░░▀▄░░░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█░░")
        print("░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░▒░░░█░")
        print("░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░░░░█░")
        print("░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░░░░█░░")
        print(f"{Style.RESET_ALL}")

        print(f"{Fore.CYAN}1. Normal Spammer\n2. Medium Spammer\n3. Advanced Spammer{Style.RESET_ALL}")
        spammer_choice = input(f"{Fore.MAGENTA}Choose a spam mode (1/2/3): {Style.RESET_ALL}")

        if spammer_choice == '1':
            client.loop.run_until_complete(normal_spammer())
        elif spammer_choice == '2':
            client.loop.run_until_complete(medium_spammer())
        elif spammer_choice == '3':
            client.loop.run_until_complete(advanced_spammer(client))
