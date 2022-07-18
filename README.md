# fbi/open-up

**tl;dr** "Debug" finicky CI failures

Have you ever encountered a finicky CI problem where you feel like yelling "I JUST WANT A TERMINAL WITH THE AGENT" at the screen? Well, this little hacky pile of garbage will allow you to bust into your agent jobs and _actually do that_. 

The project is quite simple, but should meet MOST of your debugging needs. It uses a storage queue on an account YOU control to pass messages back and forth from the agent to a place where your local CLI can grab them.

Depending on the platform that the `fbi` agent is run on, it will either leverage `bash` or `pwsh` as the invoking shell.


`.github/workflows/<your-problem-action>.yml`
```yml
- bash: |
    pip install fbi-open-up
    fbi -c "<connection string>"
  displayName: "A step inserted into your problem build"
```

_On your machine._

```bash
/>openup "<connection string>"
```

_In a github action._

```yml
steps:
  # <your normal job steps having issues here>
  # fbi-open-up takes a dep on python > 3. it does not update your selected python version though
  - uses: semick-dev/fbi-open-up
    with:
      fbi-queue-cs:
      fbi-queue-name: 'agent-actions' # this is not required, but will default to `agent-interactions
      fbi-max-iterations: '180' # time in seconds this thing will be waiting for
```
