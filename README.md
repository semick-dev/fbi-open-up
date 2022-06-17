# fbi-open-up

**tl;dr** "Debug" finicky CI failures

Have you ever encountered a finicky CI problem where you feel like yelling "I JUST WANT A TERMINAL WITH THE AGENT" at the screen? Well, this little hacky pile of garbage will allow you to bust into your agent jobs and _actually do that_.

This little python project is quite simple, but should meet MOST of your debugging needs. It uses a storage queue on an account YOU control to pass messages back and forth from the agent to a place where your local CLI can grab them.

_Agent process_
```yml
- bash: |
    <set python version and install>
    fbi "<connection string>"
  displayName: "Run the agent"
  timeOutInMinutes: 60
```

_On your machine_

```bash
/>openup "<connection string>"
Found a session start message, connecting to <YourBuildAgentName>

Select your shell

1. pwsh
2. bash

1
<cwd on agent>/> ls
...
```



