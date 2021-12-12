# commands

MAN = """
**SYNTAX**:
    helper [COMMAND] [FLAGS] [FLAG ARGUMENT]

**COMMANDS**:
    help:
        writes manual

    github:
        writes github organization link
        
        **FLAGS**:
            -p, --project
                writes github project link
                
    documentation:
        writes documentation link
        
    guildid:
        writes guild id
        
    channelid:
        writes channel id
        
    anonymous:
        sends message received from private message to channel
    
         **REQUIRED FLAGS:**
            -c, --channel
                specifies channel id
                
            -C, --content
                specifies content of message
                
            -u, --user (optional)
                specifies what user should helper tag
                
        example:
            helper anonymous -c 1234567890 -C Hello World -u 1234567890
"""

GITHUB = "https://github.com/SquareScreenStudio"
GH_ORGANIZATION = "Not yet!"

DOCUMENTATION = "https://docs.google.com/document/d/1jDGHhu1_2GO7maR9NCFdLR155DnHShqQhOwBq8d5J9E/edit?usp=sharing"

# messages
HELP = "Unknown command. Type \"help\" command for a list of commands."

INVALID_FLAGS = "Invalid flags. Type \"help\" command for a list of commands."

MISSING_FLAGS = "Missing required flags. Type \"help\" command for a list of commands."
