# slack-pandemic-simulator

Simulates a pandemic in Slack.

## How it works

Each user in a Slack workspace will be seeded with a random vulnerability score. This should be weighted towards the majority not being vulnerable. This score will be between 0 i.e. not vulnerable at all, through to 1 i.e. completely vulnerable.

A single user in the Slack workspace will also be seeded as patient 0 i.e. they have the virus.

When users post messages on Slack there is a chance that the virus will be transmitted. This will be based on the distance (time in this case) between the messages sent. If two messages between two different users are sent within a 2 minute time period "contact" will be made between the two users.

When contact is made between two users it is first determined whether one (or both) of the users has the virus. If one of them does have the virus and the other does not then a check is made to see whether the virus has spread to the non-infected person. This will initially begin with a 1 in 10 chance of transmission.

If neither have the virus or both have the virus then there is no change.

Users are instantly contagious, there is no incubation period.

Users may be told that they have symptoms after two days (meaning they have the chance to self isolate). This will be a 50/50 chance of them showing symptoms.

After two days it is possible for the user to be hospitalised (put into a private Slack channel). This will be based on the initial vulnerability score.

If the user never ended up in hospital they are now immune to the virus and won't infect anyone from that time or be reinfected.

If they did end up in hospital after two days it is possible that the user can die (put into death private Slack channel). 50/50 chance of survival. If they survive they are now immune and won't infect anyone else.
