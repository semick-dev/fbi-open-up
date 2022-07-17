# fbi/open-up

**tl;dr** "Debug" finicky CI failures

Have you ever encountered a finicky CI problem where you feel like yelling "I JUST WANT A TERMINAL WITH THE AGENT" at the screen? Well, this little hacky pile of garbage will allow you to bust into your agent jobs and _actually do that_. It at least approaches that!

The project is quite simple, but should meet MOST of your debugging needs. It uses a storage queue on an account YOU control to pass messages back and forth from the agent to a place where your local CLI can grab them.

todo, if I ever get around to it:

- shell syntax highlighting on response

_devops/actions yaml_
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

Here is an `openup` session in practice! (still local)

![it_actually_works](https://user-images.githubusercontent.com/479566/179384275-e1c3fc5b-6c40-423e-bdf9-f34020eb84de.gif)





