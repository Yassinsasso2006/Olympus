# 🏛️ Olympus Master-Bot-System
A divine assembly of Discord bots, each inspired by the gods and guardians of Greek mythology, built to serve the will of **The Council of Elders**. Olympus brings order, justice, and swift communication to your server through a modular, mythology-driven bot framework.

## ⚔️ The Pantheon of Bots

#### 🛶 **Charon the Ferryman of Souls**
Guide of the newly arrived, Charon ensures only the worthy cross into your server. Handles verification with precision, assigning roles and filtering entry like the gatekeeper of the underworld.

##### ***_Features:_***
- [x] `/verify` 
    - Description: It takes an unverified memeber and verified them. How you ask? It takes away the unverified role and gives them the standard member roles.
    - Input: `Member`
    - Output: **Nothing**

- [x] `/unverify`
    - Description: It takes a verified member and reveres the verfication process. It gives them the unverified role and gives them the standard member roles.
    - Input: `Member`
    - Output: **Nothing**

##### ***_Notes:_***


#### 👁️ **Argus the All-Seeing Guardian**
With a hundred virtual eyes, Argus never sleeps. He scans your realm for forbidden images, detects rising chaos with AI-powered threat assessment, and whispers to the gods (moderators) when his vigilance is needed—either across servers or through ephemeral messages.

##### ***_Features:_***
- [ ] `/ping mod`
    - Description: Any moderator pings that a member does, he gets prompted whether he wants to ping them silently or not.
    - Trigger Event: When someone tags `@Moderator`
    - Input: `Mod Team` (Different mod categories)
    - Output: Sends a ping to a private channel alerting the mod team
    - Notes:
        - I can do something else, have the AI scan the chat and pick the most suitable mod team. If the AI fails to determine one, then tag them all. (Test run this before deploying)

- [ ] `Monitors chat`
    - Description: This just monitors the server chats and give each a `threat_level`. And once it passes a certain threshold then it tags the chat mods.
    - Input: 
    - Output:

##### ***_Notes:_***

#### ⚖️ **Themis The Embodiment of Justice**
The goddess of order watches closely. Themis records every warning, strike, and infraction, building a tapestry of member behavior. Her scales remain balanced, her judgment fair, her memory long.

##### ***_Features:_***
- [ ] `/warn` 
    - Description:
    - Input: 
    - Output:

- [ ] `/strike`
    - Description:
    - Input: 
    - Output:

- [ ] `/history`
    - Description:
    - Input: 
    - Output:

##### ***_Notes:_***

#### ✉️ **Hermes The Messenger**
Fleet-footed and endlessly adaptable, Hermes handles communication and support. He crafts intricate ticket systems for all needs—whether mortal disputes or divine tasks—and delivers messages with speed and style.

##### ***_Features:_***
- [ ] `Create Ticket` **Button** 
    - Description: It's en embed, when clicked a prompt is given where they have to chose the category.
    - Input: 
    - Output:

- [ ] `Close Ticket` **Button**
    - Description:
    - Input: 
    - Output:

    Ticket Categories:
    - Scamming
    - Verfication
    - Report a member
    - Suggestions
    - Partnership
    - Technical Issues
    - Report a rule-break
    - Report a mod (Chat, Ticket, Dailies, MC, Roleplay, Event)
    - Report an admin (Yassin, Cheesy, Maxim, Luci, PunPun, Ghost)


##### ***_Notes:_***




## Requirements

**Run**: pip install discord.py python-dotenv

There are 2 different virtual enviroments, depending on which operating system you're using Linux or windows. Due to python compiling different on each operating system.

To run each bot you'll need the corresponding .env file.

### On Windows
source .venv-windows/Scripts/activate

### On Linux
source .venv-linux/bin/activate

### Extras:
- Use these commands to sync branch with main:
git fetch origin
git merge origin/main

To do list:
- Add a TLDR
- Themis DMs member about warn/strike
- Themis has messages as evidence

Bugs so far:
- Olympus command only works on linux. But also try to find a way to make it universal among computers. Wtf am I doing, I have midterms. I ain't free to waste time on this fucking code